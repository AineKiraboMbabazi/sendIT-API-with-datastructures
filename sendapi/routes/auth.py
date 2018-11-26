import re
from flask_jwt_extended import (JWTManager, create_access_token)
import datetime
from flask import request, jsonify
from sendapi.models.user import User
from config import app_config
from sendapi import app
from validations import Validator

import os


@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    """
        Function creates user
        :return success message:
    """
    request_data = request.get_json()
    print(request_data)
    if len(request_data.keys()) != 2:
        return jsonify({"message": "some fields are missing"}), 400
    email = request_data['email']
    password = request_data['password']
    signup_validator = Validator()
    if not signup_validator.validate_email(email):
        return jsonify({"message": "You entered an invalid email or the\
                         email is missing"}), 400

    if not signup_validator.validate_password(password):
        return jsonify({"message": "You entered an invalid password or \
                        password is missing"}), 400
    if email == 'admin@admin.com':
        role = 'admin'
    else:
        role = 'user'
    user = User()
    if user.get_user_by_email(email):
        return jsonify({"message": "Email already exists"}), 400
    user.create_user(request_data['email'], request_data['password'], role)
    user.get_user_by_email(email)
    return jsonify({"message": "user created successfully"}), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
        Function login user
        :return success message, authentication token, userId:
    """
    request_data = request.get_json(force=True)
    if len(request_data.keys()) != 2:
        return jsonify({"message": "some fields are missing"}), 401
    email = request_data['email']
    password = request_data['password']
    login_validation = Validator()
    if not login_validation.validate_email(email):
        return jsonify({"message": "You entered an invalid email or the\
                         email is missing"}), 401

    if not login_validation.validate_password(password):
        return jsonify({"message": "You entered an invalid password,\
                         password should be atleast 8 characters long"}), 401

    user = User()
    check_user = user.get_user_by_email(email)
    if check_user:
        expires = datetime.timedelta(days=1)
        auth_token = create_access_token(identity=check_user[0],
                                         expires_delta=expires)
        return jsonify({
            'message': 'login successful',
            'auth_token': auth_token}), 200

    return jsonify({"message": "You are not a system user"}), 401
