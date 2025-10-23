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

# TODO: completely overwrite file with <tasks>
def write_to_file(tasks):
    pass

# run with `curl 127.0.0.1:5000/tasks`
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(read_tasks_file())

# TODO: run with `curl -X PUT 127.0.0.1:5000/tasks/TASK_NUMBER -H "Content-Type: application/json" -d '{"status": "NEW_STATUS"}'`
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    return jsonify({'error': 'unimplemented!'}), 501 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)