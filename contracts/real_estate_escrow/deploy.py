from algosdk import account, mnemonic
from algosdk.encoding import decode_address, encode_address
from algosdk.v2client import algod
from algosdk.future import transaction
from contract import approval_program, clear_state_program
from pyteal import compileTeal, Mode
from utility.general import get_private_key_from_mnemonic, wait_for_confirmation, compile_program, intToBytes
from utility.state import read_global_state
from utility.time import get_current_timestamp, get_future_timestamp_in_days, get_future_timestamp_in_secs
import config
import json
import time

# create new application
def create_app(
    client,
    private_key,
    approval_program,
    clear_program,
    global_schema,
    local_schema,
    app_args,
):
    sender = account.address_from_private_key(private_key)

    on_complete = transaction.OnComplete.NoOpOC.real
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        approval_program,
        clear_program,
        global_schema,
        local_schema,
        app_args,
    )

    # txn = transaction.ApplicationUpdateTxn(
    #     sender,
    #     params,
    #     354,
    #     approval_program,
    #     clear_program,
    #     app_args
    # )

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)

    print(transaction_response)

    app_id = transaction_response["application-index"]
    
    # app_id = transaction_response["txn"]["txn"]["apid"]
    
    print("Created new app-id:", app_id)

    return app_id

def main():
    algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
    creator_private_key = get_private_key_from_mnemonic(config.creator_mnemonic)

    # seller_private_key = get_private_key_from_mnemonic(config.seller_mnemonic)
    # buyer_private_key = get_private_key_from_mnemonic(config.buyer_mnemonic)
    # print('buyer_private_key', buyer_private_key)

    # public_key = mnemonic.to_public_key(config.buyer_mnemonic)

    # print('public_key', public_key)

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 12
    global_bytes = 5
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)
 
    approval_program_ast = approval_program()
    approval_program_teal = compileTeal(
        approval_program_ast, mode=Mode.Application, version=5
    )
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    clear_state_program_ast = clear_state_program()
    clear_state_program_teal = compileTeal(
        clear_state_program_ast, mode=Mode.Application, version=5
    )
    clear_state_program_compiled = compile_program(
        algod_client, clear_state_program_teal
    )

    inspectionBegin = int(get_current_timestamp())
    inspectionEnd = int(get_future_timestamp_in_secs(60))
    inspectionExtension = int(get_future_timestamp_in_secs(120))
    closingDate = int(get_future_timestamp_in_secs(240))
    closingDateExtension = int(get_future_timestamp_in_secs(360))
    
    app_args = [
        intToBytes(inspectionBegin), #
        intToBytes(inspectionEnd), #
        intToBytes(inspectionExtension), #
        intToBytes(closingDate), #
        intToBytes(closingDateExtension), #
        300000, # sale_price
        100000, # 1st_escrow_amount
        200000, # 2nd_escrow_amount
        decode_address("RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM"), # buyer
        decode_address("QHGMAMCTEHZ2RQV2DRXSPAKIIT3REVK46CHNDJSW6WNXJLSJ7BB76NHDGY"), # seller
        "" # arbiter
    ]

    app_id = create_app(
        algod_client,
        creator_private_key,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        app_args,
    )

    global_state = read_global_state(
            algod_client, account.address_from_private_key(creator_private_key), app_id
    ),

    print("Global state: {}".format(
            json.dumps(global_state, indent=4)
        )
    )

if __name__ == "__main__":
    main()
    # print(decode_address("RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM"))