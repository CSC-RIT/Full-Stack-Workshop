from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mock_tasks = [
    {'id': 1, 'name': 'Complete project proposal', 'owner': 'Alice', 'status': 'In Progress'},
    {'id': 2, 'name': 'Review design mockups', 'owner': 'Bob', 'status': 'To Do'},
    {'id': 3, 'name': 'Deploy to staging', 'owner': 'Alice', 'status': 'Done'},
    {'id': 4, 'name': 'Write user documentation', 'owner': 'Charlie', 'status': 'To Do'},
    {'id': 5, 'name': 'Fix login bug', 'owner': 'Bob', 'status': 'In Progress'},
]

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(mock_tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'New status is required'}), 400

    task_found = False
    for task in mock_tasks:
        if task['id'] == task_id:
            task['status'] = new_status
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

    id = 1 + max([id['id'] for id in mock_tasks])
    mock_tasks.append({'id': id, 'name': task_name, 'owner': task_owner, 'status': 'To Do'})

    return jsonify({'message': 'Task added successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
