"""
SAL Blockchain - Record Verified Participation on Algorand TestNet
Phase 5: Write verified attendance hash to immutable blockchain.
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction

# ----- STEP 4: Generate Account (run first time) -----
# Set to True to generate new account, False to write to blockchain
GENERATE_ACCOUNT = False

# ----- STEP 6: Paste your mnemonic after funding -----
MNEMONIC = "PASTE YOUR MNEMONIC HERE"

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""


def main():
    if GENERATE_ACCOUNT:
        # Step 4: Create new TestNet account
        private_key, address = account.generate_account()
        print("ADDRESS:", address)
        print("MNEMONIC (SAVE THIS):")
        print(mnemonic.from_private_key(private_key))
        return

    # Step 6: Write hash to blockchain
    if "PASTE" in MNEMONIC or not MNEMONIC.strip():
        print("ERROR: Replace MNEMONIC with your 25-word phrase, then set GENERATE_ACCOUNT = False")
        return

    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
    private_key = mnemonic.to_private_key(MNEMONIC)
    sender = account.address_from_private_key(private_key)

    params = client.suggested_params()

    # Store verified attendance hash in transaction note (immutable)
    note = b"VERIFIED_ATTENDANCE_HASH:abc123xyz"

    txn = transaction.PaymentTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        note=note,
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)

    print("Transaction ID:", txid)
    print("Verify at: https://testnet.algoexplorer.io/tx/" + txid)


if __name__ == "__main__":
    main()
