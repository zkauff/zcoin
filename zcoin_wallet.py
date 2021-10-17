import tkinter as tk
from tkinter import * 
import socket
import os
import requests
import yaml
import multiprocessing
import time 

PORT = 5432

class zcoin_wallet_app():

    def __init__(self, user):
        """
        Opens up a wallet application for the given user. 
        Runs a zcoin_instance on port 5432 as a subprocess.
        :param user: a hashed representation for the given user
        """
        self.master = tk.Tk()
        self.instance = multiprocessing.Process(target=os.system, args=("python zcoin_instance.py -p 5432",))
        self.instance.start()
        # TODO: read user and initial peers from .yaml
        # TODO: run program in background to start up api
        self.api = f"http://{socket.gethostbyname(socket.gethostname())}:{PORT}"
        self.peers = []
        with open("well_known_peers.yaml", 'r') as stream:
            peers = yaml.load(stream)['known_peers']
            print(peers)
        self.master.title('ZCoin Wallet')
        self.user = user
        self.displayVar = StringVar()
        #check_funds will set the displayVar
        self.check_funds()
        """
        Labels:
        -   Displays user
        -   Displays the user's current available funds
        """
        Label(self.master, text=user).grid(row=0)
        Label(self.master, textvariable=self.displayVar).grid(row=0, column=1)
        """
        Buttons:
        -   First button updates the user's available funds
        -   Second button closes the application
        """
        tk.Button(self.master, text='Check Again', width=25, command=self.check_funds).grid(row=1)
        tk.Button(self.master, text='Close Application', width=25, command=self.master.destroy).grid(row=1, column=1)

        self.master.mainloop()
        self.instance.terminate()

    def check_funds(self):
        self.funds = 0
        response = requests.get(self.api + "/chain")
        if response.status_code == 200:
            chain = response.json()["chain"]
            for block in chain:
                for transaction in block["transactions"]:
                    if transaction["receiver"] == self.user:
                        self.funds = self.funds + transaction["amount"]
            self.displayVar.set(f"AVAILABLE FUNDS={self.funds} zcoin")



if __name__ == '__main__':
    zcoin_wallet_app("ztk@iastate.edu")