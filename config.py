import os

class Config:
    # 🔹 Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-XD")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-clave-secreta")

    # 🔹 Base de datos relacional (SQLite persistente en disco)
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # Base de datos persistente
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔹 Configuración de ChromaDB
    CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")

    # 🔹 Redis (para futuras tareas en segundo plano con Celery)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
