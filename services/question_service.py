from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_core.documents import Document
import os

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    collection: str

class QuestionService:
    @staticmethod
    def retrieve(state: State):
        """Recupera documentos similares desde Chroma"""
        chroma_path = "chroma_db"
        collection_name = state["collection"]

        embeddings = OllamaEmbeddings(
            model="llama3:8b",
            base_url="http://localhost:11434"
        )

        vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings,
            collection_name=collection_name
        )

        retrieved_docs = vector_store.similarity_search(state["question"])

        return {"context": retrieved_docs}

    @staticmethod
    def generate(state: State):
        """Genera una respuesta basada en los documentos recuperados"""
        llm = init_chat_model("llama3:8b", model_provider="ollama", base_url="http://localhost:11434")
        prompt = hub.pull("rlm/rag-prompt")

        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        
        return {"answer": response.content}

    @staticmethod
    def answer_question(data):
        """Ejecuta el flujo de recuperación y generación"""
        graph_builder = StateGraph(State).add_sequence([QuestionService.retrieve, QuestionService.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()

        response = graph.invoke({"question": data["question"], "collection": data["collection"]})

        return {"respuesta": response["answer"]}
