from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String, nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)