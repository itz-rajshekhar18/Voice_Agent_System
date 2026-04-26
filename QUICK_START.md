# ⚡ Quick Start Guide

Get your Voice AI Assistant running in 5 minutes!

---

## 🎯 Prerequisites Check

Before starting, make sure you have:

- [ ] **Python 3.10+** installed
  ```bash
  python --version
  ```

- [ ] **Node.js 18+** installed
  ```bash
  node --version
  ```

- [ ] **OpenRouter API Key** from https://openrouter.ai/

---

## 🚀 3-Step Setup

### Step 1: Set Your API Key (30 seconds)

Your OpenRouter API key is already configured in `backend/.env`!

If you need to change it, edit `backend/.env`:
```env
OPENROUTER_API_KEY=your-key-here
```

Or set it as an environment variable:
```powershell
$env:OPENROUTER_API_KEY="your-openrouter-api-key-here"
```

> **Note:** Your current key is already set and working!

---

### Step 2: Install Dependencies (2-3 minutes)

**Backend (Automated):**
```bash
# Double-click: setup-backend.bat
# This creates venv and installs everything!
```

**OR Manual:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# venv\Scripts\activate.bat  # Windows CMD
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

**Frontend:**
```bash
cd voice_agent_system
npm install
```

---

### Step 3: Start the App (30 seconds)

**Option A - Automatic (Recommended):**

Double-click `start-all.bat`

**Option B - Manual:**

Open two terminals:

**Terminal 1 - Backend:**
```bash
cd backend
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd voice_agent_system
npm run dev
```

---

## 🎉 You're Ready!

Open your browser and go to:

### **http://localhost:5173**

---

## 🎤 First Steps

### 1. Grant Microphone Permission
When prompted, click **"Allow"** to enable voice input.

### 2. Try Voice Input
1. Click the large circular button at the bottom
2. Say: **"Add a task to buy groceries"**
3. Watch the AI respond!

### 3. Try Text Input
Type in the chat box: **"What are my tasks?"**

---

## 💡 Quick Tips

### Voice Commands to Try:
- "Add a high priority task to finish the report"
- "What are my pending tasks?"
- "Mark buy groceries as done"
- "Remember that I prefer morning meetings"
- "What do you remember about me?"

### Using the Interface:
- **Chat Panel (Left):** Type or speak your messages
- **Task List (Right Top):** View and manage tasks
- **Memory Panel (Right Bottom):** See what the AI remembers
- **Voice Button (Bottom Center):** Click to speak

---

## 🔧 Quick Troubleshooting

### Backend won't start?
```bash
# Check if API key is set
echo $env:ANTHROPIC_API_KEY

# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Frontend won't start?
```bash
# Clear cache and reinstall
cd voice_agent_system
rm -rf node_modules
npm install
```

### Voice not working?
- Use **Chrome** or **Edge** browser
- Grant microphone permissions
- Check system microphone settings

### Can't connect to backend?
- Make sure backend is running (Terminal 1)
- Check http://localhost:5000/api/health
- Look for errors in backend terminal

---

## 📚 Need More Help?

- **Detailed Setup:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Features:** See [FEATURES.md](FEATURES.md)
- **Problems:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **All Docs:** See [INDEX.md](INDEX.md)

---

## ✅ Success Checklist

You should see:

- [ ] Backend running on port 5000
  ```
  * Running on http://0.0.0.0:5000
  ```

- [ ] Frontend running on port 5173
  ```
  ➜  Local:   http://localhost:5173/
  ```

- [ ] Browser shows the app interface
- [ ] Voice button is visible
- [ ] Can send messages (text or voice)
- [ ] AI responds to messages
- [ ] Tasks appear in the sidebar

---

## 🎊 That's It!

You now have a fully functional voice-enabled AI assistant!

### What You Can Do:
✅ Manage tasks with voice or text  
✅ Have natural conversations with AI  
✅ Store and recall important information  
✅ Get intelligent responses powered by Claude  

### Next Steps:
1. Explore all features
2. Try different voice commands
3. Customize the configuration
4. Read the full documentation

---

## 🚨 Common First-Time Issues

### "ANTHROPIC_API_KEY not set"
**Fix:** Run the command from Step 1 again

### "Port 5000 already in use"
**Fix:** 
```bash
# Find and kill the process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "npm: command not found"
**Fix:** Install Node.js from https://nodejs.org/

### "Module not found" errors
**Fix:** Make sure you're in the correct directory
```bash
# For backend
cd backend
pip install -r requirements.txt

# For frontend
cd voice_agent_system
npm install
```

---

## 💻 System Requirements

### Minimum:
- **OS:** Windows 10+, macOS 10.15+, Linux
- **RAM:** 4GB
- **Storage:** 500MB free space
- **Browser:** Chrome 90+ or Edge 90+
- **Internet:** Required for AI features

### Recommended:
- **RAM:** 8GB+
- **Storage:** 1GB free space
- **Browser:** Latest Chrome or Edge
- **Microphone:** Good quality for voice input

---

## 🎯 Quick Command Reference

### Start Everything:
```bash
# Windows
start-all.bat

# Manual
cd backend && python api.py
cd voice_agent_system && npm run dev
```

### Stop Everything:
Press `Ctrl + C` in each terminal

### Restart Backend:
```bash
cd backend
python api.py
```

### Restart Frontend:
```bash
cd voice_agent_system
npm run dev
```

### Check Status:
```bash
# Backend health
curl http://localhost:5000/api/health

# Frontend
# Open http://localhost:5173
```

---

## 🌟 Pro Tips

### For Best Voice Recognition:
1. Use a good quality microphone
2. Speak clearly and at moderate pace
3. Reduce background noise
4. Wait for button to pulse before speaking

### For Better Performance:
1. Close unnecessary browser tabs
2. Use Chrome or Edge
3. Keep backend and frontend running
4. Restart servers if they become slow

### For Easier Development:
1. Keep both terminals visible
2. Watch for errors in terminals
3. Use browser DevTools (F12)
4. Check Network tab for API calls

---

## 🎓 Learning Path

### Beginner:
1. ✅ Complete this quick start
2. Try basic voice commands
3. Explore the interface
4. Read [FEATURES.md](FEATURES.md)

### Intermediate:
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Explore the code
3. Customize configuration
4. Try modifying features

### Advanced:
1. Study [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Implement new features
3. Optimize performance
4. Deploy to production

---

## 📞 Getting Help

### Documentation:
- [README.md](README.md) - Overview
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Fix issues
- [INDEX.md](INDEX.md) - All documentation

### Online Resources:
- Anthropic Docs: https://docs.anthropic.com/
- React Docs: https://react.dev/
- Flask Docs: https://flask.palletsprojects.com/

---

## 🎉 Enjoy Your AI Assistant!

You're all set to:
- 🎤 Talk to your AI assistant
- ✅ Manage tasks effortlessly
- 🧠 Store important information
- 💬 Have natural conversations

**Have fun exploring!** 🚀

---

*Need help? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)*
