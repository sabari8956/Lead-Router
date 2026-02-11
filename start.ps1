# Real Estate Lead Management System - Startup Script
# This script starts all three components of the system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Real Estate Lead Management System   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your API keys." -ForegroundColor Yellow
    Write-Host "See .env.example for reference." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Starting all components..." -ForegroundColor Green
Write-Host ""

# Start Telegram Bot
Write-Host "[1/3] Starting Telegram Bot..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host 'TELEGRAM BOT' -ForegroundColor Cyan; python src/bot.py"

Start-Sleep -Seconds 2

# Start Backend API
Write-Host "[2/3] Starting Backend API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; Write-Host 'BACKEND API' -ForegroundColor Cyan; python app.py"

Start-Sleep -Seconds 2

# Start Frontend Server
Write-Host "[3/3] Starting Frontend Dashboard..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host 'FRONTEND DASHBOARD' -ForegroundColor Cyan; python -m http.server 8080"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All components started successfully!  " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the dashboard at: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop all components, close all PowerShell windows." -ForegroundColor Yellow
Write-Host ""

# Open browser
Write-Host "Opening dashboard in browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "Press any key to exit this window (components will keep running)..." -ForegroundColor Gray
pause
