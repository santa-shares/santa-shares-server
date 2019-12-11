from extensions import db
from app import app
from models import User

with app.app_context():

    users = User.query.filter_by(id=11).all()
    for user in users:
        print(user.name)