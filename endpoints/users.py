import json, uuid, logging
from flask import request, g, abort
from flask_restful import Resource
from endpoints import api
from extensions import db
import models
from tools import error
from exceptions import UserNameAlreadyExists

logger = logging.getLogger(__name__)

class Users(Resource):
    def get(self):
            json_response = {
                "data" : [{
                    "user_id" : user.id,
                    "user_name" : user.user_name,
                } for user in models.User.query.all()]
            }
            return json_response, 200

    def post(self):
        user_name = request.json.get('user_name')
        if user_name is None: abort(400, "No username provided")
        if models.User.query.filter_by(user_name=user_name).count() > 0: abort(400, "Username already exists.")

        token = str(uuid.uuid4())

        user = models.User(user_name=user_name, email="test@fnc.co.uk", token=token, balance=1000_00) 
        db.session.add(user)
        db.session.commit()

        json_response = {
            "user_id" : user.id,
            "token" : token
        }
        return json_response, 201

class User(Resource):
    def get(self, user_id=None):
        if user_id is None: abort(400)
        return [{
                "user_id" : user.id,
                "user_name" : user.user_name,
                "balance" : user.balance,
                "items" : [{
                    "item_id" : user_item.item_id,
                    "item_name" : user_item.item.name,
                    "amount" : user_item.amount,
                    "price" : user_item.item.get_current_price(),
            } for user_item in user.items]
        } for user in models.User.query.filter_by(id=user_id)]

api.add_resource(Users, "/users")
api.add_resource(User, "/users/<int:user_id>")