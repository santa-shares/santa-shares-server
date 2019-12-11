from extensions import db
from app import app
from models import User

with app.app_context():
    user = User.query.filter_by(id=4).first()
    db.session.delete(user)
    db.session.commit()