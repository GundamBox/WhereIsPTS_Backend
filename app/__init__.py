import logging
import os

from flask import Blueprint, Flask, current_app, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from app.common.database import db
from app.common.exception import FlaskException
from app.models.schema import ma

try:
    from config import config
except ImportError:
    print("Please execute `cp config_example.py config.py` and edit it before run server.")
    exit(1)

logger = logging.getLogger(__name__)


def handle_exception(error):
    if current_app.config['DEBUG']:
        response = jsonify(error.to_dict())
    else:
        response = jsonify({})
    response.status_code = error.status_code
    return response


def create_app(config_name=None):

    config_name = config_name or os.getenv('FLASK_ENV')
    app_config = config[config_name]

    app = Flask(__name__)
    app.config.from_object(app_config)

    db.init_app(app)
    ma.init_app(app)

    app.db = db
    app.app_context().push()

    app_config.init_app(app)

    app.register_error_handler(FlaskException, handle_exception)

    from app.api.v1 import channel_controller, store_controller, vote_controller
    app.register_blueprint(channel_controller, url_prefix='/api/v1')
    app.register_blueprint(vote_controller, url_prefix='/api/v1')
    app.register_blueprint(store_controller, url_prefix='/api/v1')

    CORS(app)
    CSRFProtect(app)
    Migrate(app, db)

    return app
