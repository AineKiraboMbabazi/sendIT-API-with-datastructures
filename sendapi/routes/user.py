import re
# from flask_jwt_extended import (get_jwt_identity,create_access_token, jwt_required)
from flask_jwt_extended import get_jwt_identity,jwt_required
import datetime
from flask import request, jsonify
from sendapi.models.user import User
from config import app_config
from sendapi import app
from validations import validate_email,validate_password




@app.route("/api/v1/users", methods=['GET'])
@jwt_required
def fetch_all_users():
    current_user=get_jwt_identity() 
    user=User() 
    check_id=(user.get_user_by_id(current_user))
    if check_id['role'] =='admin':
        return jsonify(user.get_users()),200
    return jsonify({"message":"Only Admin can view all users"}),400
    
    
# @jwt_required
# @app.route("/api/v1/users/<int:userId>/parcels", methods=['GET'])
# def fetch_all_parcels_by_user(userId):
#     user_id=get_jwt_identity()
#     if user_id != userId:
#         return jsonify({"message":"you can only view the parcels you have created"}),400
#     parcels=user.get_parcels_by_specific_user(user_id)
#     return parcels

@app.route("/api/v1/users/<int:userId>", methods=['DELETE'])
@jwt_required
def delete_user(userId):
    user_id=get_jwt_identity()
    print(user_id)
    user=User() 
    get_user_by_id=(user.get_user_by_id(user_id))
    print(get_user_by_id)
    if get_user_by_id['role'] =='admin':
        user.delete_user(userId)
        return jsonify({"message":"user has been deleted"}),200
    return jsonify({"message":"Only admin can delete users"}),400


@app.route("/api/v1/users/<int:userId>", methods=['GET'])
@jwt_required
def get_user(userId):
    user_id=get_jwt_identity()
    if user_id!=userId:
        return jsonify({"message":"You can only view your details"})
    user=User() 
    get_user_by_id=(user.get_user_by_id(user_id))
    print(get_user_by_id)
    if get_user_by_id['role'] =='admin':
        return jsonify(get_user_by_id),400

