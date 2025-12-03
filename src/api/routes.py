from flask import Blueprint, request, jsonify
from src.service.todo_service import todo_service

api_bp = Blueprint('api', __name__)


@api_bp.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = todo_service.get_all_tasks()
    return jsonify(tasks), 200


@api_bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.json or {}
    if not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    new_task = todo_service.create_task(
        title=data['title'],
        priority=data.get('priority', 'normal')
    )
    return jsonify(new_task), 201


@api_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = todo_service.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return '', 204