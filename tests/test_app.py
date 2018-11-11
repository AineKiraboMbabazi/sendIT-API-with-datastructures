import unittest
import datetime
from flask import json, request, jsonify
# import sys
# sys.path.append("../")
from sendapi import app 
from sendapi.models import reset_parcels,users, Users, parcels,Parcels
from sendapi import routes

class TestApp(unittest.TestCase):
    def setUp(self):
        self.Parcels = Parcels()
        self.Users=Users()
        

    def test_endpoint_index(self):
        self.client = app.test_client()
        response = self.client.get(
            '/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),{"message": "Welcome to sendIT API"})
    def test_model_can_fetch_all_parcels(self):

        self.assertIsNotNone(self.Parcels.get_parcels())

    def test_model_can_fetch_all_parcels_as_a_list(self):

        self.assertIsInstance(self.Parcels.get_parcels(), dict)

    def test_endpoint_fetches_all_entries_before_post(self):

        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),{'message': 'No parcels have been found'})

    def test_endpoint_fetches_all_entries_after_post(self):

        self.client = app.test_client()
        response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
            {
                
                "destination": "Arua",  
                "pickup": "Masaka", 
                "status": "intransit", 
                "userId": 2
            }
        ))
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            '/api/v1/parcels', content_type='application/json')
        
        self.assertEqual(json.loads(response.data),[
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
        response_data =  json.loads(response.data)
        
        self.assertIsNotNone(response_data[0]['userId'])
        self.assertIsNotNone(response_data[0]['parcelId'])
        self.assertIsNotNone(response_data[0]['creation_date'])
        
        self.assertEqual(response_data[0]['parcelId'],1)
       

    
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
        response_data =  json.loads(response.data)
        self.assertIsNotNone(response_data[0]['destination'])
        self.assertIsNotNone(response_data[0]['pickup'])
        self.assertIsNotNone(response_data[0]['status'])
        self.assertIsNotNone(response_data[0]['userId'])
        self.assertIsNotNone(response_data[0]['parcelId'])
        self.assertIsNotNone(response_data[0]['creation_date'])
        self.assertEqual(response_data[0]['destination'], 'Arua')
        self.assertEqual(response_data[0]['pickup'],'Masaka')
        self.assertEqual(response_data[0]['status'],'intransit')
        self.assertEqual(response_data[0]['userId'],2)
        self.assertEqual(response_data[0]['parcelId'],1)
        self.assertEqual(response_data[0]['creation_date'],datetime.date.today().strftime('%Y-%m-%d'))

    def test_can_fetch_specific_parcel(self):
        
        self.assertIsInstance(self.Parcels.get_specific_parcel(1),dict)
        self.assertEqual(self.Parcels.get_specific_parcel(100000000000),{"message":"The parcel with that id doesnot exist"})
    
    def test_fetch_specific_parcel_endpoint_before_post(self):
        
        self.client = app.test_client()
        response = self.client.get(
            '/api/v1/parcels/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json.loads(response.data))
        self.assertIsInstance(json.loads(response.data),dict)

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
        response_data =  json.loads(response.data)
        self.assertIsNotNone(response_data)
        self.assertIsInstance(response_data,dict)
        self.assertEqual(response_data,{
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
        self.assertEqual(response_data['pickup'],'Masaka')
        self.assertEqual(response_data['status'],'intransit')
        self.assertEqual(response_data['userId'],2)
        self.assertEqual(response_data['parcelId'],1)
        self.assertEqual(response_data['creation_date'],datetime.date.today().strftime('%Y-%m-%d'))
    
    def test_get_parcels_by_specific_user(self):

        self.assertIsInstance(self.Parcels.get_parcels_by_specific_user(1)[0],dict)
        self.assertIsNotNone(self.Parcels.get_parcels_by_specific_user(1))
        self.assertIsInstance(self.Parcels.get_parcels_by_specific_user(1)[1],list)
        self.assertIsInstance(self.Parcels.get_parcels_by_specific_user(1),tuple)

    # def test_endpoint_before_post_fetches_all_parcels_by_specific_user(self):
        
    #     self.client = app.test_client()
    #     response = self.client.get(
    #         '/api/v1/users/<int:userId>/parcels', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response[0])
    #     self.assertIsNotNone(response[1])
    #     self.assertIsInstance(response[0],dict)
    #     self.assertEqual(response[0],{"message":"The user with that Id has not created any parcel Delivery orders"})
    #     self.assertIsInstance(response[1],list)
    #     self.assertEqual(response[1],[])

    # def test_endpoint_after_post_fetches_all_parcels_by_specific_user(self):
   
    #     self.client=app.test_client()
    #     response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
    #         {
                
    #             "userId":2,
    #             "status":"intransit",
    #             "pickup":"Masaka",
    #             "destination":"Arua"
                
    #         }
    #     ))
    #     response = self.client.get(
    #         '/api/v1/users/2/parcels', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response[0])
    #     self.assertIsNotNone(response[1])
    #     self.assertIsInstance(response[0],dict)
    #     self.assertEqual(response[0],{"Created by":2,"Number of parcels":1})
    #     self.assertIsInstance(response[1],list)
    #     self.assertEqual(response[1],{
    #     "creation_date": datetime.date.today().strftime('%Y-%m-%d'),
    #     "destination": "Arua",
    #     "parcelId": 1,
    #     "pickup": "Masaka",
    #     "status": "intransit",
    #     "userId": 2
    #     })
    #     self.assertIsNotNone(response[0].get['destination'])
    #     self.assertIsNotNone(response[0].get['pickup'])
    #     self.assertIsNotNone(response[0].get['status'])
    #     self.assertIsNotNone(response[0].get['userId'])
    #     self.assertIsNotNone(response[0].get['parcelId'])
    #     self.assertIsNotNone(response[0].get['creation_date'])
    # def test_cancel_specific_order_before_post(self):
        
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1))
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1),{"message":"The order you are trying to cancel doesnot exist"})
    #     self.assertIsInstance(self.Parcels.cancel_specific_parcel(1),dict)
    
    # def test_cancel_specific_order_after_post_model(self):
        
    #     neworder={
    #         "creation_date": "2018-11-10",
    #         "destination": "Arua",
    #         "parcelId": 1,
    #         "pickup": "Masaka",
    #         "status": "intransit",
    #         "userId": 2
    #     }
    #     parcels.append(neworder)
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1))
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[0][0],{"message": "parcel delivery order has been canceled"})
    #     self.assertIsInstance(self.Parcels.cancel_specific_parcel(1)[1],list)
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[1].get['destination'])
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[1].get['pickup'])
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[1].get['status'])
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[1].get['userId'])
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[1].get['parcelId'])
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1)[1].get['creation_date'])
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[1].get['destination'], 'Arua')
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[1].get['pickup'],'Masaka')
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[1].get['status'],'intransit')
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[1].get['userId'],2)
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[1].get['parcelId'],1)
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1)[1].get['creation_date'],'2018-11-10')

    # def test_endpoint_cancels_order_before_post(self):
    #     self.assertIsNotNone(self.Parcels.cancel_specific_parcel(1))
    #     self.assertEqual(self.Parcels.cancel_specific_parcel(1),{"message":"The order you are trying to cancel doesnot exist"})
    #     self.assertIsInstance(self.Parcels.cancel_specific_parcel(1),dict)
    
    # def test_cancel_specific_order_after_post(self):
        
    #     self.client=app.test_client()
    #     response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
    #         {
                
    #             "userId":2,
    #             "status":"intransit",
    #             "pickup":"Masaka",
    #             "destination":"Arua"
                
    #         }
    #     ))
    #     self.Parcels.cancel_specific_parcel(1)
    #     response = self.client.get(
    #         '/api/v1/users/2/parcels', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response(1)[0][0],{"message": "parcel delivery order has been canceled"})
    #     self.assertIsInstance(response(1)[1],list)
    #     self.assertIsNotNone(response(1)[1].get['destination'])
    #     self.assertIsNotNone(response(1)[1].get['pickup'])
    #     self.assertIsNotNone(response(1)[1].get['status'])
    #     self.assertIsNotNone(response.get['userId'])
    #     self.assertIsNotNone(response(1)[1].get['parcelId'])
    #     self.assertIsNotNone(response(1)[1].get['creation_date'])
    #     self.assertEqual(response(1)[1].get['destination'], 'Arua')
    #     self.assertEqual(response(1)[1].get['pickup'],'Masaka')
    #     self.assertEqual(response(1)[1].get['status'],'intransit')
    #     self.assertEqual(response(1)[1].get['userId'],2)
    #     self.assertEqual(response(1)[1].get['creation_date'],datetime.date.today().strftime('%Y-%m-%d'))

    # def test_auto_increment_id_users(self):
    #     self.assertEqual(self.Users.auto_increment_id(),1)
    
    # def test_auto_increment_id_parcels(self):
    #     self.assertEqual(self.Users.auto_increment_id(),1)

    # def test_create_user(self):
    #     self.assertIsInstance(self.Users.create_user(),dict)
        
    # def test_get_users(self):
    #     self.assertEqual(self.Users.get_users(),{"message":"No users have been created"})
    #     self.assertIsInstance(self.Users.get_users(),dict)
    #     newuser={
	
    #         "email":"me@gmail.com",
    #         "password":"intransit"
        
            
    #     }
    #     users.append(newuser)
    #     self.assertIsNotNone(self.Users.get_users())
    #     self.assertEqual(self.Users.get_users(),{
    #         "email": "me@gmail.com",
    #         "password": "intransit",
    #         "userId": 1
    #     })

    # def test_endpoint_gets_users(self):
    #     self.client = app.test_client()

    #     response = self.client.get(
    #         '/api/v1/users', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response)
    #     self.assertIsInstance(response,dict)
    #     self.assertEqual(response,{"message":"No users have been created"})

    # def test_endpoint_gets_users_after_post(self):
    #     self.client = app.test_client()
    #     response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
    #         {
                
    #            "email":"me@gmail.com",
    #             "password":"intransit"
                
    #         }
    #     ))
    #     response = self.client.get(
    #         '/api/v1/users', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response)
    #     self.assertIsInstance(response,dict)
    #     self.assertEqual(response,{
    #         "email": "me@gmail.com",
    #         "password": "intransit",
    #         "userId": 1
    #     })
    #     self.assertIsNotNone(response.get["userId"])
    #     self.assertIsNotNone(response.get["password"])
    #     self.assertIsNotNone(response.get["email"])

    # def test_endpoint_posts_users(self):
    #     self.client = app.test_client()
    #     response=self.client.post('/api/v1/parcels',content_type='application/json', data=json.dumps(
    #         {
                
    #            "email":"me@gmail.com",
    #             "password":"intransit"
                
    #         }
    #     ))
        
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIsNotNone(response)
    #     self.assertIsInstance(response,dict)
    #     self.assertEqual(response,{
    #         "email": "me@gmail.com",
    #         "password": "intransit",
    #         "userId": 1
    #     })
    #     self.assertIsNotNone(response.get["userId"])
    #     self.assertIsNotNone(response.get["password"])
    #     self.assertIsNotNone(response.get["email"])
    def tearDown(self):
        self.Parcels = None
        self.Users=None
        reset_parcels()
if "__name__" == "__main__":
    unittest.main()
