import json
import hashlib
import pprint
from urllib.parse import urlparse
import requests 

DIFFICULTY=5

"""
A local instance of the blockchain. 
"""
class BlockChain(object):
    def __init__(self, difficulty=DIFFICULTY):
        self.pow_difficulty = difficulty
        self.chain = []
        self.peer_nodes = set()
        # The list of transactions that will go into the next block. 
        self.current_transactions = [] 
        self.build_genesis()
        pass

    def print(self):
        for block in self.chain:
            pprint.pprint(block)

    def build_genesis(self):
        self.build_block(proof_num=0, prev_hash=0)
        pass

    def build_block(self, proof_num, prev_hash):
        block = {
            'idx' : len(self.chain),
            'proof_num' : proof_num,
            'prev_hash' : prev_hash,
            'transactions' : self.current_transactions
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def confirm_block_validity(prev_proof, proof, threshold):
        guess = hashlib.sha256(f"{prev_proof}{proof}".encode()).hexdigest()
        print(guess)
        for i in range(threshold):
            if guess[i] == '0':
                continue
            else:
                return False
        print(proof)
        print(prev_proof)
        return True
    
    def confirm_chain_validity(self, chain):
        """
        Confirms the validity of the provided blockchain
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        idx = 1 
        while(idx < len(chain)):
            block = chain[idx]
            # Ensure the hash is correctly pointing to previous block and that
            # the proof of work algorithm was correctly calculated.
            if block["prev_hash"] != self.hash(last_block) or not self.confirm_block_validity(
                    last_block["proof_num"], 
                    block["proof_num"], 
                    self.pow_difficulty):
                print(f"last block proof: {last_block['proof_num']}")
                print(f"block proof: {block['proof_num']}")
                return False 
            else:
                idx = idx + 1
                last_block = block
        return True 

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, receiver, amount):
        """
        Creates a new transaction to go into the Block successfully mined. 
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
        })
        return len(self.chain) + 1

    def proof_of_work(self, prev_proof):
        """
        Simple Proof of Work Algorithm that attempts to find a proof number
            such that a sha256 of {prev_proof}{proof} produces a valid hash
            with {self.pow_difficulty} leading zeros.
        :param prev_proof: <int>
        :param block: <dict>
        :param difficulty: <int>
        :return: <int>
        """
        proof = 0
        valid = False
        while valid is False:
            proof += 1
            valid = self.confirm_block_validity(prev_proof, proof, self.pow_difficulty)
        return proof

    @property
    def last_block(self):
        return self.chain[-1]

    def mine_block(self, miner):
        # Figure out the valid proof number.
        last_block = self.last_block
        last_proof = last_block['proof_num']
        proof = self.proof_of_work(last_proof)

        # Reward the miner. 
        # ROOT_NODE sender signifies the coin is brand new.
        self.new_transaction(
            sender="ROOT_NODE",
            receiver=miner,
            amount=1,
        )

        # Add to the chain. 
        previous_hash = self.hash(last_block)
        block = self.build_block(proof, previous_hash)

        return block

    def register_peer_node(self, address):
        """
        Add new node to our list of peer nodes
        :param address: <str> Address of the peer node node. Eg. 'http://192.168.0.5:5000'
        :return: True if successful 
        """
        try:
            self.peer_nodes.add(urlparse(address).path)
            return True
        except:
            return False
        
    def consensus(self):
        """
        Performs the consensus algorithm by looking at our peers for the longest valid chain.
        :return: <int> was this chain replaced
        :return: <list> our new blockchain
        :return: <str> where we got the blockchain from
        """
        # Stores the blockchain once we've reached consensus
        resolved_chain = self.chain
        # the maximum length chain we've seen so far
        curr_max = len(self.chain)
        authoritative_chain_source = None
        rc = 0
        for node in self.peer_nodes:
            try:
                print(f"checking with {node}")
                resp = requests.get(f"http://{node}/chain")
                if resp.status_code == 200: # successful
                    tmp_len = resp.json()["length"]
                    tmp_chain = resp.json()["chain"]
                    pprint.pprint(tmp_chain)
                    if tmp_len > curr_max and self.confirm_chain_validity(tmp_chain):
                            curr_max = tmp_len
                            resolved_chain = tmp_chain
                            rc = 1
                            authoritative_chain_source = node
            except:
                pass
        self.chain = resolved_chain
        return (rc, resolved_chain, authoritative_chain_source)

if __name__ == "__main__":
    blockchain = BlockChain(difficulty=DIFFICULTY)
    pprint.pprint(blockchain.mine_block("galaxy"))