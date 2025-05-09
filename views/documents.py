from flask import request, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.document_service import DocumentService

ALLOWED_EXTENSIONS = {"pdf", "txt", "docx", "md"}

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadDocument(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        file = request.files.get("file")

        if not file:
            return {"message": "No se envió ningún archivo"}, 400

        response = DocumentService.upload_document(user_id, file)
        return response

class ListDocuments(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        response = DocumentService.list_documents(user_id)
        return response

class DownloadDocument(Resource):
    @jwt_required()
    def get(self, document_id):
        response = DocumentService.download_document(document_id)
        return response

class DeleteDocument(Resource):
    @jwt_required()
    def delete(self, document_id):
        response = DocumentService.delete_document(document_id)
        return response
    
class ListIndexedDocuments(Resource):
    @jwt_required()
    def get(self):
        """Devuelve una lista de documentos almacenados en ChromaDB"""
        response = DocumentService.list_indexed_documents()
        return response
