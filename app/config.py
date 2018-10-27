import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'jhGJJJhty%$#*hghghf$Tf')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')


configuration = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

key = Config.SECRET_KEY
 