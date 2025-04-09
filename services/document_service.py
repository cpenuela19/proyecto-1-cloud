import os
from flask import send_file, jsonify
from celery import Celery
from models.database import db
from models.document import Document, DocumentSchema

document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure Celery
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
celery_app = Celery('tasks', broker=f'redis://{redis_host}:{redis_port}/0')

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

        os.remove(document.file_url)
        db.session.delete(document)
        db.session.commit()

        return {"message": "Documento eliminado con éxito"}, 200

    @staticmethod
    def process_document(document_id, text):
        """Genera embeddings de forma asíncrona y los guarda en ChromaDB"""
        print(f"Enviando documento {document_id} para procesamiento asíncrono...")

        # Enviar tarea al worker
        task = celery_app.send_task(
            'tasks.generate_embeddings',
            args=[document_id, text],
            kwargs={"chroma_path": os.getenv("CHROMA_PATH", "chroma_db")}
        )

        return jsonify({
            "message": "Documento enviado para procesamiento",
            "task_id": task.id
        }), 202  # 202 Accepted

    @staticmethod
    def search_similar(query_text):
        """Busca documentos similares en ChromaDB de forma asíncrona"""
        task = celery_app.send_task(
            'tasks.search_documents',
            args=[query_text],
            kwargs={"k": 10, "chroma_path": os.getenv("CHROMA_PATH", "chroma_db")}
        )
        
        return jsonify({
            "message": "Búsqueda en proceso",
            "task_id": task.id
        }), 202

    @staticmethod
    def list_indexed_documents():
        """Devuelve una lista de documentos almacenados en ChromaDB"""
        # Necesita ser implementado en el worker
        task = celery_app.send_task('tasks.list_documents')
        return jsonify({
            "message": "Obteniendo documentos indexados",
            "task_id": task.id
        }), 202