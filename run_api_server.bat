@echo off
REM ============================================
REM InspiroAI Flask API Server Launcher
REM ============================================
REM This script starts the Flask API server
REM

echo ============================================
echo InspiroAI - Flask API Server
echo ============================================
echo.

REM Check if venv exists
if not exist ".venv\" (
    echo Error: Virtual environment not found!
    echo Please create venv first: python -m venv .venv
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting Flask API server...
echo.
echo Server will run at: http://localhost:5000
echo.
echo To test the API:
echo   1. Open another terminal
echo   2. Run: python production\test_endpoints.py
echo.
echo To open web UI:
echo   1. Open production/index.html in your browser
echo   2. Or visit: http://localhost:5000/index.html
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

cd production
python api_server.py

pause
