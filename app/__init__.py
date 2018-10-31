from flask import Flask, redirect, make_response, jsonify
from flask_bcrypt import Bcrypt
from .config import configuration
from flask_cors import CORS

bcrypt = Bcrypt()


from app.models.database import Database_connection
from app.views.products_views import don_item
from app.views.users_views import don_user
from app.views.sales_views import don_sale


db = Database_connection()


def create_app(environment):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(configuration[environment])
    app.register_blueprint(don_item)
    app.register_blueprint(don_user)
    app.register_blueprint(don_sale)
    db



    @app.errorhandler(404)
    def not_found(e):
        response_object = {
            "message": "The requested url is not available please check the url and try again",
            "status": "fail"
        }
        return(make_response(jsonify(response_object)), 404)

    @app.route('/')
    def root():
        return redirect("https://njeri.herokuapp.com/apidocs/#/")
    return app
