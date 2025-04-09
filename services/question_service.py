import os
from celery import Celery
from flask import jsonify

# Configure Celery
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
celery_app = Celery('tasks', broker=f'redis://{redis_host}:{redis_port}/0')

class QuestionService:
    @staticmethod
    def answer_question(data):
        """Ejecuta el flujo de RAG de forma asíncrona"""
        question = data.get("question")
        collection = data.get("collection", "documentos")
        
        task = celery_app.send_task(
            'tasks.answer_question',
            args=[question],
            kwargs={"collection": collection, "chroma_path": os.getenv("CHROMA_PATH", "chroma_db")}
        )
        
        return jsonify({
            "message": "Procesando pregunta",
            "task_id": task.id
        }), 202