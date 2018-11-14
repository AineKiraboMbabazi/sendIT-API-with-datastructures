import datetime

from flask import jsonify, request
from .validator import Validator
from sendapi.models.user_model import users, User
from sendapi.models.parcel_model import parcels, Parcel


class ParcelController:

    def create_parcel(self):
        request_data = request.get_json(force=True)
        userId = request_data['userId']
        status = request_data['status']
        pickup = request_data['pickup']
        destination = request_data['destination']
        parcel = Parcel(userId, status, pickup, destination).to_dictionary()
        for user in users:
            if user['userId'] == userId:
                parcels.append(parcel)
                return jsonify(parcel), 201

    def get_parcels(self):
        if len(parcels) > 0:
            return parcels
        return {"message": "No parcels have been found"}

    def get_specific_parcel(self, parcelId):
        Validator().validate_id(parcelId)
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                return jsonify(parcel), 200
        return jsonify({"message": "The parcel with that id doesnot exist"}), 200

    def get_parcels_by_specific_user(self, userId):
        Validator().validate_id(userId)
        userparcels = list()

        for parcel in parcels:
            if parcel['userId'] == userId:
                userparcels.append(parcel)
        if len(userparcels) == 0:

            return jsonify({"message": "The user with that Id has not created any parcel Delivery orders"}), 200
        return userparcels

    def cancel_specific_parcel(self, parcelId):
        Validator().validate_id(parcelId)
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcel['status'] = 'canceled'
                return jsonify({"message": "parcel delivery order has been canceled"}, parcel), 200
        return jsonify({"message": "The order you are trying to cancel doesnot exist"}), 200

    def delete_parcel(self, parcelId):
        Validator().validate_id(parcelId)
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcels.remove(parcel)
                return jsonify({"message": "Your parcel has been deleted"}), 200


def reset_parcels():
    parcels.clear()
