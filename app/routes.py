from flask import Blueprint, jsonify, request
import redis
from app.tasks import celery

bp = Blueprint('routes', '__name__')

@bp.route('/start-task', methods = ['POST'])
def start_task():
    data = request.json
    task  = celery.tasks['app.tasks.long_running_task'].apply_async(args=[data])
    return jsonify({"task_id ": task.id}),202

@bp.route("/task-status/<task_id>", methods = ['GET'])
def task_staus(task_id):
    
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state" : task.state, "status ": "Task is pending..."}
    elif task.state == "SUCCESS":
        response = {"state" : task.state, "status ": task.result}
    else:
        response = {"state" : task.state, "status ": str(task.info)}
    
    return jsonify(response)
        

@bp.route('/')
def index():
    redis.incr('hits')
    return 'This page has been visited {} times.'.format(redis.get('hits'))