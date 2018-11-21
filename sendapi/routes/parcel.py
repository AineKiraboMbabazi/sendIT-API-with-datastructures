import re
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify
from sendapi import app
from config import app_config
from validations import Validator
from sendapi.models.parcel import Parcel
from sendapi.models.user import User
import datetime



"""Endpoint for the index page"""


@app.route("/index")
@app.route("/")
def index():
    return jsonify({"message": "Welcome to sendIT API"}), 200


"""
    Endpoint for creating a parcel
"""


@app.route("/api/v1/parcels", methods=['POST'])
@jwt_required
def create_parcel_order():
    """
        function to create a parcel
    """
    request_data = request.get_json()
    if len(request_data.keys() )!= 2:
        return jsonify({"message": "Some fields are missing"}), 400
    userid = get_jwt_identity()
    if not userid:
        return jsonify({"message": "You are not a registered user"})
    request_data = request.get_json(force=True)
    userId = userid
    status = 'pending'
    destination = request_data['destination']
    pickup = request_data['pickup']
    present_location = pickup
    creation_date= datetime.date.today().strftime('%Y-%m-%d')
    validate_input=Validator()
    if not (validate_input.validate_string_input(destination)):
        return jsonify({"message": "destination Field should contain strings"}), 400
    if not (validate_input.validate_string_input(pickup)):
        return jsonify({"message": "pickup Field should contain strings"}), 400
    parcel = Parcel()
    parcel.create_parcel(
        userId, creation_date,status, destination, pickup, present_location)
    
    return jsonify({"message": "Your parcel order has been created"}), 201


"""
    Endpoint for fetching all parcels
"""


@app.route("/api/v1/parcels", methods=['GET'])
@jwt_required
def fetch_all_parcels():
    parcel = Parcel()
    user = User()
    userid = get_jwt_identity()
    if not userid:
        return jsonify({'msg': 'Missing Authorization Header'}),401
    get_user = user.get_user_by_id(userid)
    if not get_user:
        return jsonify({"message":" No parcels to fetch"}),404
    if get_user['role'] == 'admin':
        parcel=Parcel()
        parcels = parcel.get_all_parcels()
        if parcels==[]:
            return jsonify({"message":"No parcels found"}),404
        return jsonify({'parcels': parcels}), 200

    return jsonify({"message": "Only administrators can view parcels"}), 400


@app.route("/api/v1/parcels/<int:parcelId>", methods=['GET'])
def fetch_specific_parcel(parcelId):
    parcel = Parcel()
    single_parcel = parcel.get_single_parcel(parcelId)
    if not single_parcel:
        return jsonify({"message":"Parcel with that id doesnot exist"}),404
    return jsonify({'parcel':single_parcel}), 200


@app.route("/api/v1/parcels/<int:parcelId>", methods=['PUT'])
@jwt_required
def cancel_specific_parcel(parcelId):
    userid = get_jwt_identity()
    parcel = Parcel()
    if not parcel.get_single_parcel(parcelId):
        return jsonify({"message":" parcel doesnot exist"}),404
    parcel_owner_id = parcel.get_single_parcel(parcelId)['userid']
    if parcel_owner_id != userid:
        return jsonify({"message": "You can only cancel an order you created"}), 400
    parcel.cancel_parcel(parcelId)
    return jsonify({"message": "Your parcel order has been cancelled"}), 200


@app.route("/api/v1/parcels/present_location/<int:parcelId>", methods=['PUT'])
@jwt_required
def update_present_location(parcelId):
    userid = get_jwt_identity()
    parcel = Parcel()
    user = User()
    editor = user.get_user_by_id(userid)['role']
    if editor != 'admin':
        return jsonify({"message": "You can only update the present location if you are an admin"}), 400
    request_data = request.get_json(force=True)
    newlocation = request_data['new location']
    validate_input=Validator().validate_string_input(newlocation)
    if not validate_input:
        return jsonify({"message": "The new location should be a none empty string"})
    parcel.update_present_location(parcelId, newlocation)
    parcel=parcel.get_single_parcel(parcelId)
    return jsonify({"message": "Your location has been updated ","updated parcel":parcel}), 200


@app.route("/api/v1/parcels/destination/<int:parcelId>", methods=['PUT'])
@jwt_required
def update_destination(parcelId):
    userid = get_jwt_identity()
    parcel = Parcel()
    user = User()
    editor = user.get_user_by_id(userid)['role']
    if not editor:
        return jsonify({"message":"You are not a registered Admin of the system"}),401
    if editor != 'admin':
        return jsonify({"message": "You can only update the present location if you are an admin"}), 400
    request_data = request.get_json(force=True)
    destination = request_data['destination']
    letters = re.compile('[A-Za-z]')
    if not destination or destination.isspace() or not letters.match(destination):
        jsonify({"message":"destination must be a non empty string"}),400
    
    parcel.update_destination(parcelId, destination)
    parcel=parcel.get_single_parcel(parcelId)
    return jsonify({"message": "Your destination has been updated ","updated parcel":parcel}), 200


@app.route("/api/v1/parcels/<int:parcelId>", methods=['DELETE'])
@jwt_required
def delete_parcel(parcelId):
    userid = get_jwt_identity()
    user = User()
    parcel = Parcel()
    editor = user.get_user_by_id(userid)['role']
    if editor == 'admin':
        parcel.delete_parcel(parcelId)
        return jsonify({"message": "Your parcel has been deleted"}), 200
    return jsonify({"message": "only administrators can delete parcels"}), 400
