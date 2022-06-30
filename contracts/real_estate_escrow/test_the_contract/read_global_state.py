from algosdk import account
from algosdk.future import transaction
from algosdk.v2client import algod
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

from utility.general import get_private_key_from_mnemonic
from utility.state import read_global_state
import config
import json

if __name__ == "__main__":
    algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
    creator_private_key = get_private_key_from_mnemonic(config.creator_mnemonic)

    global_state = read_global_state(
        algod_client, account.address_from_private_key(creator_private_key), config.app_id
    ),

    print("Global state: {}".format(
            json.dumps(global_state, indent=4)
        )
    )