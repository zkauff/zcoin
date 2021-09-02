import hashlib
import time

"""
One Block in our blockchain
"""
class Block(object):
    def __init__(self,
                 idx, 
                 proof_num,
                 prev_hash,
                 data,
                 timestamp=time.time()):
        self.idx = idx
        self.proof_num = proof_num
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp

    def print(self):
        block_str = "----------\nBlock ID: {}\nProof #{}\nPrev Hash: {}\nData: {}\nTimestamp: {}\n----------".format(
            self.idx,
            self.proof_num,
            self.prev_hash,
            self.data,
            self.timestamp
            )
        print(block_str)

    @property
    def compute_hash(self):
        block_str = "{}{}{}{}{}".format(
            self.idx,
            self.proof_num,
            self.prev_hash,
            self.data,
            self.timestamp
            )
        return hashlib.sha256(block_str.encode()).hexdigest()

