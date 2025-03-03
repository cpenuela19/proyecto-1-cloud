import os
from flask import jsonify, send_file
from models.database import db
from models.document import Document, DocumentSchema
from models.chroma_db import chroma_db  # Migramos de FAISS a ChromaDB

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
        """Genera embeddings y los guarda en ChromaDB"""
        response = chroma_db.add_embedding(document_id, text)

        # Depuración: Ver exactamente qué devuelve ChromaDB
        print(f"📌 Respuesta de ChromaDB: {response}")

        return response

    @staticmethod
    def search_similar(query_text):
        """Busca documentos similares en ChromaDB y devuelve detalles con score y filename."""
        try:
            # 🔹 Usamos `similarity_search_with_score()` en lugar de `similarity_search()`
            results = chroma_db.search(query_text, k=5, with_score=True)

            # Convertir los resultados en un formato JSON serializable
            similar_documents = []
            for doc, score in results:
                document_id = doc.metadata.get("document_id", "N/A")
                
                # Obtener el documento original de la base de datos (para filename)
                document = Document.query.get(document_id)
                
                similar_documents.append({
                    "id": document_id,
                    "score": round(score, 3) if score else "N/A",  # 🔹 Score de similitud redondeado
                    "filename": document.filename if document else "Desconocido"
                })

            return {"similar_documents": similar_documents}, 200

        except Exception as e:
            return {"message": f"Error en la búsqueda semántica: {str(e)}"}, 500

