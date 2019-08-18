"""Models"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Model for User"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    _password = db.Column("password", db.String)
    name = db.Column(db.String)
    registration_at = db.Column(db.DateTime, default=datetime.utcnow)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @property
    def password(self):
        """Return the password"""
        return self._password

    @password.setter
    def password(self, password):
        """Hash password"""
        self._password = argon2.generate_password_hash(password)

    def __init__(self, id=None):
        self.id = id

class Key(db.Model):
    """Model for Key"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)
    uses = db.Column(db.Integer, default=0)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    user = db.relationship(
        "User",
        back_populates=db.backref("users", lazy="dynamic")
    )

class Request(db.Model):
    """Model for function"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Log(db.Model):
    """Model for Log"""
    id = db.Column(db.Integer, primary_key=True)
    succes = db.Column(db.Boolean, default=False)
    date_time = db.Column(db.DateTime)

    key_id = db.Column(
        db.Integer,
        db.ForeignKey('key.id')
    )
    key = db.relationship(
        "Key",
        back_populates=db.backref("logs", lazy="dynamic")
    )
    request_id = db.Column(
        db.Integer,
        db.ForeignKey('request.id')
    )
    request = db.relationship(
        "Request",
        back_populates=db.backref("logs", lazy="dynamic")
    )
