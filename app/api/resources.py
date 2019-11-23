from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from app.model.key import create_entropy
from app.model.faucet import get_testnet_coins

parser = reqparse.RequestParser()
parser.add_argument('address', type=str)
parser.add_argument('asset', type=str)

class Create_Entropy(Resource):

    def post(self):
        entropy = create_entropy()
        return entropy

class Get_Testnet_Coins(Resource):

    def post(self):
        args = parser.parse_args()
        address = args.get('address')
        asset = args.get('asset')
        tx_id = get_testnet_coins(address, asset)
        return tx_id
