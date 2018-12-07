import re
from flask_jwt_extended import (JWTManager,get_jwt_identity,jwt_required)
import datetime
from flask import request, jsonify
from sendapi.models.user import User
from sendapi.models.parcel import Parcel
from config import app_config
from sendapi import app
from validations import Validator


@app.route("/api/v1/users", methods=['GET'])
@jwt_required
def fetch_all_users():
    """
        Function fetch all users
        :return success message:
    """
    current_user = get_jwt_identity()
    user = User()
    find_user_with_id = (user.get_user_by_id(current_user))
    if not find_user_with_id:
        return jsonify({"message": "No users found"}), 404
    if find_user_with_id['role'] == 'admin':
        return jsonify(user.get_users()), 200
    return jsonify({"message": "Only Admin can view all users"}), 401


@app.route("/api/v1/users/<int:userId>/parcels", methods=['GET'])
@jwt_required
def fetch_all_parcels_by_user(userId):
    """
        Function fetch all parcels by user
        :param userId:
        :return success message:
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "You are not logged in"}), 401
    if user_id != userId:
        return jsonify({"message": "you can only view the parcels you have created"}), 401
    parcel = Parcel()
    parcels = parcel.fetch_parcels_by_user(userId)
    if not parcels:
        return jsonify({"message": "User has not yet created any orders", 'status_code': 404}), 404
    return jsonify({"parcels": parcels, 'status_code': 200}), 200


@app.route("/api/v1/users/<int:userId>", methods=['DELETE'])
@jwt_required
def delete_user(userId):
    """
        Function delete user
        :param userId:
        :return success message:
    """
    user_id = get_jwt_identity()
    user = User()
    get_user_by_id = (user.get_user_by_id(user_id))
    if not get_user_by_id:
        return jsonify({"message": "You are not a system user"}), 401
    if get_user_by_id['role'] == 'admin':
        user.delete_user(userId)
        return jsonify({"message": "user has been deleted"}), 200
    return jsonify({"message": "Only admin can delete users"}), 400


@app.route("/api/v1/users/<int:userId>", methods=['GET'])
@jwt_required
def get_user(userId):
    """
        Function get user
        :param userId:
        :return user details:
    """
    user_id = get_jwt_identity()
    if user_id != userId:
        return jsonify({"message": "You can only view your details"})
    user = User()
    get_user_by_id = (user.get_user_by_id(user_id))
    if not get_user_by_id:
        return jsonify({"message": "You are not a registered user"}), 401
    if get_user_by_id['role'] == 'admin' and user_id == userId:
        return jsonify(get_user_by_id), 200
    return jsonify({"message": "only admin can access user details"}), 401
