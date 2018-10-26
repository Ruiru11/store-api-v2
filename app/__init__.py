from flask import Flask
from flask_bcrypt import Bcrypt
from .config import config_by_name

bcrypt = Bcrypt()


from app.models.database import Database_connection
from app.views.products_views import don_item
from app.views.users_views import don_user
from app.views.sales_views import don_sale


db = Database_connection()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config_by_name[environment])
    app.register_blueprint(don_item)
    app.register_blueprint(don_user)
    app.register_blueprint(don_sale)
    db
    return app
