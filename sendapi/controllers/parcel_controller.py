import datetime
import re

from flask import jsonify, request
from sendapi.models.user_model import User, users
from sendapi.models.parcel_model import parcels, Parcel


class ParcelController:

    """Function to create a parcel"""

    def create_parcel(self):
        request_data = request.get_json(force=True)
        userId = request_data['userId']
        status = request_data['status']
        pickup = request_data['pickup']
        destination = request_data['destination']

        """ validate status, pickup and destination """

        data = [status, pickup, destination]

        for item in data:
            if not item or item.isspace():
                return jsonify({"message": "one parameter is missing"}), 400

            letters = re.compile('[A-Za-z]')
            if not letters.match(item):
                return jsonify({"message": "must contain letters"}), 400

        parcel = Parcel(userId, status, pickup, destination).to_dictionary()
        for user in users:
            if user['userId'] == userId:
                parcels.append(parcel)
                return jsonify(parcel), 201
            return jsonify({"message": "unknown userId"}), 400

    """ Function to fetch all parcels"""

    def get_parcels(self):
        if len(parcels) > 0:
            return jsonify(parcels), 200
        return jsonify({"message": "No parcels have been found"}), 200

    """Function to fetch a particular parcel"""

    def get_specific_parcel(self, parcelId):

        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                return jsonify(parcel), 200
        return jsonify({"message": "The parcel with that id doesnot exist"}), 200

    """Function to cancel an parcel"""

    def cancel_specific_parcel(self, parcelId):

        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcel['status'] = 'canceled'
                return jsonify({"message": "parcel delivery order has been canceled"}, parcel), 200
        return jsonify({"message": "The order you are trying to cancel doesnot exist"}), 200

    """Function to delete a parcel"""

    def delete_parcel(self, parcelId):

        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcels.remove(parcel)
                return jsonify({"message": "Your parcel has been deleted"}), 200
            return jsonify({"message": "The parcel your deleting doesnt exist"}), 400
 
"""Function to reset parcels list"""


def reset_parcels():
    parcels.clear()
    return parcels
