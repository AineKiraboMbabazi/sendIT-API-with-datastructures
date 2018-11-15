import re
from flask import jsonify, request
from sendapi.models.user_model import users, User
from sendapi.models.parcel_model import parcels, Parcel
# from sendapi.controllers.parcel_controller import validate_id
from sendapi.controllers.parcel_controller import return_parcels

def validate_id(id):
    if not id:
        return jsonify({"message": "The Id is required"}), 400
    if id < 0:
        return jsonify({"message": "The Id must be a positive integer"}), 400
    if not isinstance(id, int):
        return jsonify({"message": "The Id must be an integer"}), 400
def validate_email(email):
    expression = re.compile(
        r"(^[a-zA-Z0-9-.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not expression.match(email):
        return jsonify({"message": "You entered an invalid email"}), 400


def validate_password(password):
    if not password or password.isspace():
        return jsonify({"message": "The password is required"}), 400


class UserController:

    def create_user(self):
        request_data = request.get_json(force=True)
        email = request_data['email']
        password = request_data['password']
        validate_email(email)
        validate_password(password)
        user = User(email, password).to_dictionary()
        users.append(user)
        return jsonify(user), 201

    def get_users(self):
        if len(users) > 0:
            return jsonify(users), 200

        return jsonify({"message": "No users have been created"}), 200

    def get_parcels_by_specific_user(self, userId):
        parcels = return_parcels()
        validate_id(userId)
        userparcels = list()

        for parcel in parcels:
            if parcel['userId'] == userId:
                userparcels.append(parcel)
        if len(userparcels) == 0:

            return jsonify({"message": "The user with that Id has not created any parcel Delivery orders"}), 200
        return userparcels


def users_list():
    return users


def reset_users():
    users.clear()


