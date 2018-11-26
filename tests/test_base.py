import unittest
from flask import json, jsonify
from sendapi import app
from sendapi.models.database import DatabaseConnection


class TestBase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        databasecon = DatabaseConnection()
        databasecon.create_db_tables()
        self.client = app.test_client()

        self.parcel = {
            "destination": "Arua",
            "pickup": "Masaka",
            "description": "This is a order for a car parcel delivery"
            }

        self.missing_fields = {
            "destination": "Arua",
            "pickup": "Masaka"
            }

        self.invaliddestination = {
            "destination": "  ",
            "pickup": "Masaka",
            "description": "This is a order for a car parcel delivery"
            }

        self.invalidpickup = {
            "destination": "Arua",
            "pickup": "        ",
            "description": "This is a order for a car parcel delivery"}
        self.user = {
                        "email": "mbabazi@gmil.com",
                        "password": "password"
                    }
        self.admin = {
                "email": "admin@admin.com",
                "password": "password"
            }
        self.present_location = {
            "new location": "ntinda"
        }
        self.newdestination = {
            "destination": "ntinda"
        }
        self.parcel = {
                "pickup": "entebbe",
                "destination": "jinja",
                "description": "This is a order for a car parcel delivery"
            }
        self.missing_password = {
                "email": "mbabazi@gmil.com",
                "password": "  "
            }
        self.missing_email = {
                "email": "",
                "password": "mbabaziom"
            }
        self.user_missing_fields = {
                "password": "mbabaziom"
            }

    def get_admin_token(self):
        result = self.client.post('/api/v1/auth/signup',
                                  content_type='application/json',
                                  data=json.dumps(self.admin))
        self.assertEqual(result.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application\
        /json', data=json.dumps(self.admin))
        self.assertEqual(response.status_code, 200)
        authentication_token = response.json['auth_token']
        return authentication_token

    def get_user_token(self):
        result = self.client.post('/api/v1/auth/signup',
                                  content_type='application/json',
                                  data=json.dumps(self.user))
        self.assertEqual(result.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application\
        /json', data=json.dumps(self.user))
        self.assertEqual(response.status_code, 200)
        authentication_token = response.json['auth_token']
        return authentication_token

    def tearDown(self):
        databasecon = DatabaseConnection()
        databasecon.drop_table('users')
        databasecon.drop_table('parcels')
