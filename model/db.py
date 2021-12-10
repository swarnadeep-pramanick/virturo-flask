from app.app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Role {self.name}"


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Country {self.name}"


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    event_id = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, first_name, last_name, email, password, role_id, event_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.role_id = role_id
        self.event_id = event_id

    def checkpassword(self, password):
        if check_password_hash(self.password, password):
            return True

    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    slug = db.Column(db.String(255))
    name = db.Column(db.String(255))
    link = db.Column(db.String(255))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, name, slug, user_id, link, start_date, end_date):
        self.name = name
        self.slug = slug
        self.link = link
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"Event {self.name}"


class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(80))
    value = db.Column(db.String(255))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, field):
        self.field = field

    def __repr__(self):
        return f"Content {self.field}"


class ContentMaster(db.Model):
    __tablename__ = 'content_masters'
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(80))
    value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __repr__(self):
        return f"Content {self.field}"


class Notification(db.Model):
    __tablename__ = 'notfications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.Text)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, title, message, event_id):
        self.title = title
        self.message = message
        self.event_id = event_id

    def __repr__(self):
        return f"Notification {self.title}"


class SeenNotification(db.Model):
    __tablename__ = 'seen_notfications'
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notfications.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seen = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, notification_id, user_id):
        self.notification_id = notification_id
        self.user_id = user_id

    def __repr__(self):
        return f"Seen Notification {self.seen}"


class UserLocation(db.Model):
    __tablename__ = 'user_locations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(80))
    type_location = db.Column(db.String(150), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    current_status = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now())
