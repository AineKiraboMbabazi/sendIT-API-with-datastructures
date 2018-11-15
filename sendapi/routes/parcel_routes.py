
from flask import request, jsonify
from sendapi import app
from sendapi.models.user_model import User
from sendapi.models.parcel_model import parcels, Parcel
from sendapi.controllers.parcel_controller import ParcelController 


"""Endpoint for the index page"""
@app.route("/index")
@app.route("/")
def index():
    return jsonify({"message": "Welcome to sendIT API"}), 200

"""Endpoint for creating a parcel"""
@app.route("/api/v1/parcels", methods=['POST'])
def create_parcel_order():
    return ParcelController().create_parcel()

"""Endpoint for fetching all parcels"""
@app.route("/api/v1/parcels", methods=['GET'])
def fetch_all_parcels():
    return ParcelController().get_parcels()


@app.route("/api/v1/parcels/<int:parcelId>", methods=['GET'])
def fetch_specific_parcel(parcelId):
    return ParcelController().get_specific_parcel(parcelId)


@app.route("/api/v1/parcels/<int:parcelId>", methods=['PUT'])
def cancel_specific_parcel(parcelId):
    return ParcelController().cancel_specific_parcel(parcelId)


@app.route("/api/v1/parcels/<int:parcelId>", methods=['DELETE'])
def delete_parcel(parcelId):
    return ParcelController().delete_parcel(parcelId)
