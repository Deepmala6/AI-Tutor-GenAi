import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    LLM_API_KEY = os.getenv('OPENAI_API_KEY', '')
    MAX_REFINEMENTS = 1

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4')
    LLM_API_KEY = os.getenv('OPENAI_API_KEY', '')
    MAX_REFINEMENTS = 1

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    LLM_MODEL = 'mock'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, DevelopmentConfig)
