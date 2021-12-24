from app.app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, name, created_at=datetime.now()):
        self.name = name
        self.created_at = created_at

    def __repr__(self):
        return f"Role {self.name}"


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, name, created_at=datetime.now()):
        self.name = name
        self.created_at = created_at

    def __repr__(self):
        return f"Country {self.name}"


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    phone_active = db.Column(db.Boolean(), default=False)
    country_id = db.Column(db.Integer, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    event_id = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, first_name, last_name, email, phone, country_id=0, password=None, role_id=1, event_id=None, created_at=datetime.now()):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.role_id = role_id
        self.event_id = event_id
        self.phone = phone
        self.country_id = country_id
        self.created_at = created_at

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
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, name, slug, user_id, link, start_date, end_date, created_at=datetime.now()):
        self.name = name
        self.slug = slug
        self.link = link
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at

    def __repr__(self):
        return f"Event {self.name}"


class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100))
    value = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(80))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, field, value=None, type=None, created_at=datetime.now()):
        self.field = field
        self.value = value
        self.type = type
        self.created_at = created_at

    def __repr__(self):
        return f"Content {self.field}"


class ContentMaster(db.Model):
    __tablename__ = 'content_masters'
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(80))
    value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, field, value, created_at=datetime.now()):
        self.field = field
        self.value = value
        self.created_at = created_at

    def __repr__(self):
        return f"Content {self.field}"


class Notification(db.Model):
    __tablename__ = 'notfications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.Text)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, title, message, event_id, created_at=datetime.now()):
        self.title = title
        self.message = message
        self.event_id = event_id
        self.created_at = created_at

    def __repr__(self):
        return f"Notification {self.title}"


class SeenNotification(db.Model):
    __tablename__ = 'seen_notfications'
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notfications.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seen = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, notification_id, user_id, created_at=datetime.now()):
        self.notification_id = notification_id
        self.user_id = user_id
        self.created_at = created_at

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
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, type, type_location, event_id, created_at=datetime.now()):
        self.type = type
        self.type_location = type_location
        self.event_id = event_id
        self.created_at = created_at


class Faq(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    question = db.Column(db.String(150), nullable=False)
    answer = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, question, answer, event_id, created_at=datetime.now()):
        self.question = question
        self.event_id = event_id
        self.answer = answer
        self.created_at = created_at


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, title, url, created_at=datetime.now()):
        self.title = title
        self.url = url
        self.created_at = created_at


class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sent_to = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    message = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, sender_id, sent_to, subject, message, created_at=datetime.now()):
        self.sender_id = sender_id
        self.sent_to = sent_to
        self.subject = subject
        self.message = message
        self.created_at = created_at


class Menu(db.Model):
    _tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, default=0)
    event_id = db.Column(db.Integer, default=0)
    type = db.Column(db.String(100))
    name = db.Column(db.String(100), default=None, nullable=True)
    status = db.Column(db.Boolean(), default=True)
    position = db.Column(db.Integer, default=0)
    sub = db.Column(db.Integer, default=0)
    iClass = db.Column(db.String(70), nullable=True)
    link = db.Column(db.String(100), nullable=True)
    link_type = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, parent_id=0, event_id=0, name=None, link=None, type=None, position=0, iClass=None, link_type=None, created_at=datetime.now()):
        self.parent_id = parent_id
        self.event_id = event_id
        self.position = position
        self.link = link
        self.name = name
        self.type = type
        self.iClass = iClass
        self.link_type = link_type
        self.created_at = created_at


class Booth(db.Model):
    _tablename__ = 'booths'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String(100))
    calendly_link = db.Column(db.String(255), default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, event_id=0, name=None, calendly_link=None, user_id=None, created_at=datetime.now()):

        self.event_id = event_id
        self.name = name
        self.calendly_link = calendly_link
        self.user_id = user_id
        self.created_at = created_at


class Page(db.Model):
    _tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, event_id=0, name=None, created_at=datetime.now()):

        self.event_id = event_id
        self.name = name
        self.created_at = created_at


class SessionRoom(db.Model):
    _tablename__ = 'session_rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, event_id=0, name=None, created_at=datetime.now()):

        self.event_id = event_id
        self.name = name
        self.created_at = created_at
