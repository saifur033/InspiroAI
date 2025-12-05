#!/usr/bin/env pwsh
<#
.SYNOPSIS
InspiroAI Flask API Server Launcher
.DESCRIPTION
Starts the Flask API server with venv activation
#>

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "InspiroAI - Flask API Server" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
$venvPath = ".\.venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Create venv first: python -m venv .venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow

# Activate venv
& "$venvPath\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starting Flask API server..." -ForegroundColor Green
Write-Host ""
Write-Host "Server will run at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "To test the API:" -ForegroundColor Yellow
Write-Host "  1. Open another terminal" -ForegroundColor White
Write-Host "  2. Run: python production\test_endpoints.py" -ForegroundColor White
Write-Host ""
Write-Host "To open web UI:" -ForegroundColor Yellow
Write-Host "  1. Open production/index.html in your browser" -ForegroundColor White
Write-Host "  2. Or visit: http://localhost:5000/index.html" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location production
& python api_server.py

Read-Host "Press Enter to exit"
