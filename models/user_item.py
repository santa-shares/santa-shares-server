from extensions import db

class UserItem(db.Model):
    __tablename__ = 'user_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    amount = db.Column(db.Integer)