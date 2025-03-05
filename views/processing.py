from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.document_service import DocumentService

class ProcessDocument(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        document_text = data.get("text")
        document_id = data.get("document_id")

        if not document_text or not document_id:
            return {"message": "Texto y document_id son obligatorios"}, 400

        response = DocumentService.process_document(document_id, document_text)

        if "embedding" not in response:
            return {"message": "No se pudo generar el embedding"}, 500

        return response

class SearchSimilarDocuments(Resource):
    @jwt_required()
    def post(self):
        query_text = request.json.get("query")
        if not query_text:
            return {"message": "Se requiere una consulta"}, 400

        response = DocumentService.search_similar(query_text)
        return response