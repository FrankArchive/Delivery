from flask import session, request
from flask_restx import Namespace, Resource

from delivery.models import User, db
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
        ).data

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
