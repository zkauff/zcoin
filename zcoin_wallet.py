import tkinter as tk
from tkinter import * 
import socket
import os
import requests
import yaml
import multiprocessing
import time 
import hashlib 

PORT = 5432

class zcoin_wallet_app():

    def __init__(self, user):
        """
        Opens up a wallet application for the given user. 
        Runs a zcoin_instance on port 5432 as a subprocess.
        :param user: a hashed representation for the given user
        """
        self.window = tk.Tk()
        #self.instance = multiprocessing.Process(target=os.system, args=("python zcoin_instance.py -p 5432",))
        #self.instance.start()
        self.url = f"http://{socket.gethostbyname(socket.gethostname())}:{PORT}"
        self.peers = []
        with open("well_known_peers.yaml", 'r') as stream:
            peers = yaml.safe_load(stream)['known_peers']
            print(peers)
        self.window.title('ZCoin Wallet')
        self.user_display = Frame(master=self.window)
        self.options = Frame(master=self.window)
        self.new_transaction_labels = Frame(master=self.window)
        self.new_transaction = Frame(master=self.window)
        self.alert = Frame(master=self.window)

        self.setting_up_transaction=False
        self.user = hashlib.sha256(user.encode()).hexdigest()
        self.displayVar = StringVar()
        #check_funds will set the displayVar
        self.check_funds()
        """
        Labels:
        -   Displays user
        -   Displays the user's current available funds
        """
        Label(self.user_display, width=75, text=self.user).pack(side=LEFT, anchor=tk.W)
        Label(self.user_display, width=50, textvariable=self.displayVar).pack(side=RIGHT, anchor=tk.W)

        """
        Buttons:
        -   First button updates the user's available funds
        -   Second button starts a new transaction
        """
        Button(self.options, text='Refresh Balance', width=50, command=self.check_funds).pack(side=LEFT, anchor=tk.W)
        Button(self.options, text='New Transaction', width=50, command=self.setup_new_transaction).pack(side=RIGHT, anchor=tk.W)
        #tk.Button(self.window, text='Close application', width=25, command=self.window.destroy).grid(row=2, column=2)

        self.user_display.pack()
        self.options.pack()
        self.new_transaction_labels.pack()
        self.new_transaction.pack()
        self.alert.pack()
        self.window.mainloop()

    def setup_new_transaction(self):
        if not self.setting_up_transaction:
            self.setting_up_transaction = True
            # Validate to ensure that only floats are in the entry field
            vcmd = (self.window.register(self.validate), 
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            """
            Text fields: 
            -   Transaction recipient
            -   Amount        
            """
            Label(self.new_transaction_labels, text="New transaction recipient", width=50).pack(side=LEFT, anchor=tk.W)
            Label(self.new_transaction_labels, text="New transaction amount", width=50).pack(side=RIGHT, anchor=tk.W)
            self.recipient = Entry(self.new_transaction, width=50)#, validate='key', validatecommand=vcmd)
            self.recipient.pack(side=LEFT, anchor=tk.W)
            self.amount = Entry(self.new_transaction, width=50)#, validate='key', validatecommand=vcmd)
            self.amount.pack(side=RIGHT, anchor=tk.W)
            Button(self.alert, text="Submit transaction", width=100, command=self.submit_transaction).pack()


    def submit_transaction(self):
        params = {'sender': self.user,
                  'recipient': self.recipient.get(),
                  'amount': float(self.amount.get())}
        resp = requests.post(self.url + '/transactions/new', json=params)
        Label(self.alert, text=resp.text).pack()
        print(resp.text)

    def validate(self, action, index, value, prior_value, text,
        validation_type, trigger_type, widget_name):
        print("validation not implemented yet")

    def check_funds(self):
        self.funds = 0
        response = requests.get(self.url + "/chain")
        if response.status_code == 200:
            chain = response.json()["chain"]
            for block in chain:
                for transaction in block["transactions"]:
                    if transaction["receiver"] == self.user:
                        self.funds = self.funds + transaction["amount"]
            self.displayVar.set(f"AVAILABLE FUNDS={self.funds} zcoin")



if __name__ == '__main__':
    zcoin_wallet_app(os.environ["ZCOIN_USER"])