from extensions import db
from app import app
from models import User, UserLog

USER_ID = 13

with app.app_context():
    
    user = User.query.filter_by(id=USER_ID).first()
    for user_log in UserLog.query.filter_by(user_id=USER_ID).all():
        db.session.delete(user_log)
    db.session.delete(user)

    db.session.commit()