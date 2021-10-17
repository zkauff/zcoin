from zcoin_instance import zcoin_instance
import socket
import pytest
import json
from BlockChain import BlockChain

ip = "0.0.0.0"
inst1 = None 
PORT1 = 5000

@pytest.fixture
def run_client_instances():
    global ip, inst1
    inst1 = zcoin_instance(PORT1, "root@zcoin.com").app.test_client()
    ip = socket.gethostbyname(socket.gethostname())

def test_mining_updates_chain(run_client_instances):
    original_chain = json.loads(inst1.get("/chain").data.decode())["length"]
    inst1.get("/mine")
    inst1.get("/mine") 
    new_chain = json.loads(inst1.get("/chain").data.decode())["length"]
    assert new_chain == original_chain + 2

def test_transaction_gets_mined(run_client_instances):
    resp = inst1.post("/transactions/new", 
        data=json.dumps(dict(sender="ROOT_NODE",
                             recipient="zkauff",
                             amount=3)),
        content_type='application/json',
        follow_redirects=True)
    inst1.get("/mine")
    resp=json.loads(inst1.get("/chain").data.decode())
    receiver = resp["chain"][resp["length"] - 1]["transactions"][0]["receiver"]
    assert receiver=="zkauff"