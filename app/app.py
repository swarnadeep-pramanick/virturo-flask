from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from flask_session import Session
from jinja2 import Template
from datetime import datetime
from flask_login import LoginManager
template_path = str(os.getcwd()) + '/templates'
static_path = str(os.getcwd()) + '/static'
app = Flask(__name__, template_folder=template_path, static_folder=static_path)

app.debug = True
app.secret_key = "asdkjashdkjasdknamksdfldshfksnfmnasdfklhasdfasdf"
app.permanent_session_lifetime = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/eventdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
# login_manager.session_protection = None
login_manager.init_app(app)
template = Template("""
# Generation started on {{ now() }}
... this is the rest of my template...
# Completed generation.
""")
template.globals['now'] = datetime.utcnow
