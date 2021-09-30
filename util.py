import json
import time
from datetime import datetime


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