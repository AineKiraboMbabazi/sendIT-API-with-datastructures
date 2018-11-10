
from flask import  request, jsonify
from app import app
from app.models import parcels, Parcels
from app.models import users, Users

Parcels = Parcels()
Users = Users()


@app.route("/index")
@app.route("/")
def index():
    return jsonify([{"message": "Welcome to sendIT API"}]), 200


@app.route("/api/v1/parcels", methods=['POST'])
def create_parcel_order():
    newparcel = Parcels.create_parcel()
    return jsonify(newparcel), 201


@app.route("/api/v1/users", methods=['POST'])
def add_new_user():
    newuser = Users.create_user()
    return jsonify(newuser), 201


@app.route("/api/v1/users", methods=['GET'])
def fetch_all_users():
    all_users = Users.get_users()
    return jsonify(all_users), 200


@app.route("/api/v1/parcels", methods=['GET'])
def fetch_all_parcels():
    all_parcels = Parcels.get_parcels()
    return jsonify(all_parcels), 200


@app.route("/api/v1/parcels/<int:parcelId>", methods=['GET'])
def fetch_specific_parcel(parcelId):
    single_parcel = Parcels.get_specific_parcel(parcelId)
    return jsonify(single_parcel), 200


@app.route("/api/v1/users/<int:userId>/parcels", methods=['GET'])
def fetch_all_parcels_by_user(userId):
    parcels_by_user = Parcels.get_parcels_by_specific_user(userId)
    return jsonify(parcels_by_user), 200


# @app.route("/api/v1/parcels/<int:parcelId>", methods=['PUT'])
# def cancel_specific_parcel(parcelId):
#     cancel_order = Parcels.delete_specific_parcel(parcelId)
#     return jsonify(cancel_order), 204
