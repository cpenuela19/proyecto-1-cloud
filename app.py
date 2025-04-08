from flask import Flask  # ❌ ya no usamos render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models.database import db, setup_db
from models.chroma_db import chroma_db
from config import Config

# Importar Vistas (Endpoints)
from views.auth import SignUp, LogIn
from views.documents import UploadDocument, ListDocuments, DownloadDocument, DeleteDocument, ListIndexedDocuments
from views.processing import ProcessDocument, SearchSimilarDocuments
from views.question import AskQuestion

import time
import requests

# Inicialización del servidor Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos
setup_db(app)

# Inicializar extensiones
jwt = JWTManager(app)
CORS(app)

# Registrar endpoints
api = Api(app)
api.add_resource(SignUp, "/signup")
api.add_resource(LogIn, "/login")
api.add_resource(UploadDocument, "/upload")
api.add_resource(ListDocuments, "/documents")
api.add_resource(DownloadDocument, "/download/<int:document_id>")
api.add_resource(DeleteDocument, "/delete/<int:document_id>")
api.add_resource(ProcessDocument, "/process")
api.add_resource(SearchSimilarDocuments, "/search")
api.add_resource(AskQuestion, "/ask")
api.add_resource(ListIndexedDocuments, "/list_indexed")

# (Opcional) Esperar a Ollama en caso de que esté en contenedor
def wait_for_ollama(url="http://ollama:11434", retries=10, delay=3):
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Ollama está listo.")
                return True
        except:
            print(f"⏳ Esperando a Ollama... intento {i+1}/{retries}")
            time.sleep(delay)
    raise RuntimeError("❌ No se pudo conectar a Ollama.")

# Ejecutar app
if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            print("✅ Base de datos SQL inicializada correctamente.")
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos SQL: {e}")

        print("✅ Chroma VectorDB Inicializado")

    app.run(host="0.0.0.0", port=5000, debug=True)
