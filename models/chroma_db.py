from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class ChromaDB:
    def __init__(self, collection_name="documentos"):
        self.chroma_path = "chroma_db"
        self.embeddings = OllamaEmbeddings(model="llama3:8b", base_url="http://localhost:11434")

        self.vector_store = Chroma(
            persist_directory=self.chroma_path,
            embedding_function=self.embeddings,
            collection_name=collection_name
        )

    def add_embeddings(self, documents):
        """Agrega documentos con embeddings a Chroma"""
        self.vector_store.add_documents(documents)

    def search(self, query, k=5):
        """Realiza una búsqueda semántica"""
        return self.vector_store.similarity_search(query, k=k)

chroma_db = ChromaDB()
