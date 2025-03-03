from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

class ChromaDB:
    def __init__(self, collection_name="documentos"):
        self.chroma_path = "chroma_db"
        self.embeddings = OllamaEmbeddings(model="llama3:8b", base_url="http://localhost:11434")

        try:
            self.vector_store = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=self.embeddings,
                collection_name=collection_name
            )
        except Exception as e:
            print(f"❌ Error inicializando ChromaDB: {e}")
            self.vector_store = None

    def add_embedding(self, document_id, text):
        """Convierte texto en embeddings y lo almacena en Chroma"""
        if not self.vector_store:
            print("❌ ChromaDB no está disponible")
            return {"message": "ChromaDB no está disponible"}

        print(f"📌 Generando embeddings para documento {document_id}...")

        try:
            doc = Document(page_content=text, metadata={"document_id": document_id})
            embeddings = self.embeddings.embed_documents([text])

            print(f"✅ Embeddings generados: {embeddings[:5]}")  # Solo muestra los primeros 5

            self.vector_store.add_documents([doc])

            response = {"message": "Embedding almacenado en Chroma", "embedding": embeddings}
            print(f"📌 Respuesta final de add_embedding: {response}")
            return response

        except Exception as e:
            print(f"❌ Error generando embeddings: {e}")
            return {"message": f"Error generando embeddings: {e}"}, 500


    def search(self, query, k=5, with_score=False):
        """Realiza una búsqueda semántica en ChromaDB"""
        if not self.vector_store:
            print("❌ ChromaDB no está disponible")
            return []

        if with_score:
            results = self.vector_store.similarity_search_with_score(query, k=k)
        else:
            results = self.vector_store.similarity_search(query, k=k)

        print(f"🔎 Resultados de búsqueda: {results}")
        return results

# Instancia global de ChromaDB
chroma_db = ChromaDB()
