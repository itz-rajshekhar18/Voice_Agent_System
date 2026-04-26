# Troubleshooting Guide

## 🔍 Common Issues and Solutions

---

## Backend Issues

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Cause:** Flask or other Python dependencies not installed

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list | grep -i flask
```

---

### Issue: "ANTHROPIC_API_KEY not set"

**Cause:** Environment variable not configured

**Solution (Windows PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

**Solution (Windows CMD):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Permanent Solution:**
1. Open System Properties → Environment Variables
2. Add new user variable: `ANTHROPIC_API_KEY`
3. Restart terminal

**Verify:**
```powershell
echo $env:ANTHROPIC_API_KEY
```

---

### Issue: "Address already in use" (Port 5000)

**Cause:** Another application is using port 5000

**Solution 1 - Find and stop the process:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution 2 - Change the port:**
Edit `backend/api.py`:
```python
port = int(os.environ.get('PORT', 5001))  # Changed from 5000
```

Then update frontend config in `voice_agent_system/src/config.ts`:
```typescript
export const API_BASE_URL = 'http://localhost:5001/api'
```

---

### Issue: "ImportError: cannot import name 'ToDoAgent'"

**Cause:** Python can't find the module

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Run from the backend directory
python api.py
```

---

### Issue: Backend starts but crashes immediately

**Cause:** Syntax error or missing dependency

**Solution:**
1. Check the error message in terminal
2. Look for the specific line number
3. Common issues:
   - Missing comma in Python code
   - Incorrect indentation
   - Missing import statement

**Debug mode:**
```python
# In api.py, check debug is enabled
app.run(host='0.0.0.0', port=port, debug=True)
```

---

## Frontend Issues

### Issue: "npm: command not found"

**Cause:** Node.js not installed or not in PATH

**Solution:**
1. Download Node.js from https://nodejs.org/
2. Install with default options
3. Restart terminal
4. Verify:
```bash
node --version
npm --version
```

---

### Issue: "Cannot find module" errors during npm install

**Cause:** Corrupted node_modules or package-lock.json

**Solution:**
```bash
cd voice_agent_system

# Delete node_modules and package-lock
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

### Issue: "CORS policy" error in browser console

**Full error:**
```
Access to fetch at 'http://localhost:5000/api/chat' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Cause:** Backend not running or CORS not configured

**Solution:**
1. **Check backend is running:**
   - Open http://localhost:5000/api/health
   - Should see: `{"status": "healthy", ...}`

2. **Verify CORS is enabled in backend:**
   ```python
   # In api.py
   from flask_cors import CORS
   CORS(app)  # This line must be present
   ```

3. **Restart backend server**

---

### Issue: Frontend shows blank page

**Cause:** JavaScript error or build issue

**Solution:**
1. **Open browser console (F12)**
2. **Look for errors**
3. **Common fixes:**
   ```bash
   # Clear cache and restart
   cd voice_agent_system
   rm -rf node_modules/.vite
   npm run dev
   ```

---

### Issue: "Failed to fetch" errors

**Cause:** Backend not running or wrong API URL

**Solution:**
1. **Verify backend is running:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Check API URL in config:**
   ```typescript
   // voice_agent_system/src/config.ts
   export const API_BASE_URL = 'http://localhost:5000/api'
   ```

3. **Check browser network tab (F12):**
   - Look for failed requests
   - Check request URL
   - Check response status

---

## Voice Issues

### Issue: Voice button doesn't work

**Cause:** Browser doesn't support Web Speech API

**Solution:**
1. **Use supported browser:**
   - ✅ Google Chrome (recommended)
   - ✅ Microsoft Edge
   - ❌ Firefox (limited support)
   - ❌ Safari (limited support)

2. **Check browser console for errors**

3. **Verify microphone permissions:**
   - Chrome: Settings → Privacy → Microphone
   - Allow for localhost

---

### Issue: "Microphone permission denied"

**Cause:** Browser doesn't have microphone access

**Solution:**
1. **Grant permission when prompted**

2. **If already denied:**
   - Chrome: Click lock icon in address bar
   - Click "Site settings"
   - Change Microphone to "Allow"
   - Refresh page

3. **Windows microphone settings:**
   - Settings → Privacy → Microphone
   - Enable "Allow apps to access your microphone"

---

### Issue: Voice recognition not accurate

**Cause:** Poor audio quality or background noise

**Solution:**
1. **Use a good quality microphone**
2. **Reduce background noise**
3. **Speak clearly and at moderate pace**
4. **Position microphone correctly**
5. **Test microphone:**
   - Windows: Settings → System → Sound → Test microphone

---

### Issue: No voice output (TTS not working)

**Cause:** Speech synthesis not available or volume muted

**Solution:**
1. **Check system volume**
2. **Check browser audio:**
   - Right-click browser tab
   - Check if "Mute site" is enabled
3. **Test in console:**
   ```javascript
   const utterance = new SpeechSynthesisUtterance("test");
   window.speechSynthesis.speak(utterance);
   ```

---

### Issue: Voice recognition stops immediately

**Cause:** No speech detected or timeout

**Solution:**
1. **Start speaking immediately after clicking button**
2. **Check microphone is working:**
   - Test in other apps (e.g., Voice Recorder)
3. **Adjust timeout in code:**
   ```typescript
   // In App.tsx
   recognitionRef.current.continuous = true;  // Keep listening
   ```

---

## API Issues

### Issue: "Invalid API key" from Anthropic

**Cause:** Wrong or expired API key

**Solution:**
1. **Verify API key:**
   - Go to https://console.anthropic.com/
   - Check API keys section
   - Generate new key if needed

2. **Set correct key:**
   ```powershell
   $env:ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. **Restart backend server**

---

### Issue: "Rate limit exceeded" from Anthropic

**Cause:** Too many API requests

**Solution:**
1. **Wait a few minutes**
2. **Check usage:**
   - https://console.anthropic.com/
   - View usage dashboard
3. **Implement rate limiting in code**
4. **Upgrade API plan if needed**

---

### Issue: Slow AI responses

**Cause:** Network latency or API load

**Solution:**
1. **Check internet connection**
2. **Try again later**
3. **Reduce message length**
4. **Check Anthropic status:**
   - https://status.anthropic.com/

---

## Data Issues

### Issue: Tasks not persisting

**Cause:** JSON file not being saved

**Solution:**
1. **Check file permissions:**
   ```bash
   ls -la backend/todos.json
   ```

2. **Verify save is called:**
   ```python
   # In todo_manager.py
   def add(self, ...):
       # ... code ...
       self.save()  # This must be called
   ```

3. **Check for errors in backend logs**

---

### Issue: "JSON decode error"

**Cause:** Corrupted JSON file

**Solution:**
1. **Backup current file:**
   ```bash
   cp backend/todos.json backend/todos.json.backup
   ```

2. **Reset file:**
   ```bash
   echo "[]" > backend/todos.json
   echo "{}" > backend/memory.json
   ```

3. **Restart backend**

---

### Issue: Old data showing up

**Cause:** Browser cache or stale state

**Solution:**
1. **Hard refresh browser:**
   - Windows: Ctrl + Shift + R
   - Mac: Cmd + Shift + R

2. **Clear browser cache:**
   - Chrome: Settings → Privacy → Clear browsing data

3. **Restart both servers**

---

## Build Issues

### Issue: "TypeScript error" during build

**Cause:** Type mismatch or missing types

**Solution:**
1. **Check error message for specific file and line**

2. **Common fixes:**
   ```bash
   # Update TypeScript
   npm install typescript@latest

   # Install missing types
   npm install --save-dev @types/node
   ```

3. **Ignore errors temporarily:**
   ```bash
   # In package.json
   "build": "tsc -b --noEmit false && vite build"
   ```

---

### Issue: Vite build fails

**Cause:** Build configuration or dependency issue

**Solution:**
```bash
cd voice_agent_system

# Clean build cache
rm -rf dist node_modules/.vite

# Reinstall dependencies
npm install

# Try build again
npm run build
```

---

## Performance Issues

### Issue: Slow page load

**Cause:** Large bundle size or slow network

**Solution:**
1. **Check bundle size:**
   ```bash
   npm run build
   # Look at dist/ folder size
   ```

2. **Optimize imports:**
   ```typescript
   // Bad
   import * as React from 'react'
   
   // Good
   import { useState, useEffect } from 'react'
   ```

3. **Enable production mode**

---

### Issue: High memory usage

**Cause:** Memory leak or too many messages

**Solution:**
1. **Limit message history:**
   ```typescript
   // In App.tsx
   const MAX_MESSAGES = 50;
   if (messages.length > MAX_MESSAGES) {
     setMessages(messages.slice(-MAX_MESSAGES));
   }
   ```

2. **Clear conversation periodically**

3. **Restart browser**

---

## Network Issues

### Issue: "Network error" or "Failed to fetch"

**Cause:** Network connectivity or firewall

**Solution:**
1. **Check internet connection**

2. **Disable VPN temporarily**

3. **Check firewall settings:**
   - Allow Python and Node.js through firewall

4. **Try different network**

---

### Issue: Requests timing out

**Cause:** Slow network or server overload

**Solution:**
1. **Increase timeout:**
   ```typescript
   // In fetch call
   const controller = new AbortController();
   const timeout = setTimeout(() => controller.abort(), 30000);
   
   fetch(url, { signal: controller.signal })
   ```

2. **Check backend logs for errors**

3. **Restart backend server**

---

## Development Issues

### Issue: Hot reload not working

**Cause:** File watcher issue

**Solution:**
1. **Restart dev server:**
   ```bash
   # Stop with Ctrl+C
   npm run dev
   ```

2. **Check file watcher limits (Linux/Mac):**
   ```bash
   echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   ```

3. **Manually refresh browser**

---

### Issue: Changes not reflecting

**Cause:** Browser cache or build cache

**Solution:**
1. **Hard refresh:** Ctrl + Shift + R

2. **Clear Vite cache:**
   ```bash
   rm -rf node_modules/.vite
   ```

3. **Restart dev server**

---

## Debugging Tips

### Enable Verbose Logging

**Backend:**
```python
# In api.py
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```typescript
// In App.tsx
console.log('State:', { messages, todos, memories });
```

### Check Browser Console

1. Open DevTools: F12
2. Check Console tab for errors
3. Check Network tab for failed requests
4. Check Application tab for storage

### Check Backend Logs

1. Look at terminal running `python api.py`
2. Check for error messages
3. Look for stack traces

### Test API Directly

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

# Test todos endpoint
curl http://localhost:5000/api/todos
```

---

## Still Having Issues?

### Checklist

- [ ] Backend server is running (port 5000)
- [ ] Frontend server is running (port 5173)
- [ ] ANTHROPIC_API_KEY is set
- [ ] All dependencies installed
- [ ] Using supported browser (Chrome/Edge)
- [ ] Microphone permissions granted
- [ ] No firewall blocking connections
- [ ] Internet connection working
- [ ] Checked browser console for errors
- [ ] Checked backend terminal for errors

### Get Help

1. **Check documentation:**
   - README.md
   - SETUP_GUIDE.md
   - FEATURES.md

2. **Search for error message:**
   - Google the exact error
   - Check Stack Overflow

3. **Create minimal reproduction:**
   - Isolate the issue
   - Test with minimal code

4. **Gather information:**
   - Error messages
   - Browser console logs
   - Backend terminal output
   - Steps to reproduce

---

## Quick Fixes

### Nuclear Option (Reset Everything)

```bash
# Backend
cd backend
rm todos.json memory.json
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Frontend
cd voice_agent_system
rm -rf node_modules package-lock.json dist
npm install

# Restart everything
```

### Fresh Start

```bash
# Stop all servers (Ctrl+C)

# Set API key
$env:ANTHROPIC_API_KEY="your-key"

# Start backend
cd backend
python api.py

# In new terminal, start frontend
cd voice_agent_system
npm run dev

# Open browser
# http://localhost:5173
```

---

Remember: Most issues are caused by:
1. Missing dependencies
2. Wrong API key
3. Servers not running
4. Browser compatibility
5. Microphone permissions

Check these first! 🔍
