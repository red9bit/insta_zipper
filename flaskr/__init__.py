from flask import Flask
from logging.config import dictConfig as logger_dictConfig

from .logging import LOGGER_CONF
from . import api


def create_app():
    # configure logger
    logger_dictConfig(LOGGER_CONF)
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)
    app.register_blueprint(api.bp)
    return app
