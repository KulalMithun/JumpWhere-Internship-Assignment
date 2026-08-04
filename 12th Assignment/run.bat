@echo off
echo ===================================================
echo Starting PrivateGPT Document Chat Application...
echo ===================================================

:: 1. Copy .env if not present
if not exist "backend\.env" (
    echo Creating backend\.env from .env.example...
    copy .env.example backend\.env
)

:: 2. Start Backend in a new window
echo Starting FastAPI Backend on http://localhost:8000 ...
start "PrivateGPT Backend" cmd /k "cd backend && pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: 3. Start Frontend in a new window
echo Starting Next.js Frontend on http://localhost:3000 ...
start "PrivateGPT Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ===================================================
echo Backend API Docs: http://localhost:8000/docs
echo Frontend App:     http://localhost:3000
echo ===================================================
echo Setup complete! You can safely close this terminal. 
echo (Please keep the separate "PrivateGPT Backend" and "PrivateGPT Frontend" windows open.)
echo ===================================================
