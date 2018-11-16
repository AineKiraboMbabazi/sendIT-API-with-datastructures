import re
from flask import jsonify, request
from sendapi.models.user import users, User
from sendapi.models.parcel import parcels, Parcel


class UserController:

    """ 
        function creates user
    """

    def create_user(self):
        request_data = request.get_json(force=True)
        email = request_data['email']
        password = request_data['password']
        if not email or email.isspace():
            return jsonify({"message": "The email is required"}), 400

        expression = re.compile(
            r"(^[a-zA-Z0-9-.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not expression.match(email):
            return jsonify({"message": "You entered an invalid email"}), 400

        if not password or password.isspace():
            return jsonify({"message": "The password is required"}), 400

        user = User(email, password).to_dictionary()
        users.append(user)
        return jsonify(user), 201

    """
        Function retrieves all users
    """

    def get_users(self):
        if len(users) > 0:
            return jsonify(users), 200

        return jsonify({"message": "No users have been created"}), 200

    """
        function retrieves parcels by a user
    """

    def get_parcels_by_specific_user(self, userId):

        userparcels = list()

        for parcel in parcels:
            if parcel['userId'] == userId:
                userparcels.append(parcel)

        if len(userparcels) == 0:

            return jsonify({"message": "The user with that Id has not created any parcel Delivery orders"}), 200
        return jsonify(userparcels), 200

    """
        Function to delete a user
    """

    def delete_user(self, userId):

        for user in users:
            if user['userId'] == userId:
                users.remove(user)
                return jsonify({"message": "Your user has been deleted"}), 200


"""
    function to reset users
"""


def reset_users():
    users.clear()
    return users
