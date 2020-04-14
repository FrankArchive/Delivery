from flask import Blueprint
from flask_restx import Api

from .auth import auth
from .tokens import tokens
from .users import users
from .packages import packages
from .nodes import nodes

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_blueprint, version="v1", doc='/docs')
api.add_namespace(auth, '/')
api.add_namespace(users, '/users')
api.add_namespace(tokens, '/token')
api.add_namespace(packages, '/package')
api.add_namespace(nodes, '/nodes')
