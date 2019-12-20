import logging, json, models, datetime
from flask import request, g, abort
from flask_restful import Resource, marshal_with, fields
from extensions import auth, db
from endpoints import api

logger = logging.getLogger(__name__)

item_fields = {
    "item_id" : fields.Integer(attribute="id"),
    "item_name" : fields.String(attribute="name"),
    "price" : fields.Integer(),
    "amount" : fields.Integer
}

class Items(Resource):
    @marshal_with(item_fields)
    def get(self):
        items = models.Item.query.all()
        for item in items: item.price = item.get_current_price()
        return items

class Item(Resource):
    @marshal_with(item_fields)
    def get(self, item_id=None):
        if item_id is None: abort(404)
        item = models.Item.query.filter_by(id=item_id).first()
        item.price = item.get_current_price()
        return item

api.add_resource(Items, '/items')
api.add_resource(Item, '/items/<int:item_id>')