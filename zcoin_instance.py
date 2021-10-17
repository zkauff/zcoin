from uuid import uuid4

from flask import Flask, jsonify, request
from BlockChain import BlockChain
import argparse
import socket
import json
import hashlib

class zcoin_instance(object):
    def __init__(self, port, user=None, initial_peers=[]):
        # Instantiate our Node
        self.app = Flask(__name__)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        print(f"Starting app on {self.ip}:{port}")
        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        # Generate a globally unique address for this node
        if user:
            node_identifier = hashlib.sha256(user.encode()).hexdigest()
        else:
            node_identifier = str(uuid4()).replace("-", "")

        # Instantiate the Blockchain
        blockchain = BlockChain(initial_peers=initial_peers)

        @self.app.route("/mine", methods=["GET"])
        def mine():
            block = blockchain.mine_block(miner=node_identifier)

            response = {
                "message": "New Block Mined!!!",
                "index": block["idx"],
                "transactions": block["transactions"],
                "proof": block["proof_num"],
                "previous_hash": block["prev_hash"],
            }
            return jsonify(response), 200

        @self.app.route("/transactions/new", methods=["POST"])
        def new_transaction():
            values = json.loads(request.data, strict=False)
            print(f"Incoming transaction:\n    {values}")
            # Check that the required fields are in the POST'ed data
            required_params = ["sender", "recipient", "amount"]
            try:
                if not all(k in values for k in required_params):
                    return "Missing parameters", 400
            except:
                return "Missing parameters", 400
                # Create a new Transaction
            index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])
            if index > 0:
                response = {"message": f"Transaction will be added to Block {index} when it is mined."}
            else:
                response = {"message": f"{values['sender']} has insufficient funds for transaction!"}
            return jsonify(response), 201

        @self.app.route("/chain", methods=["GET"])
        def full_chain():
            bc = {
                "chain": blockchain.chain,
                "length": len(blockchain.chain),
            }
            return jsonify(bc), 200

        @self.app.route("/peers/add", methods=["POST"])
        def add_peers():
            values = request.get_json()
            required_params = ["peers"]
            try: 
                if not all(k in values for k in required_params):
                    return "Missing parameters", 400
            except:
                return "Missing parameters", 400
            peers = values.get("peers")
            for peer in peers:
                blockchain.register_peer_node(peer)
            return jsonify({
                "message": "Success! Added peers to our instance",
                "all_peers": list(blockchain.peer_nodes)
            }), 201

        @self.app.route("/peers/consensus", methods=["GET"])
        def resolve_conflicts():
            (was_replaced, new_chain, source) = blockchain.consensus()

            if was_replaced:
                response = {
                    "message": f"Chain was successfully replaced with {source}'s chain",
                    "new_chain": new_chain
                }
            else:
                response = {
                    "message": "This chain was determined to be authoritative after confering with peers.",
                    "chain": blockchain.chain
                }

            return jsonify(response), 200
        
    def run(self):
        self.app.run(host=self.ip, port=self.port)

    def get(self):
        self.resolve_conficts()
        return self.app.test_client().get("/chain")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Z-coin client application on the provided port.")
    parser.add_argument("-p", "--port", type=int, help="the port to run the REST interface on.")
    args = parser.parse_args()
    zcoin_instance(args.port).run()