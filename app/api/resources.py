from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from app.model.faucet import get_testnet_coins

parser = reqparse.RequestParser()
parser.add_argument('receiver_str', type=str)
parser.add_argument('asset_str', type=str)

class Create_Entropy(Resource):

    def post(self):
        entropy = create_entropy()
        return entropy

class Get_Testnet_Coins(Resource):

    def post(self):
        args = parser.parse_args()
        receiver = args.get('receiver_str')
        asset = args.get('asset_str')
        tx_id = get_testnet_coins(receiver, asset)
        return tx_id
