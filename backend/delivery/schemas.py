from marshmallow import fields

from .models import ma, Token, User, Node, Package


class UserSchema(ma.SQLAlchemyAutoSchema):
    views = {
        'self': [
            'username', 'phone', 'address',
            'registeration_date'
        ],
        'others': ['username'],
        'courier': ['username', 'phone']
    }

    class Meta:
        model = User
        include_fk = True

    def __init__(self, view=None, *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(UserSchema, self).__init__(*args, **kwargs)


class NodeSchema(ma.SQLAlchemyAutoSchema):
    manager = fields.Nested(UserSchema, only=['username'])
    connected = fields.List(fields.Integer(required=True))
    views = {
        'public': ['uuid', 'manager', 'location', 'connected']
    }

    class Meta:
        model = Node
        include_fk = True

    def __init__(self, view='public', *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(NodeSchema, self).__init__(*args, **kwargs)


class TokenSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema, only=['username', 'phone'])
    address = fields.Nested(NodeSchema, only=['uuid', 'location', 'manager'])
    views = {
        'generate': ['token', 'address'],
        'query': ['id', 'user', 'token', 'address'],
    }

    class Meta:
        model = Token
        include_fk = True

    def __init__(self, view=None, *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(TokenSchema, self).__init__(*args, **kwargs)


class PackageSchema(ma.SQLAlchemyAutoSchema):
    percent_progress = fields.Float(required=True)
    path = fields.List(fields.Integer(required=True))
    courier = fields.Nested(UserSchema, only=['username', 'phone'])
    sender = fields.Nested(UserSchema, only=['username'])
    current_node = fields.Nested(NodeSchema)
    next_node = fields.Nested(NodeSchema)
    views = {
        'sending': ['token', 'percent_progress', 'path'],
        'delivering': ['token', 'address', 'phone'],
        'receiving': ['token', 'percent_progress', 'path', 'courier', 'sender', 'current_node', 'next_node'],
    }

    class Meta:
        model = Package
        include_fk = True

    def __init__(self, view=None, *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(PackageSchema, self).__init__(*args, **kwargs)
