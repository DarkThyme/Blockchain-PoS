# Blockchain-PoS
A Python-based Blockchain with Smart Contracts, Digital Signatures, Peer-to-Peer Networking, and Proof-of-Stake (PoS) Mechanism
 Features
✅ Blockchain Implementation – Securely stores transactions in blocks
✅ Proof-of-Stake (PoS) Consensus – Chooses validators based on staked tokens
✅ Digital Signatures & Cryptography – Uses ECDSA for transaction verification
✅ Smart Contracts (Basic) – Enforces transaction rules before processing
✅ Peer-to-Peer (P2P) Network – Syncs blockchain across multiple nodes
✅ Flask API – Allows interaction with the blockchain via REST API

 How It Works
1️⃣ Users generate cryptographic keys for signing transactions
2️⃣ Transactions are digitally signed and verified before adding to the blockchain
3️⃣ The system selects a PoS validator based on staked tokens
4️⃣ Blocks are added to the blockchain and synchronized across the network
5️⃣ Users can stake tokens to increase their chances of becoming a validator

 Technologies Used
Python (Core Logic)

Flask (REST API)

ECDSA (Elliptic Curve Cryptography for Digital Signatures)

Requests (P2P Network Communication)

 Usage Instructions
Clone the repository:
git clone https://github.com/DarkThyme/Blockchain-PoS.git
cd Blockchain-PoS

Install dependencies:
pip install -r requirements.txt

Start the blockchain server:
python BlockChain.py

Run the test script:
python test_blockchain.py


