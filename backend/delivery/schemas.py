from marshmallow import fields

from .models import ma, Token, User, Node


class UserSchema(ma.ModelSchema):
    views = {
        'self': [
            'username', 'phone', 'address',
            'registeration_date'
        ],
        'others': ['username']
    }

    class Meta:
        model = User
        include_fk = True

    def __init__(self, view=None, *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(UserSchema, self).__init__(*args, **kwargs)


class NodeSchema(ma.ModelSchema):
    manager = fields.Nested(UserSchema, only=['username'])
    views = {
        'public': ['uuid', 'manager', 'location', '_connected']
    }

    class Meta:
        model = Node
        include_fk = True

    def __init__(self, view='public', *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(NodeSchema, self).__init__(*args, **kwargs)


class TokenSchema(ma.ModelSchema):
    user = fields.Nested(UserSchema, only=['name', 'phone'])
    address = fields.Nested(NodeSchema, only=['uuid', 'location', 'manager'])
    views = {
        'generate': ['token', 'address'],
        'query': ['id', 'token', 'address'],
    }

    class Meta:
        model = Token
        include_fk = True

    def __init__(self, view=None, *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(TokenSchema, self).__init__(*args, **kwargs)
