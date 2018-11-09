import unittest
from flask import request, jsonify
# import sys
# sys.path.append("..")
from app.models import users, Users, Parcels, parcels
from app import routes
from app import app


class TestApp(unittest.TestCase):
    def settup(self):
        self.Parcels = self.Parcels()
        # Users=Users()

    def test_model_can_fetch_all_parcels(self):

        self.assertIsNotNone(self.Parcels.get_parcels())

    def test_model_can_fetch_all_parcels_as_a_list(self):

        self.assertIsInstance(self.Parcels.get_parcels(), list)

    def test_endpoint_fetches_all_entries(self):
        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.Parcels = None


        # Users=None
if "__name__" == "__main__":
    unittest.main()
