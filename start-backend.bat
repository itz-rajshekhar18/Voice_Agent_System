@echo off
echo Starting Voice Agent Backend...
cd backend
call venv\Scripts\activate.bat
python api.py
