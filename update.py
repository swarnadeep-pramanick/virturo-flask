from app.app import db
from model.db import User, Role, Country, Menu
from faker import Faker
fakeGen = Faker()


def populate(n=5):
    for entry in range(n):
        fakeCountry = fakeGen.country()
        fakeDates = fakeGen.date()
        country = Country(name=fakeCountry)
        db.session.add(country)
        db.session.commit()


try:
    db.create_all()
    roles = ['Eventee', 'Admin', 'Exibiter', 'Delegate', 'Speaker', 'Attendee']
    for role in roles:
        rl = Role(role)
        db.session.add(rl)
        db.session.commit()
    user = User(first_name="Swarnadeep", last_name="Pramanick",
                email="swarnadeep@gmail.com", password="Swarn225", role_id=1, phone='9474698578')
    populate(200)
    db.session.add_all([user])
    db.session.commit()
    print(user.id)


except ValueError:
    print('error')
