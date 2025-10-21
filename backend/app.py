from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

TASKS_FILE = 'tasks.json'

# read whole file to python list
def read_tasks_file():
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# add a new task to the file
def append_task_to_file(task):
    with open(TASKS_FILE, 'r') as file:
        tasks = read_tasks_file()
    with open(TASKS_FILE, 'w') as file:
        tasks.append(task)
        json.dump(tasks, file, indent=4)

# completely overwrite file with <tasks>
def write_to_file(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# run with `curl 127.0.0.1:5000/tasks`
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(read_tasks_file())

# run with `curl -X PUT 127.0.0.1:5000/tasks/TASK_NUMBER -H "Content-Type: application/json" -d '{"status": "NEW_STATUS"}'`
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'New status is required'}), 400

    task_found = False
    tasks = read_tasks_file()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            write_to_file(tasks)
            task_found = True
            break

    if not task_found:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task status updated successfully', 'task': task})

# run with `curl -X POST 127.0.0.1:5000/tasks/add -H "Content-Type: application/json" -d '{"name": "TASK_NAME", "owner": "TASK_OWNER"}'`
@app.route('/tasks/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get('name')
    task_owner = data.get('owner')

    if not task_name:
        return jsonify({'error': 'New task name is required'}), 400

    if not task_owner:
        return jsonify({'error': 'New task owner is required'}), 400

    # make the id one more than the max
    id = 1 + max([task['id'] for task in read_tasks_file()])
    # store it in a variable so we can include it in the return stmt
    new_task = {'id': id, 'name': task_name, 'owner': task_owner, 'status': 'To Do'}
    append_task_to_file(new_task)

    return jsonify({'message': 'Task added successfully', 'task': new_task})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
