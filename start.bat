@echo off

rem Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

rem Install necessary packages using pip
pip install pyserial pandas keyboard openpyxl

rem Open your Python script
python serialData.py

pause