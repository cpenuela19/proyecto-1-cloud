from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Solo crea las tablas si no existen
