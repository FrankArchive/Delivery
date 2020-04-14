from flask import request, session, abort
from flask_restx import Namespace, Resource

from delivery.models import db, Package, Token, Node
from delivery.utils import authed, verify_keys

packages = Namespace('packages')


@packages.route('')
class Packages(Resource):
    @authed
    def get(self):
        if 'filter' not in request.args.keys():
            abort(403, 'insufficient arguments')
        f = request.args['filter']
        ret = {}
        for k, v in {'sending': 'sender_id',
                     'receiving': 'receiver_id',
                     'delivering': 'courier_id'}.items():
            ret[k] = Package.query.filter_by(**{v: session['user_id']}).all() \
                if f == 'all' or f == k else []
        return ret

    @authed
    @verify_keys({'token': str, 'node_uuid': str})
    def post(self):
        token = Token.query.filter_by(token=request.json['token']).first()
        first_node = Node.query.filter_by(uuid=request.json['node_uuid']).first()
        if not token:
            abort(404, 'No such token')
        if not first_node:
            abort(404, 'No such node')

        package = Package(
            sender_id=session['user_id'],
            courier_id=session['user_id'],
            receiver_id=token.user_id,
            next_node_id=first_node.id,
        )
        db.session.add(package)
        db.session.commit()
        return {'uuid': package.token}

    @authed
    @verify_keys({'uuid': str})
    def patch(self):
        package = Package.query.filter_by(token=request.json['uuid']).first()

        if not package:
            abort(404, 'No such package')
        if package.next.manager_id != session['user_id']:
            abort(403, 'Not node manager')

        package.current_node_id = package.next_node_id
        package.next_node_id = package.current_node_id + 1
        db.session.commit()
        return {}
