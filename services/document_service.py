import os
from flask import jsonify, send_file
from models.database import db
from models.document import Document, DocumentSchema
from models.vector_db import vector_db  # FAISS
from services.embedding_service import EmbeddingService  # Generación de embeddings

document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Asegurar que la carpeta exista

class DocumentService:
    @staticmethod
    def upload_document(user_id, file):
        """Guarda un documento y lo procesa con IA"""
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        new_document = Document(user_id=user_id, filename=filename, file_url=file_path)
        db.session.add(new_document)
        db.session.commit()

        return document_schema.dump(new_document), 201

    @staticmethod
    def list_documents(user_id):
        """Lista los documentos de un usuario"""
        documents = Document.query.filter_by(user_id=user_id).all()
        return documents_schema.dump(documents), 200

    @staticmethod
    def download_document(document_id):
        """Descarga un documento dado su ID"""
        document = Document.query.get(document_id)
        if not document:
            return {"message": "Documento no encontrado"}, 404
        return send_file(document.file_url, as_attachment=True)

    @staticmethod
    def delete_document(document_id):
        """Elimina un documento de la base de datos"""
        document = Document.query.get(document_id)
        if not document:
            return {"message": "Documento no encontrado"}, 404

        os.remove(document.file_url)  # Borrar archivo físico
        db.session.delete(document)
        db.session.commit()

        return {"message": "Documento eliminado con éxito"}, 200

    @staticmethod
    def process_document(document_id, text):
        """Genera embeddings y los guarda en FAISS"""
        embedding_vector = EmbeddingService.generate_embedding(text)
        vector_db.add_embeddings([embedding_vector])

        return {"message": "Documento procesado con IA", "embedding": embedding_vector}, 201
