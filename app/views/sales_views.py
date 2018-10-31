from flask import Blueprint, jsonify
from flask_restful import reqparse

# local import
from app.controllers.sales_controllers import Sales
from app.controllers.users_controllers import Users

usr = Users()


don_sale = Blueprint('sales', __name__, url_prefix="/api/v2")

sale_insatnce = Sales()


@don_sale.route("/sales", methods=["POST"])
@usr.logged_in
def create_sale(res=None, user_id=None):
    """
        The function helps handles all arguments required for creating,
        a sales record.
       Parameter:
                name:Name of employee creatin the sales order is of type str.
                description:contains all the information realting to a sale.
       Return:
            Arguments are passed to the create_sale() function,
            from sales_controller to create a sale order
     """
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('user_id', user_id)
    parser.add_argument("description", action="append", type=str,
                        help="must be given", location="json")
    parser.add_argument("cost", type=int, required=True,
                        help="this cannot be empty", location="json")
    data = parser.parse_args()

    return sale_insatnce.create_sale(data)


@don_sale.route("/sales", methods=["GET"])
@usr.logged_in
@usr.check_admin
def get_sales(res=None, user_role=None, user_id=None):
    """The function is used to get all sales created"""
    sales = sale_insatnce.get_sales()
    sales_data = []
    for i in sales:
        data = {
            "cost": i[2],
            "sale_id":i[0],
            "user_id":i[1],
            "description":i[3]
        }
        sales_data.append(data)

    return (jsonify({
        "sales":sales_data
    }))


@don_sale.route("/sales/<id>", methods=["GET"])
@usr.logged_in
@usr.check_admin
def get_sale(id, res=None, user_role=None, user_id=None):
    """The function gets a single order using its id"""
    sale = sale_insatnce.get_sale(id)
    if sale:
        data = {
            "cost": sale[2],
            "sale_id":sale[0],
            "user_id":sale[1],
            "description":sale[3]
            }
        return  jsonify({
            "sales":data
        })
    else:
        return jsonify(
            {
                "message":"sale not found"
            }
        ), 404


@don_sale.route("/user-sales/<id>", methods=["GET"])
@usr.logged_in
@usr.check_admin
def get_user_sales(id, res=None, user_role=None, user_id=None):
    """The function gets a single order using its id"""
    return sale_insatnce.get_user_sales(id)
