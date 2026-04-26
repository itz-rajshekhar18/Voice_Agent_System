@echo off
echo ========================================
echo   Backend Setup Script
echo   Setting up virtual environment...
echo ========================================
echo.

cd backend

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.10+ is installed
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 5: Verifying installation...
pip list
echo.

echo ========================================
echo   Backend Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure OPENROUTER_API_KEY is set in backend/.env
echo 2. Run: start-backend.bat
echo 3. Or manually: cd backend, venv\Scripts\activate.bat, python api.py
echo.
echo ========================================
pause
