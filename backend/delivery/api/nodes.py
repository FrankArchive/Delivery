from flask import request, session, abort
from flask_restx import Namespace, Resource

from delivery.models import Node
from delivery.schemas import NodeSchema
from delivery.utils import authed, verify_keys

nodes = Namespace('nodes')

@nodes.route('')
class Nodes(Resource):
    def get(self):
        return NodeSchema(many=True).dump(
            Node.query.all()
        )
