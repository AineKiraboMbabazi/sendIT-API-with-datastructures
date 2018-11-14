import re

from flask import jsonify, make_response

class Validator:
    def validate_id(self, id):
        if not id:
            return jsonify({"message":"The Id is required"}),400
        if id<0:
            return jsonify({"message":"The Id must be a positive integer"}),400
        if not isinstance(id,int):
            return jsonify({"message":"The Id must be an integer"}),400

    def validate_password(self,password):
        if not password or password.isspace():
            return jsonify({"message":"The password is required"}),400

    def validate_string(self, anystring):
        if not anystring or anystring.isspace():
            return jsonify({"message":"One of the string inputs is missing"}),400
        letters= re.compile('[A-Za-z]')
        if not letters.match(anystring):
            return jsonify({"message":"The field input must contain letters"}),400

    def validate_email(self,email):
        expression=re.compile(r"(^[a-zA-Z0-9-.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not expression.match(email):
            return jsonify({"message":"You entered an invalid email"}),400