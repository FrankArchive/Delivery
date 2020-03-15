import datetime

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    registeration_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)


class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)


class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    current_node_id = db.Column(db.Integer, primary_key=True)
    next_node_id = db.Column(db.Integer, primary_key=True)

    current_node = db.relationship(
        'Node', foreign_keys='Package.current_node_id', lazy='select'
    )
    next_node = db.relationship(
        'Node', foreign_keys='Package.next_node_id', lazy='select'
    )


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    user = db.relationship(
        'User', foreign_keys='Token.user_id', lazy='select'
    )
