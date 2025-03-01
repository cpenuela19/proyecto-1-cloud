# In-memory FAISS vector database
import faiss
import numpy as np

class VectorDB:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # Distancia Euclidiana

    def add_embeddings(self, embeddings):
        embeddings = np.array(embeddings, dtype='float32')
        self.index.add(embeddings)

    def search(self, query_vector, k=5):
        query_vector = np.array([query_vector], dtype='float32')
        distances, indices = self.index.search(query_vector, k)
        return distances[0], indices[0]
    
# Instancia global de FAISS
vector_db = VectorDB(dimension=768)  # Ajusta el tamaño según el modelo
