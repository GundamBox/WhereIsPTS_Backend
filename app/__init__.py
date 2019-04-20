import logging
import os

from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app.commom import utils
from app.commom.database import db
from config import config


def create_app(config_name='default'):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app)

    from app.v1.api import search, store
    app.register_blueprint(search, url_prefix='/api/v1')
    app.register_blueprint(store, url_prefix='/api/v1')

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
