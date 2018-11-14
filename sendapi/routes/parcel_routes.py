
from flask import request, jsonify
from sendapi import app
from sendapi.models.user_model import users, User
from sendapi.models.parcel_model import parcels, Parcel
from sendapi.controllers.controller import AppController 


@app.route("/index")
@app.route("/")
def index():
    return jsonify({"message": "Welcome to sendIT API"}), 200


@app.route("/api/v1/parcels", methods=['POST'])
def create_parcel_order():
    return AppController().create_parcel()


@app.route("/api/v1/parcels", methods=['GET'])
def fetch_all_parcels():
    return AppController().get_parcels()


@app.route("/api/v1/parcels/<int:parcelId>", methods=['GET'])
def fetch_specific_parcel(parcelId):
    return AppController().get_specific_parcel(parcelId)


@app.route("/api/v1/parcels/<int:parcelId>", methods=['PUT'])
def cancel_specific_parcel(parcelId):
    return AppController().cancel_specific_parcel(parcelId)


@app.route("/api/v1/parcels/<int:parcelId>", methods=['DELETE'])
def delete_parcel(parcelId):
    return AppController().delete_parcel(parcelId)
