import requests
import json

def get_testnet_coins(address_str, asset_str):
    print("address:", address_str)
    print("asset:  ", asset_str)

    asset_dict = {
        "btm":  "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "btc":  "d50a426bdaaf1458d161aba4d8c3ebdd095eac7e1bbeb4a0252a3737ccf2d492",
        "eth":  "a0889e1080999e59ed552865a1d3ee677202796222141ccc3552041708aad76c",
        "usdt": "4483893ef7d9aac788c0e9e49a12398c1d35a2172adb1c8dc551fd169a6f5703",
    }

    account_id = "a6015f95-11f6-4183-8570-84c3c7b85e98"
    # account_id = "94e33787-d27a-47cb-a74f-8e59c6e1c68d"
    password = "123456"
    fee = 10**7    # transaction fee is 0.01 BTM
    amount = 10**9 # user can get 10 BTM or other asset test coin

    build_url = "http://127.0.0.1:9889/build-transaction"
    sign_url = "http://127.0.0.1:9889/sign-transaction"
    submit_url = "http://127.0.0.1:9889/submit-transaction"

    if asset_str == "btm":
        asset_id = asset_dict['btm']
    elif asset_str == "btc":
        asset_id = asset_dict['btc']
    elif asset_str == "eth":
        asset_id = asset_dict['eth']
    elif asset_str == "usdt":
        asset_id = asset_dict['usdt']
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
                "address": address_str,
                "type": "control_address"
            })
    
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }
    proxies = {
        "http": None,
        "https": None
    }

    # build transaction
    transaction_json = json.dumps(transaction_dict)
    response = requests.post(build_url, data=transaction_json, headers=headers, proxies=proxies)
    if response.content:
        response = response.json()
        print("build transaction completely.")
    else:
        return {
            "tx_id": "",
            "message": "failed to get test coin, build transaction failed.",
            "result": False
            }

    # sign transaction
    built_transaction_dict = {
        "password": password,
        "transaction": response['data']
    }
    built_transaction_json = json.dumps(built_transaction_dict)
    response = requests.post(sign_url, data=built_transaction_json, headers=headers, proxies=proxies)
    if response.content:
        response = response.json()
        print("sign transaction completely.")
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
    response = requests.post(submit_url, headers=headers, data=signed_transaction_json, proxies=proxies)
    if response.content:
        response = response.json()
        print("submit transaction completely.")
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
