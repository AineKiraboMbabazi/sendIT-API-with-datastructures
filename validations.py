from flask import jsonify,request
import re

def validate_email(email):
    expression = re.compile(
        r"(^[a-zA-Z0-9-.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not expression.match(email) or email.isspace():
        print('i get here')
        return True

def  validate_password(password):
    if not password or password.isspace():
        return jsonify({"message": "You entered an invalid password or password is missing"}), 400

    