from algosdk import account, logic
from algosdk.future import transaction
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
import json
# import base64
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

from utility.general import get_private_key_from_mnemonic
# from utility.state import read_global_state
import config

if __name__ == "__main__":
    algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
    # creator_private_key = get_private_key_from_mnemonic(config.creator_mnemonic)

    buyer_private_key = get_private_key_from_mnemonic(config.buyer_mnemonic)

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 

    application_info=algod_client.application_info(config.app_id)

    print("Application Info for app id: {}".format(
        json.dumps(application_info, indent=4)))