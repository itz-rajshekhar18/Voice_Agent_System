# Quick Setup Guide

## 🚀 Quick Start (Windows)

### Step 1: Set Your API Key

Open PowerShell and run:
```powershell
$env:ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

Or add it permanently to your system environment variables.

### Step 2: Start Everything

Double-click `start-all.bat` - this will open two terminal windows:
- Backend API (port 5000)
- Frontend Dev Server (port 5173)

### Step 3: Open the App

Navigate to: **http://localhost:5173**

That's it! 🎉

---

## 📋 Detailed Setup

### Prerequisites

1. **Python 3.10+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **Anthropic API Key** - [Get one here](https://console.anthropic.com/)

### Backend Setup

#### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
# Double-click setup-backend.bat
# OR run in PowerShell:
.\setup-backend.ps1
```

This will:
- Create virtual environment
- Activate it
- Install all dependencies
- Verify installation

#### Option 2: Manual Setup

1. Open terminal in the project root

2. Navigate to backend:
   ```bash
   cd backend
   ```

3. Create virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate virtual environment:
   
   **Windows PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows CMD:**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```
   
   You should see `(venv)` at the start of your prompt.

5. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

7. Set API key (choose one method):

   **Option A - Using .env file (recommended):**
   
   The `.env` file already exists with your OpenRouter API key!
   
   Verify it contains:
   ```env
   OPENROUTER_API_KEY=your-key-here
   PORT=5000
   FLASK_ENV=development
   ```

   **Option B - Environment variable (temporary):**
   ```powershell
   # PowerShell
   $env:OPENROUTER_API_KEY="your-key"
   ```
   ```cmd
   # CMD
   set OPENROUTER_API_KEY=your-key
   ```

8. Start the backend:
   ```bash
   python api.py
   ```

   You should see:
   ```
   INFO:__main__:OpenRouter API key loaded successfully
   * Running on http://0.0.0.0:5000
   ```

**Important:** Always activate the virtual environment before working on the backend!

### Frontend Setup

1. Open a NEW terminal in the project root
2. Navigate to frontend:
   ```bash
   cd voice_agent_system
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Start the dev server:
   ```bash
   npm run dev
   ```

   You should see:
   ```
   VITE ready in XXX ms
   ➜  Local:   http://localhost:5173/
   ```

5. Open http://localhost:5173 in your browser

---

## 🎤 Using the Voice Features

### First Time Setup

1. When you first open the app, your browser will ask for microphone permission
2. Click "Allow" to enable voice input

### Voice Input

1. Click the large circular voice button at the bottom
2. Speak your message clearly
3. The button will pulse while listening
4. Your speech will be transcribed and sent to the AI

### Voice Output

- The AI's responses will be spoken automatically
- You can adjust your system volume to control the speech volume

### Supported Browsers

✅ **Best Experience:**
- Google Chrome
- Microsoft Edge

⚠️ **Limited Support:**
- Safari (voice recognition may not work)
- Firefox (voice recognition may not work)

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'flask'`
**Solution:** Run `pip install -r requirements.txt` in the backend folder

**Problem:** `ANTHROPIC_API_KEY not set`
**Solution:** Set the environment variable as shown above

**Problem:** `Port 5000 already in use`
**Solution:** 
- Stop any other service using port 5000
- Or edit `backend/api.py` and change the port number

### Frontend Issues

**Problem:** `npm: command not found`
**Solution:** Install Node.js from https://nodejs.org/

**Problem:** CORS errors in browser console
**Solution:** Make sure the backend is running on port 5000

**Problem:** Voice button doesn't work
**Solution:** 
- Check browser compatibility (use Chrome/Edge)
- Grant microphone permissions
- Check browser console for errors

**Problem:** `Cannot find module` errors
**Solution:** Delete `node_modules` folder and run `npm install` again

### Voice Issues

**Problem:** Microphone not working
**Solution:**
1. Check Windows microphone permissions
2. Check browser microphone permissions
3. Test microphone in other apps

**Problem:** Voice recognition not accurate
**Solution:**
- Speak clearly and at a moderate pace
- Reduce background noise
- Check microphone quality

**Problem:** No voice output
**Solution:**
- Check system volume
- Check browser audio permissions
- Try refreshing the page

---

## 📁 Project Structure

```
voice-agent/
├── backend/                    # Python Flask API
│   ├── agent.py               # AI agent logic
│   ├── api.py                 # Flask REST API
│   ├── memory.py              # Memory storage
│   ├── todo_manager.py        # Task management
│   ├── voice.py               # Voice interface
│   ├── requirements.txt       # Python dependencies
│   ├── todos.json            # Task storage
│   └── memory.json           # Memory storage
│
├── voice_agent_system/        # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.tsx          # Main app
│   │   ├── config.ts        # Configuration
│   │   └── main.tsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite config
│
├── start-all.bat             # Start both servers
├── start-backend.bat         # Start backend only
├── start-frontend.bat        # Start frontend only
└── README.md                 # Documentation
```

---

## 🎯 Usage Examples

### Managing Tasks

**Add a task:**
- "Add a task to buy groceries"
- "Create a high priority task to finish the report by Friday"

**View tasks:**
- "What are my tasks?"
- "Show me my pending tasks"

**Complete a task:**
- Click the checkbox next to the task
- Or say: "Mark buy groceries as done"

**Delete a task:**
- Click the trash icon
- Or say: "Delete the groceries task"

### Using Memory

**Save information:**
- "Remember that I prefer morning meetings"
- "Save that my favorite color is blue"

**Recall information:**
- "What do you remember about me?"
- "What's my favorite color?"

### General Chat

- "What's the weather like?" (requires internet)
- "Tell me a joke"
- "Help me plan my day"

---

## 🔧 Advanced Configuration

### Change API Port

Edit `backend/api.py`:
```python
port = int(os.environ.get('PORT', 5000))  # Change 5000 to your port
```

### Change Frontend Port

Edit `voice_agent_system/vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    port: 5173  // Change to your preferred port
  }
})
```

### Customize Voice Settings

Edit `voice_agent_system/src/config.ts`:
```typescript
export const VOICE_CONFIG = {
  language: 'en-US',      // Change language
  speechRate: 0.9,        // 0.1 to 10 (speed)
  speechPitch: 1,         // 0 to 2 (pitch)
  speechVolume: 1,        // 0 to 1 (volume)
}
```

---

## 📝 Development

### Backend Development

The backend uses Flask with hot-reload enabled. Changes to Python files will automatically restart the server.

### Frontend Development

The frontend uses Vite with HMR (Hot Module Replacement). Changes to React files will update instantly in the browser.

### Building for Production

**Frontend:**
```bash
cd voice_agent_system
npm run build
```

The built files will be in `voice_agent_system/dist/`

**Backend:**
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

---

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Check the browser console for errors (F12)
3. Check the backend terminal for errors
4. Ensure all dependencies are installed
5. Verify your API key is set correctly

---

## 🎉 You're All Set!

Enjoy your voice-enabled AI assistant! The AI can help you:
- ✅ Manage your tasks
- 🧠 Remember important information
- 💬 Have natural conversations
- 🎤 Interact using voice or text

Have fun! 🚀
