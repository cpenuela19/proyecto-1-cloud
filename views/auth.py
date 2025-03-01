from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from services.auth_service import AuthService  # Nueva capa de servicio

class SignUp(Resource):
    def post(self):
        try:
            data = request.json
            if not data.get("username") or not data.get("email") or not data.get("password"):
                return {"message": "Todos los campos son obligatorios"}, 400

            response = AuthService.register_user(data)
            return response
        except Exception as e:
            return {"message": f"Error en el registro: {str(e)}"}, 500

class LogIn(Resource):
    def post(self):
        try:
            data = request.json
            response = AuthService.login_user(data)
            return response
        except Exception as e:
            return {"message": f"Error en el inicio de sesión: {str(e)}"}, 500
