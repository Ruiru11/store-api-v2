from flask import jsonify, make_response, request
import datetime
import jwt
from app.models.database import Database_connection
from functools import wraps
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
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return False
        else:
            return True

    def validate_password(self, password):
        """The function to validate password"""
        match = re.match(r'[a-z]{6,}', password)
        if match is None:
            response_object = {
                "status": "fail",
                "message": "password too short should be atleast 6 characters"
            }
            return(make_response(jsonify(response_object)), 409)
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
                return(make_response(jsonify(response_object)), 409)
        elif password is not True:
            return password
        elif email is not True:
            response_object = {
                "status": "fail",
                "message": "email format wrong"
            }
            return(make_response(jsonify(response_object)), 409)

    def get_user(self):
        """The function to ge all users """
        self.connection.cursor.execute("""SELECT * FROM users""")
        users = self.connection.cursor.fetchall()
        return(make_response(jsonify(users)))

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
            return(make_response(jsonify(response)), 404)
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
                return(make_response(jsonify(response)), 409)

    def generate_token(self, id, username, role):
        """Generate authentication token."""
        payload = {
            'exp': datetime.datetime.now() + datetime.timedelta(seconds=9000),
            'iat': datetime.datetime.now(),
            'sub': id,
            'username': username,
            'role': role
        }
        return jwt.encode(
            payload,
            'qwertyuiop',
            algorithm='HS256'
        ).decode("utf-8")

    def logged_in(self, func):
        """The function to check if a user is logged in"""
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                payload = jwt.decode(token, 'qwertyuiop')
                user_id = payload['sub']
                self.connection.cursor.execute(
                    " SELECT * FROM users WHERE id=%s ", [user_id])
                user = self.connection.cursor.fetchone()
                if user:
                    responseObject = {
                        'staus': 'sucess',
                        'message': 'user logged in'
                    }
                    new_kwargs = {
                        'res': responseObject,
                        'user_id': user[0]
                    }
                    kwargs.update(new_kwargs)
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User not found'
                    }
                    return make_response(jsonify(responseObject), 404)
            except jwt.ExpiredSignatureError:
                responseObject = {
                    'status': 'Fail',
                    'message': 'Wrong Token or expired Token please login'
                }
                return make_response(jsonify(responseObject), 403)
            except jwt.exceptions.DecodeError:
                responseObject = {
                    'status': 'Fail',
                    'message': 'Invalid token type or no token provided; please check your token or if none provided provide one '
                }
                return make_response(jsonify(responseObject), 500)
            return func(*args, **kwargs)
        return decorator

    def check_admin(self, func):
        """The function to check if a logged in user is an admin"""
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                payload = jwt.decode(token, 'qwertyuiop')
                user_role = payload['role']
                print("user", user_role)
                if user_role == 'admin':
                    new_kwargs = {
                        'user_role': user_role
                    }
                    kwargs.update(new_kwargs)
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Un-authorized Access only Admin allowed'
                    }
                    return make_response(jsonify(responseObject), 403)
            except jwt.ExpiredSignatureError:
                responseObject = {
                    'status': 'Fail',
                    'message': 'Token expired please login'
                }
                return make_response(jsonify(responseObject), 403)
            return func(*args, **kwargs)
        return decorator

    def update_user(self, id):
        """The function to elevate user status by admin"""
        self.connection.cursor.execute(
            "UPDATE users SET role='admin' WHERE id=%s",
            [id])
        response_object = {
            "satus": "pass",
            "message": "User elevated to admin"
        }
        return(make_response(jsonify(response_object)))
