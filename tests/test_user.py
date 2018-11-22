import unittest
from flask import json, jsonify
from sendapi.routes.user import fetch_all_users, delete_user
from sendapi import app
from sendapi.models.database import DatabaseConnection


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user={
            "email": "me@gmail.com",
            "password": "intransit"
            }
        self.admin={
                "email": "admin@admin.com",
                "password": "password"
            }
        self.parcel={
                "pickup": "entebbe",
                "destination": "jinja"
            }
 
    def test_endpoint_fetches_all_users(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(self.admin))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(self.admin))
        self.assertEqual(response.status_code,200)
        authentication_token=response.json['auth_token']
        get_users=self.client.get('/api/v1/users', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        self.assertEqual(get_users.status_code,200)
        self.assertEqual(get_users.json,[{
                "email": "admin@admin.com",
                "password": "password",
                "role":'admin',
                "userid":1
            }])
        
    def test_endpoint_doesnt_fetch_all_users_if_not_admin(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code,200)
        authentication_token=response.json['auth_token']
        get_users=self.client.get('/api/v1/users', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        self.assertEqual(get_users.status_code,401)
        self.assertEqual(get_users.json,{"message":"Only Admin can view all users"})

    
    def test_endpoint_fetches_all_userparcels(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code,200)
        authentication_token=response.json['auth_token']
        self.client.post('/api/v1/parcels', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' },data=json.dumps(self.parcel))
        self.assertEqual(result.status_code,201)
        get_users=self.client.get('/api/v1/users/1/parcels', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        self.assertEqual(get_users.status_code,401)
        self.assertEqual(get_users.json,{"message":'You are not logged in'})
    
    def test_endpoint_deletes_user(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(self.admin))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(self.admin))
        self.assertEqual(response.status_code,200)
        authentication_token=response.json['auth_token']
        get_users=self.client.delete('/api/v1/users/1', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        self.assertEqual(get_users.status_code,200)
        self.assertEqual(get_users.json,{"message":"user has been deleted"})

    def test_endpoint_doesnt_delete_user_if_its_not_admin(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code,200)
        authentication_token=response.json['auth_token']
        get_users=self.client.delete('/api/v1/users/1', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        self.assertEqual(get_users.status_code,400)
        self.assertEqual(get_users.json,{"message":"Only admin can delete users"})

    def test_endpoint_fetches_user(self):
        result=self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(result.status_code,201)
        response=self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code,200)
        authentication_token=response.json['auth_token']
        get_users=self.client.get('/api/v1/users/1', content_type='application/json', headers={'Authorization':f'Bearer {authentication_token}' })
        self.assertEqual(get_users.status_code,401)
        self.assertEqual(get_users.json,{"message":"only admin can access user details"})

    
    def tearDown(self):
        databasecon = DatabaseConnection()
        databasecon.drop_table('users')
   
if "__name__" == "__main__":
    unittest.main()
