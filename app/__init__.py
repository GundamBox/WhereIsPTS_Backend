import logging
import os

from flask import Blueprint, Flask
from flask_cors import CORS

from flask_migrate import Migrate

from app.commom import utils
from app.commom.database import db
from app.models.schema import ma
from config import config


def create_app(config_name=os.getenv('FLASK_CONFIG')):

    if not config_name:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    CORS(app)

    from app.v1.api import channel_controller, store_controller, vote_controller
    app.register_blueprint(channel_controller, url_prefix='/api/v1')
    app.register_blueprint(vote_controller, url_prefix='/api/v1')
    app.register_blueprint(store_controller, url_prefix='/api/v1')

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    return app
