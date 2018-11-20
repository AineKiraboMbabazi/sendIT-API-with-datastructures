import re
from flask_jwt_extended import get_jwt_identity,create_access_token, jwt_required
import datetime
from flask import request, jsonify
from sendapi.models.user import User
from config import app_config
from sendapi import app
from validations import validate_email,validate_password

import os

@jwt_required
@app.route("/api/v1/users", methods=['GET'])
def fetch_all_users():
    current_user=get_jwt_identity()
    print (current_user)
    user=User()
    check_id=(user.get_user_by_id(current_user))
    print(check_id)
    if check_id:
        role=check_id['role']
        if role=='admin':
            return user .get_users()
        return jsonify({"message":"Only Admin can view all users"}),400
    return jsonify({"message":"You are not a registered user"}),400
    
# @jwt_required
# @app.route("/api/v1/users/<int:userId>/parcels", methods=['GET'])
# def fetch_all_parcels_by_user(userId):
#     user_id=get_jwt_identity()
#     if user_id != userId:
#         return jsonify({"message":"you can only view the parcels you have created"}),400
#     parcels=user.get_parcels_by_specific_user(user_id)
#     return parcels
@jwt_required
@app.route("/api/v1/users/<int:userId>", methods=['DELETE'])
def delete_user(userId):
    user_id=get_jwt_identity()
    if user_id=='admin':  
        user=User()
        user.delete_user(userId)
    return jsonify({"message":"Only admin can delete users"}),400
