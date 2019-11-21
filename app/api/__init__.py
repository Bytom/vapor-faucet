from flask import Blueprint
from flask_restful import Api

from app.api.resources import Create_Entropy
from app.api.resources import Get_Testnet_Coins

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(Create_Entropy, '/create_entropy')
api.add_resource(Get_Testnet_Coins, '/get_testnet_coins')