from flask import jsonify, make_response
from app.models.database import Database_connection
import psycopg2
import uuid


class Sales(object):
    """This is a class for handling all sales activities. """

    def __init__(self):
        """The constructor for sales class."""
        self.connection = Database_connection()

        # creates an empty list
        self.sales = []

    def create_sale(self, data):
        """
        The function creates a new sale order.
        Parameter:
                  data:This are values that are passed,
                        they are defined and handled
                        in sales_views.py
        Returns:
                Sales:A sale record  
        """
        # generating an id
        try:
            sale_id = str(uuid.uuid4())
            self.connection.cursor.execute("""INSERT INTO sales(sale_id, user_id, cost, description) 
            VALUES (%s, %s, %s, %s);""",
                                           (sale_id,
                                            data['user_id'],
                                            data['cost'],
                                            data['description']))
            print("Inserting DATA into sales")
            response_object = {
                "satus": "pass",
                "message": "sale  created succesfully"
            }
            return(make_response(jsonify(response_object)))

        except (Exception, psycopg2.DatabaseError) as error:
            print("ERROR inserting into sales", error)
            response_object = {
                "satus": "fail",
                "message": "Entry with same id already exists or wrong format used"
            }
            return(make_response(jsonify(response_object)))

    def get_sales(self):
        """
        The function to get all sales created.
        Returns:
            products: A list of all created sales.
        """
        self.connection.cursor.execute("""SELECT * FROM sales""")
        response = self.connection.cursor.fetchall()
        return(jsonify(response))

    def get_sale(self, id):
        """
        The function to get a specific sale record.
        Parameter:
                id: This is the unique identification number
                 of a sale order
        Returns:
                Sales:A single sale order
        """
        self.connection.cursor.execute(
            " SELECT * FROM sales WHERE sale_id=%s ", [id])
        response = self.connection.cursor.fetchone()
        return(make_response(jsonify(response)))
