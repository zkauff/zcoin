from Block import Block
import util
from util import transaction
from util import confirm_validity
import json
import hashlib
DIFFICULTY = 3
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
            block.print()

    def build_genesis(self):
        self.build_block(proof_num=0, prev_hash=0)
        pass

    def build_block(self, proof_num, prev_hash, data=None):
        if not data:
            data = self.current_transactions
        block = {
            'idx' : len(self.chain),
            'proof_num' : proof_num,
            'prev_hash' : prev_hash,
            'transactions' : data
        }
        self.proof_of_work(proof_num, block, self.pow_difficulty)
        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def confirm_validity(block, prev_block):
        if(
            prev_block.idx + 1 != block.idx
            or prev_block.compute_hash != block.prev_hash
            or prev_block.timestamp >= block.timestamp
            or not util.verify_hash_zeroes(block.compute_hash, DIFFICULTY)
            ):
            return False
        else:
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
        self.current_transactions.append(transaction(sender, receiver, amount).json())
        print(f"current_transactions: {self.current_transactions}")
        return len(self.chain) + 1

    @staticmethod
    def proof_of_work(prev_proof, block, difficulty):
        """
        Simple Proof of Work Algorithm
        :param prev_proof: <int>
        :param block: <Block>
        :param difficulty: <int>
        :return: <int>
        """
        proof = 0
        while confirm_validity(prev_proof, proof) is False:
            proof += 1 
        return proof

    @property
    def last_block(self):
        return self.chain[-1]

    def mine_block(self, miner):
        self.new_transaction(
            sender="ROOT",
            receiver=miner,
            amount=1
        )
        last_block = self.last_block
        block = self.build_block(last_block.proof_num + 1, last_block.compute_hash)
        self.proof_of_work(last_block.proof_num, block, self.pow_difficulty)
        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True
    
    @staticmethod
    def get_block_object(block_data):
        return Block(
            block_data['idx'],
            block_data['proof_num'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp']
        )

def main():
    blockchain = BlockChain(difficulty=DIFFICULTY)
    last_block = blockchain.last_block
    proof_num = blockchain.proof_of_work(last_block.proof_num, last_block, blockchain.pow_difficulty)
    blockchain.mine_block("galaxy")
    data = transaction("galaxy", "galaxy2", 50).json()
    last_hash = last_block.compute_hash
    blockchain.build_block(blockchain.last_block.proof_num + 1, last_hash, data)
    blockchain.build_block( 
        blockchain.last_block.proof_num + 1,
        blockchain.last_block.compute_hash, 
        transaction("galaxy2", "galaxy", 10).json()
        )
    blockchain.print()

if __name__ == "__main__":
    main()