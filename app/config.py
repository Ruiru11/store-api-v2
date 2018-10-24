import os
import testing.postgresql
import psycopg2
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Fhhty%$#*hghghf$Tf')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'postgres://postgres@localhost:5432/postgres/'


class TestingConfig(Config):
    Postgresql = testing.postgresql.Postgresql()
    DEBUG = True
    TESTING = True,
    print('>>>>>>>>>>>>>>>>>>', Postgresql.url())
    DATABASE_URL = Postgresql.url()


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}

key = Config.SECRET_KEY
