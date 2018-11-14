from flask import jsonify, request
from .validator import Validator
from sendapi.models.user_model import users, User
from sendapi.models.parcel_model import parcels, Parcel


class UserController:

    def create_user(self):
        request_data = request.get_json(force=True)
        email = request_data['email']
        password = request_data['password']
        Validator().validate_email(email)
        Validator().validate_password(password)
        user = User(email, password).to_dictionary()
        users.append(user)
        return jsonify(user), 201

    def get_users(self):
        if len(users) > 0:
            return jsonify(users), 200

        return jsonify({"message": "No users have been created"}), 200


def reset_users():
    users.clear()
