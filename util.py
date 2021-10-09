import json
import time
from datetime import datetime
import hashlib

@staticmethod
def verify_hash_zeroes(hash, threshold):
    if threshold > len(hash):
        raise RuntimeError("Requesting a hash with more zeros than elements of the hash!")
    for i in range(threshold):
        if hash[i] == '0':
            continue
        else:
            return 0
    return 1

def confirm_validity(prev_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{prev_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

class transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()

    def json(self):
        json_dict = {}
        json_dict["sender"] = self.sender
        json_dict["receiver"] = self.receiver
        json_dict["transaction_amount"] = self.amount
        json_dict["timestamp"] = self.timestamp.strftime("%m/%d/%y %H:%M:%S")
        return json.dumps(json_dict, indent=4)

transaction("ztk", "ztk2", 50).json()