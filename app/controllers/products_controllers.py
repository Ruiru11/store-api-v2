from flask import jsonify, make_response
from app.models.database import Database_connection
import psycopg2
import uuid


class Items(object):
    """This is a class for handling all product activities."""

    def __init__(self):
        """The constructor for products class. """

        self.connection = Database_connection()

    def validate_name(self, name):
        """The fuction to validate name"""
        if len(name) == 0:
            return False
        else:
            return True

    def validate_category(self, category):
        """The function to validate category"""
        if category != "Household":
            return False
        else:
            return True

    def validate_price(self, price):
        """The function to validate price"""
        if price < 0:
            return False
        else:
            return True

    def create_item(self, data):
        """The function to create a product"""
        price = self.validate_price(data['price'])
        category = self.validate_category(data['category'])
        name = self.validate_name(data['name'])
        if price and category and name is True:
            try:
                item_id = str(uuid.uuid4())
                self.connection.cursor.execute("""INSERT INTO products(product_id, name,category, description, price)
                VALUES(%s, %s, %s, %s, %s);""",
                                               (item_id,
                                                data['name'],
                                                data['category'],
                                                data['description'],
                                                data['price']))
                print("INSERTING DATA into products")
                response_object = {
                    "message": "Product created",
                    "status": "pass"
                }
                return(make_response(jsonify(response_object)), 201)

            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR inserting into products", error)
                response_object = {
                    "status": "fail",
                    "message": "product already exists"
                }
                return(make_response(jsonify(response_object)), 409)
        elif price is not True:
            response_object = {
                "status": "fail",
                "message": "price cannot be negative"
            }
            return(make_response(jsonify(response_object)), 409)
        elif category is not True:
            response_object = {
                "status": "fail",
                "message": "By default category should be Household"
            }
            return(make_response(jsonify(response_object)), 409)
        elif name is not True:
            response_object = {
                "status": "fail",
                "message": "name cannot be empty"
            }
            return(make_response(jsonify(response_object)), 409)

    def get_items(self):
        """
        The function to get all products created.

        Returns:
            products: A list of all created products.
        """
        self.connection.cursor.execute(
            """SELECT * FROM products"""
        )
        item = self.connection.cursor.fetchall()
        return item

    def get_item(self, id):
        """
        The function to gets a specific product using its unique id.return.

        Parameters:
            id: This is the identiication number of product to be viewed.

        Returns:
            Products: A single product


        """
        self.connection.cursor.execute(
            "SELECT * FROM  products WHERE product_id=%s", [id]
        )
        res = self.connection.cursor.fetchone()
        return res
        # self.connection.cursor.execute(
        #     "SELECT * FROM  products WHERE product_id=%s", [id])
        # response = self.connection.cursor.fetchone()
        # return(make_response(jsonify(response)))

    def delete_product(self, id):
        """The function to delete a product"""
        self.connection.cursor.execute(
            "SELECT * FROM  products WHERE product_id=%s", [id]
        )
        res = self.connection.cursor.fetchone()
        if not res:
            response_object = {
                "message": "Product doesnot exist, can't delete ",
                "status": "Fail"
            }
            return(make_response(jsonify(response_object)), 404)
        else:
            self.connection.cursor.execute(
                "DELETE FROM products WHERE product_id=%s", [id])
            response_object = {
                "message": "product deleted",
                "status": "pass"
            }
            return(make_response(jsonify(response_object)))

    def update_product(self, id):
        """The function to modify a product"""
        self.connection.cursor.execute(
            "SELECT * FROM  products WHERE product_id=%s", [id]
        )
        res = self.connection.cursor.fetchone()
        if not res:
            response_object = {
                "message": "Product doesnot exist, can't update ",
                "status": "Fail"
            }
            return(make_response(jsonify(response_object)), 404)
        else:
            self.connection.cursor.execute(
                "UPDATE products SET category='construction' WHERE product_id=%s",
                [id])
            response_object = {
                "satus": "pass",
                "message": "status update complete"
            }
            return(make_response(jsonify(response_object)))
