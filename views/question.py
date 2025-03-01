from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.question_service import QuestionService

class AskQuestion(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        question = data.get("question")
        collection = data.get("collection")

        if not question or not collection:
            return {"message": "Debe proporcionar una pregunta y la colección"}, 400

        response = QuestionService.answer_question({"question": question, "collection": collection})
        return jsonify(response)
