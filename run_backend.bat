@echo off
echo ============================================================
echo  AI Resume Matcher - FastAPI Backend
echo ============================================================
echo Starting on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
call venv\Scripts\activate.bat
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
pause
