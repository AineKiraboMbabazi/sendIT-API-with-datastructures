import datetime
import re

from flask import jsonify, request
from sendapi.models.user_model import User, users
from sendapi.models.parcel_model import parcels, Parcel


class ParcelController:

    """Function to create a parcel"""

    def create_parcel(self):
        # users = users_list()
        request_data = request.get_json(force=True)
        userId = request_data['userId']
        status = request_data['status']
        pickup = request_data['pickup']
        destination = request_data['destination']

        """ validate id"""
        if not userId:
            return jsonify({"message": "The Id is required"}), 400
        if userId < 0:
            return jsonify({"message": "The Id must be a positive integer"}), 400
        if not isinstance(userId, int):
            return jsonify({"message": "The Id must be an integer"}), 400

        """ validate status, pickup and destination """
        data = [status, pickup, destination]
        for item in data:
            if not item or item.isspace():
                return jsonify({"message": "one parameter is missing"}), 400
            letters = re.compile('[A-Za-z]')
            if not letters.match(item):
                return jsonify({item: "must contain letters"}), 400

        parcel = Parcel(userId, status, pickup, destination).to_dictionary()
        for user in users:
            if user['userId'] == userId:
                parcels.append(parcel)
                return jsonify(parcel), 201

            return jsonify({"message": "The user id that you have entered doesnot  exist"}), 200

    """ Function to fetch all parcels"""

    def get_parcels(self):
        if len(parcels) > 0:
            return jsonify(parcels), 200
        return jsonify({"message": "No parcels have been found"}), 200

    """Function to fetch a particular parcel"""

    def get_specific_parcel(self, parcelId):
        """ validate id"""
        if not parcelId:
            return jsonify({"message": "The Id is required"}), 400
        if parcelId < 0:
            return jsonify({"message": "The Id must be a positive integer"}), 400
        if not isinstance(parcelId, int):
            return jsonify({"message": "The Id must be an integer"}), 400
        
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                return jsonify(parcel), 200
        return jsonify({"message": "The parcel with that id doesnot exist"}), 200

    """Function to cancel an parcel"""

    def cancel_specific_parcel(self, parcelId):
        """ validate id"""
        if not parcelId:
            return jsonify({"message": "The Id is required"}), 400
        if parcelId < 0:
            return jsonify({"message": "The Id must be a positive integer"}), 400
        if not isinstance(parcelId, int):
            return jsonify({"message": "The Id must be an integer"}), 400
        
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcel['status'] = 'canceled'
                return jsonify({"message": "parcel delivery order has been canceled"}, parcel), 200
        return jsonify({"message": "The order you are trying to cancel doesnot exist"}), 200

    """Function to delete a parcel"""

    def delete_parcel(self, parcelId):
        """ validate id"""
        if not parcelId:
            return jsonify({"message": "The Id is required"}), 400
        if parcelId < 0:
            return jsonify({"message": "The Id must be a positive integer"}), 400
        if not isinstance(parcelId, int):
            return jsonify({"message": "The Id must be an integer"}), 400

        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcels.remove(parcel)
                return jsonify({"message": "Your parcel has been deleted"}), 200


"""function to return parcels list"""


def return_parcels():
    return parcels


"""Function to reset parcels list"""


def reset_parcels():
    parcels.clear()
