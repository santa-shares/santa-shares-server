import json, uuid, logging
from flask import request, g, abort
from flask_restful import Resource, marshal_with, fields
from endpoints import api
from extensions import db
import models

logger = logging.getLogger(__name__)

public_user_fields = {
    "user_id" : fields.Integer(attribute="id"),
    "user_name" : fields.String,
    "balance" : fields.String
}

private_user_fields = {
    "user_id" : fields.Integer(attribute="id"),
    "user_name" : fields.String,
    "balance" : fields.String,
    "token" : fields.String
}

class Users(Resource):
    @marshal_with(public_user_fields)
    def get(self):
        return models.User.query.all(), 200

    @marshal_with(private_user_fields)
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