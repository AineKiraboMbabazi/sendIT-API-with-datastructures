import unittest
import datetime
from flask import json, request, jsonify
from sendapi import app
from sendapi.models.parcel_model import parcels, Parcel
from sendapi.models.user_model import users, User
from sendapi.controllers.parcel_controller import ParcelController, reset_parcels
from sendapi.controllers.user_controller import reset_users


class TestApp(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()
        

    parcel = {"destination": "Arua",
              "pickup": "Masaka",
              "status": "intransit",
              "userId": 2,
              "parcelId": 1
              }

    def post_endpoint(self):

        response = self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "Arua",
                "pickup": "Masaka",
                "status": "intransit",
                "userId": 2
            }
        ))
        return response

    def get_endpoint(self):
        response = self.client.get(
            '/api/v1/parcels', content_type='application/json')
        return response

    def test_endpoint_index(self):

        response = self.client.get(
            '/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
                         "message": "Welcome to sendIT API"})

    def test_endpoint_fetches_all_entries_before_post(self):

        response = self.get_endpoint()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
                         'message': 'No parcels have been found'})

    def test_endpoint_fetches_all_entries_after_post(self):

        parcels.append(self.parcel)
        response_data = self.get_endpoint()
        response = (response_data).json
        self.assertEqual(response, [{"destination": "Arua",
                                     "pickup": "Masaka",
                                     "status": "intransit",
                                     "userId": 2,
                                     "parcelId": 1
                                     }])

        self.assertEqual(response_data.status_code, 200)

    def test_fetch_specific_parcel_endpoint_before_post(self):

        response = self.client.get(
            '/api/v1/parcels/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), dict)
        self.assertEqual(json.loads(response.data), {
                         "message": "The parcel with that id doesnot exist"})

    def test_fetch_specific_parcel_after_post(self):
        parcels.append(self.parcel)
        response = self.client.get(
            '/api/v1/parcels/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), dict)
        self.assertEqual(json.loads(response.data), {"destination": "Arua",
                                                     "pickup": "Masaka",
                                                     "status": "intransit",
                                                     "userId": 2,
                                                     "parcelId": 1
                                                     })

    def test_endpoint_doesnot_cancels_order_before_post(self):
        response = self.client.put(
            '/api/v1/parcels/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), dict)
        self.assertEqual(json.loads(response.data), {
                         "message": "The order you are trying to cancel doesnot exist"})

    def test_endpoint_deletes_specific_order_after_post(self):
        parcels.append(self.parcel)
        response = self.client.delete(
            '/api/v1/parcels/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
                         "message": "Your parcel has been deleted"})

    
    def test_create_parcels(self):
        users.append({
            "userId": 1,
            "email": "mbabazi@gmil.com ",
            "password": " password"
        }
        )
        response = self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "Arua",
                "pickup": "Masaka",
                "status": "intransit",
                "userId": 1
            }
        ))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {
            "parcelId": 1,
            "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
            "destination": "Arua",
            "pickup": "Masaka",
            "status": "intransit",
            "userId": 1
        })

    def test_create_parcels_with_unknown_user(self):
        users.append({
            "userId": 1,
            "email": "mbabazi@gmil.com ",
            "password": " password"
        }
        )
        response = self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "Arua",
                "pickup": "Masaka",
                "status": "intransit",
                "userId": 2
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "unknown userId"})

    def test_create_parcels_with_empty_status(self):
        self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
            {

                "email": "mbabazi@gmil.com ",
                "password": " password"}
        ))
        response = self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "Arua",
                "pickup": "Masaka",
                "status": " ",
                "userId": 1
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "one parameter is missing"})

    def test_create_parcels_with_empty_pickup(self):
        users.append({
            "userId": 1,
            "email": "mbabazi@gmil.com ",
            "password": " password"
        }
        )
        response = self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "Arua",
                "pickup": "Masaka",
                "status": " ",
                "userId": 1
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "one parameter is missing"})

    def test_create_parcels_with_invalid_strings(self):
        users.append({
            "userId": 1,
            "email": "mbabazi@gmil.com ",
            "password": " password"
        }
        )
        response = self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "2456",
                "pickup": "1234",
                "status": "345 ",
                "userId": 1
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "must contain letters"})

    def test_reset_parcel(self):
        self.assertEqual(reset_parcels(), [])

    def tearDown(self):

        reset_parcels()
        reset_users()


if "__name__" == "__main__":
    unittest.main()
