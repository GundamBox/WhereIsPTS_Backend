import os
import logging
from app.commom.utils import SQLAlchemyHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sqlalchemyhandler = SQLAlchemyHandler()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    WTF_CSRF_SECRET_KEY = os.environ.get(
        'WTF_CSRF_SECRET_KEY') or 'hard to guess string'

    RECAPTCHA_PUBLIC_KEY = 'enter_your_public_key'
    RECAPTCHA_PRIVATE_KEY = 'enter_your_private_key'
    RECAPTCHA_OPTIONS = {'theme': 'white'}

    @classmethod
    def init_app(cls, app):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sqlalchemyhandler.setFormatter(formatter)

        loggers = [logger,
                   logging.getLogger('flask.app')]

        for l in loggers:
            l.addHandler(sqlalchemyhandler)


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    RECAPTCHA_DISABLE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://<user_name>:<user_password>@localhost/whereispts_dev'

    @classmethod
    def init_app(cls, app):
        logger.setLevel(logging.DEBUG)
        sqlalchemyhandler.setLevel(logging.DEBUG)

        super().init_app(app)


class TestingConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    RECAPTCHA_DISABLE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://<user_name>:<user_password>@localhost/whereispts_test'

    @classmethod
    def init_app(cls, app):
        print(cls.SQLALCHEMY_DATABASE_URI)
        logger.setLevel(logging.DEBUG)
        sqlalchemyhandler.setLevel(logging.DEBUG)

        super().init_app(app)


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    RECAPTCHA_DISABLE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://<user_name>:<user_password>@localhost/whereispts'

    @classmethod
    def init_app(cls, app):
        logger.setLevel(logging.WARNING)
        sqlalchemyhandler.setLevel(logging.WARNING)

        super().init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
