import requests
import json

def get_testnet_coins(receiver_str, asset_str):
    asset_dict = {
        "btm": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "btc": "aaffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "eth": "bbffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    }

    account_id = "10CJPO1HG0A02"
    password = "12345"
    fee = 10**7    # transaction fee is 0.01 BTM
    amount = 10**9 # user can get 10 BTM or other asset test coin

    build_url = "http://127.0.0.1:9888/build-transaction"
    sign_url = "http://127.0.0.1:9888/sign-transaction"
    submit_url = "http://127.0.0.1:9888/submit-transaction"

    if asset_str == "btm":
        asset_id = asset_dict['btm']
    elif asset_str == "btc":
        asset_id = asset_dict['btc']
    elif asset_str == "eth":
        asset_id = asset_dict['eth']
    else:
        return {
            "tx_id": "",
            "message": "failed to get test coin, asset is invalid",
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
    
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }

    # build transaction
    transaction_json = json.dumps(transaction_dict)
    print("transaction_json:", transaction_json)
    response = requests.post(build_url, data=transaction_json)
    if response.content:
        response = response.json()
    else:
        return {
            "tx_id": "",
            "message": "failed to get test coin, build transaction failed.",
            "result": False
            }

    print("response:", response)

    # sign transaction
    built_transaction_dict = {
        "password": password,
        "transaction": response['data']
    }
    built_transaction_json = json.dumps(built_transaction_dict)
    response = requests.post(sign_url, data=built_transaction_json)
    if response.content:
        response = response.json()
    else:
        return {
            "tx_id": "",
            "message": "failed to get test coin, sign transaction failed.",
            "result": False
            }

    # submit transaction
    signed_transaction_dict = {
        "raw_transaction": response['data']['transaction']['raw_transaction']
    }
    signed_transaction_json = json.dumps(signed_transaction_dict)
    response = requests.post(submit_url, headers=headers, data=signed_transaction_json)
    if response.content:
        response = response.json()
    else:
        return {
            "tx_id": "",
            "message": "failed to get test coin, submit transaction failed.",
            "result": False
            }
    
    return {
        "tx_id": response['data']['tx_id'],
        "message": "get test coin successfully.",
        "result": True
    }

receiver = "sm1qwrcll07ney9zutvng2w3gw8y7jmsyhfkx7vhv7"
asset = "btm"
r = get_testnet_coins(receiver, asset)
print("txID:", r)
