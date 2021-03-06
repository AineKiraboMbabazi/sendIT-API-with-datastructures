import re
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
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
    if len(request_data.keys()) != 3:
        return jsonify({"message": "Some fields are missing"}), 400
    userid = get_jwt_identity()
    if not userid:
        return jsonify({'msg': 'Missing Authorization Header'}), 401
    request_data = request.get_json(force=True)
    userId = userid
    status = 'pending'
    destination = request_data['destination']
    description = request_data['description']
    pickup = request_data['pickup']
    present_location = pickup
    creation_date = datetime.date.today().strftime('%Y-%m-%d')
    validate_input = Validator()
    if not (validate_input.validate_string_input(destination)):
        return jsonify({"message": "destination Field should\
                         contain strings"}), 400
    if not (validate_input.validate_string_input(description)):
        return jsonify({"message": "destination Field should\
                         contain strings"}), 400
    if not (validate_input.validate_string_input(pickup)):
        return jsonify({"message": "pickup Field should contain strings"}), 400
    parcel = Parcel()
    parcel.create_parcel(userId, creation_date, status, destination,
                         pickup, present_location, description)

    return jsonify({"message": "Your parcel order has been created"}), 201


"""
    Endpoint for fetching all parcels
"""


@app.route("/api/v1/parcels", methods=['GET'])
@jwt_required
def fetch_all_parcels():
    """
        Function fetch all parcels
        :return parcels list:
    """
    parcel = Parcel()
    user = User()
    userid = get_jwt_identity()
    if not userid:
        return jsonify({'msg': 'Missing Authorization Header'}), 401
    get_user = user.get_user_by_id(userid)
    if not get_user:
        return jsonify({"message": " No user with that id"}), 404
    if get_user['role'] == 'admin':
        parcel = Parcel()
        parcels = parcel.get_all_parcels()
        if parcels == []:
            return jsonify({"message": "No parcels found"}), 404
        return jsonify({'parcels': parcels}), 200

    return jsonify({"message": "Only administrators can view parcels"}), 400


@app.route("/api/v1/parcels/<int:parcelId>", methods=['GET'])
@jwt_required
def fetch_specific_parcel(parcelId):
    """
        Function fetch specific parcel
        :return parcel:
    """
    userId = get_jwt_identity()
    if not userId:
        return({"message": "Missing authentication header"}), 401
    parcel = Parcel()
    single_parcel = parcel.get_single_parcel(parcelId)
    if not single_parcel:
        return jsonify({"message": "Parcel with that id doesnot exist"}), 404
    return jsonify({'parcel': single_parcel}), 200


@app.route("/api/v1/parcels/<int:parcelId>", methods=['PUT'])
@jwt_required
def cancel_specific_parcel(parcelId):
    """
        Function cancel parcel
        :return success message:
    """
    userid = get_jwt_identity()
    parcel = Parcel()
    Parcel_to_edit = parcel.get_single_parcel(parcelId)
    if not Parcel_to_edit:
        return jsonify({"message": " parcel doesnot exist"}), 404
    parcel_owner_id = Parcel_to_edit['userid']
    if parcel_owner_id != userid:
        return jsonify({"message": "You can only cancel an \
                        order you created"}), 400
    parcel_status = Parcel_to_edit['status']
    if parcel_status == 'Cancelled' or parcel_status == 'Delivered':
        return jsonify({"message": "Cant update a cancelled or deivered \
                        order "}), 400
    parcel.cancel_parcel(parcelId)
    return jsonify({"message": "Your parcel order has been cancelled"}), 200


@app.route("/api/v1/parcels/present_location/<int:parcelId>", methods=['PUT'])
@jwt_required
def update_present_location(parcelId):
    """
        Function to update present location
        :return success message:
    """
    request_data = request.get_json(force=True)
    newlocation = request_data['new location']
    if not get_jwt_identity():
        return jsonify({"message": "Some fields are missing"}), 400
    if len(request_data.keys()) != 1:
        return jsonify({"message": "Some fields are missing"}), 400
    validate_input = Validator().validate_string_input(newlocation)
    if not validate_input:
        return jsonify({"message": "The new location should be a none\
                         empty string"}), 400
    userid = get_jwt_identity()
    parcel = Parcel()
    user = User()
    editor = user.get_user_by_id(userid)['role']
    if editor != 'admin':
        return jsonify({"message": "You can only update the present location\
                         if you are an admin"}), 400
    Parcel_to_edit = Parcel().get_single_parcel(parcelId)
    if not Parcel_to_edit or Parcel_to_edit['status'] == 'Cancelled':
        return ({"message": "The parcel you are tring to edit doesnt\
                 exist"}), 400
    if Parcel_to_edit['present_location'] == newlocation:
        return jsonify({"message": "Present location is upto date"}), 400
    if newlocation == Parcel_to_edit['destination']:
        Parcel_to_edit['status'] = 'Delivered'
        return jsonify({"message": "order delivered"}), 200
    parcel.update_present_location(parcelId, newlocation)
    parcel = parcel.get_single_parcel(parcelId)
    return jsonify({"message": "Your location has been updated ",
                    "updated parcel": parcel}), 200


@app.route("/api/v1/parcels/destination/<int:parcelId>", methods=['PUT'])
@jwt_required
def update_destination(parcelId):
    """
        Function update destination
        :return success message:
    """
    userid = get_jwt_identity()
    parcel = Parcel()
    user = User()
    if not userid:
        return jsonify({"message": "Unauthorised access"}), 401

    editor = user.get_user_by_id(userid)['role']
    parcel = parcel.get_single_parcel(parcelId)

    if not parcel or parcel['status'] == 'Cancelled':
        return jsonify({"message": "The parcel you are editing doesnt\
                         exist"}), 404
    if not editor:
        return jsonify({"message": "You are not a registered user of the \
                        system"}), 401
    if editor != 'user' or parcel['userid'] != userid:
        return jsonify({"message": "You can only update destination of the\
                         parcel you have created "}), 400
    request_data = request.get_json(force=True)
    if len(request_data.keys()) != 1:
        return jsonify({"message": "Some fields are missing"}), 400
    destination = request_data['destination']
    validate_destination = Validator().validate_string_input(destination)
    if not validate_destination:
        jsonify({"message": "destination must be a non empty string"}), 400
    Parcel().update_destination(parcelId, destination)
    parcel = Parcel().get_single_parcel(parcelId)
    return jsonify({"message": "Your destination has been updated ",
                    "updated parcel": parcel}), 200


@app.route("/api/v1/parcels/<int:parcelId>", methods=['DELETE'])
@jwt_required
def delete_parcel(parcelId):
    """
        Function delete
        :return success message:
    """
    userid = get_jwt_identity()
    if not userid:
        return jsonify({"message": "unauthorised access"}), 401
    user = User()
    parcel = Parcel()
    parcel_to_delete = parcel.get_single_parcel(parcelId)
    if not parcel_to_delete or parcel_to_delete['status'] == 'Deleted':
        return jsonify({"message": "Order doesnt exist"}), 400
    editor = user.get_user_by_id(userid)['role']
    if editor == 'admin':
        parcel.delete_parcel(parcelId)
        return jsonify({"message": "Your parcel has been deleted"}), 200
    return jsonify({"message": "only administrators can delete parcels"}), 400
