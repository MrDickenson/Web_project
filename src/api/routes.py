import time
import uuid
import random
from flask import Blueprint, request, jsonify, g, make_response, render_template
from src.service.todo_service import todo_service
from src.service.db import get_idempotency_key, save_idempotency_key

api_bp = Blueprint('api', __name__)

rate_limit_store = {}
RATE_LIMIT_WINDOW = 10
RATE_LIMIT_MAX_REQ = 5


@api_bp.before_request
def before_request_hook():
    g.request_id = request.headers.get('X-Request-Id') or str(uuid.uuid4())

    if request.endpoint and 'static' not in request.endpoint:
        ip = request.remote_addr
        now = time.time()
        record = rate_limit_store.get(ip, {'count': 0, 'start_time': now})

        if now - record['start_time'] > RATE_LIMIT_WINDOW:
            record = {'count': 1, 'start_time': now}
        else:
            record['count'] += 1

        rate_limit_store[ip] = record

        if record['count'] > RATE_LIMIT_MAX_REQ:
            resp = make_error_response("Too Many Requests", 429, "RATE_LIMIT_EXCEEDED")
            resp.headers['Retry-After'] = 2
            return resp


@api_bp.after_request
def after_request_hook(response):
    response.headers['X-Request-Id'] = g.get('request_id', 'unknown')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Idempotency-Key, X-Request-Id'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    return response


def make_error_response(error_msg, status, code=None, details=None):
    body = {
        "error": error_msg,
        "code": code,
        "details": details,
        "requestId": g.get('request_id')
    }
    return make_response(jsonify(body), status)


@api_bp.route('/health', methods=['GET'])
def health():
    if random.random() < 0.1:
        time.sleep(2)
    return jsonify({"status": "ok"})


@api_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@api_bp.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = todo_service.get_all_tasks()
    return jsonify(tasks), 200


@api_bp.route('/tasks', methods=['POST'])
def add_task():
    idem_key = request.headers.get('Idempotency-Key')
    if not idem_key:
        return make_error_response("Idempotency-Key header is required", 400, "MISSING_HEADER")

    cached = get_idempotency_key(idem_key)
    if cached:
        return jsonify(cached['response_body']), cached['status_code']

    rand_val = random.random()
    if rand_val < 0.20:
        time.sleep(random.uniform(0.5, 2.0))

    if rand_val > 0.80:
        status = random.choice([500, 503])
        return make_error_response("Simulated Server Error", status, "SERVER_ERROR")

    data = request.json or {}
    if not data.get('title'):
        return make_error_response("Title is required", 400, "VALIDATION_ERROR")

    new_task = todo_service.create_task(
        title=data['title'],
        priority=data.get('priority', 'normal')
    )

    save_idempotency_key(idem_key, 201, new_task)

    return jsonify(new_task), 201


@api_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = todo_service.delete_task(task_id)
    if not success:
        return make_error_response("Task not found", 404, "NOT_FOUND")
    return '', 204


@api_bp.route('/tasks', methods=['OPTIONS'])
def options_tasks():
    return '', 200