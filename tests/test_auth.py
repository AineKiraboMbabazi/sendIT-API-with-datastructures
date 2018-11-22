import unittest
from flask import json, jsonify
from sendapi.routes.auth import create_user, login
from sendapi import app
from sendapi.models.database import DatabaseConnection


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_can_create_user(self):
        """
            function to creates user
        """

        response = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmil.com",
                "password": "password"
            }
        ))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json, {'message': 'user created successfully'})
    def test_cant_create_user_with_invalid_password(self):
        """
            function to creates user
        """

        response = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmil.com",
                "password": "  "
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "You entered an invalid password or password is missing"})

    def test_cant_create_user_with_invalid_email(self):
        """
            function to creates user
        """

        response = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": " ",
                "password": "password"
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "You entered an invalid email or the email is missing"})

    def test_cant_create_user_with_duplicate_email(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps({
            "email": "mbabazi@gmil.com ",
            "password": " password"
        }
        ))
        response = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmil.com ",
                "password": " password"
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json,{"message": "You entered an invalid email or the email is missing"})

    def test_cannot_create_user_when_fields_are_missing(self):
        """
            function to test creating a user falwith ni
            """
        response = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": "mbzi@gmil.com ",

            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "some fields are missing"})

    def test_cant_login_before_signup(self):
        """
            function to creates user
        """

        response = self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmail.com",
                "password": "password"
            }
        ))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "You are not a system user"})

    def test_cant_login_user_with_invalid_email(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps({
            "email": "mbabazi@gmil.com ",
            "password": " password"
        }
        ))
        response = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(
            {
                "email": "  ",
                "password": "password"
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json,{"message": "You entered an invalid email or the email is missing"})
    
    def test_cant_login_user_with_invalid_password(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps({
            "email": "mbabazi@gmil.com ",
            "password": "password"
        }
        ))
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(
            {
                "email": "mbababa@gmms.com",
                "password": "   "
            }
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json,{"message": "You entered an invalid password, password should be atleast 8 characters long"})
    
    def test_can_login_successfully(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps({
            "email": "mbabazi@gmil.com",
            "password": "password"
        }
        ))
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps(
            {
                "email": "mbabazi@gmil.com",
                "password": "password"
            }
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['message'],'login successful')

    def tearDown(self):
        databasecon = DatabaseConnection()
        databasecon.drop_table('users')
        # pass
