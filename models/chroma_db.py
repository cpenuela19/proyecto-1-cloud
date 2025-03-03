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
            print("✅ ChromaDB inicializado correctamente.")
        except Exception as e:
            print(f"❌ Error inicializando ChromaDB: {e}")
            self.vector_store = None

    def add_embedding(self, document_id, text):
        """Convierte texto en embeddings y lo almacena en Chroma"""
        if not self.vector_store:
            print("❌ ChromaDB no está disponible")
            return {"message": "ChromaDB no está disponible"}

        # Verificar si el documento ya está en ChromaDB para evitar duplicados
        existing_docs = self.vector_store.get(where={"document_id": document_id})
        if existing_docs:
            print(f"🔹 Documento {document_id} ya está indexado en ChromaDB.")
            return {"message": "Documento ya indexado en ChromaDB"}

        print(f"📌 Generando embeddings para documento {document_id}...")

        try:
            doc = Document(page_content=text, metadata={"document_id": document_id})
            self.vector_store.add_documents([doc])

            print(f"✅ Documento {document_id} agregado a ChromaDB")
            return {"message": "Documento almacenado en ChromaDB"}

        except Exception as e:
            print(f"❌ Error generando embeddings: {e}")
            return {"message": f"Error generando embeddings: {e}"}, 500

    def search(self, query, k=5, with_score=False):
        """Realiza una búsqueda semántica en ChromaDB y devuelve documentos con score"""
        if not self.vector_store:
            print("❌ ChromaDB no está disponible")
            return []

        try:
            if with_score:
                results = self.vector_store.similarity_search_with_score(query, k=k)
            else:
                results = self.vector_store.similarity_search(query, k=k)

            print(f"🔎 Resultados de búsqueda en ChromaDB: {results}")
            return results
        except Exception as e:
            print(f"❌ Error en la búsqueda de ChromaDB: {e}")
            return []

    def list_documents(self):
        """Lista los documentos almacenados en ChromaDB"""
        if not self.vector_store:
            return {"message": "ChromaDB no está disponible"}

        try:
            docs = self.vector_store.get()
            print(f"📄 Documentos en ChromaDB: {docs}")
            return docs
        except Exception as e:
            print(f"❌ Error al listar documentos en ChromaDB: {e}")
            return []

# Instancia global de ChromaDB
chroma_db = ChromaDB()
