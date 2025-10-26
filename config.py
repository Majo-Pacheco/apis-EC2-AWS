import os

class Config:
    """Base configuration"""
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'mock-key')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'mock-secret')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
