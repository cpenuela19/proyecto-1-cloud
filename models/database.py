from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    """Inicializa la base de datos y crea las tablas si no existen."""
    db.init_app(app)
    with app.app_context():
        db.create_all()  # ✅ Asegura que las tablas sean creadas
        print("✅ Base de datos inicializada correctamente.")
