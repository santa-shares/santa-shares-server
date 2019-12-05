import logging, json
from flask import request, g, abort
from flask_restful import Resource
from models.item import Item
from tools import error
from extensions import auth, db
from endpoints import api

logger = logging.getLogger(__name__)

class Items(Resource):

    def get(self):
        json_response = {
            "data" : [{
                "item_id" : item.id,
                "item_name" : item.name,
                "price" : item.get_current_price(),
                "amount" : item.amount
            } for item in Item.query.all()]
        }
        return json_response

api.add_resource(Items, '/items')