from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for todos
todos = []
next_id = 1

@app.route('/todos', methods=['GET'])
def get_todos():
    """Return a list of all to-do items"""
    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    """Add a new to-do item"""
    global next_id
    
    # Check if request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # Validate that 'task' field is present
    if not data or 'task' not in data:
        return jsonify({"error": "Task field is required"}), 400
    
    # Validate that task is not empty
    task = data['task'].strip()
    if not task:
        return jsonify({"error": "Task cannot be empty"}), 400
    
    # Create new todo item
    new_todo = {
        "id": next_id,
        "task": task
    }
    
    todos.append(new_todo)
    next_id += 1
    
    return jsonify(new_todo), 201

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "Todo API",
        "endpoints": {
            "GET /todos": "Get all todos",
            "POST /todos": "Add a new todo (requires JSON with 'task' field)"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)