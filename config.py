import os

class Config:
    # 🔹 Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-XD")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-clave-secreta")

    # 🔹 PostgreSQL en Cloud SQL
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "rag_db")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔹 Configuración de ChromaDB
    CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
    
    # 🔹 Worker config
    WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
    WORKER_PORT = os.getenv("WORKER_PORT", "11434")
    
    # 🔹 Redis para procesamiento asíncrono
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")