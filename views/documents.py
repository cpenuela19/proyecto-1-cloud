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

        if not file or file.filename == "":
            return {"message": "No se envió ningún archivo"}, 400

        if not allowed_file(file.filename):
            return {"message": "Formato de archivo no permitido"}, 400

        response = DocumentService.upload_document(user_id, file)
        return response
