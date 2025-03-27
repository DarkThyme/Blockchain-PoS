import requests
from BlockChain import generate_keys, sign_transaction

BASE_URL = "http://127.0.0.1:5000"

#Step 1: Generate Keys
private_key, public_key = generate_keys()
print(f"Private Key: {private_key}")
print(f"Public Key: {public_key}")

#Step 2: Sign a Transaction
sender = "Alice"
receiver = "Bob"
amount = 100
signature = sign_transaction(private_key, sender, receiver, amount)

#Step 3: Send the Signed Transaction to Blockchain
transaction_data = {
    "sender": sender,
    "receiver": receiver,
    "amount": amount,
    "signature": signature,
    "public_key": public_key
}

response = requests.post(f"{BASE_URL}/add_transaction", json=transaction_data)
print("Transaction Response:", response.json())

#Step 4: Fetch the Updated Blockchain Data
response = requests.get(f"{BASE_URL}/get_chain")
print("Blockchain Data:", response.json())

#Step 5: Stake Tokens for Proof-of-Stake
stake_data = {
    "node": sender,
    "amount": 500
}
response = requests.post(f"{BASE_URL}/stake", json=stake_data)
print("Stake Response:", response.json())
