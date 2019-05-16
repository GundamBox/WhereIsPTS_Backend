import logging
import os

from flask import Blueprint, Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from app.commom.database import db
from app.models.schema import ma
from config import config

logger = logging.getLogger(__name__)


def create_app(config_name):

    config_name = config_name or os.getenv('FLASK_CONFIG')
    app_config = config[config_name]

    app = Flask(__name__)
    app.config.from_object(app_config)

    db.init_app(app)
    ma.init_app(app)

    app.db = db
    app.app_context().push()

    app_config.init_app(app)

    from app.api.v1 import channel_controller, store_controller, vote_controller
    app.register_blueprint(channel_controller, url_prefix='/api/v1')
    app.register_blueprint(vote_controller, url_prefix='/api/v1')
    app.register_blueprint(store_controller, url_prefix='/api/v1')

    CORS(app)
    CSRFProtect(app)
    Migrate(app, db)

    return app
