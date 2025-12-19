@echo off
setlocal enabledelayedexpansion

TITLE SAICA Scribe - Auto Launcher
cd /d "%~dp0\code"

echo =========================================
echo        SAICA Scribe - Auto Launcher      
echo =========================================
echo.

:: 1. Port Cleanup (Kill process on port 8000)
echo [Cleaning] Checking for old processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo    Killing PID %%a...
    taskkill /F /PID %%a >nul 2>&1
)

:: 2. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed or not in PATH.
    echo Please install it from python.org and check "Add Python to PATH" during installation.
    pause
    exit /b
)

:: 3. Setup Virtual Env
if not exist ".venv" (
    echo [Setup] Creating virtual environment...
    python -m venv .venv
)

:: 4. Activate & Install
echo [Setup] Checking dependencies...
call .venv\Scripts\activate.bat
pip install -q pip-system-certs
pip install -q -r requirements.txt

:: 5. Launch
echo [Launch] Starting Server...
echo    Browser will open in 2 seconds.

start "" cmd /c "timeout /t 2 >nul & start http://localhost:8000"

python web_app.py

echo.
echo Server stopped.
pause
