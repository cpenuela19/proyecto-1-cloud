from celery import Celery
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_core.documents import Document
import os

# Configure Celery
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
app = Celery('tasks', broker=f'redis://{redis_host}:{redis_port}/0')

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    collection: str

@app.task
def generate_embeddings(document_id, text, chroma_path="chroma_db", collection_name="documentos"):
    """Generate embeddings for a document and store in ChromaDB"""
    try:
        embeddings = OllamaEmbeddings(
            model="llama3:8b",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )

        vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings,
            collection_name=collection_name
        )

        doc = Document(page_content=text, metadata={"document_id": document_id})
        vector_store.add_documents([doc])
        
        return {"status": "success", "message": "Documento almacenado en ChromaDB"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.task
def search_documents(query_text, k=5, chroma_path="chroma_db", collection_name="documentos"):
    """Search for similar documents in ChromaDB"""
    try:
        embeddings = OllamaEmbeddings(
            model="llama3:8b",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )

        vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings,
            collection_name=collection_name
        )

        results = vector_store.similarity_search_with_score(query_text, k=k)
        
        processed_results = []
        for doc, score in results:
            processed_results.append({
                "document_id": doc.metadata.get("document_id"),
                "score": float(score),
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        
        return {"status": "success", "results": processed_results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.task
def answer_question(question, collection="documentos", chroma_path="chroma_db"):
    """Execute the RAG flow to answer a question"""
    try:
        # 1. Retrieve relevant documents
        embeddings = OllamaEmbeddings(
            model="llama3:8b",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )

        vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings,
            collection_name=collection
        )

        retrieved_docs = vector_store.similarity_search(question)
        
        # 2. Generate response with LLM
        llm = init_chat_model("llama3:8b", model_provider="ollama", 
                              base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
        prompt = hub.pull("rlm/rag-prompt")

        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        messages = prompt.invoke({"question": question, "context": docs_content})
        response = llm.invoke(messages)
        
        return {"status": "success", "answer": response.content}
    except Exception as e:
        return {"status": "error", "message": str(e)}