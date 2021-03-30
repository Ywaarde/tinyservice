from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_type):

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_type)

    api = Api(app)

    db.init_app(app)

    with app.app_context():
        from .routes import initialize_routes
        initialize_routes(api)

        db.create_all()

    return app
