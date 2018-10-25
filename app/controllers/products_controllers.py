from flask import jsonify, make_response
from app.models.database import Database_connection
import psycopg2
import uuid


class Items(object):
    """This is a class for handling all product activities."""

    def __init__(self):
        """The constructor for products class. """

        self.connection = Database_connection()

    def create_item(self, data):
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
        return(jsonify(item))

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
        item = self.connection.cursor.fetchone()
        return(make_response(jsonify(item)))

    def delete_product(self, id):
        self.connection.cursor.execute(
            "DELETE FROM products WHERE product_id=%s", [id]
        )
        response_object = {
            "satus": "pass",
            "message": "order deleted"
        }
        return(make_response(jsonify(response_object)))
