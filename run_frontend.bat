@echo off
echo ============================================================
echo  AI Resume Matcher - Streamlit HR Dashboard
echo ============================================================
echo Starting on http://localhost:8501
echo Make sure the FastAPI backend is already running!
echo.
call venv\Scripts\activate.bat
streamlit run frontend/streamlit_app.py --server.port 8501
pause
