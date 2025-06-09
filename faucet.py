from flask import Flask, request, jsonify
from flask_cors import CORS
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import os
import json

app = Flask(__name__)
CORS(app)

# Load keypair from Render environment variable
FAUCET_SECRET = os.environ.get("FAUCET_KEYPAIR_JSON")
if not FAUCET_SECRET:
    raise ValueError("Missing FAUCET_KEYPAIR_JSON in environment variables")

secret = json.loads(FAUCET_SECRET)
creator = Keypair.from_bytes(bytes(secret))
client = Client("https://api.devnet.solana.com")

TOKEN_MINT_ADDRESS = "9tc7JNiGyTpPqzgaJMJnQWhLsuPWusVXRR7HgQ3ng5xt"  # Rampana token mint

@app.route("/")
def health():
    return "Rampana Faucet is Live!"

@app.route("/claim", methods=["POST"])
def claim():
    data = request.get_json()
    wallet_address = data.get("wallet")
    if not wallet_address:
        return jsonify({"error": "Missing wallet address"}), 400

    try:
        response = client.request_airdrop(Pubkey.from_string(wallet_address), 1000000000)  # 0.001 SOL
        return jsonify({"success": True, "tx": response["result"]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
