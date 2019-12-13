import json, uuid, logging, datetime
from flask import request, g, abort
from flask_restful import Resource, marshal_with, fields
from endpoints import api
from extensions import db, auth
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


user_history_fields = {
    "time" : fields.DateTime,
    "balance" : fields.Integer,
    "stock_value" : fields.Integer,
    "stock_amount" : fields.Integer,
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = models.User.query.all() 
        for user in users:
            user.stock_value = sum([user_item.item.get_current_price() * user_item.amount for user_item in user.items])
            user.total = user.balance + user.stock_value
        return users, 200

    @marshal_with(user_register_fields)
    def post(self):
        user_name = request.json.get('user_name')
        if user_name is None: abort(400, "No [user_name] provided.")
        if models.User.query.filter_by(user_name=user_name).count() > 0: abort(400, "[user_name] already exists.")

        # how many users have the same ip
        # ip_address = request.remote_addr
        # if models.User.query.filter_by(ip_address=ip_address).count() > 10: abort(400, "Too many accounts have been registered with this ip. Delete some accounts then try again.")

        try:
            user = models.User(
                user_name=user_name,
                token=str(uuid.uuid4()),
                datetime_created=datetime.datetime.now(),
                balance=1000_00,
                ip_address="dontcare"
            ) 
            db.session.add(user)
            db.session.commit()
            return user, 201
        except Exception as e:
            logger.error(e)
            abort(500)

    @auth.login_required
    def delete(self):
        db.session.delete(g.current_user)

class User(Resource):
    @marshal_with(user_status_fields)
    def get(self, user_id=None):
        if user_id is None: abort(400)
        user = models.User.query.filter_by(id=user_id).first()
        if user is None:
            return None

        for user_item in user.items:
            user_item.price = user_item.item.get_current_price()
        return user

class UserHistory(Resource):

    @marshal_with(user_history_fields)
    def get(self, user_id):
        user = models.User.query.filter_by(id=user_id).first()
        if user is None: abort(400, "No user with ID.")

        start_time = user.datetime_created
        time = start_time
        end_time = datetime.datetime.now()

        data = []
        time_delta = datetime.timedelta(minutes=30)
        user_history = models.UserLog.query.filter_by(user_id=user_id).order_by(models.UserLog.datetime).all()
        index = 0
        current_user_history = None
        next_user_history = next(iter(user_history), None)
        data_point_index = 0
        items = {}
        while time < end_time and data_point_index < 100:
            data_point_index += 1
            while next_user_history is not None and time > next_user_history.datetime:
                current_user_history = next_user_history
                index += 1
                next_user_history = user_history[index] if index < len(user_history) else None            
                if current_user_history.item_id not in items:
                    items[current_user_history.item] = 0
                if current_user_history.buy_sell:
                    items[current_user_history.item] += current_user_history.amount
                else: 
                    items[current_user_history.item] -= current_user_history.amount
                    if items[current_user_history.item] == 0:
                        del items[current_user_history.item]
            
            # stock value is price of all items at this point in time.
            stock_value = sum([item.get_price_at(time) * items[item] for item in items])

            data.append({
                "time" : time,
                "balance" : current_user_history.balance if current_user_history is not None else 100000,
                "stock_value" : stock_value,
                "stock_amount" : sum([items[item] for item in items])
            })
            time += time_delta

        return data

api.add_resource(Users, "/users")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserHistory, "/users/<int:user_id>/history")