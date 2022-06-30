from algosdk import mnemonic
import base64

def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    # return base64.encode(private_key)
    return private_key

def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo

# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])

# convert 64 bit integer i to byte string
def intToBytes(i):
    return i.to_bytes(8, "big")