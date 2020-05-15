from flask import session, request, abort
from flask_restx import Namespace, Resource

from delivery.models import User, Node, db, Courier
from delivery.schemas import UserSchema
from delivery.utils import authed

users = Namespace("users")


@users.route('')
class Users(Resource):
    @authed
    def get(self):
        return UserSchema(view='self').dump(
            User.query.filter_by(
                id=session['user_id']
            ).first()
        )

    @authed
    def patch(self):
        user = User.query.filter_by(
            id=session['user_id']
        ).first()
        r = request.json
        for k in ['username', 'phone', 'address']:
            if k in r.keys():
                user.__setattr__(k, r[k])
        db.session.commit()
        return {}

    @authed
    def options(self):
        node = Node.query.filter_by(manager_id=session['user_id']).first()
        if node is None:
            abort(403, '只有站点管理员可以调用')

        return UserSchema(many=True, view='courier').dump(
            [c.user_id for c in Courier.query.filter_by(node_id=node.id).all()]
        )
