@echo off
echo ========================================
echo   Voice-Enabled AI Assistant
echo   Starting Backend and Frontend...
echo ========================================
echo.

echo Starting Backend Server...
start "Backend API" cmd /k "cd backend && call venv\Scripts\activate.bat && python api.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Dev" cmd /k "cd voice_agent_system && npm run dev"

echo.
echo ========================================
echo   Both servers are starting!
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to close this window...
pause > nul
