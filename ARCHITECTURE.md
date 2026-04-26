# System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              React Frontend (Port 5173)               │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │     Chat     │  │   Todo List  │  │   Memory   │ │  │
│  │  │  Interface   │  │              │  │   Panel    │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │         Voice Button Component               │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │      Web Speech API (Browser Native)         │   │  │
│  │  │  • Speech Recognition (Input)                │   │  │
│  │  │  • Speech Synthesis (Output)                 │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            │ HTTP/REST API                   │
│                            ▼                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend (Port 5000)                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    API Layer (api.py)                 │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  Endpoints:                                     │ │  │
│  │  │  • POST /api/chat                               │ │  │
│  │  │  • GET/POST/PUT/DELETE /api/todos               │ │  │
│  │  │  • GET/POST /api/memories                       │ │  │
│  │  │  • GET /api/health                              │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Agent Layer (agent.py)                   │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  • Conversation History Management              │ │  │
│  │  │  • Tool Call Parsing & Execution                │ │  │
│  │  │  • Context Building                             │ │  │
│  │  │  • Response Generation                          │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Todo      │  │   Memory    │  │   Voice     │        │
│  │  Manager    │  │   Store     │  │  Interface  │        │
│  │             │  │             │  │  (Optional) │        │
│  │ • Add       │  │ • Get       │  │ • Listen    │        │
│  │ • Update    │  │ • Set       │  │ • Speak     │        │
│  │ • Delete    │  │ • Get All   │  │             │        │
│  │ • List      │  │ • Snapshot  │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │ todos.json  │  │memory.json  │                          │
│  └─────────────┘  └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS API Call
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Anthropic Claude API                        │
│                  (External Service)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### 1. User Sends Message (Voice)

```
User speaks
    ↓
Web Speech API (Browser)
    ↓
Transcribed text
    ↓
React App State
    ↓
HTTP POST /api/chat
    ↓
Flask API Endpoint
    ↓
Agent.chat(message)
    ↓
Build context (todos + memories)
    ↓
Call Claude API
    ↓
Parse response for tool calls
    ↓
Execute tools (add/update tasks, save memories)
    ↓
Return response + updated state
    ↓
React updates UI
    ↓
Speech Synthesis speaks response
```

### 2. User Sends Message (Text)

```
User types message
    ↓
React form submit
    ↓
HTTP POST /api/chat
    ↓
[Same as voice flow from here]
```

### 3. User Toggles Task

```
User clicks checkbox
    ↓
React onClick handler
    ↓
HTTP PUT /api/todos/:id
    ↓
Flask API Endpoint
    ↓
TodoManager.update()
    ↓
Update todos.json
    ↓
Return updated task
    ↓
React updates UI
```

---

## 🧩 Component Breakdown

### Frontend Components

```
App.tsx (Root)
├── ChatInterface.tsx
│   ├── Message bubbles (user/assistant)
│   ├── Typing indicator
│   ├── Input form
│   └── Auto-scroll
│
├── TodoList.tsx
│   ├── Todo items (pending)
│   ├── Todo items (completed)
│   ├── Checkboxes
│   └── Delete buttons
│
├── MemoryPanel.tsx
│   ├── Memory cards
│   └── Key-value display
│
└── VoiceButton.tsx
    ├── Microphone icon
    ├── Pulse animation
    └── Click handler
```

### Backend Modules

```
api.py (Flask App)
├── Route handlers
├── CORS configuration
└── Error handling

agent.py (AI Agent)
├── ToDoAgent class
│   ├── chat() - Main entry point
│   ├── _call_claude() - API call
│   ├── _process_tools() - Parse tool calls
│   ├── _dispatch() - Route to tool handlers
│   └── Tool handlers (add, update, delete, etc.)

todo_manager.py (Task Management)
├── ToDoManager class
│   ├── add() - Create task
│   ├── update() - Modify task
│   ├── delete() - Remove task
│   ├── list_all() - Get all tasks
│   └── save() - Persist to JSON

memory.py (Memory Storage)
├── MemoryStore class
│   ├── get() - Retrieve value
│   ├── set() - Store value
│   ├── get_all() - Get all memories
│   └── save() - Persist to JSON

voice.py (Voice Interface - Optional)
├── VoiceInterface class
│   ├── listen() - Speech recognition
│   └── speak() - Text-to-speech
```

---

## 🔌 API Contract

### Request/Response Formats

#### POST /api/chat
**Request:**
```json
{
  "message": "Add a task to buy groceries"
}
```

**Response:**
```json
{
  "response": "I've added a task to buy groceries with medium priority.",
  "todos": [
    {
      "id": "abc123",
      "title": "Buy groceries",
      "done": false,
      "priority": "medium",
      "created": "2026-04-27T10:30:00"
    }
  ],
  "memories": {
    "preference": "morning meetings"
  }
}
```

#### GET /api/todos
**Response:**
```json
{
  "todos": [
    {
      "id": "abc123",
      "title": "Buy groceries",
      "done": false,
      "priority": "medium",
      "due": "2026-04-28",
      "created": "2026-04-27T10:30:00"
    }
  ]
}
```

#### PUT /api/todos/:id
**Request:**
```json
{
  "done": true
}
```

**Response:**
```json
{
  "todo": {
    "id": "abc123",
    "title": "Buy groceries",
    "done": true,
    "priority": "medium",
    "created": "2026-04-27T10:30:00"
  }
}
```

---

## 🔐 Security Architecture

### Current Implementation

```
┌─────────────────────────────────────────┐
│           Browser (Frontend)            │
│  • No authentication                    │
│  • API key not exposed                  │
│  • CORS requests                        │
└─────────────────────────────────────────┘
                  │
                  │ HTTP (localhost)
                  ▼
┌─────────────────────────────────────────┐
│         Flask Backend (API)             │
│  • CORS enabled (all origins)           │
│  • No authentication                    │
│  • No rate limiting                     │
│  • API key in environment               │
└─────────────────────────────────────────┘
                  │
                  │ HTTPS
                  ▼
┌─────────────────────────────────────────┐
│         Anthropic API                   │
│  • API key authentication               │
│  • Rate limiting                        │
│  • Usage tracking                       │
└─────────────────────────────────────────┘
```

### Production Recommendations

```
┌─────────────────────────────────────────┐
│           Browser (Frontend)            │
│  • JWT token storage                    │
│  • Secure cookie handling               │
│  • HTTPS only                           │
└─────────────────────────────────────────┘
                  │
                  │ HTTPS
                  ▼
┌─────────────────────────────────────────┐
│         API Gateway / Load Balancer     │
│  • SSL termination                      │
│  • Rate limiting                        │
│  • DDoS protection                      │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Flask Backend (API)             │
│  • JWT authentication                   │
│  • CORS (specific origins)              │
│  • Input validation                     │
│  • API key in secrets manager           │
└─────────────────────────────────────────┘
                  │
                  ├─────────────────────┐
                  ▼                     ▼
┌─────────────────────────┐  ┌─────────────────────┐
│      Database           │  │   Anthropic API     │
│  • Encrypted at rest    │  │  • API key auth     │
│  • Access control       │  │  • Rate limiting    │
└─────────────────────────┘  └─────────────────────┘
```

---

## 📊 State Management

### Frontend State Flow

```
┌─────────────────────────────────────────┐
│          App.tsx (Root State)           │
│                                         │
│  State:                                 │
│  • messages: Message[]                  │
│  • todos: Todo[]                        │
│  • memories: Memory                     │
│  • isLoading: boolean                   │
│  • isListening: boolean                 │
│                                         │
│  Effects:                               │
│  • fetchTodos() on mount                │
│  • fetchMemories() on mount             │
│  • Initialize speech recognition        │
│                                         │
│  Handlers:                              │
│  • handleSendMessage()                  │
│  • handleVoiceInput()                   │
│  • handleToggleTodo()                   │
│  • handleDeleteTodo()                   │
└─────────────────────────────────────────┘
                  │
                  │ Props
                  ▼
┌─────────────────────────────────────────┐
│            Child Components             │
│                                         │
│  ChatInterface                          │
│  • Receives: messages, onSendMessage    │
│  • Local state: input text              │
│                                         │
│  TodoList                               │
│  • Receives: todos, onToggle, onDelete  │
│  • No local state                       │
│                                         │
│  MemoryPanel                            │
│  • Receives: memories                   │
│  • No local state                       │
│                                         │
│  VoiceButton                            │
│  • Receives: isListening, onClick       │
│  • No local state                       │
└─────────────────────────────────────────┘
```

### Backend State Management

```
┌─────────────────────────────────────────┐
│         Application Startup             │
│                                         │
│  Initialize:                            │
│  • MemoryStore() → loads memory.json    │
│  • ToDoManager() → loads todos.json     │
│  • VoiceInterface()                     │
│  • ToDoAgent(memory, todos)             │
└─────────────────────────────────────────┘
                  │
                  │ Singleton instances
                  ▼
┌─────────────────────────────────────────┐
│         Request Handling                │
│                                         │
│  Each request:                          │
│  • Uses shared instances                │
│  • Modifies in-memory state             │
│  • Persists to JSON files               │
│  • Returns updated state                │
└─────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

### Development (Current)

```
┌─────────────────────────────────────────┐
│         Developer Machine               │
│                                         │
│  Terminal 1:                            │
│  └─ python api.py (port 5000)           │
│                                         │
│  Terminal 2:                            │
│  └─ npm run dev (port 5173)             │
│                                         │
│  Browser:                               │
│  └─ http://localhost:5173               │
└─────────────────────────────────────────┘
```

### Production (Recommended)

```
┌─────────────────────────────────────────┐
│              Internet                   │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         CDN (Frontend Assets)           │
│  • Static files                         │
│  • Global distribution                  │
│  • HTTPS                                │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Load Balancer                   │
│  • SSL termination                      │
│  • Health checks                        │
│  • Auto-scaling                         │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Backend Servers                 │
│  • Gunicorn + Flask                     │
│  • Multiple instances                   │
│  • Container-based (Docker)             │
└─────────────────────────────────────────┘
                  │
                  ├─────────────────────┐
                  ▼                     ▼
┌─────────────────────────┐  ┌─────────────────────┐
│      Database           │  │   External APIs     │
│  • PostgreSQL           │  │  • Anthropic        │
│  • Redis (cache)        │  │                     │
└─────────────────────────┘  └─────────────────────┘
```

---

## 🔄 Technology Stack Summary

### Frontend Stack
```
React 19.2
  └─ TypeScript 6.0
      └─ Vite 8.0
          ├─ ESLint (linting)
          ├─ CSS3 (styling)
          └─ Web Speech API (voice)
```

### Backend Stack
```
Python 3.14
  └─ Flask 3.1
      ├─ Flask-CORS (CORS handling)
      ├─ Anthropic SDK (AI)
      ├─ SpeechRecognition (voice input)
      ├─ pyttsx3 (voice output)
      └─ sounddevice (audio backend)
```

### Infrastructure
```
Development:
  ├─ Flask dev server (backend)
  └─ Vite dev server (frontend)

Production (Recommended):
  ├─ Gunicorn (WSGI server)
  ├─ Nginx (reverse proxy)
  ├─ PostgreSQL (database)
  ├─ Redis (caching)
  └─ Docker (containerization)
```

---

This architecture provides a solid foundation for a voice-enabled AI assistant while remaining simple enough for development and learning purposes.
