import unittest
from flask import json, jsonify
#from sendapi.routes.auth import create_user, login
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
            "description":"This is a order for a car parcel delivery"
            }

        self.parcel_with_missing_fields= {
            "pickup": "Masaka"}

        self.parcel_with_invalid_destination = {
            "destination": "  ",
            "pickup": "Masaka",
            "description":"This is a order for a car parcel delivery"
            }
        
        self.parcel_with_invalid_pickup = {
            "destination": "Arua",
            "pickup": "        ",
            "description":"This is a order for a car parcel delivery"}
        self.user={
            "email": "me@gmail.com",
            "password": "intransit"
            }
        self.admin={
                "email": "admin@admin.com",
                "password": "password"
            }
        self.present_location={
            "new location":"ntinda"
        }
        self.newdestination={
            "destination":"ntinda"
        }

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
                "destination": "jinja",
                "description":"This is a order for a car parcel delivery"
            }

    def tearDown(self):
        databasecon = DatabaseConnection()
        databasecon.drop_table('users')
        databasecon.drop_table('parcels')

        # pass
