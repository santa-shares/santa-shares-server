import json, uuid, logging
from flask import request, g, abort
from flask_restful import Resource, marshal_with, fields
from endpoints import api
from extensions import db
import models

logger = logging.getLogger(__name__)

user_fields = {
    "user_id" : fields.Integer(attribute="id"),
    "user_name" : fields.String,
    "balance" : fields.Integer,
    "stock_value" : fields.Integer,
    "total" : fields.Integer
}

user_register_fields = {
    "user_id" : fields.Integer(attribute="id"),
    "user_name" : fields.String,
    "balance" : fields.Integer,
    "token" : fields.String,
}

item_fields = {
    "item_id" : fields.Integer(attribute="item_id"),
    "item_name" : fields.String(attribute="item.name"),
    "amount" : fields.Integer,
    "price" : fields.Integer,
}

user_status_fields = {
    "user_id" : fields.Integer(attribute="id"),
    "user_name" : fields.String,
    "balance" : fields.Integer,
    'items': fields.List(fields.Nested(item_fields))
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = models.User.query.all() 
        for user in users:
            user.stock_value = sum([user_item.item.get_current_price() for user_item in user.items])
            user.total = user.balance + user.stock_value
        return users, 200

    @marshal_with(user_register_fields)
    def post(self):
        user_name = request.json.get('user_name')
        if user_name is None: abort(400, "No [user_name] provided.")
        if models.User.query.filter_by(user_name=user_name).count() > 0: abort(400, "[user_name] already exists.")

        try:
            user = models.User(user_name=user_name, email="test@fnc.co.uk", token=str(uuid.uuid4()), balance=1000_00) 
            db.session.add(user)
            db.session.commit()
            return user, 201
        except Exception as e:
            logger.error(e)
            abort(500)

class User(Resource):
    @marshal_with(user_status_fields)
    def get(self, user_id=None):
        if user_id is None: abort(400)
        user = models.User.query.filter_by(id=user_id).first()
        for user_item in user.items:
            user_item.price = user_item.item.get_current_price()
        return user

api.add_resource(Users, "/users")
api.add_resource(User, "/users/<int:user_id>")