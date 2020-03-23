import os

from flask import Flask
from flask_migrate import upgrade, Migrate
from flask_session import Session, SqlAlchemySessionInterface

from .api import api_blueprint
from .utils import get_db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    db_url = get_db()
    app.config['SQLALCHEMY_DATABASE_URI'] = str(db_url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    with app.app_context():
        from .models import db, ma, User, Node, Package, Token
        Session(app)
        SqlAlchemySessionInterface(app, db, "sessions", "sess_")
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)
        if db_url.drivername.startswith("sqlite"):
            db.create_all()
        else:
            upgrade()
            pass
        app.register_blueprint(api_blueprint)
    return app
