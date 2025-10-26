import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    TESTING = os.environ.get('FLASK_TESTING', 'False') == 'True'
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-key-123'
    
    # AWS Configuration - these will be loaded from environment variables
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    
    @classmethod
    def validate_aws_credentials(cls):
        """Validate that required AWS credentials are set"""
        required = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required AWS credentials: {', '.join(missing)}")

# Validate AWS credentials when the config is loaded
Config.validate_aws_credentials()

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
