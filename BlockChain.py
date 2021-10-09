from Block import Block
import util
from util import transaction

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
        block = Block(
            idx = len(self.chain),
            proof_num = proof_num,
            prev_hash = prev_hash,
            transactions = data
        )
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

    def get_data(self, sender, receiver, amount):
        """
        Creates a new transaction to go into the Block successfully mined. 
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append(transaction(sender, receiver, amount).json())
        return len(self.chain) + 1

    @staticmethod
    def proof_of_work(prev_proof, block, difficulty):
        """
        Simple Proof of Work Algorithm:
         - Find a nonce such that block.compute_hash() contains leading self.difficulty zeroes,
         where the block.compute_hash() is an encoding of 
            block.idx,
            block.nonce
            block.proof_num,
            block.prev_hash,
            block.transactions, 
            block.timestampe
        :param prev_proof: <int>
        :param block: <Block>
        :param difficulty: <int>
        :return: <int>
        """
        i = 0
        # Try to find a nonce such that the block's hash has `difficulty` zeros.
        while True:
            block.set_nonce(i)
            h = block.compute_hash
            if util.verify_hash_zeroes(h, difficulty):
                return prev_proof + 1
            i = i + 1

    @property
    def latest_block(self):
        return self.chain[-1]

    def mine_block(self, miner):
        self.get_data(
            sender="ROOT",
            receiver=miner,
            amount=1
        )
        last_block = self.latest_block
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
    last_block = blockchain.latest_block
    proof_num = blockchain.proof_of_work(last_block.proof_num, last_block, blockchain.pow_difficulty)
    blockchain.mine_block("galaxy")
    data = transaction("galaxy", "galaxy2", 50).json()
    last_hash = last_block.compute_hash
    blockchain.build_block(blockchain.latest_block.proof_num + 1, last_hash, data)
    blockchain.build_block( 
        blockchain.latest_block.proof_num + 1,
        blockchain.latest_block.compute_hash, 
        transaction("galaxy2", "galaxy", 10).json()
        )
    blockchain.print()

if __name__ == "__main__":
    main()