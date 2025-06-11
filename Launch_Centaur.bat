@echo off
REM AI Qube Centaur Ecosystem - Desktop Launcher
REM Double-click this file to start the Centaur Control Center

echo.
echo ====================================================
echo   🏛️ AI Qube Centaur Ecosystem Control Center
echo ====================================================
echo.
echo Starting the desktop application...
echo.

REM Change to the correct directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if required dependencies are installed
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ❌ tkinter not available! Installing dependencies...
    pip install tkinter
)

REM Launch the GUI application
echo ✅ Launching Centaur Control Center...
python centaur_launcher.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error.
    pause
)
