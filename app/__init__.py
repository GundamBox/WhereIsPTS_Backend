import logging
import os

from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app.models import db
from app.utils import common


def create_app():

    app = Flask(__name__)
    CORS(app)

    if 'APP_SETTINGS' in os.environ:
        env = os.environ['APP_SETTINGS']
    else:
        env = 'dev'

    config_path = 'app/settings/{env}.ini'.format(env=env)
    config = common.import_config(config_path)

    for key, value in dict(config['FLASK']).items():
        app.config[key] = value

    from .controller.search import search
    app.register_blueprint(search)

    from .controller.store import store
    app.register_blueprint(store)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
