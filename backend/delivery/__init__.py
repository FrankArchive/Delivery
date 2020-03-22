import os

from flask import Flask
from flask_session import Session

from .api import api_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB') or 'sqlite:///test.db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    with app.app_context():
        from .models import db
        Session(app).app.session_interface.db.create_all()
        db.init_app(app)
        app.db = db
        db.create_all()

    app.register_blueprint(api_blueprint)
    return app
