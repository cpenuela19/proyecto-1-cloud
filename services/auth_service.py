from flask_jwt_extended import create_access_token
from models.database import db
from models.user import User, UserSchema

user_schema = UserSchema()

class AuthService:
    @staticmethod
    def register_user(data):
        """Registra un nuevo usuario en la base de datos"""
        if User.query.filter_by(username=data["username"]).first():
            return {"message": "El nombre de usuario ya está en uso"}, 409

        if User.query.filter_by(email=data["email"]).first():
            return {"message": "El correo ya está registrado"}, 409

        new_user = User(username=data["username"], email=data["email"])
        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201

    @staticmethod
    def login_user(data):
        """Autentica un usuario y devuelve un token JWT"""
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return {"message": "Credenciales incorrectas"}, 401

        access_token = create_access_token(identity=user.id)

        return {
            "message": "Inicio de sesión exitoso",
            "token": access_token,
            "user": user_schema.dump(user),
        }, 200
