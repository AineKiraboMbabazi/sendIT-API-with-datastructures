# from flask import request, jsonify
# from sendapi import app
# from sendapi.models.user import users, User
# from sendapi.models.parcel import parcels, Parcel
# from sendapi.controllers.user  import UserController


# @app.route("/api/v1/users", methods=['POST'])
# def add_new_user():
#     return UserController() .create_user()


# @app.route("/api/v1/users", methods=['GET'])
# def fetch_all_users():
#     return UserController() .get_users()


# @app.route("/api/v1/users/<int:userId>/parcels", methods=['GET'])
# def fetch_all_parcels_by_user(userId):
#     return UserController().get_parcels_by_specific_user(userId)


# @app.route("/api/v1/users/<int:userId>", methods=['DELETE'])
# def delete_user(userId):
#     return UserController().delete_user(userId)
