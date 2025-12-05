# InspiroAI - Automatic App Launcher with venv activation
# এটি automatic venv activate করবে এবং Streamlit app চালাবে

Set-Location "d:\Important File\I\InspiroAI"

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "InspiroAI - Starting Application" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check and create venv if needed
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install/update requirements silently
Write-Host "Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet --disable-pip-version-check 2>&1 | Out-Null
Write-Host "✓ Dependencies ready" -ForegroundColor Green

# Navigate to production folder
Set-Location "production"

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "✓ App Starting..." -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Local URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host "🌐 Network URL: http://192.168.0.169:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run Streamlit app
python -m streamlit run app.py --logger.level=error
