from zcoin_client import zcoin_instance
import socket
import pytest
import json

ip = "0.0.0.0"
inst1 = None 
PORT1 = 5000

@pytest.fixture
def run_client_instances():
    global ip, inst1, inst2
    inst1 = zcoin_instance(PORT1).app.test_client()
    ip = socket.gethostbyname(socket.gethostname())

def test_consensus_update_chain(run_client_instances):
    """
    Sets up two instances of the blockchain. One will not mine any coins,
    and the other will mine one coin with some transactions.
    The consensus algorithm will be run and the blockchain without any mined
    coins should accept the other chain.
    """
    original_chain = json.loads(inst1.get("/chain").data.decode())["length"]
    inst1.get("/mine")
    inst1.get("/mine") 
    new_chain = json.loads(inst1.get("/chain").data.decode())["length"]
    assert new_chain == original_chain + 2