@echo off
REM Sentiment Analysis Backend Setup Script for Windows

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo Sentiment Analysis - Backend Setup
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Found: !PYTHON_VERSION!
echo.

echo [2/4] Creating virtual environment...
python -m venv venv
if !errorlevel! neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo [4/4] Installing dependencies...
echo This may take 2-3 minutes...
pip install --upgrade pip
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo ====================================================
echo Setup Complete!
echo ====================================================
echo.
echo Next steps:
echo 1. Create/edit .env file with your MongoDB URL
echo    - Copy from MongoDB Atlas connection string
echo    - Format: mongodb+srv://user:pass@cluster/sentiment_db
echo.
echo 2. Run backend with:
echo    python -m uvicorn main:app --reload
echo.
echo 3. Access API documentation at:
echo    http://localhost:8000/docs
echo.
echo ====================================================
echo.

pause
