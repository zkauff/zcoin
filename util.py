import json
import time
from datetime import datetime
import hashlib
from flask import jsonify

def verify_hash_zeroes(hash, threshold):
    if threshold > len(hash):
        raise RuntimeError("Requesting a hash with more zeros than elements of the hash!")
    for i in range(threshold):
        if hash[i] == '0':
            continue
        else:
            return False
    return True

def confirm_validity(prev_proof, proof, difficulty):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        :return: <str> hash of the proof
        """

        guess = f'{prev_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return (verify_hash_zeroes(guess_hash, difficulty), guess_hash)