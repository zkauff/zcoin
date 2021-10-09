import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from BlockChain import BlockChain

if __name__ == "__main__":
    # Instantiate our Node
    app = Flask(__name__)

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = BlockChain()


    @app.route('/mine', methods=['GET'])
    def mine():
        # We run the proof of work algorithm to get the next proof...
        last_block = blockchain.last_block
        last_proof = last_block['proof_num']
        proof = blockchain.proof_of_work(last_proof, 0, 0)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            sender="0",
            receiver=node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.build_block(proof, previous_hash)

        response = {
            'message': "New Block Mined!!!",
            'index': block['idx'],
            'transactions': block['transactions'],
            'proof': block['proof_num'],
            'previous_hash': block['prev_hash'],
        }
        return json.dumps(response), 200

        return "We'll mine a new Block"
    
    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        values = request.get_json()

        print(values)
        
        # Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        try:
            if not all(k in values for k in required):
                return 'Missing values', 400
        except:
            return 'Missing values', 400

            # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index}'}
        return json.dumps(response), 201

    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return json.dumps(response), 200

    app.run(host='0.0.0.0', port=5000)