from flask import Flask
from . import api


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    app.register_blueprint(api.bp)
    return app
