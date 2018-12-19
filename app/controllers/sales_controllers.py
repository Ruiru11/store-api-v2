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

    def validate_cost(self, cost):
        """The function to validate cost"""
        if cost < 0:
            return False
        else:
            return True

    def validate_description(self, description):
        """The function to validate description"""

        description = description.strip().split(",")
        print('description', description)
        response = None
        for i in description:
            print(i)
            self.connection.cursor.execute(
                """ SELECT * FROM products WHERE name=%s""", [i]
            )
            res = self.connection.cursor.fetchone()
            if not res:
                response = False
                break
            else:
                response = True
                continue
        print('response', response)
        return response

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
        cost = self.validate_cost(data['cost'])
        description = self.validate_description(data['description'])
        if cost and description is True:
            try:
                sale_id = str(uuid.uuid4())
                self.connection.cursor.execute("""INSERT INTO sales(sale_id, user_id, user_email, cost, description) 
                VALUES (%s, %s,  %s, %s, %s);""",
                                               (sale_id,
                                                data['user_id'],
                                                data['user_email'],
                                                data['cost'],
                                                data['description']))
                print("Inserting DATA into sales")
                response_object = {
                    "satus": "pass",
                    "message": "sale  created succesfully"
                }
                return(make_response(jsonify(response_object)), 201)

            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR inserting into sales", error)
                response_object = {
                    "satus": "fail",
                    "message": "Entry with same id already exists or wrong format used"
                }
                return(make_response(jsonify(response_object)))
        elif cost is not True:
            response_object = {
                "status": "fail",
                "message": "cost cannot be negative"
            }
            return(make_response(jsonify(response_object)), 409)
        elif description is not True:
            response_object = {
                "status": "fail",
                "message": "one or several of the items you are trying to make a sale of is not in store please check again"
            }
            return(make_response(jsonify(response_object)), 409)

    def get_sales(self):
        """
        The function to get all sales created.
        Returns:
            products: A list of all created sales.
        """
        self.connection.cursor.execute("""SELECT * FROM sales""")
        response = self.connection.cursor.fetchall()
        return response

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
        res = self.connection.cursor.fetchone()
        return res
        # if not res:
        #     response_object = {
        #         "message": "No sale with that id exists",
        #         "status": "fail"
        #     }
        #     return(make_response(jsonify(response_object)), 404)
        # else:
        #     self.connection.cursor.execute(
        #         " SELECT * FROM sales WHERE sale_id=%s ", [id])
        #     response = self.connection.cursor.fetchone()
        #     return(make_response(jsonify(response)))

    def get_user_sales(self, id):
        """
        The function to get specific sale records of a user.
        Parameter:
                id: This is the unique identification number
                 of a user
        Returns:
                Sales:All sales orders of a user
        """
        self.connection.cursor.execute(
            " SELECT * FROM sales WHERE user_id=%s ", [id])
        user = self.connection.cursor.fetchall()
        if not user:
            response = {
                'status': 'fail',
                'message': 'user has not created a sale or is not an employee'
            }
            return(make_response(jsonify(response)), 404)
        else:
            self.connection.cursor.execute(
                " SELECT * FROM sales WHERE user_id=%s ", [id])
            response = self.connection.cursor.fetchall()
            return response
