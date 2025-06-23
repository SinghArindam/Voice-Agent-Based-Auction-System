@echo off
set "VENV_DIR=.venv"
set "REQUIREMENTS_FILE=.\backend\requirements.txt"
set "BACKEND_DIR=backend"

REM Check if virtual environment already exists
if not exist "%VENV_DIR%\" (
    echo Virtual environment not found. Creating...
    python -m venv "%VENV_DIR%"
) else (
    echo Virtual environment already exists. Skipping creation.
)

echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate"

echo Installing/Updating dependencies...
pip install -r "%REQUIREMENTS_FILE%"

echo Running backend server...
cd "%BACKEND_DIR%"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload