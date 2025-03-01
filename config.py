import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-clave-secreta")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Eliminamos PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
