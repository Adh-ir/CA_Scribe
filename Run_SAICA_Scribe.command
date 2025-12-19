#!/bin/bash

# SAICA Scribe - Smart Launcher for Mac
# Double-click to run!

# 1. Colors & UX
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}       SAICA Scribe - Auto Launcher      ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# 2. Get the directory of this script (resolve symlinks/double-clicks)
cd "$(dirname "$0")/code" || exit
echo -e "📂 Working Directory: $(pwd)"

# 3. Port Cleanup (Fixes "Address in Use" error)
echo -e "🧹 Checking for zombie processes on port 8000..."
PID=$(lsof -ti:8000)
if [ -n "$PID" ]; then
    echo -e "${RED}   Killing old process (PID $PID)...${NC}"
    kill -9 "$PID"
    sleep 1
else
    echo -e "${GREEN}   Port 8000 is clear.${NC}"
fi

# 4. Check Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    # Verify version 3
    VER=$(python --version 2>&1)
    if [[ $VER == *"Python 3"* ]]; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Error: Python 3 is required. Found $VER.${NC}"
        echo "Please install Python from python.org"
        read -n 1 -s -r -p "Press any key to exit..."
        exit 1
    fi
else
    echo -e "${RED}Error: Python 3 not found.${NC}"
    echo "Please install Python 3.10+ from python.org"
    read -n 1 -s -r -p "Press any key to exit..."
    exit 1
fi

# 5. Virtual Environment (Hidden)
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "🌱 Creating Python Virtual Environment (First Run)..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

# Activate Venv
source "$VENV_DIR/bin/activate"

# 6. Install Dependencies
echo -e "📦 checking dependencies..."
pip install -q -r requirements.txt

# 7. Launch
echo -e "🚀 Launching Application..."
echo -e "${GREEN}   Browser will open automatically.${NC}"

# Open browser after 2 seconds
(sleep 2 && open "http://localhost:8000") &

# Run Server
python web_app.py

# Keep terminal open on error
echo ""
echo -e "${RED}Server stopped.${NC}"
read -n 1 -s -r -p "Press any key to close..."
