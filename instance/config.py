import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}