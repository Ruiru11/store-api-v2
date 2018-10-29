import os
#import testing.postgresql
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'jhGJJJhty%$#*hghghf$Tf')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')


#class TestingConfig(Config):
 #   Postgresql = testing.postgresql.Postgresql()
  #  DEBUG = True
   # TESTING = True
    #DATABASE_URL = Postgresql.url()
class TestingConfig(config):
    DEBUG=True
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
