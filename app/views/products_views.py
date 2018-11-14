from flask import Blueprint, jsonify
from flask_restful import reqparse

# local import
from app.controllers.products_controllers import Items
from app.controllers.users_controllers import Users

usr = Users()


don_item = Blueprint('products', __name__, url_prefix="/api/v2")

product_instance = Items()


@don_item.route("/products", methods=["POST"])
@usr.logged_in
@usr.check_admin
def create_item(res=None, user_role=None, user_id=None, user_email=None):
    """
        The function handles all arguments required for
        creating a new product.

        Parameter:
            name:Name of product and is of type str,
                 the field must be included
            category:Category of product is of type str,
                     the field must be included
            price:Price of product is of type str,
                    the field must be included
            description:Description of product is of type str,
                        the field must be included
        Returns:
            Arguments are passed to the create_item function
            in procucts_controllers to create the product

        """
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True,
                        help="name required", location="json")
    parser.add_argument("category", type=str, required=True,
                        help="name required", location="json")
    parser.add_argument("price", type=int, required=True,
                        help="name required", location="json")
    parser.add_argument("description", type=str, required=True,
                        help="description required", location="json")
    data = parser.parse_args()
    return product_instance.create_item(data)


@don_item.route("/products", methods=["GET"])
@usr.logged_in
def get_items(res=None, user_id=None, user_email=None):
    """The function is used to get all product created"""
    products = product_instance.get_items()
    products_data = []
    for i in products:
        data = {
            "product_id": i[4],
            "product_name": i[0],
            "description": i[1],
            "price": i[2],
            "category_name": i[3]
        }
        products_data.append(data)

    return (jsonify({
        "products": products_data
    }))


@don_item.route("/products/<id>", methods=["GET"])
@usr.logged_in
def get_item(id, res=None, user_id=None, user_email=None):
    """The function returns a specific product using its unique id"""
    product = product_instance.get_item(id)
    if product:
        data = {
            "product_id": product[4],
            "product_name": product[0],
            "description": product[1],
            "price": product[2],
            "category_name": product[3]
        }
        return jsonify({
            "product": data
        })
    else:
        return jsonify(
            {
                "message": "Product not found"
            }
        ), 404


@don_item.route('/products/<id>', methods=['DELETE'])
@usr.logged_in
@usr.check_admin
def delete_product(id, res=None, user_id=None, user_role=None,user_email=None):
    return product_instance.delete_product(id)


@don_item.route('/products/<id>', methods=['PUT'])
@usr.logged_in
@usr.check_admin
def update_product(id, res=None, user_id=None, user_role=None, user_email=None):
    return product_instance.update_product(id)
