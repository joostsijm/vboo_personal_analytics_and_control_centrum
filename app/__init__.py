
"""
Website and API
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# App
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.update(
    TESTING=True,
    SQLALCHEMY_DATABASE_URI='mysql://PAD_Database:PAD_Database@db.pla33.ga:17204/PAD_Database',
    SECRET_KEY='g6DGM5y2bVhb0mxdCRELI5m7fnzzoJ2y',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SEND_FILE_MAX_AGE_DEFAULT=1296000,
)


# DB
db = SQLAlchemy(app)

# Migration
migrate = Migrate(app, db)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

# config
app.config.update(DEBUG=True, SECRET_KEY='iliasmitchelrobintimjoost')
