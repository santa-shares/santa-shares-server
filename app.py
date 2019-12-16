import logging, os, json, logging, math, urllib, uuid, datetime, random
from flask import Flask, escape, jsonify, request, abort, g
#from models import User, UserItem, Item
#from extensions import db, auth
#from endpoints import api_blueprint

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger("santa-shares")
#logger.info("Application starting.")

#DB_CONNECTION = os.environ.get("DB_CONNECTION")

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

#app.register_blueprint(api_blueprint)

# @auth.verify_token
# def verify_token(token):
#     if token is None: return False
#     g.current_user = User.query.filter_by(token=token).first()
#     is_verified = g.current_user is not None
#     if is_verified: logger.info(f"AUTHORISED: [{token}]")
#     else: logger.info(f"DENIED: [{token}]")
#     return is_verified

# @auth.error_handler
# def auth_error():
#     return abort(401, "Access Denied.")

@app.route("/")
def index():
    return "Is this fast?"

if __name__ == "__main__":
    app.run(port="80",debug=False)