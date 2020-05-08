from flask import request, session, abort
from flask_restx import Namespace, Resource

from delivery.models import db, Package, Token, Node
from delivery.schemas import PackageSchema
from delivery.utils import authed, verify_keys
from delivery.calc import calculate_path

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
            pkgs = Package.query.filter_by(**{v: session['user_id']}).all() \
                if f == 'all' or f == k else []
            ret[k] = [PackageSchema(view=k).dump(item) for item in pkgs]

        return ret

    @authed
    @verify_keys({'token': str, 'node_uuid': str})
    def post(self):
        token = Token.query.filter_by(token=request.json['token']).first()
        first_node = Node.query.filter_by(
            uuid=request.json['node_uuid']).first()
        if not token:
            abort(404, 'No such token')
        if not first_node:
            abort(404, 'No such node')

        try:
            path = calculate_path(first_node.id, token.address.id)
        except ValueError:
            abort(404, 'Unreachable')

        package = Package(
            sender_id=session['user_id'],
            courier_id=session['user_id'],
            receiver_id=token.user_id,
            next_node_id=first_node.id,
            path=path,
        )
        db.session.add(package)
        db.session.commit()
        return {'uuid': package.token}

    @authed
    @verify_keys({'uuid': str})
    def put(self):
        package = Package.query.filter_by(token=request.json['uuid']).first()

        if not package:
            abort(404, 'No such package')
        if package.receiver_id == session['user_id']:
            package.progress = len(package.path)-1
            db.session.commit()
            return {'msg': 'successfully delivered'}
        if package.next.manager_id != session['user_id']:
            abort(403, 'Not node manager')

        package.progress = package.progress + 1
        db.session.commit()
        return {'msg': 'package arrived at '+package.current_node.id}
