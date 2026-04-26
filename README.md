# Voice-Enabled AI To-Do Agent

A modern web application featuring a voice-enabled AI assistant powered by GPT-4o Mini via OpenRouter. The assistant helps you manage tasks, remember important information, and have natural conversations.

## 🎯 Quick Links

- **[⚡ Quick Start](QUICK_START.md)** - Get running in 5 minutes
- **[📚 Full Documentation](INDEX.md)** - Complete documentation index
- **[🔧 Setup Guide](SETUP_GUIDE.md)** - Detailed installation instructions
- **[✨ Features](FEATURES.md)** - All features explained
- **[🏗️ Architecture](ARCHITECTURE.md)** - System design and architecture
- **[🆘 Troubleshooting](TROUBLESHOOTING.md)** - Fix common issues

## Features

- 🎤 **Voice Input**: Speak naturally to interact with the AI assistant
- 🔊 **Voice Output**: The assistant speaks responses back to you
- ✅ **Task Management**: Add, update, complete, and delete tasks
- 🧠 **Memory System**: The assistant remembers important information about you
- 💬 **Natural Conversations**: Chat naturally with Claude AI via OpenRouter
- 🎨 **Modern UI**: Beautiful, responsive interface built with React

## Architecture

### Backend (Python + Flask)
- **Flask API**: RESTful API endpoints for frontend communication
- **Claude Integration**: Uses OpenRouter API for access to Claude AI
- **Tool Calling**: Agent can execute tools (add tasks, save memories, etc.)
- **Persistent Storage**: Tasks and memories saved to JSON files

### Frontend (React + TypeScript + Vite)
- **React Components**: Modular, reusable UI components
- **Web Speech API**: Browser-based voice recognition and synthesis
- **Real-time Updates**: Instant UI updates when tasks/memories change
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenRouter API Key (get one at https://openrouter.ai/)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set your OpenRouter API key:

Create or edit `backend/.env`:
```env
OPENROUTER_API_KEY=your-api-key-here
PORT=5000
FLASK_ENV=development
```

Or set as environment variable:
```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-api-key-here"
```

5. Start the Flask API server:
```bash
python api.py
```

The backend will run on `http://localhost:5000`

**Note:** Always activate the virtual environment before working on the backend!

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd voice_agent_system
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. **Start Both Servers**: Make sure both backend (port 5000) and frontend (port 5173) are running

2. **Open the App**: Navigate to `http://localhost:5173` in your browser

3. **Grant Microphone Permission**: Allow microphone access when prompted

4. **Interact with the Assistant**:
   - Click the large voice button to speak
   - Or type messages in the chat input
   - The assistant will respond with voice and text

5. **Manage Tasks**:
   - Say: "Add a task to buy groceries"
   - Say: "What are my pending tasks?"
   - Click checkboxes to mark tasks complete
   - Click trash icons to delete tasks

6. **Save Memories**:
   - Say: "Remember that I prefer morning meetings"
   - The assistant will automatically save important information

## API Endpoints

### Chat
- `POST /api/chat` - Send a message to the agent
  - Body: `{"message": "your message"}`
  - Returns: `{"response": "...", "todos": [...], "memories": {...}}`

### Tasks
- `GET /api/todos` - Get all tasks
- `POST /api/todos` - Create a new task
- `PUT /api/todos/:id` - Update a task
- `DELETE /api/todos/:id` - Delete a task

### Memories
- `GET /api/memories` - Get all memories
- `POST /api/memories` - Save a memory

### Utility
- `GET /api/health` - Health check
- `POST /api/reset` - Reset conversation history

## Project Structure

```
.
├── backend/
│   ├── agent.py           # Claude agent with tool calling
│   ├── api.py             # Flask REST API
│   ├── memory.py          # Memory storage system
│   ├── todo_manager.py    # Task management
│   ├── voice.py           # Voice interface (optional)
│   ├── requirements.txt   # Python dependencies
│   ├── todos.json         # Task storage
│   └── memory.json        # Memory storage
│
└── voice_agent_system/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.tsx    # Chat UI
    │   │   ├── TodoList.tsx         # Task list UI
    │   │   ├── MemoryPanel.tsx      # Memory display
    │   │   └── VoiceButton.tsx      # Voice input button
    │   ├── App.tsx                  # Main app component
    │   └── main.tsx                 # Entry point
    ├── package.json
    └── vite.config.ts
```

## Technologies Used

### Backend
- Python 3.14
- Flask - Web framework
- Anthropic Claude API - AI assistant
- SpeechRecognition - Voice input (optional)
- pyttsx3 - Text-to-speech (optional)

### Frontend
- React 19 - UI framework
- TypeScript - Type safety
- Vite - Build tool
- Web Speech API - Voice recognition & synthesis
- CSS3 - Styling with animations

## Browser Compatibility

Voice features require:
- Chrome/Edge (recommended)
- Safari (limited support)
- Firefox (limited support)

## Troubleshooting

### Backend Issues
- **API Key Error**: Make sure `ANTHROPIC_API_KEY` environment variable is set
- **Port 5000 in use**: Change port in `api.py` or stop conflicting service
- **Module not found**: Run `pip install -r requirements.txt`

### Frontend Issues
- **CORS Error**: Ensure backend is running on port 5000
- **Voice not working**: Check browser compatibility and microphone permissions
- **Build errors**: Delete `node_modules` and run `npm install` again
