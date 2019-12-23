from extensions import db
from app import app
from models import User

with app.app_context():
    jon = User.query.filter_by(id=7).first()
    jon.balance += 1800_00

    storage = User.query.filter_by(id=11).first()
    storage.balance -= 10000_00

    alasdair = User.query.filter_by(id=10).first()
    alasdair.balance -= 2400_00
    db.session.commit()
