import unittest
import testing.postgresql
import json

# Generate Postgresql class which shares the generated database
Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)


def tearDownModule(self):
    # clear cached database at end of tests
    Postgresql.clear_cache()


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Use the generated Postgresql class instead of testing.postgresql.Postgresql
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_admin_create_sale(self):
        token = self.auth_token
        res = self.client().post(
            "api/v2/sales",
            data=json.dumps(self.sale_data),
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 201)


if __name__ == '__main__':
    unittest.main()
