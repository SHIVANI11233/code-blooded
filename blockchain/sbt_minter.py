from algosdk import algod, transaction, mnemonic
import time

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

MNEMONIC = "PASTE YOUR TESTNET MNEMONIC HERE"
private_key = mnemonic.to_private_key(MNEMONIC)
creator = mnemonic.to_public_key(MNEMONIC)

def mint_attendance_sbt(student_address, session_name):
    params = client.suggested_params()

    txn = transaction.AssetConfigTxn(
        sender=creator,
        sp=params,
        total=1,                # only ONE token
        decimals=0,
        default_frozen=True,    # cannot move
        unit_name="ATTEND",
        asset_name=f"Attendance-{session_name}",
        manager="",             # no manager
        reserve="",
        freeze="",
        clawback=""             # no clawback
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)

    print("SBT creation TXID:", txid)
    return txid

