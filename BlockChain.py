import util
from util import confirm_validity
import json
import hashlib
import pprint

DIFFICULTY=5

"""
Blockchain implementation using the Block class from Block.py as our 
links in the chain.
"""
class BlockChain(object):
    def __init__(self, difficulty=DIFFICULTY):
        self.pow_difficulty = difficulty
        self.chain = []
        self.nodes = set()
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
        block["hash"] = self.proof_of_work(proof_num, block, self.pow_difficulty)
        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def confirm_validity(proof, prev_proof, threshold):
        guess = hashlib.sha256(f"{prev_proof}{proof}".encode()).hexdigest()
        for i in range(threshold):
            if guess[i] == '0':
                continue
            else:
                return (False, None)
        return (True, guess)

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

    def proof_of_work(self, prev_proof, block=None):
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
        proof_hash = ""
        while valid is False:
            (valid, proof_hash) = self.confirm_validity(prev_proof, proof, self.pow_difficulty)
            proof += 1
        if block: 
            block["hash"] = proof_hash
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

    # Unused so far.
    def create_node(self, address):
        self.nodes.add(address)
        return True
        
if __name__ == "__main__":
    blockchain = BlockChain(difficulty=DIFFICULTY)
    pprint.pprint(blockchain.mine_block("galaxy"))