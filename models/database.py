from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    """Inicializa la base de datos SQLAlchemy"""
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()  # Solo crea las tablas si no existen
        print("✅ Base de datos SQL inicializada correctamente.")
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
