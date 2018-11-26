import unittest
from flask import json, jsonify
from sendapi.routes.user import fetch_all_users, delete_user
from sendapi import app
from sendapi.models.database import DatabaseConnection
from .test_base import TestBase


class TestUsers(TestBase):

    def test_can_create_user(self):
        """
            function to test user creation
        """

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(self.user))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json, {'message': 'user created successfully'})

    def test_cant_create_user_with_invalid_password(self):
        """
            function to test user creation without valid password
        """
        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(self.missing_password))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "You entered an invalid password or \
                        password is missing"})

    def test_cant_create_user_with_invalid_email(self):
        """
            function to creates user
        """

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(self.missing_email))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "You entered an invalid email or the\
                         email is missing"})

    def test_cant_create_user_with_duplicate_email(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json',
                         data=json.dumps(self.user))
        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(self.user))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "Email already exists"})

    def test_cannot_create_user_when_fields_are_missing(self):
        """
            function to test creating a user falwith ni
            """
        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(self.user_missing_fields))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "some fields are missing"})

    def test_cant_login_before_signup(self):
        """
            function to creates user
        """

        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.user))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, {"message": "You are not a system user"})

    def test_cant_login_user_with_invalid_email(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup', content_type='application\
        /json', data=json.dumps(self.user))
        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(self.missing_email))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "You entered an invalid email or the\
                         email is missing"})

    def test_cant_login_user_with_invalid_password(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json',
                         data=json.dumps(self.user))
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.missing_password))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, {"message": "You entered an invalid password,\
                         password should be atleast 8 characters long"})

    def test_can_login_successfully(self):
        """
            function to creates user
        """
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json',
                         data=json.dumps(self.user))
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['message'], 'login successful')

    def test_endpoint_fetches_all_users(self):
        token = self.get_admin_token()
        users = self.client.get('/api/v1/users',
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(users.status_code, 200)
        self.assertEqual(users.json, [{
            "email": "admin@admin.com",
            "role": 'admin',
            "userid": 1
        }])

    def test_endpoint_doesnt_fetch_all_users_if_not_admin(self):
        token = self.get_user_token()
        users = self.client.get('/api/v1/users',
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(users.status_code, 401)
        self.assertEqual(users.json, {
                         "message": "Only Admin can view all users"})

    def test_endpoint_fetches_all_userparcels(self):
        token = self.get_user_token()
        self.client.post('/api/v1/parcels',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        users = self.client.get('/api/v1/users/1/parcels',
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(users.status_code, 200)
        self.assertIsInstance(users.json, dict)

    def test_endpoint_deletes_user(self):
        token = self.get_admin_token()
        users = self.client.delete('/api/v1/users/1',
                                   content_type='application/json',
                                   headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(users.status_code, 200)
        self.assertEqual(users.json, {
            "message": "user has been deleted"})

    def test_endpoint_doesnt_delete_user_if_its_not_admin(self):
        token = self.get_user_token()
        users = self.client.delete('/api/v1/users/1',
                                   content_type='application/json',
                                   headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(users.status_code, 400)
        self.assertEqual(users.json, {
                         "message": "Only admin can delete users"})

    def test_endpoint_fetches_user(self):
        token = self.get_user_token()
        users = self.client.get('/api/v1/users/1',
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(users.status_code, 401)
        self.assertEqual(users.json, {
                         "message": "only admin can access user details"})


if "__name__" == "__main__":
    unittest.main()
