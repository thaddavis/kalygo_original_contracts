from re import M
from algosdk import account
from algosdk.future import transaction
from algosdk.v2client import algod
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))
import config
from utility.general import get_private_key_from_mnemonic, wait_for_confirmation, intToBytes
import json


def trigger_pull_out(client, private_key, app_id, app_args):
    sender = account.address_from_private_key(private_key)
    
    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)


if __name__ == "__main__":
    algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
    buyer_private_key = get_private_key_from_mnemonic(config.buyer_mnemonic)

    app_args = [
        "signal_pull_out"
    ]
    trigger_pull_out(algod_client, buyer_private_key, config.app_id, app_args)