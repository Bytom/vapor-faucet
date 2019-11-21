import requests
import json

def get_testnet_coins(receiver_str, asset_str):
    asset_dict = {
        "btm": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "btc": "aaffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "eth": "bbffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    }

    account_id = "0KN9JNBA00A02"
    fee = 1000000         # transaction fee is 0.01 BTM
    amount = 10 * 100000000 # user can get 10 BTM or other asset test coin

    if asset_str == "btm":
        asset_id = asset_dict['btm']
    elif asset_str == "btc":
        asset_id = asset_dict['btc']
    elif asset_str == "eth":
        asset_id = asset_dict['eth']
    else:
        return {
            "tx_id": "",
            "message": "asset is invalid",
            "result": False
            }

    transaction_dict = {
        "actions":[],
        "ttl":0,
        "time_range":0
    }

    # actions for tx fee
    transaction_dict['actions'].append({
                "account_id": account_id,
                "amount": fee,
                "asset_id": asset_dict['btm'],
                "type": "spend_account",
                "use_unconfirmed": True
            })

    # action for spend asset
    transaction_dict['actions'].append({
                "account_id": account_id,
                "amount": amount,
                "asset_id": asset_id,
                "type": "spend_account",
                "use_unconfirmed": True
            })

     # action for receive asset
    transaction_dict['actions'].append({
                "amount": amount,
                "asset_id": asset_id,
                "address": receiver_str,
                "type": "control_address"
            })
    
    transaction_json = json.dumps(transaction_dict)
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }
    build_url = "http://127.0.0.1:9888/build-transaction"
    response = requests.post(build_url, data=transaction_json).json()
    built_transaction_dict = {
        "password": "12345",
        "transaction": response['data']
    }
    built_transaction_json = json.dumps(built_transaction_dict)
    sign_url = "http://127.0.0.1:9888/sign-transaction"
    response = requests.post(sign_url, headers=headers, data=built_transaction_json).json()
    signed_transaction_dict = {
        "raw_transaction": response['data']['transaction']['raw_transaction']
    }
    signed_transaction_json = json.dumps(signed_transaction_dict)
    submit_url = "http://127.0.0.1:9888/submit-transaction"
    response = requests.post(submit_url, headers=headers, data=signed_transaction_json).json()
    
    return {
        "tx_id": response['data']['tx_id'],
        "message": "get test coin successfully.",
        "result": True
    }
