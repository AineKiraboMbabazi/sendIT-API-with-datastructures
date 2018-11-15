import unittest
from flask import json, request, jsonify
from sendapi import app
from sendapi.models.user_model import users, User
from sendapi.models.parcel_model import parcels
from sendapi.routes import user_routes
from sendapi.controllers.parcel_controller import reset_parcels 
from sendapi.controllers.user_controller import UserController, reset_users


class TestUserendpoint(unittest.TestCase):
    
    user={
        "email": "me@gmail.com",
        "password": "intransit"
        }
    def setUp(self):
        self.client=app.test_client()

    """Test endpoint creates user"""
    def test_endpoint_posts_user(self):
        response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(self.user))
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data,
            {
                "userId":1,
                "email": "me@gmail.com",
                "password": "intransit"
            }
        )
    
        
    """ Test endpoint doesn't post user without email"""
    def test_endpoint_doesnot_post_user_without_email(self):

        response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
            {
        "email": " ",
        "password": " password"
        }
        ))
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response_data, {"message": "The email is required"})
        
    """Test endpoint doesnot create user when password field is empty"""
    def test_endpoint_doesnt_post_user_without_password(self):

        response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
            {
        "email": "me@gmail.com",
        "password": " "
        }
        ))
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response_data, {"message": "The password is required"
        })

    """Test endpoint doesnt create user without a valid email"""
    def test_endpoint_doesnt_post_user_without_valid_password(self):

        response = self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(
            {
        "email": "itworks",
        "password": " password"
        }
        ))
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response_data, {"message": "You entered an invalid email"})

    """Test fetch users"""
    def test_endpoint_fetches_no_users_before_post(self):
        response = self.client.get(
            '/api/v1/users', content_type='application/json')
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data,{"message": "No users have been created"})

    def test_endpoint_fetches_all_users_after_post(self):
        self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(self.user))
        response = self.client.get(
            '/api/v1/users', content_type='application/json')
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data,[{'email': 'me@gmail.com', 'password': 'intransit', 'userId': 1}])
    
    
    def test_endpoint_fetches_no_parcels_by_user_If_they_dont_exist(self):
        response = self.client.get(
            '/api/v1/users/1/parcels', content_type='application/json')
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data,{"message": "The user with that Id has not created any parcel Delivery orders"})
    
    def test_endpoint_deletes_user(self):
        self.client.post('/api/v1/users', content_type='application/json', data=json.dumps(self.user))
        self.client.post('/api/v1/parcels', content_type='application/json', data=json.dumps(
            {

                "destination": "Arua",
                "pickup": "Masaka",
                "status": "intransit",
                "userId": 1
            }
        ))
        
        response =self.client.delete(
            '/api/v1/users/1', content_type='application/json')
       
        response_data=json.loads(response.data)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data,{"message": "Your user has been deleted"})  
    def tearDown(self):
        
        reset_users()
        reset_parcels()
   
if "__name__" == "__main__":
    unittest.main()
