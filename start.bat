@echo off
echo ========================================
echo   Real Estate Lead Management System
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create a .env file with your API keys.
    echo See .env.example for reference.
    pause
    exit /b 1
)

echo Starting all components...
echo.

REM Start Telegram Bot
echo [1/3] Starting Telegram Bot...
start "Telegram Bot" cmd /k "cd /d %CD% && echo TELEGRAM BOT && python src/bot.py"

timeout /t 2 /nobreak >nul

REM Start Backend API
echo [2/3] Starting Backend API...
start "Backend API" cmd /k "cd /d %CD%\backend && echo BACKEND API && python app.py"

timeout /t 2 /nobreak >nul

REM Start Frontend Server
echo [3/3] Starting Frontend Dashboard...
start "Frontend Dashboard" cmd /k "cd /d %CD%\frontend && echo FRONTEND DASHBOARD && python -m http.server 8080"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   All components started successfully!
echo ========================================
echo.
echo Access the dashboard at: http://localhost:8080
echo.
echo To stop all components, close all command windows.
echo.

REM Open browser
echo Opening dashboard in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080

echo.
echo Press any key to exit this window (components will keep running)...
pause >nul
