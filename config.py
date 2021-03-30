
class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    """Run sqlite in memory for testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False