from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.question_service import QuestionService

class AskQuestion(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        question = data.get("question")
        collection = data.get("collection", "documentos")

        if not question:
            return {"message": "Debe proporcionar una pregunta"}, 400

        response = QuestionService.answer_question({"question": question, "collection": collection})
        return jsonify(response)
