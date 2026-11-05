@echo off
cd /d "%~dp0"

:: 윈도우 한글 인코딩(CP949) 충돌 방지 (UTF-8 강제 활성화)
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: 1. 로그 디렉토리 생성
if not exist "logs" mkdir logs

:: 2. Streamlit 서버 구동 (0.0.0.0 바인딩 및 headless 모드)
".venv\Scripts\python.exe" -m streamlit run app.py --server.headless true --server.port 8501 --server.address 0.0.0.0 >> "logs\streamlit_stdout.log" 2>&1
