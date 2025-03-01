import numpy as np
from sentence_transformers import SentenceTransformer

# Cargar modelo de embeddings (puede cambiarse según necesidades)
MODEL_NAME = "all-MiniLM-L6-v2"  # Modelo ligero y eficiente
model = SentenceTransformer(MODEL_NAME)

class EmbeddingService:
    @staticmethod
    def generate_embedding(text):
        """Genera un embedding para un texto dado"""
        embedding = model.encode(text)
        return embedding.tolist()  # Convertir a lista para compatibilidad con FAISS
