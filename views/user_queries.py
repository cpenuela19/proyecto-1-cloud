from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.query_service import QueryService

class UserQueryHistory(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        response = QueryService.get_user_queries(user_id)

        if not response:
            return {"message": "No hay consultas registradas para este usuario"}, 404

        return response
