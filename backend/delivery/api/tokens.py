from flask import session, request, abort
from flask_restx import Namespace, Resource

from delivery.models import Token, Node, db
from delivery.schemas import TokenSchema, UserSchema
from delivery.utils import authed, verify_keys

tokens = Namespace('tokens')


@tokens.route('')
class Tokens(Resource):
    @authed
    def get(self):
        return TokenSchema(many=True, view='query').dump(
            Token.query.filter_by(user_id=session['user_id']).all()
        )

    @authed
    @verify_keys({'node_uuid': str})
    def put(self):
        node = Node.query.filter_by(uuid=request.json['node_uuid']).first()
        if node is None:
            abort(400)
        token = Token(session['user_id'], node.id)
        db.session.add(token)
        db.session.commit()
        return {
            'token': TokenSchema(view='generate').dump(token),
            'user': UserSchema(view='self').dump(token.user)
        }

    @authed
    @verify_keys({'id': int})
    def delete(self):
        token = Token.query.filter_by(id=request.json['id']).first()
        if token is None:
            abort(400)
        db.session.delete(token)
        db.session.commit()
        return {'msg': '成功删除收货token'}
