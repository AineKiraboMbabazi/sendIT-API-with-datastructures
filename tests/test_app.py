import unittest
import datetime
from flask import json, request, jsonify
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
    
    def test_create_parcel(self):
        self.assertIsInstance(self.Parcels.create_parcel()[0],dict)

    def test_create_parcel_message(self):
        self.assertEqual(self.Parcels.create_parcel()[1],{"message":"Your order has been created"})

    def test_create_parcel_order(self):
        self.client=app.test_client()
        response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
            {
                 
                "destination": "Arua",  
                "pickup": "Masaka", 
                "status": "intransit", 
                "userId": 2
            }
        ))
        self.assertEqual(response.status_code,201)
        self.assertIsNotNone(response[0].get['destination'])
        self.assertIsNotNone(response[0].get['pickup'])
        self.assertIsNotNone(response[0].get['status'])
        self.assertIsNotNone(response[0].get['userId'])
        self.assertIsNotNone(response[0].get['parcelId'])
        self.assertIsNotNone(response[0].get['creation_date'])

        self.assertEqual(response[0].get['destination'], 'Arua')
        self.assertEqual(response[0].get['pickup'],'Masaka')
        self.assertEqual(response[0].get['status'],'intransit')
        self.assertEqual(response[0].get['userId'],2)
        self.assertEqual(response[0].get['parcelId'],1)
        self.assertEqual(response[0].get['creation_date'],datetime.date.today().strftime('%Y-%m-%d'))
    def test_can_fetch_specific_parcel(self):
        
        self.assertIsInstance(self.Parcels.get_specific_parcel(1),dict)
        
        self.assertIsInstance(self.Parcels.get_specific_parcel(100000000000),{"message":"The parcel with that id doesnot exist"})
    
    def test_fetch_specific_parcel_endpoint_before_post(self):
        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/parcels/<int:parcelId>', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response)
        self.assertIsInstance(response,dict)

    def test_fetch_specific_parcel_endpoint_after_post(self):
        self.client = app.test_client()
        response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
            {
                
                "userId":2,
                "status":"intransit",
                "pickup":"Masaka",
                "destination":"Arua"
                
            }
        ))
        response = self.client.get(
            '/api/v1/parcels/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response)
        self.assertIsInstance(response,dict)
        self.assertEqual(response,{
            "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
            "destination": "Arua",
            "parcelId": 1,
            "pickup": "Masaka",
            "status": "intransit",
            "userId": 2
        })
        self.assertIsNotNone(response.get['destination'])
        self.assertIsNotNone(response.get['pickup'])
        self.assertIsNotNone(response.get['status'])
        self.assertIsNotNone(response.get['userId'])
        self.assertIsNotNone(response.get['parcelId'])
        self.assertIsNotNone(response.get['creation_date'])

        self.assertEqual(response.get['destination'], 'Arua')
        self.assertEqual(response.get['pickup'],'Masaka')
        self.assertEqual(response.get['status'],'intransit')
        self.assertEqual(response.get['userId'],2)
        self.assertEqual(response.get['parcelId'],1)
        self.assertEqual(response.get['creation_date'],datetime.date.today().strftime('%Y-%m-%d'))
    def test_get_parcels_by_specific_user(self):
        # Parcels.
        self.assertIsInstance(self.Parcels.get_parcels_by_specific_user(1)[0],dict)
        self.assertIsNone(self.Parcels.get_parcels_by_specific_user(1))
        self.assertIsInstance(self.Parcels.get_parcels_by_specific_user(1)[1],list)
        self.assertIsInstance(self.Parcels.get_parcels_by_specific_user(1),list)

    def test_endpoint_before_post_fetches_all_parcels_by_specific_user(self):
        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/users/<int:userId>/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response[0])
        self.assertIsNotNone(response[1])
        self.assertIsInstance(response[0],dict)
        self.assertEqual(response[0],{"message":"The user with that Id has not created any parcel Delivery orders"})
        self.assertIsInstance(response[1],list)
        self.assertEqual(response[1],[])

    def test_endpoint_after_post_fetches_all_parcels_by_specific_user(self):
   
        self.client=app.test_client()
        response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
            {
                
                "userId":2,
                "status":"intransit",
                "pickup":"Masaka",
                "destination":"Arua"
                
            }
        ))
        response = self.client.get(
            '/api/v1/users/2/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response[0])
        self.assertIsNotNone(response[1])
        self.assertIsInstance(response[0],dict)
        self.assertEqual(response[0],{"Created by":2,"Number of parcels":1})
        self.assertIsInstance(response[1],list)
        self.assertEqual(response[1],{
        "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
        "destination": "Arua",
        "parcelId": 1,
        "pickup": "Masaka",
        "status": "intransit",
        "userId": 2
        })
        self.assertIsNotNone(response[0].get['destination'])
        self.assertIsNotNone(response[0].get['pickup'])
        self.assertIsNotNone(response[0].get['status'])
        self.assertIsNotNone(response[0].get['userId'])
        self.assertIsNotNone(response[0].get['parcelId'])
        self.assertIsNotNone(response[0].get['creation_date'])
    def tearDown(self):
        self.Parcels = None


        # Users=None
if "__name__" == "__main__":
    unittest.main()
