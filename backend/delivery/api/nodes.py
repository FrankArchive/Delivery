from flask_restx import Namespace, Resource

from delivery.models import Node
from delivery.schemas import NodeSchema

nodes = Namespace('nodes')


@nodes.route('')
class Nodes(Resource):
    @staticmethod
    def get():
        return NodeSchema(many=True).dump(Node.query.all())
