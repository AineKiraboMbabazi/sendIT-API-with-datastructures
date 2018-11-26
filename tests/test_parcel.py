import datetime
import unittest
from flask import json, jsonify
from sendapi import app
from .test_base import TestBase
from sendapi.models.database import DatabaseConnection


class TestParcel(TestBase):

    def test_index(self):
        result = self.client.get('/', content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json, {"message": "Welcome to sendIT API"})

    def test_create_parcels(self):
        authentication_token = self.get_admin_token()
        get_create_parcel = self.client.post('/api/v1/parcels',
                                             content_type='application/json',
                                             headers={'Authorization': f'Bearer\
                                                      {authentication_token}'},
                                             data=json.dumps(self.parcel))
        self.assertEqual(get_create_parcel.status_code, 201)
        self.assertEqual(get_create_parcel.json, {
            "message": "Your parcel order has been created"})

    def test_create_parcels_with_no_token(self):
        result = self.client.post('/api/v1/auth/signup',
                                  content_type='application/json',
                                  data=json.dumps(self.admin))
        self.assertEqual(result.status_code, 201)
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.admin))
        self.assertEqual(response.status_code, 200)
        get_create_parcel = self.client.post('/api/v1/parcels',
                                             content_type='application/json',
                                             data=json.dumps(self.parcel))
        self.assertEqual(get_create_parcel.status_code, 401)
        self.assertEqual(get_create_parcel.json, {
                            'msg': 'Missing Authorization Header'})

    def test_create_parcel_with_invalid_destination(self):
        authentication_token = self.get_admin_token()
        get_create_parcel = self.client.post('/api/v1/parcels',
                                             content_type='application/json',
                                             headers={'Authorization': f'Bearer\
                                              {authentication_token}'},
                                             data=json.dumps(self.
                                                             invaliddestination
                                                             ))
        self.assertEqual(get_create_parcel.status_code, 400)
        self.assertEqual(get_create_parcel.json, {"message": "destination Field should\
                         contain strings"})

    def test_create_parcel_with_invalid_pickup(self):
        authentication_token = self.get_admin_token()
        get_create_parcel = self.client.post('/api/v1/parcels',
                                             content_type='application/json',
                                             headers={'Authorization': f'Bearer\
                                                      {authentication_token}'},
                                             data=json.dumps(
                                                self.invalidpickup))
        self.assertEqual(get_create_parcel.status_code, 400)
        self.assertEqual(get_create_parcel.json, {
            "message": "pickup Field should contain strings"})

    def test_create_parcel_with_missing_fields(self):
        token = self.get_admin_token()
        parcel = self.client.post('/api/v1/parcels',
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {token}'},
                                  data=json.dumps(self.missing_fields))
        self.assertEqual(parcel.status_code, 400)
        self.assertEqual(parcel.json, {"message": "Some fields are missing"})

    def test_doesnt_create_parcels_if_not_user(self):
        result = self.client.post('/api/v1/auth/signup',
                                  content_type='application/json',
                                  data=json.dumps(self.admin))
        self.assertEqual(result.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application\
        /json', data=json.dumps(self.admin))
        self.assertEqual(response.status_code, 200)
        get_create_parcel = self.client.post('/api/v1/parcels', content_type='application\
        /json', data=json.dumps(self.parcel))
        self.assertEqual(get_create_parcel.status_code, 401)
        self.assertEqual(get_create_parcel.json, {
            'msg': 'Missing Authorization Header'})

    def test_fetch_all_parcels(self):
        token = self.get_admin_token()
        self.client.post('/api/v1/parcels', content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcels = self.client.get('/api/v1/parcels',
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcels.status_code, 200)

    def test_fetch_all_parcels_as_user(self):
        token = self.get_user_token()
        self.client.post('/api/v1/parcels', content_type='application\
        /json', headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcels = self.client.get('/api/v1/parcels',
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcels.status_code, 400)
        self.assertEqual(parcels.json, {
            "message": "Only administrators can view parcels"})

    def test_doesnot_fetch_all_parcels_before_post(self):
        token = self.get_admin_token()
        parcels = self.client.get('/api/v1/parcels',
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcels.status_code, 404)
        self.assertEqual(parcels.json, {"message": "No parcels found"})

    def test_fetch_all_parcels_without_token(self):
        token = self.get_admin_token()
        self.client.post('/api/v1/parcels', content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcels = self.client.get('/api/v1/parcels',
                                  content_type='application/json')
        self.assertEqual(parcels.status_code, 401)
        self.assertEqual(parcels.json, {'msg': 'Missing Authorization Header'})

    def test_fetch_specific_parcel(self):
        token = self.get_admin_token()
        self.client.post('/api/v1/parcels',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.get('/api/v1/parcels/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcel.status_code, 200)

    def test_cancel_specific_parcel(self):
        token = self.get_admin_token()
        self.client.post('/api/v1/parcels',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.put('/api/v1/parcels/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcel.status_code, 200)
        self.assertEqual(parcel.json, {
            "message": "Your parcel order has been cancelled"})

    def test_cancel_specific_parcel_which_doesnt_exist(self):
        token = self.get_admin_token()
        parcel = self.client.put('/api/v1/parcels/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcel.status_code, 404)
        self.assertEqual(parcel.json, {"message": " parcel doesnot exist"})

    def test_fetch_specific_parcel_when_parcel_doesnot_exist(self):
        token = self.get_admin_token()
        parcel = self.client.get('/api/v1/parcels/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(parcel.status_code, 404)
        self.assertEqual(parcel.json, {
            "message": "Parcel with that id doesnot exist"})

    def test_update_present_location_as_admin(self):
        token = self.get_admin_token()
        self.client.post('/api/v1/parcels', content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.put('/api/v1/parcels/present_location/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'},
                                 data=json.dumps(self.present_location))
        self.assertEqual(parcel.status_code, 200)

    def test_update_present_location(self):
        token = self.get_user_token()
        self.client.post('/api/v1/parcels', content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.put('/api/v1/parcels/present_location/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'},
                                 data=json.dumps(self.present_location))
        self.assertEqual(parcel.status_code, 400)

    def test_update_destination(self):
        token = self.get_user_token()
        self.client.post('/api/v1/parcels',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.put('/api/v1/parcels/destination/1',
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'},
                                 data=json.dumps(self.newdestination))
        self.assertEqual(parcel.status_code, 200)

    def test_delete_parcel(self):
        token = self.get_admin_token()
        self.client.post('/api/v1/parcels',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.delete('/api/v1/parcels/1',
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {token}'},
                                    data=json.dumps(self.newdestination))
        self.assertEqual(parcel.status_code, 200)
        self.assertEqual(parcel.json, {
            "message": "Your parcel has been deleted"})

    def test_delete_parcel_as_user(self):
        token = self.get_user_token()
        self.client.post('/api/v1/parcels',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'},
                         data=json.dumps(self.parcel))
        parcel = self.client.delete('/api/v1/parcels/1',
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {token}'},
                                    data=json.dumps(self.newdestination))
        self.assertEqual(parcel.status_code, 400)
        self.assertEqual(parcel.json, {
            "message": "only administrators can delete parcels"})


if "__name__" == "__main__":
    unittest.main()
