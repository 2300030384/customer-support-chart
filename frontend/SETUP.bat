@echo off
REM Sentiment Analysis Frontend Setup Script for Windows

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo Sentiment Analysis - Frontend Setup
echo ====================================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/3] Checking Node.js installation...
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✓ Node: !NODE_VERSION!
echo ✓ NPM:  !NPM_VERSION!
echo.

echo [2/3] Installing dependencies...
echo This may take 1-2 minutes...
npm install
if !errorlevel! neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [3/3] Starting development server...
echo Frontend will open at http://localhost:5173
echo.
npm run dev

pause
