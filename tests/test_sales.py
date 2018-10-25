import unittest
import json
from app import create_app, db


class SalesTestCase(unittest.TestCase):
    """ TestCase for Menus"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.prod_data = {
            "description": "cement,nails,paint",
            "price": "500"
        }

        self.user_data = {
            "email": "meth@mail.com",
            "password": "shssss",
        }
        self.login_data = {
            "email": "meth@mail.com",
            "password": "shssss"
        }
        self.admin_data = {
            "email": "admin@mail.com",
            "password": "adminpassword"
        }

        with self.app.app_context():
            db.create_tables()

        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.admin_data),
            headers={"content-type": "application/json"}
        )
        self.auth_token = json.loads(res.data.decode('utf-8'))['token']

    def test_admin_login(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.admin_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_admin_create_sale(self):
        token = self.auth_token
        res = self.client().post(
            "api/v2/sales",
            data=json.dumps(self.prod_data),
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 201)

    def test_create_user(self):
        token = self.auth_token
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
            data=json.dumps(self.login_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def get_user_token(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.login_data),
            headers={"content-type": "application/json"}
        )
        response = json.loads(res.data.decode('utf-8'))['token']
        return response

    def test_normal_user_creating_sale(self):
        token = self.get_user_token()
        res = self.client().post(
            "api/v2/sales",
            data=json.dumps(self.prod_data),
            headers={"content-type": "application/js",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()
