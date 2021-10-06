import json
import time
from datetime import datetime

def verify_hash_zeroes(hash, threshold):
    if threshold > len(hash):
        raise RuntimeError("Requesting a hash with more zeros than elements of the hash!")
    for i in range(threshold):
        if hash[i] == '0':
            continue
        else:
            return 0
    return 1

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