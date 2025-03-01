from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models.database import db
from models.vector_db import vector_db  # FAISS en memoria
from models.chroma_db import chroma_db  # Nueva base de datos en Chroma
from config import Config  # Configuración modular

# Importar Vistas (Endpoints)
from views.auth import SignUp, LogIn
from views.documents import UploadDocument, ListDocuments, DownloadDocument, DeleteDocument
from views.processing import ProcessDocument, SearchSimilarDocuments
from views.question import AskQuestion  # Nuevo endpoint para preguntas

app = Flask(__name__)
app.config.from_object(Config)  # Cargar configuración desde `config.py`

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Crear la API y registrar los endpoints
api = Api(app)
api.add_resource(SignUp, "/signup")
api.add_resource(LogIn, "/login")
api.add_resource(UploadDocument, "/upload")
api.add_resource(ListDocuments, "/documents")
api.add_resource(DownloadDocument, "/download/<int:document_id>")
api.add_resource(DeleteDocument, "/delete/<int:document_id>")
api.add_resource(ProcessDocument, "/process")
api.add_resource(SearchSimilarDocuments, "/search")
api.add_resource(AskQuestion, "/ask")  # 🔥 Nuevo endpoint de preguntas

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear tablas solo si no existen
        print("🔥 FAISS VectorDB Inicializado")
        print("🔥 Chroma VectorDB Inicializado")
    app.run(debug=True)
