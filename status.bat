@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================================
echo  [리치유니 무인 블로그 자동화 공장] 현재 가동 상태 점검
echo ========================================================

netstat -ano | findstr :8501 | findstr LISTENING >nul
if %ERRORLEVEL% equ 0 (
    echo [상태] 정상 가동 중 (RUNNING)
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (
        echo [PID] %%a
    )
    echo [접속 URL] http://localhost:8501
) else (
    echo [상태] 중지됨 (STOPPED)
)

echo.
echo [최근 작업 로그 (logs\automation.log 마지막 10줄)]
if exist "logs\automation.log" (
    powershell -Command "Get-Content -Path logs\automation.log -Tail 10"
) else (
    echo 작업 로그 파일이 아직 생성되지 않았습니다. (첫 발행 시 기록됨)
)

echo ========================================================
pause
