@echo off
cd /d "%~dp0"
python -m venv venv
python "flaskServer.py"
call "venv\Scripts\activate"
REM Pause to view output
pause
