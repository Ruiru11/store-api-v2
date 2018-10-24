import unittest
import json
from app import create_app, db


class UsersTestCase(unittest.TestCase):
    """Represesnts users testcase """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client

        self.user_data = {
            "email": "yyy@mail.com",
            "password": "shssss"
        }

        self.new_data = {
            "email": "mail.com",
            "password": "shssss",
            "username": "ruiru"
        }

        self.signin_data = {
            "email": "yyy@mail.com",
            "password": "shssss"
        }
        self.admin_data = {
            "email": "admin@mail.com",
            "password": "adminpassword"
        }

        with self.app.app_context():
            db.create_tables()

    def test_admin_login(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.admin_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def get_admin_token(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.admin_data),
            headers={"content-type": "application/json"}
        )
        response = json.loads(res.data.decode('utf-8'))['token']
        return response

    def test_user_signup(self):
        token = self.get_admin_token()
        res = self.client().post(
            "api/v2/signup",
            data=json.dumps(self.user_data),
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 201)

    def test_user_signin(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.signin_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
