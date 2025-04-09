from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from celery import Celery
import os

# Configure Celery
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
celery_app = Celery('tasks', broker=f'redis://{redis_host}:{redis_port}/0')

class TaskStatus(Resource):
    @jwt_required()
    def get(self, task_id):
        """Obtiene el estado de una tarea asíncrona"""
        task = celery_app.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'La tarea está pendiente de ejecución'
            }
        elif task.state == 'FAILURE':
            response = {
                'state': task.state,
                'status': 'La tarea falló',
                'error': str(task.info)
            }
        else:
            response = {
                'state': task.state,
                'status': 'Tarea completada' if task.state == 'SUCCESS' else 'En progreso',
                'result': task.result if task.state == 'SUCCESS' else None
            }
            
        return jsonify(response)