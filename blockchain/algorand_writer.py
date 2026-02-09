"""
SAL - Write verified attendance to Algorand TestNet
Phase 5: Immutable blockchain record.
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# Paste your 25-word mnemonic after funding on TestNet faucet
MNEMONIC = "PASTE YOUR MNEMONIC HERE"


def write_to_blockchain(attendance_hash: str, session_id: str) -> str:
    """Write verified participation to Algorand. Returns transaction ID."""
    if "PASTE" in MNEMONIC or not MNEMONIC.strip():
        raise ValueError("Set MNEMONIC in blockchain/algorand_writer.py (fund account at TestNet faucet first)")

    private_key = mnemonic.to_private_key(MNEMONIC)
    sender = account.address_from_private_key(private_key)

    params = client.suggested_params()
    note = f"VERIFIED|{session_id}|{attendance_hash}".encode()

    txn = transaction.PaymentTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        note=note,
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    return txid
