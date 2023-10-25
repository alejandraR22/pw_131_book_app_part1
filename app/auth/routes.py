from . import auth_blueprint as auth_bp
from flask_jwt_extended import create_access_token
from flask import request, make_response, jsonify
from ..models import User
from datetime import timedelta

@auth_bp.route("/register", methods=["POST"])
def handle_register():
    data = request.json

    if data is None:
        response = {"message": "Username and password are required to register"}
        return response, 400

    username = data.get("username")
    if username is None:
        response = {"message": "Username is required"}
        return response, 400

    password = data.get("password")
    if password is None:
        response = {"message": "Password is required"}
        return response, 400

    existing_user = User.query.filter_by(username=username).one_or_none()
    if existing_user is not None:
        response = {"message": "Username already in use"}
        return response, 400

    user = User(username=username, password=password)
    user.create()

    response = {"message": "User registered", "user": user.to_response()}
    return response, 201

@auth_bp.route("/login", methods=["POST"])
def handle_login():
    data = request.json

    if data is None:
        response = {"message": "Username and password are required to login"}
        return response, 400

    username = data.get("username")
    if username is None:
        response = {"message": "Username is required"}
        return response, 400

    password = data.get("password")
    if password is None:
        response = {"message": "Password is required"}
        return response, 400

    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        response = {"message": "User not found. Please register an account before trying to log in"}
        return response, 400

    if not user.compare_password(password):
        response = {"message": "Invalid credentials"}
        return response, 401

    auth_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

    response = jsonify({"message": "Successfully logged in", "token": auth_token, "user": user.to_response()})
    response.headers["Authorization"] = f"Bearer {auth_token}"
    return response, 200