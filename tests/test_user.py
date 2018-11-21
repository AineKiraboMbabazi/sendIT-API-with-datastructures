import unittest
from flask import json, jsonify
from sendapi.routes.user import fetch_all_users, delete_user
from sendapi import app
from sendapi.models.database import DatabaseConnection


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    user={
        "email": "me@gmail.com",
        "password": "intransit"
        }


    def test_endpoint_fetches_all_users(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmaail.com",
                "password": "password"
            }
        ))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmaail.com",
                "password": "password"
            }
        ))
        
        self.assertEqual(response.status_code,200)
        # authentication_token=response.json['auth_token']
        # get_users=self.client.get('/api/v1/users', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        # self.assertEqual(get_users.status_code,200)
        # print(get_users.json)
        # 

#     """Test endpoint creates user"""
#     def test_endpoint_posts_user(self):
#         response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(self.user))
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response_data,
#             {
#                 "userId":1,
#                 "email": "me@gmail.com",
#                 "password": "intransit"
#             }
#         )
    
        
#     """ Test endpoint doesn't post user without email"""
#     def test_endpoint_doesnot_post_user_without_email(self):

#         response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
#             {
#         "email": " ",
#         "password": " password"
#         }
#         ))
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 400)
        
#         self.assertEqual(response_data, {"message": "The email is required"})
        
#     """Test endpoint doesnot create user when password field is empty"""
#     def test_endpoint_doesnt_post_user_without_password(self):

#         response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
#             {
#         "email": "me@gmail.com",
#         "password": " "
#         }
#         ))
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 400)
        
#         self.assertEqual(response_data, {"message": "The password is required"
#         })

#     """Test endpoint doesnt create user without a valid email"""
#     def test_endpoint_doesnt_post_user_without_valid_password(self):

#         response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
#             {
#         "email": "itworks",
#         "password": " password"
#         }
#         ))
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 400)
        
#         self.assertEqual(response_data, {"message": "You entered an invalid email"})

#     """Test fetch users"""
#     def test_endpoint_fetches_no_users_before_post(self):
#         response = self.client.get(
#             '/api/v1/users', content_type='application/json')
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_data,{"message": "No users have been created"})

#     def test_endpoint_fetches_all_users_after_post(self):
#         self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(self.user))
#         response = self.client.get(
#             '/api/v1/users', content_type='application/json')
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, list)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_data,[{'email': 'me@gmail.com', 'password': 'intransit', 'userId': 1}])
    
    
#     def test_endpoint_fetches_no_parcels_by_user_If_they_dont_exist(self):
#         response = self.client.get(
#             '/api/v1/users/1/parcels', content_type='application/json')
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_data,{"message": "The user with that Id has not created any parcel Delivery orders"})
    
#     def test_endpoint_deletes_user(self):
#         self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(self.user))
#         self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
#             {

#                 "destination": "Arua",
#                 "pickup": "Masaka",
#                 "status": "intransit",
#                 "userId": 1
#             }
#         ))
        
#         response =self.client.delete(
#             '/api/v1/users/1', content_type='application/json')
       
#         response_data=json.loads(response.data)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_data,{"message": "Your user has been deleted"})  
#     def test_endpoint_fetches_all_userparcels(self):
#         parcels.append(  {
#                 "parcelId":1,
#                 "destination": "Arua",
#                 "pickup": "Masaka",
#                 "status": " ",
#                 "userId": 1
#             })
#         response =self.client.get(
#             '/api/v1/users/1/parcels', content_type='application/json')
#         self.assertEqual(response.status_code,200)
#         self.assertIsInstance(response.json,list)
#         self.assertEqual(response.json,[ {
#                 "parcelId":1,
#                 "destination": "Arua",
#                 "pickup": "Masaka",
#                 "status": " ",
#                 "userId": 1
#             }])

    
    def tearDown(self):
        databasecon = DatabaseConnection()
        databasecon.drop_table('users')
   
if "__name__" == "__main__":
    unittest.main()
