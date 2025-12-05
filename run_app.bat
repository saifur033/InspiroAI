@echo off
REM InspiroAI - Automatic Streamlit App Launcher
REM এটি venv activate করবে এবং app চালাবে

title InspiroAI Application
cd /d "d:\Important File\I\InspiroAI"

REM Check if venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created.
)

REM Activate venv
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo ✓ Virtual environment activated
echo.

REM Navigate to production folder
cd production

REM Run Streamlit app
echo ===================================
echo InspiroAI Starting...
echo ===================================
echo.
echo Local URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo.

python -m streamlit run app.py --logger.level=error

pause

