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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
