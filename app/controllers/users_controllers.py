from flask import jsonify, make_response
from app.models.database import Database_connection
import psycopg2
from app import bcrypt
import uuid
import re


class Users(object):
    """This function deals with all user activities"""

    def __init__(self):
        self.connection = Database_connection()

    def validate_email(self, email):
        """The fuction to validate email"""
        match = re.match(
            r'(^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$)',
            email)
        if match is None:
            response_object = {
                "status": "fail",
                "message": "Please enter a valid email"
            }
            return(make_response(jsonify(response_object)), 403)
        elif len(email) == '':
            response_object = {
                "status": "fail",
                "message": " email cannot be empty"
            }
            return(make_response(jsonify(response_object)))
        else:
            return True

    def validate_password(self, password):
        """The function to validate password"""
        match = re.match(r'[a-z]{6,}', password)
        if match is None:

            response_object = {
                "status": "fail",
                "message": "password format wrong"
            }
            return(make_response(jsonify(response_object)))
        elif len(password) == '':
            response_object = {
                "status": "fail",
                "message": " password cannot be empty"
            }
            return(make_response(jsonify(response_object)), 403)
        else:
            return True

    def create_user(self, data):
        """
        The function to create new users. 

        Parameters:
                data:This are the arguments passed,
                                they are defined in user_views file.

        """
        email = self.validate_email(data['email'])
        password = self.validate_password(data['password'])
        if email and password is True:
            try:
                user_id = uuid.uuid4()
                print(data)
                encrypted_password = bcrypt.generate_password_hash(
                    data['password'], 12).decode("utf-8")
                self.connection.cursor.execute("""INSERT INTO users(id, email, password, role)
                VALUES(%s,%s,%s, %s);""",
                                               (str(user_id), data['email'],
                                                encrypted_password,
                                                'attendant'))
                print("Inserting data into users")
                response_object = {
                    "status": "pass",
                    "message": "user added succesfuly"
                }
                return(make_response(jsonify(response_object)), 201)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                response_object = {
                    "status": "fail",
                    "message": "Email already registered"
                }
                return(make_response(jsonify(response_object)))
        elif password is not True:
            return password
        elif email is not True:
            return email
        else:
            return email and password

    def all_users(self):
        """The function to ge all users """
        self.connection.cursor.execute("""SELECT * FROM users""")
        users = self.connection.cursor.fetchall()
        for user in users:
            return(jsonify(users))

    def signin_user(self, data):
        """
        The function logs in a user.

        Parameters:
            data[email]:email used during signup.
            data[password]:password used during signup

        Returns:
            Users:Signs in a user and also generates a token.
        """
        self.connection.cursor.execute(
            " SELECT * FROM users WHERE email=%s ", [data['email']])
        user = self.connection.cursor.fetchone()
        if not user:
            response = {
                'status': 'fail',
                'message': 'Email not registered create an account'
            }
            return(make_response(jsonify(response)))
        else:
            check_hash = bcrypt.check_password_hash(
                user[2], data['password']
            )
            if check_hash is True:
                user_id = user[0]

                token = self.generate_token(str(user_id), user[2], user[3],)
                response = {
                    'status': 'success',
                    'message': 'Sign in successful',
                    'token': str(token)
                }
                return(make_response(jsonify(response)))
            else:
                response = {
                    'status': 'fail',
                    'message': 'Incorrect password!!'
                }
                return(make_response(jsonify(response)))
