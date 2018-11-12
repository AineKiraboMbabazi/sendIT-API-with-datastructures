import unittest
import datetime
from flask import json, request, jsonify
# import sys
# sys.path.append("../")
from sendapi import app
from sendapi.models import reset_users, reset_parcels, users, Users, parcels, Parcels
from sendapi import routes


class TestApp(unittest.TestCase):
    def setUp(self):
        self.Parcels = Parcels()
        self.Users = Users()
        self.client = app.test_client()

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

    def test_model_can_fetch_all_parcels(self):

        self.assertIsNotNone(self.Parcels.get_parcels())

    def test_model_can_fetch_all_parcels_as_a_list(self):

        self.assertIsInstance(self.Parcels.get_parcels(), dict)

    def test_endpoint_fetches_all_entries_before_post(self):

        response = self.get_endpoint()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
                         'message': 'No parcels have been found'})

    def test_endpoint_fetches_all_entries_after_post(self):
        response = self.post_endpoint()

        self.assertEqual(response.status_code, 201)

        response = self.get_endpoint()
        self.assertEqual(json.loads(response.data), [
            {
                "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
                "destination": "Arua",
                "parcelId": 1,
                "pickup": "Masaka",
                "status": "intransit",
                "userId": 2
            }
        ])
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNotNone(response_data[0]['userId'])
        self.assertIsNotNone(response_data[0]['parcelId'])
        self.assertIsNotNone(response_data[0]['creation_date'])

        self.assertEqual(response_data[0]['parcelId'], 1)

    def test_create_parcel_order(self):

        response = self.post_endpoint()
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIsNotNone(response_data[0]['destination'])
        self.assertIsNotNone(response_data[0]['pickup'])
        self.assertIsNotNone(response_data[0]['status'])
        self.assertIsNotNone(response_data[0]['userId'])
        self.assertIsNotNone(response_data[0]['parcelId'])
        self.assertIsNotNone(response_data[0]['creation_date'])
        self.assertEqual(response_data[0]['destination'], 'Arua')
        self.assertEqual(response_data[0]['pickup'], 'Masaka')
        self.assertEqual(response_data[0]['status'], 'intransit')
        self.assertEqual(response_data[0]['userId'], 2)
        self.assertEqual(response_data[0]['parcelId'], 1)
        self.assertEqual(
            response_data[0]['creation_date'], datetime.date.today().strftime('%Y-%m-%d'))

    def test_can_fetch_specific_parcel(self):

        self.assertIsInstance(self.Parcels.get_specific_parcel(1), dict)
        self.assertEqual(self.Parcels.get_specific_parcel(100000000000), {
                         "message": "The parcel with that id doesnot exist"})

    def get_single_parcel(self):
        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/parcels/1', content_type='application/json')
        return response

    def test_fetch_specific_parcel_endpoint_before_post(self):

        response = self.get_single_parcel()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json.loads(response.data))
        self.assertIsInstance(json.loads(response.data), dict)

    def test_fetch_specific_parcel_endpoint_after_post(self):
        self.client = app.test_client()
        response = self.post_endpoint()
        response = self.get_single_parcel()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIsNotNone(response_data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response_data, {
            "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
            "destination": "Arua",
            "parcelId": 1,
            "pickup": "Masaka",
            "status": "intransit",
            "userId": 2
        })

        self.assertIsNotNone(response_data['destination'])
        self.assertIsNotNone(response_data['pickup'])
        self.assertIsNotNone(response_data['status'])
        self.assertIsNotNone(response_data['userId'])
        self.assertIsNotNone(response_data['parcelId'])
        self.assertIsNotNone(response_data['creation_date'])
        self.assertEqual(response_data['destination'], 'Arua')
        self.assertEqual(response_data['pickup'], 'Masaka')
        self.assertEqual(response_data['status'], 'intransit')
        self.assertEqual(response_data['userId'], 2)
        self.assertEqual(response_data['parcelId'], 1)
        self.assertEqual(
            response_data['creation_date'], datetime.date.today().strftime('%Y-%m-%d'))

    def test_get_parcels_by_specific_user(self):

        self.assertIsInstance(
            self.Parcels.get_parcels_by_specific_user(1), dict)
        self.assertIsNotNone(self.Parcels.get_parcels_by_specific_user(1))

    def test_endpoint_before_post_fetches_all_parcels_by_specific_user(self):

        response = self.client.get(
            '/api/v1/users/1/parcels', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, {
                         "message": "The user with that Id has not created any parcel Delivery orders"})

    def test_endpoint_after_post_fetches_all_parcels_by_specific_user(self):

        self.client = app.test_client()
        response = self.post_endpoint()
        response = self.client.get(
            '/api/v1/users/2/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(response, [{
            "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
            "destination": "Arua",
            "parcelId": 1,
            "pickup": "Masaka",
            "status": "intransit",
            "userId": 2
        }])
        self.assertIsNotNone(response[0]['destination'])
        self.assertIsNotNone(response[0]['pickup'])
        self.assertIsNotNone(response[0]['status'])
        self.assertIsNotNone(response[0]['userId'])
        self.assertIsNotNone(response[0]['parcelId'])
        self.assertIsNotNone(response[0]['creation_date'])

    def test_cancel_specific_order_before_post(self):

        self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1))
        self.assertEqual(self.Parcels.cancel_specific_parcel(
            1), {"message": "The order you are trying to cancel doesnot exist"})
        self.assertIsInstance(self.Parcels.cancel_specific_parcel(1), dict)

    def test_cancel_specific_order_after_post_model(self):

        neworder = {
            "creation_date": "2018-11-10",
            "destination": "Arua",
            "parcelId": 1,
            "pickup": "Masaka",
            "status": "intransit",
            "userId": 2
        }
        parcels.append(neworder)
        self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1))

        self.assertEqual(self.Parcels.cancel_specific_parcel(1)[0], {
                         "message": "parcel delivery order has been canceled"})
        self.assertIsInstance(self.Parcels.cancel_specific_parcel(1)[1], dict)
        self.assertIsNotNone(
            self.Parcels.cancel_specific_parcel(1)[1]['destination'])
        self.assertIsNotNone(
            self.Parcels.cancel_specific_parcel(1)[1]['pickup'])
        self.assertIsNotNone(
            self.Parcels.cancel_specific_parcel(1)[1]['status'])
        self.assertIsNotNone(
            self.Parcels.cancel_specific_parcel(1)[1]['userId'])
        self.assertIsNotNone(
            self.Parcels.cancel_specific_parcel(1)[1]['parcelId'])
        self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[
                             1]['creation_date'])
        self.assertEqual(self.Parcels.cancel_specific_parcel(1)[
                         1]['destination'], 'Arua')
        self.assertEqual(self.Parcels.cancel_specific_parcel(1)[
                         1]['pickup'], 'Masaka')
        self.assertEqual(self.Parcels.cancel_specific_parcel(1)[
                         1]['status'], 'canceled')
        self.assertEqual(
            self.Parcels.cancel_specific_parcel(1)[1]['userId'], 2)
        self.assertEqual(self.Parcels.cancel_specific_parcel(1)[
                         1]['parcelId'], 1)
        self.assertEqual(self.Parcels.cancel_specific_parcel(1)[
                         1]['creation_date'], '2018-11-10')

    def test_endpoint_cancels_order_before_post(self):
        self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1))
        self.assertEqual(self.Parcels.cancel_specific_parcel(
            1), {"message": "The order you are trying to cancel doesnot exist"})
        self.assertIsInstance(self.Parcels.cancel_specific_parcel(1), dict)

    def test_endpoint_cancels_specific_order_after_post(self):

        response = self.post_endpoint()
        response = self.client.put(
            '/api/v1/parcels/1', content_type='application/json')

        response = self.get_endpoint()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response)

        response = json.loads(response.data)

        self.assertEqual(response, [
            {'creation_date': '2018-11-11',
             'destination': 'Arua',
             'parcelId': 1,
             'pickup': 'Masaka',
             'status': 'canceled',
             'userId': 2}
        ])
        self.assertIsInstance(response, list)
        self.assertIsNotNone(response[0]['destination'])
        self.assertIsNotNone(response[0]['pickup'])
        self.assertIsNotNone(response[0]['status'])
        self.assertIsNotNone(response[0]['userId'])
        self.assertIsNotNone(response[0]['parcelId'])
        self.assertIsNotNone(response[0]['creation_date'])

    def test_auto_increment_id_users(self):
        self.assertEqual(self.Users.auto_increment_id(), 1)

    def test_auto_increment_id_parcels(self):
        self.assertEqual(self.Users.auto_increment_id(), 1)

    def test_get_users(self):
        self.assertEqual(self.Users.get_users(), {
                         "message": "No users have been created"})
        self.assertIsInstance(self.Users.get_users(), dict)
        newuser = {

            "email": "me@gmail.com",
            "password": "intransit",
            "userId": 1

        }
        users.append(newuser)
        self.assertIsNotNone(self.Users.get_users())
        self.assertEqual(self.Users.get_users(), [{
            "email": "me@gmail.com",
            "password": "intransit",
            "userId": 1
        }])

    def test_endpoint_gets_users(self):
        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/users', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response)
        response = json.loads(response.data)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, {"message": "No users have been created"})

    def test_endpoint_gets_users_after_post(self):

        response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
            {

                "email": "me@gmail.com",
                "password": "intransit"

            }
        ))
        response = self.client.get(
            '/api/v1/users', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(response, [{
            "email": "me@gmail.com",
            "password": "intransit",
            "userId": 1
        }])
        self.assertIsNotNone(response[0]["userId"])
        self.assertIsNotNone(response[0]["password"])
        self.assertIsNotNone(response[0]["email"])

    def tearDown(self):
        self.Parcels = None
        self.Users = None
        reset_parcels()
        reset_users()


if "__name__" == "__main__":
    unittest.main()
