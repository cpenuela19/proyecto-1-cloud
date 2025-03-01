from models.database import db
from models.userQuery import UserQuery, UserQuerySchema
from models.vector_db import vector_db
from services.embedding_service import EmbeddingService

query_schema = UserQuerySchema(many=True)

class QueryService:
    @staticmethod
    def get_user_queries(user_id):
        """Devuelve el historial de consultas de un usuario"""
        queries = UserQuery.query.filter_by(user_id=user_id).all()
        return query_schema.dump(queries), 200

    @staticmethod
    def search_similar(query_text):
        """Busca documentos similares usando FAISS"""
        query_vector = EmbeddingService.generate_embedding(query_text)
        distances, indices = vector_db.search(query_vector, k=5)

        return {"similar_documents": indices.tolist(), "distances": distances.tolist()}, 200
