import datetime

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    registeration_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password, phone, *args, **kwargs):
        self.username = username
        self.password = password
        self.phone = phone


class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)


class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    current_node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    next_node_id = db.Column(db.Integer, db.ForeignKey('node.id'))

    current_node = db.relationship(
        'Node', foreign_keys='Package.current_node_id', lazy='select'
    )
    next_node = db.relationship(
        'Node', foreign_keys='Package.next_node_id', lazy='select'
    )


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship(
        'User', foreign_keys='Token.user_id', lazy='select'
    )
