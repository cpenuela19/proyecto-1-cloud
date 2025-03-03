import os
from flask import send_file, jsonify
from models.database import db
from models.document import Document, DocumentSchema
from models.chroma_db import chroma_db  # ChromaDB para embeddings

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
        print(f"📌 Procesando documento {document_id}...")

        try:
            response = chroma_db.add_embedding(document_id, text)
            print(f"📌 Respuesta completa de ChromaDB: {response}")
        except Exception as e:
            print(f"🔥 Error inesperado al llamar a add_embedding: {e}")
            return jsonify({"message": f"Error inesperado: {e}"}), 500

        if response is None:
            print("❌ ChromaDB devolvió None.")
            return jsonify({"message": "Error: ChromaDB devolvió None"}), 500

        if not isinstance(response, dict):
            print(f"❌ ChromaDB devolvió un tipo inesperado: {type(response)}")
            return jsonify({"message": "Error: Respuesta inesperada de ChromaDB"}), 500

        if "message" not in response:
            print("❌ ChromaDB no devolvió un mensaje válido.")
            return jsonify({"message": "Error: Mensaje no encontrado en la respuesta"}), 500

        # Aceptamos tanto "Documento almacenado" como "Documento ya indexado"
        if response["message"] in ["Documento almacenado en ChromaDB", "Documento ya indexado en ChromaDB"]:
            print("✅ Documento procesado correctamente.")
            return jsonify({"message": "Documento procesado correctamente"}), 200

        print("❌ No se pudo generar el embedding.")
        return jsonify({"message": "No se pudo generar el embedding"}), 500


    @staticmethod
    def search_similar(query_text):
        """Busca documentos similares en ChromaDB y devuelve detalles con score y filename."""
        try:
            results = chroma_db.search(query_text, k=10, with_score=True)

            # Filtrar resultados que tengan document_id válido
            similar_documents = []
            for doc, score in results:
                document_id = doc.metadata.get("document_id")
                document = Document.query.get(document_id) if document_id else None

                if document:
                    similar_documents.append({
                        "id": document_id,
                        "score": round(score, 3) if score else "N/A",
                        "filename": document.filename
                    })

            if not similar_documents:
                return {"message": "No se encontraron documentos relevantes"}, 404

            return {"similar_documents": similar_documents}, 200

        except Exception as e:
            return {"message": f"Error en la búsqueda semántica: {str(e)}"}, 500

    @staticmethod
    def list_indexed_documents():
        """Devuelve una lista de documentos almacenados en ChromaDB"""
        indexed_docs = chroma_db.list_documents()
        return {"indexed_documents": indexed_docs}, 200
