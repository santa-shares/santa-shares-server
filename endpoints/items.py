import logging, json, models
from flask import request, g, abort
from flask_restful import Resource, marshal_with, fields
from extensions import auth, db
from endpoints import api

logger = logging.getLogger(__name__)

item_fields = {
    "item_id" : fields.Integer(attribute="id"),
    "item_name" : fields.String(attribute="name"),
    #"price" : fields.Integer(attribute=lambda item: item.get_current_price()),
    "amount" : fields.Integer
}

class Items(Resource):
    @marshal_with(item_fields)
    def get(self):
        return models.Item.query.all()

class Item(Resource):
    @marshal_with(item_fields)
    def get(self, item_id=None):
        print(item_id)
        if item_id is None: abort(404)
        return models.Item.query.filter_by(id=item_id).first()

api.add_resource(Items, '/items')
api.add_resource(Item, '/items/<int:item_id>')