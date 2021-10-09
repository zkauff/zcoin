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
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = BlockChain()


    @app.route('/mine', methods=['GET'])
    def mine():
        block = blockchain.mine_block(miner=node_identifier)

        response = {
            'message': "New Block Mined!!!",
            'index': block['idx'],
            'transactions': block['transactions'],
            'proof': block['proof_num'],
            'hash': block['hash'],
            'previous_hash': block['prev_hash'],
        }
        return jsonify(response), 200

    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        values = request.get_json()
        # Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        try:
            if not all(k in values for k in required):
                return 'Missing values', 400
        except:
            return 'Missing values', 400
        print(f"Incoming transaction:\n    {values}")
            # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index} when it is mined.'}
        return jsonify(response), 201

    @app.route('/chain', methods=['GET'])
    def full_chain():
        bc = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(bc), 200

    app.run(host='0.0.0.0', port=5000)