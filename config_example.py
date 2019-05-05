import os

def get_secret(setting):
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Should set the {} enviroment variable".format(setting)
        print(error_msg)
        return None


class Config:
    SECRET_KEY = get_secret('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_secret('DEV_DATABASE_URL') or \
        'postgresql://<user_name>:<user_password>@localhost/whereispts_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_secret('TEST_DATABASE_URL') or \
        'postgresql://<user_name>:<user_password>@localhost/whereispts_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_secret('DATABASE_URL') or \
        'postgresql://<user_name>:<user_password>@localhost/whereispts'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
