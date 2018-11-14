import unittest
import json
from app import create_app, db


class SalesTestCase(unittest.TestCase):
    """ TestCase for Menus"""

    def setUp(self):
        self.app = create_app(environment="testing")
        self.client = self.app.test_client
        self.sale_data = {
            "description":"steel",
            "cost": "500"
        }

        self.user_data = {
            "email": "sales@mail.com",
            "password": "password",
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
            data=json.dumps(self.sale_data),
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 409)

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
            data=json.dumps(self.user_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def get_user_token(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.user_data),
            headers={"content-type": "application/json"}
        )
        response = json.loads(res.data.decode('utf-8'))['token']
        print(">>>>>>>>>>>>>>>>>>>>>",response)
        return response

    
if __name__ == '__main__':
    unittest.main()
