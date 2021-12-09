from model.db import User
from app.app import db


def is_live(user_id, active):
    admin = User.query.filter_by(id=user_id).first()
    admin.is_active = int(active)
    db.session.commit()
    return True
