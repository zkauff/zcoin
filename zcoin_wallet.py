import tkinter as tk
from tkinter import * 
import socket
import os
import requests
import yaml
import multiprocessing
import time 
import hashlib 
import argparse 

PORT = 5432

class zcoin_wallet_app():

    def __init__(self, user, addr):
        """
        Opens up a wallet application for the given user. 
        Runs a zcoin_instance on port 5432 as a subprocess.
        :param user: a hashed representation for the given user
        """
        self.window = tk.Tk()
        #self.instance = multiprocessing.Process(target=os.system, args=("python zcoin_instance.py -p 5432",))
        #self.instance.start()
        self.url = addr

        # load in well known peers so we know who to contact 
        self.peers = []
        with open("well_known_peers.yaml", 'r') as stream:
            peers = yaml.safe_load(stream)['known_peers']
            print(peers)

        self.window.title('ZCoin Wallet')

        # setup tkinter frames
        self.user_display = Frame(master=self.window)
        self.options = Frame(master=self.window)
        self.options_lvl2 = Frame(master=self.window)
        self.new_transaction_amount_frame = Frame(master=self.window)
        self.new_transaction_recipient_frame = Frame(master=self.window)
        self.new_transaction_button = Frame(master=self.window)
        self.alert = Frame(master=self.window)

        self.setting_up_transaction=False
        self.user = hashlib.sha256(user.encode()).hexdigest()
        self.balanceVar = StringVar()
        self.alertVar = StringVar()

        #check_funds will set the displayVar
        self.check_funds()
        """
        Labels:
        -   Displays user
        -   Displays the user's current available funds
        """
        Label(self.user_display, width=75, text=self.user).pack(side=LEFT, anchor=tk.W)
        Label(self.user_display, width=50, textvariable=self.balanceVar).pack(side=RIGHT, anchor=tk.W)

        """
        Buttons:
        -   First button updates the user's available funds
        -   Second button starts a new transaction
        -   Third button mines a coin on this machine's instance (if it exists)
        -   Fourth button closes application
        """
        Button(self.options, text='Refresh Balance', width=50, command=self.check_funds).pack(side=LEFT, anchor=tk.W)
        Button(self.options, text='New Transaction', width=50, command=self.setup_new_transaction).pack(side=RIGHT, anchor=tk.W)
        Button(self.options_lvl2, text='Mine coin', width=50, command=self.mine).pack(side=LEFT, anchor=tk.W)
        Button(self.options_lvl2, text='Close application', width=50, command=self.window.destroy).pack(side=RIGHT, anchor=tk.W)

        self.user_display.pack()
        self.options.pack()
        self.options_lvl2.pack()
        self.new_transaction_recipient_frame.pack()
        self.new_transaction_amount_frame.pack()
        self.new_transaction_button.pack()
        Label(self.alert, textvariable=self.alertVar).pack()
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
            self.label1 = Label(self.new_transaction_recipient_frame, text="New transaction recipient", width=50)
            self.label1.pack(side=LEFT, anchor=tk.W)
            self.label2 = Label(self.new_transaction_amount_frame, text="New transaction amount", width=50)
            self.label2.pack(side=LEFT, anchor=tk.W)
            self.recipient = Entry(self.new_transaction_recipient_frame, width=50)
            self.recipient.pack(side=LEFT, anchor=tk.W)
            self.amount = Entry(self.new_transaction_amount_frame, width=50, validate='key', validatecommand=vcmd)
            self.amount.pack(side=RIGHT, anchor=tk.W)
            self.submit_button = Button(self.new_transaction_button, text="Submit transaction", width=100, command=self.submit_transaction)
            self.submit_button.pack()
        else:
            self.setting_up_transaction = 0
            self.recipient.destroy()
            self.amount.destroy()
            self.submit_button.destroy()
            self.label1.destroy()
            self.label2.destroy()


    def submit_transaction(self):
        try:
            params = {'sender': self.user,
                      'recipient': self.recipient.get(),
                      'amount': float(self.amount.get())}
            resp = requests.post(self.url + '/transactions/new', json=params)
            self.alertVar.set(resp.text)
            self.check_funds()
        except:
            self.alertVar.set("Couldn't submit transaction.")

    def validate(self, action, index, value_if_allowed, prior_value, text,
        validation_type, trigger_type, widget_name):
        if(action=='1'):
            if text in '0123456789':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
        else:
            return True

    def mine(self):
        try:
            resp = requests.get(self.url + "/mine")
            if resp.status_code == 200:
                self.alertVar.set("Successfully mined a coin!")
                self.check_funds()
            else:
                self.alertVar.set("Couldn't connect to chain endpoint.")
        except:
            self.alertVar.set("Couldn't connect to chain endpoint.")

    def check_funds(self):
        params = {'user': self.user}
        response = requests.get(self.url + "/users/balance", json=params)
        if response.status_code == 200:
            self.balanceVar.set(f"AVAILABLE FUNDS={response.json()['balance']} zcoin")

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Run the Z-coin client application on the provided port.")
    parser.add_argument("--addr",
        default=f"http://{socket.gethostbyname(socket.gethostname())}:{PORT}", 
        help="the blockchain endpoint we should connect to")
    parser.add_argument("-u", "--user", 
        default=os.environ["ZCOIN_USER"], 
        help="the private user key to sign in with")
    args = parser.parse_args()
    zcoin_wallet_app(args.user, args.addr)