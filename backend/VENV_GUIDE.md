# 🐍 Virtual Environment Guide

This backend uses a Python virtual environment to isolate dependencies.

---

## ✅ Virtual Environment Already Created!

A virtual environment has been created in `backend/venv/`

---

## 🚀 Quick Start

### Windows PowerShell

**Activate:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

**Install Dependencies:**
```powershell
pip install -r requirements.txt
```

**Run Server:**
```powershell
python api.py
```

**Deactivate:**
```powershell
deactivate
```

---

### Windows CMD

**Activate:**
```cmd
cd backend
venv\Scripts\activate.bat
```

**Install Dependencies:**
```cmd
pip install -r requirements.txt
```

**Run Server:**
```cmd
python api.py
```

**Deactivate:**
```cmd
deactivate
```

---

### Linux/Mac

**Activate:**
```bash
cd backend
source venv/bin/activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Run Server:**
```bash
python api.py
```

**Deactivate:**
```bash
deactivate
```

---

## 📋 Complete Setup Process

### First Time Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   ```powershell
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   pip list
   ```

5. **Run the server:**
   ```bash
   python api.py
   ```

---

## 🔍 How to Know if Virtual Environment is Active

When activated, you'll see `(venv)` at the beginning of your command prompt:

```
(venv) PS C:\...\backend>
```

---

## 📦 Managing Dependencies

### Install New Package
```bash
# Activate venv first
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Update All Packages
```bash
pip install --upgrade -r requirements.txt
```

### List Installed Packages
```bash
pip list
```

### Check Specific Package
```bash
pip show package-name
```

---

## 🆘 Troubleshooting

### Issue: "Activate.ps1 cannot be loaded"

**Error:**
```
.\venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

---

### Issue: "venv not found"

**Solution:**
```bash
# Recreate virtual environment
cd backend
python -m venv venv

# Activate and install dependencies
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

---

### Issue: "pip not found"

**Solution:**
```bash
# Make sure venv is activated
# Then upgrade pip
python -m pip install --upgrade pip
```

---

### Issue: "Wrong Python version"

**Solution:**
```bash
# Check Python version
python --version

# Should be 3.10 or higher
# If not, install correct version and recreate venv
python3.10 -m venv venv
```

---

## 🔄 Recreating Virtual Environment

If you need to start fresh:

```bash
# 1. Deactivate if active
deactivate

# 2. Delete old venv
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows CMD
Remove-Item -Recurse -Force venv  # Windows PowerShell

# 3. Create new venv
python -m venv venv

# 4. Activate
.\venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate  # Linux/Mac

# 5. Install dependencies
pip install -r requirements.txt
```

---

## 📝 Best Practices

### ✅ DO:
- Always activate venv before working
- Install packages inside venv
- Update requirements.txt after installing packages
- Deactivate when done
- Add venv/ to .gitignore

### ❌ DON'T:
- Install packages globally
- Commit venv/ to git
- Mix system Python with venv
- Forget to activate venv
- Delete venv/ while activated

---

## 🎯 Why Use Virtual Environment?

### Benefits:
1. **Isolation**: Dependencies don't conflict with system Python
2. **Reproducibility**: Same environment on all machines
3. **Clean**: Easy to delete and recreate
4. **Version Control**: Lock specific package versions
5. **Multiple Projects**: Different dependencies per project

### Without Virtual Environment:
- ❌ Package conflicts
- ❌ Version mismatches
- ❌ System Python pollution
- ❌ Hard to reproduce environment
- ❌ Difficult to manage dependencies

---

## 📊 Current Dependencies

Your virtual environment includes:

```
requests>=2.31.0          # HTTP requests for OpenRouter
SpeechRecognition>=3.10.0 # Voice input
pyttsx3>=2.90            # Text-to-speech
sounddevice>=0.4.6       # Audio backend
soundfile>=0.12.1        # Audio file support
flask>=3.0.0             # Web framework
flask-cors>=4.0.0        # CORS support
python-dotenv>=1.0.0     # Environment variables
```

---

## 🔧 Advanced Usage

### Create venv with specific Python version
```bash
python3.10 -m venv venv
```

### Install from requirements.txt with specific versions
```bash
pip install -r requirements.txt --no-cache-dir
```

### Export exact versions
```bash
pip freeze > requirements-lock.txt
```

### Install in development mode
```bash
pip install -e .
```

---

## 🚀 Quick Commands Reference

### Activation
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Common Tasks
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python api.py

# Update requirements
pip freeze > requirements.txt

# Deactivate
deactivate
```

---

## 📁 Virtual Environment Structure

```
backend/
├── venv/                    # Virtual environment (not in git)
│   ├── Scripts/            # Windows executables
│   │   ├── activate.bat
│   │   ├── Activate.ps1
│   │   ├── python.exe
│   │   └── pip.exe
│   ├── Lib/                # Installed packages
│   │   └── site-packages/
│   └── pyvenv.cfg          # Configuration
│
├── api.py                  # Your code
├── agent.py
├── requirements.txt        # Dependencies list
└── .env                    # Environment variables
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Virtual environment created (`venv/` folder exists)
- [ ] Can activate venv (see `(venv)` in prompt)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] Python version correct (`python --version`)
- [ ] Can run server (`python api.py` works)
- [ ] OpenRouter API key loaded
- [ ] Server starts on port 5000

---

## 🎉 You're All Set!

Your backend now uses a virtual environment for clean dependency management!

**Remember:**
1. Always activate venv before working
2. Install packages inside venv
3. Deactivate when done

---

*Virtual environment created and ready to use!*
