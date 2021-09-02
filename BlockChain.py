from Block import Block

"""
Blockchain implementation using the Block class from Block.py as our 
links in the chain.
"""
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.curr_data = []
        self.nodes = set()
        self.build_genesis()
        pass

    def print(self):
        for block in self.chain:
            block.print()

    def build_genesis(self):
        self.build_block(proof_num=0, prev_hash=0)
        pass

    def build_block(self, proof_num, prev_hash):
        block = Block(
            idx = len(self.chain),
            proof_num = proof_num,
            prev_hash = prev_hash,
            data = self.curr_data
        )
        self.curr_data = []
        self.chain.append(block)
        return block

    @staticmethod
    def confirm_validity(block, prev_block):
        if(
            prev_block.idx + 1 != block.idx
            or prev_block.compute_hash != block.prev_hash
            or prev_block.timestamp >= block.timestamp
            ):
            return False
        else:
            return True

    def get_data(self, sender, receiver, amount):
        self.curr_data.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return True

    @staticmethod
    def proof_of_work(prev_proof):
        # TODO: actual proof
        return prev_proof + 1 

    @property
    def latest_block(self):
        return self.chain[-1]

    def mine_block(self, miner):
        self.get_data(
            sender="0",
            receiver=miner,
            quantity=1
        )
        last_block = self.latest_block
        last_proof_num = last_block.proof_num
        proof_num = self.proof_of_work(last_proof_num)
        last_hash = last_block.compute_hash
        block = self.build_block(proof_num, last_hash)
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
    blockchain = BlockChain()
    last_block = blockchain.latest_block
    last_proof_num = last_block.proof_num
    proof_num = blockchain.proof_of_work(last_proof_num)
    blockchain.get_data(
        sender="0", #this means that this node has constructed another block
        receiver="ztk@galaxy", 
        amount=1, #building a new block (or figuring out the proof number) is awarded with 1
    )
    last_hash = last_block.compute_hash
    block = blockchain.build_block(proof_num, last_hash)
    blockchain.print()

if __name__ == "__main__":
    main()