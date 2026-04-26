"""
Flask API for Voice-Enabled AI To-Do Agent
Provides REST endpoints for the frontend to interact with the agent.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

from agent import ToDoAgent
from voice import VoiceInterface
from memory import MemoryStore
from todo_manager import ToDoManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize components
memory = MemoryStore()
todos = ToDoManager()
voice = VoiceInterface()
agent = ToDoAgent(memory_store=memory, todo_manager=todos)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Voice Agent API is running"})


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Process a chat message from the user.
    Expects: {"message": "user text"}
    Returns: {"response": "agent reply", "todos": [...], "memories": {...}}
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Process message through agent
        response = agent.chat(user_message)
        
        # Get current state
        todos_list = todos.list_all()
        memories = memory.get_all()
        
        return jsonify({
            "response": response,
            "todos": todos_list,
            "memories": memories
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    try:
        todos_list = todos.list_all()
        return jsonify({"todos": todos_list})
    except Exception as e:
        logger.error(f"Get todos error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/todos', methods=['POST'])
def add_todo():
    """
    Add a new todo.
    Expects: {"title": "...", "priority": "low|medium|high", "due": "..."}
    """
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        priority = data.get('priority', 'medium')
        due = data.get('due')
        
        if not title:
            return jsonify({"error": "Title is required"}), 400
        
        task = todos.add(title=title, priority=priority, due=due)
        return jsonify({"todo": task})
    
    except Exception as e:
        logger.error(f"Add todo error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/todos/<task_id>', methods=['PUT'])
def update_todo(task_id):
    """
    Update a todo.
    Expects: {"done": true/false, "title": "..."}
    """
    try:
        data = request.get_json()
        done = data.get('done')
        new_title = data.get('title')
        
        task = todos.update(identifier=task_id, done=done, new_title=new_title)
        
        if task:
            return jsonify({"todo": task})
        else:
            return jsonify({"error": "Todo not found"}), 404
    
    except Exception as e:
        logger.error(f"Update todo error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/todos/<task_id>', methods=['DELETE'])
def delete_todo(task_id):
    """Delete a todo"""
    try:
        removed = todos.delete(task_id)
        
        if removed:
            return jsonify({"message": f"Deleted '{removed}'"})
        else:
            return jsonify({"error": "Todo not found"}), 404
    
    except Exception as e:
        logger.error(f"Delete todo error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/memories', methods=['GET'])
def get_memories():
    """Get all memories"""
    try:
        memories = memory.get_all()
        return jsonify({"memories": memories})
    except Exception as e:
        logger.error(f"Get memories error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/memories', methods=['POST'])
def save_memory():
    """
    Save a memory.
    Expects: {"key": "...", "value": "..."}
    """
    try:
        data = request.get_json()
        key = data.get('key', '').strip()
        value = data.get('value', '').strip()
        
        if not key or not value:
            return jsonify({"error": "Key and value are required"}), 400
        
        memory.set(key, value)
        return jsonify({"message": f"Saved memory: {key}"})
    
    except Exception as e:
        logger.error(f"Save memory error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation history"""
    try:
        agent.history = []
        return jsonify({"message": "Conversation reset"})
    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.warning("ANTHROPIC_API_KEY not set. Agent functionality may be limited.")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
