from flask import Blueprint, jsonify
from flask_restful import reqparse

# local imports
from app.controllers.users_controllers import Users


usr = Users()


don_user = Blueprint('users', __name__, url_prefix="/api/v2")

user_instance = Users()


@don_user.route("/signup", methods=["POST"])
@usr.logged_in
@usr.check_admin
def create_user(res=None, user_role=None, user_id=None, user_email=None):
    """
        This function creates a new user. 
    Parameters:
            username:Name to be used by user once account is created.
            email:Email to be used for verification.
            Password: To be used when signin to created account. 
                        role: This is the role of user can be attendant/admin
    Returns:
            Users:Creates a new user. 
    """
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True,
                        help="field cannot be empty", location="json")
    parser.add_argument("password", type=str, required=True,
                        help="field cannot be empty", location="json")
    data = parser.parse_args()

    return user_instance.create_user(data)


@don_user.route("/signin", methods=["POST"])
def signin_user():
    """
    The function signsin a user.

    Parameters:
        email:Email used during regestration.
        password:Password used to create account.

    Returns:
        User: Signsin a user.
    """
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True,
                        help="cannot be empty", location="json")
    parser.add_argument("password", type=str, required=True,
                        help="cannot be empty", location="json")
    data = parser.parse_args()

    return user_instance.signin_user(data)


@don_user.route('/users', methods=['GET'])
@usr.logged_in
@usr.check_admin
def get_user(res=None, user_id=None, user_role=None, user_email=None):
    users = user_instance.get_user()
    print("users>>>>", users)
    users_data = []
    for user in users:
        data = {
            "user_id": user[0],
            "user_email": user[1],
            "user_role": user[3]
        }
        users_data.append(data)
    return (jsonify({
        "users": users_data
    }))


@don_user.route('/user/<id>', methods=['PUT'])
@usr.logged_in
@usr.check_admin
def update_user(id, res=None, user_id=None, user_role=None, user_email=None):
    return user_instance.update_user(id)


@don_user.route('/user-demote/<id>', methods=['PUT'])
@usr.logged_in
@usr.check_admin
def demote_user(id, res=None, user_id=None, user_role=None, user_email=None):
    return user_instance.demote_user(id)
