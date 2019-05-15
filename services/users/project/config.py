# services/users/project/config.py


import os  # new


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # new
    SECRET_KEY = 'my_secretkey'  # new
    DEBUG_TB_ENABLED = False  # configurando debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # configurando debug toolbar


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # new
    DEBUG_TB_ENABLED = True  # configurando debug toolbar


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')  # new


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # new
