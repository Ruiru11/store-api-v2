from flask import Flask
from flask_bcrypt import Bcrypt
from .config import config_by_name

bcrypt = Bcrypt()


from app.models.database import Database_connection
from app.views.products_views import don_item
from app.views.users_views import don_user


db = Database_connection()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.register_blueprint(don_item)
    app.register_blueprint(don_user)
    db
    return app
