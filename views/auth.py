from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.database import db
from models.user import User, UserSchema
from services.auth_service import AuthService  # Nueva capa de servicio

user_schema = UserSchema()

class SignUp(Resource):
    def post(self):
        data = request.json
        if not data.get("username") or not data.get("email") or not data.get("password"):
            return {"message": "Todos los campos son obligatorios"}, 400

        response = AuthService.register_user(data)
        return response

class LogIn(Resource):
    def post(self):
        data = request.json
        response = AuthService.login_user(data)
        return response
