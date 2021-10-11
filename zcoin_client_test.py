from zcoin_client import zcoin_instance
import requests
import threading
import socket
import pytest

ip = "0.0.0.0"

@pytest.fixture
def run_client_instances():
    good_chain = zcoin_instance(5000)
    empty_chain = zcoin_instance(5001)
    p1 = threading.Thread(target=good_chain.run, args=())
    p1.daemon = True
    p1.start()
    p2 = threading.Thread(target=empty_chain.run, args=())
    p2.daemon = True
    p2.start()
    global ip
    ip = socket.gethostbyname(socket.gethostname())

def test_consensus_update_chain(run_client_instances):
    """
    Sets up two instances of the blockchain. One will not mine any coins,
    and the other will mine one coin with some transactions.
    The consensus algorithm will be run and the blockchain without any mined
    coins should accept the other chain.
    """
    requests.get(f"http://{ip}:5000/mine")
    requests.get(f"http://{ip}:5000/mine") 
    original_chain = requests.get(f"http://{ip}:5000/chain").json()
    # add peer nodes
    requests.post(f"http://{ip}:5001/peers/add", json={"peers": [f"{ip}:5000"]} )
    chain_before = requests.get(f"http://{ip}:5001/chain").json()
    requests.get(f"http://{ip}:5001/peers/consensus")
    chain_after = requests.get(f"http://{ip}:5001/chain").json()
    print(chain_before)
    print(chain_after)
    assert chain_after != chain_before
    assert chain_after == original_chain