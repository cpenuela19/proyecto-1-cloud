from models.database import db
from models.userQuery import UserQuery, UserQuerySchema
from models.chroma_db import chroma_db

query_schema = UserQuerySchema(many=True)

class QueryService:
    @staticmethod
    def get_user_queries(user_id):
        """Devuelve el historial de consultas de un usuario"""
        queries = UserQuery.query.filter_by(user_id=user_id).all()
        return query_schema.dump(queries), 200

    @staticmethod
    def search_similar(query_text):
        """Busca documentos similares usando ChromaDB"""
        results = chroma_db.search(query_text, k=5)
        return {"similar_documents": results}, 200
