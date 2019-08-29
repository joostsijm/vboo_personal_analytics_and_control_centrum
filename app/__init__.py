
"""
Website and API
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_argon2 import Argon2
from dotenv import load_dotenv
from sqlalchemy import MetaData
from rival_regions_wrapper.rival_regions_wrapper import Client

load_dotenv()

# app
class Config():
    """Config settings for the application"""
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 1296000

app = Flask(__name__)
app.config.from_object(Config())
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

# db
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
argon2 = Argon2(app)

# Rival Region wrapper
credentials = {
    "login_method": os.environ["LOGIN_METHOD"],
    "username": os.environ["USERNAME"],
    "password": os.environ["PASSWORD"]
}
rrclient = Client(show_window=os.environ["SHOW_WINDOW"] == 'True')
rrclient.set_credentials(credentials)

alt_credentials = {
    "login_method": os.environ["ALT_LOGIN_METHOD"],
    "username": os.environ["ALT_USERNAME"],
    "password": os.environ["ALT_PASSWORD"]
}
alt_rrclient = Client(show_window=os.environ["SHOW_WINDOW"] == 'True')
alt_rrclient.set_credentials(alt_credentials)
