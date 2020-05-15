from flask import request, session, abort
from flask_restx import Namespace, Resource

from delivery.calc import calculate_path
from delivery.models import db, Package, Token, Node, User
from delivery.schemas import PackageSchema
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
                     'delivering': 'courier_id',
                     'manage': ''}.items():
            pkgs = Package.query.filter_by(**{v: session['user_id']}).all() \
                if f == 'all' or f == k else []
            ret[k] = [PackageSchema(view=k).dump(item) for item in pkgs]
        return ret

    @authed
    @verify_keys({'token': str, 'user_id': int})
    def head(self):
        req = request.json
        package = Package.query.filter_by(token=req['token']).first()
        if package is None:
            abort(404, '快件不存在')
        node = package.current_node
        if node.manager_id != session['user_id']:
            abort(403, '只有快件所在站点的管理员能够调用')
        user = User.query.filter_by(id=req['id']).first()
        if user is None:
            abort(404, '用户不存在')
        package.courier_id = req['id']
        db.session.commit()
        pass

    @authed
    @verify_keys({'token': str, 'node_uuid': str})
    def post(self):
        token = Token.query.filter_by(token=request.json['token']).first()
        first_node = Node.query.filter_by(
            uuid=request.json['node_uuid']).first()
        if not token:
            abort(404, '收货节点不存在')
        if not first_node:
            abort(404, '发货节点不存在')
        try:
            path = calculate_path(first_node.id, token.address.id)
        except ValueError:
            abort(404, '收发货节点无法联通')

        package = Package(
            sender_id=session['user_id'],
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
            abort(404, '快件不存在')
        if package.receiver_id == session['user_id']:
            package.progress = len(package.path) - 1
            db.session.commit()
            return {'message': '快件成功送达'}
        if package.next_node.manager_id != session['user_id']:
            abort(403, '只有节点管理员能够调用')

        package.progress = package.progress + 1
        db.session.commit()
        return {'message': f'快件成功抵达{package.current_node.id}号节点'}
