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
        self.nonce = 2

    def set_nonce(self, nonce):
        self.nonce = nonce

    def print(self):
        block_str = "----------\nBlock ID: {}\nProof #{}\nHash: {}\nPrev Hash: {}\nData: {}\nTimestamp: {}".format(
            self.idx,
            self.proof_num,
            self.compute_hash,
            self.prev_hash,
            self.data,
            self.timestamp
            )
        print(block_str)

    @property
    def compute_hash(self):
        block_str = "{}{}{}{}{}{}".format(
            self.idx,
            self.nonce,
            self.proof_num,
            self.prev_hash,
            self.data,
            self.timestamp
            )
        return hashlib.sha256(block_str.encode()).hexdigest()

