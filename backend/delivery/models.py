import datetime
from uuid import uuid4

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from delivery.utils import hash_password

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(50))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    address = db.Column(db.Text)
    registeration_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, open_id, username, password, phone, address, *args, **kwargs):
        self.open_id = open_id
        self.username = username
        self.password = hash_password(password)
        self.phone = phone
        self.address = address


class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36))
    _connected = db.Column(db.Text)
    location = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    manager = db.relationship(
        'User', foreign_keys='Node.manager_id', lazy='select'
    )

    @property
    def connected(self):
        return [int(i) for i in self._connected.split(';')]

    @connected.setter
    def connected(self, value: list):
        self._connected = ';'.join([str(i) for i in value])

    def __init__(self, location, manager_id):
        self.location = location
        self.manager_id = manager_id
        self.uuid = str(uuid4())
        self._connected = ''


class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    courier_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    progress = db.Column(db.Integer, default=0)

    _path = db.Column(db.Text)

    @property
    def percent_progress(self):
        return self.progress / len(self.path)

    @property
    def path(self):
        return [int(i) for i in self._path.split(';')]

    @path.setter
    def path(self, value: list):
        self._path = ';'.join([str(i) for i in value])

    @property
    def current_node(self):
        return Node.query.filter_by(id=self.path[self.progress]).first()

    @property
    def next_node(self):
        return Node.query.filter_by(id=self.path[self.progress + 1]).first()

    courier = db.relationship(
        'User', foreign_keys='Package.courier_id', lazy='select')
    sender = db.relationship(
        'User', foreign_keys='Package.sender_id', lazy='select')
    receiver = db.relationship(
        'User', foreign_keys='Package.receiver_id', lazy='select')

    def __init__(self, sender_id, receiver_id, next_node_id, path):
        self.sender_id = sender_id
        self.courier_id = -1
        self.receiver_id = receiver_id
        self.current_node_id = -1
        self.next_node_id = next_node_id
        self.token = str(uuid4())
        self.path = path


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('node.id'))

    user = db.relationship(
        'User', foreign_keys='Token.user_id', lazy='select'
    )
    address = db.relationship(
        'Node', foreign_keys='Token.address_id', lazy='select'
    )

    def __init__(self, user_id, node_id):
        self.address_id = node_id
        self.user_id = user_id
        self.token = str(uuid4())


class Courier(db.Model):
    __tablename__ = 'courier'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))

    user = db.relationship(
        'User', foreign_keys='Courier.user_id', lazy='select'
    )
    node = db.relationship(
        'Node', foreign_keys='Courier.node_id', lazy='select'
    )

    def __init__(self, user_id, node_id):
        self.user_id = user_id
        self.node_id = node_id
