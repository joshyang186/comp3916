#Assignment COMP3916 by Josh Yang
#RESTful API for Tasks
#python 2.7

from flask import Flask, jsonify, make_response, abort, request, url_for
from flask_httpauth import HTTPBasicAuth
from redis import Redis
import json

app = Flask(__name__)
auth = HTTPBasicAuth()
redis = Redis(host='redis', port=6379)

redis.delete('json_data')

tasks = [
]

@auth.get_password
def get_password(username):
    if username == 'josh':
        return 'COMP3916'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
     data_from_redis = redis.get('json_data')

     if data_from_redis:
        tasks = json.loads(data_from_redis)
     else:
        tasks = []
     return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    tasks = []
    data_from_redis = redis.get('json_data')
    if data_from_redis:
      tasks = json.loads(data_from_redis)
    else:
      abort(404)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    tasks = []
    if not request.json or not 'start_date' in request.json:
        abort(400)

    data_from_redis = redis.get('json_data')
    if data_from_redis:
       tasks = json.loads(data_from_redis)
    else:
       tasks = []

    if len(tasks):
        task_id = tasks[-1]['id'] + 1
    else:
        task_id = 1

    task = {
        'id': task_id,
        'start_date': request.json['start_date'],
        'end_date': request.json.get('end_date', ""),
        'priority': request.json.get('priority', ""),
        'description': request.json.get('description', ""),
        'status': request.json.get('status', False)
    }
    tasks.append(task)

    tasks_json_dumps = json.dumps(tasks)
    redis.set('json_data', tasks_json_dumps)

    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    tasks = []
    data_from_redis = redis.get('json_data')
    if data_from_redis:
      tasks = json.loads(data_from_redis)
    else:
      abort(404)

    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'start_date' in request.json and type(request.json['start_date']) != unicode:
        abort(400)
    if 'end_date' in request.json and type(request.json['end_date']) is not unicode:
        abort(400)
    if 'priority' in request.json and type(request.json['priority']) is not unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'status' in request.json and type(request.json['status']) is not bool:
        abort(400)
    task[0]['start_date'] = request.json.get('start_date', task[0]['start_date'])
    task[0]['end_date'] = request.json.get('end_date', task[0]['end_date'])
    task[0]['priority'] = request.json.get('priority', task[0]['priority'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['status'] = request.json.get('status', task[0]['status'])

    tasks_json_dumps = json.dumps(tasks)
    redis.set('json_data', tasks_json_dumps)

    return jsonify({'task': task[0]})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    tasks = []
    data_from_redis = redis.get('json_data')
    if data_from_redis:
      tasks = json.loads(data_from_redis)
    else:
      abort(404)

    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])

    tasks_json_dumps = json.dumps(tasks)
    redis.set('json_data', tasks_json_dumps)

    return jsonify({'result': True})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

