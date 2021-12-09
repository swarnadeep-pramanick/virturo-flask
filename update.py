from app.app import db
from model.db import User, Role
try:
    db.create_all()
    role = Role("Eventee")
    user = User("Swarnadeep", "Pramanick",
                "swarnadeep@gmail.com", "Swarn225", 1)
    db.session.add_all([user, role])
    db.session.commit()
    print(user.id)

except ValueError:
    print('error')
