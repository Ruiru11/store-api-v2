import os
import psycopg2
import testing.postgresql
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Fhhty%$#*hghghf$Tf')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = " dbname='andela' user='andela21' password='andela21' host='localhost' port='5432' "
    #'postgres:andela:null//postgres@localhost:5432/andela/'


#class TestingConfig(Config):
 #  TESTING = True
 #   DATABASE_URL = " dbname='testdb' user='andela21' password='andela21' host='localhost' port='5432' "

class TestingConfig(Config):
    postgresql = testing.postgresql.Postgresql()
    DEBUG = True
    TESTING = True
    DATABASE_URL = postgresql.url()



class ProductionConfig(Config):
    DATABASE_URL = os.getenv('ENV')


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

key = Config.SECRET_KEY
