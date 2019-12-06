from models import UserLog
from flask_restful import Resource
from endpoints import api

class History(Resource):
    def get(self):
        return UserLog.query.all()

api.add_resource(History, "/history")