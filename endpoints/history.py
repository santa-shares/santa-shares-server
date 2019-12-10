from models import UserLog
from flask_restful import Resource, fields, marshal_with
from endpoints import api

user_log_fields = {
    "datetime" : fields.DateTime(),
    "buy_sell" : fields.Boolean(),
    "user_id" : fields.Integer(),
    "item_id" : fields.Integer(),
    "amount" : fields.Integer()
}

class History(Resource):

    @marshal_with(user_log_fields)
    def get(self):
        return UserLog.query.all()

api.add_resource(History, "/history")