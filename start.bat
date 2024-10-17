@echo off
REM Navigate to the directory containing the script
cd /d "%~dp0"

REM Activate the virtual environment
call myenv\Scripts\activate

REM Run the Python script
python ui.py

REM Pause the script so the console window doesn't close immediately
pause
