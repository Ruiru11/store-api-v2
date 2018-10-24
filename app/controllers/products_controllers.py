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
