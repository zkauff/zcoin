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
                 transactions,
                 timestamp=time.time()):
        self.idx = idx
        self.proof_num = proof_num
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 2

    def set_nonce(self, nonce):
        self.nonce = nonce

    def print(self):
        """
        Prints out the current block in a readable format.
        :return: <str>
        """
        block_str = "----------\nBlock ID: {}\nProof #{}\nHash: {}\nPrev Hash: {}\nData: {}\nTimestamp: {}".format(
            self.idx,
            self.proof_num,
            self.compute_hash,
            self.prev_hash,
            self.transactions,
            self.timestamp
            )
        print(block_str)
        return block_str

    @property
    def compute_hash(self):
        """
        Creates a SHA-256 hash of this block.
        :return: <str>
        """

        block_str = "{}{}{}{}{}{}".format(
            self.idx,
            self.nonce,
            self.proof_num,
            self.prev_hash,
            self.transactions,
            self.timestamp
            )
        return hashlib.sha256(block_str.encode()).hexdigest()

