"""Models"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Model for User"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    registration_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id=None):
        self.id = id

    @hybrid_property
    def key_count(self):
        """Return amount of keys"""
        return self.keys.count()


class Key(db.Model):
    """Model for Key """
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
        back_populates="keys"
    )

    @hybrid_method
    def key_count(self):
        """increment use"""
        self.used_at = datetime.now()
        self.uses += 1
        return self.keys.count()


class Request(db.Model):
    """Model for function"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Log(db.Model):
    """Model for Key """
    id = db.Column(db.Integer, primary_key=True)
    succes = db.Column(db.Boolean, default=False)
    date_time = db.Column(db.DateTime)

    key_id = db.Column(
        db.Integer,
        db.ForeignKey('key.id')
    )
    key = db.relationship(
        "Key",
        back_populates="logs"
    )
    request_id = db.Column(
        db.Integer,
        db.ForeignKey('request.id')
    )
    request = db.relationship(
        "Request",
        back_populates="logs"
    )
