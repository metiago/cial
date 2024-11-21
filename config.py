import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hex it'
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    db_uri = 'postgresql://postgres:12345678@localhost/'
    database_name = 'postgres'
    SQLALCHEMY_DATABASE_URI = db_uri + database_name


class TestingConfig(Config):
    TESTING = True
    db_uri = 'postgresql://postgres:12345678@localhost/'
    database_name = 'postgres'
    SQLALCHEMY_DATABASE_URI = db_uri + database_name


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
