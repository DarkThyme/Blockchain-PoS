# import hashlib
# import time
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score

# class Block:
#     def __init__(self, index, previous_hash, timestamp, transactions):
#         self.index = index
#         self.previous_hash = previous_hash
#         self.timestamp = timestamp
#         self.transactions = transactions
#         self.hash = self.calculate_hash()

#     def calculate_hash(self):
#         block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.trasactions}".encode()
#         return hashlib.sha256(block_string).hexdigest()
    
# class Blockchain:
#     def __init__(self):
#         self.chain = [self.create_genesis_block()]
    
#     def create_genesis_block(self):
#         return Block(0, "0", time.time(), "Genesis Block")
    
#     def add_block(self, transactions):
#         prev_block = self.chain[-1]
#         new_block = Block(len(self.chain), prev_block.hash, time.time(), transactions)
#         self.chain.append(new_block)

# my_chain = Blockchain()
# transactions = [
#     {"sender": "Ram", "receiver": "Krishna", "amount": 999},
#     {"sender": "Amar", "receiver": "Akbar", "amount": 100},
#     {"sender": "Maddy", "receiver": "Braddy", "amount": 9696}
# ]

# my_chain.add_block(transactions)

# for block in my_chain.chain:
#     print(f"Index: {block.index}.Hash: {block.hash}, Previous Hash: {block.previous_hash}, Transactions: {block.trasactions}")

# ######################################################################################################################################################################################

# data = pd.DataFrame([
#     {"amount" : 999, "is_fraud": 0},
#     {"amount" : 100, "is_fraud": 0},
#     {"amount" : 1000, "is_fraud": 1},
#     {"amount" : 9696, "is_fraud": 1},
#     {"amount" : 0, "is_fraud": 0}
# ])

# x = data[["amount"]]
# y = data["is_fraud"]

# x_train, x_test , y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42)

# model = RandomForestClassifier(n_estimators=10, random_state= 42)
# model.fit(x_train,y_train)

# y_pred = model.predict(x_test)
# print("Model Accuracy: ", accuracy_score(y_test, y_pred))

# #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#

# def is_fraudulent(transaction):
#     amount = np.array(transaction["amount"]).reshape(1,-1)
#     return model.predict(amount)[0] == 1

# new_transactions = [
#     {"sender": "Intel", "receiver": "AMD", "amount": 969},
#     {"sender": "TSMC", "receiver": "Samsung", "amount": 100000},
#     {"sender": "ASML", "receiver": "Nothing", "amount": 420}
# ]

# valid_transactions = [tx for tx in new_transactions if not is_fraudulent(tx)]

# if valid_transactions:
#     my_chain.add_block(valid_transactions)
#     print("Safe transaction added to the blockchain")
# else:
#     print("No valid transactions found")


import hashlib
import time
import json
import random
import ecdsa
import requests
from flask import Flask, request, jsonify
from threading import Thread

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, validator, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.validator = validator  # PoS Validator
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.transactions, sort_keys=True)}{self.validator}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.stakes = {}  # Stores staked amounts for PoS
        self.peers = set()

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "Network")
    
    def add_block(self, transactions):
        validator = self.select_validator()
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), prev_block.hash, time.time(), transactions, validator)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash() or current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def select_validator(self):
        if not self.stakes:
            return "Network"
        return random.choices(list(self.stakes.keys()), weights=self.stakes.values())[0]
    
    def stake_tokens(self, node, amount):
        self.stakes[node] = self.stakes.get(node, 0) + amount

blockchain = Blockchain()

app = Flask(__name__)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    sender = data['sender']
    receiver = data['receiver']
    amount = data['amount']
    signature = data['signature']
    public_key = data['public_key']

    if not verify_signature(sender, receiver, amount, signature, public_key):
        return jsonify({"message": "Invalid Signature"}), 400
    
    blockchain.add_block([data])
    return jsonify({"message": "Transaction added successfully"})

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = [{"index": block.index, "hash": block.hash, "previous_hash": block.previous_hash, "transactions": block.transactions, "validator": block.validator} for block in blockchain.chain]
    return jsonify(chain_data)

@app.route('/stake', methods=['POST'])
def stake():
    data = request.get_json()
    node = data['node']
    amount = data['amount']
    blockchain.stake_tokens(node, amount)
    return jsonify({"message": f"{node} staked {amount} tokens"})

def generate_keys():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key.to_string().hex(), public_key.to_string().hex()

def sign_transaction(private_key_hex, sender, receiver, amount):
    private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    message = f"{sender}{receiver}{amount}".encode()
    return private_key.sign(message).hex()

def verify_signature(sender, receiver, amount, signature, public_key_hex):
    public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
    message = f"{sender}{receiver}{amount}".encode()
    try:
        return public_key.verify(bytes.fromhex(signature), message)
    except ecdsa.BadSignatureError:
        return False

def sync_with_network():
    while True:
        time.sleep(30)
        for peer in blockchain.peers:
            try:
                response = requests.get(f"{peer}/get_chain")
                if response.status_code == 200:
                    external_chain = response.json()
                    if len(external_chain) > len(blockchain.chain):
                        blockchain.chain = external_chain
            except:
                pass

if __name__ == '__main__':
    Thread(target=sync_with_network).start()
    app.run(host='0.0.0.0', port=5000)

