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
            return {"message": "ChromaDB no está disponible"}

        doc = Document(page_content=text, metadata={"document_id": document_id})
        self.vector_store.add_documents([doc])
        return {"message": "Embedding almacenado en Chroma"}

    def search(self, query, k=5):
        """Realiza una búsqueda semántica"""
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)

# Instancia global de ChromaDB
chroma_db = ChromaDB()
