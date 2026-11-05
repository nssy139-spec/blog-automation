@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================================
echo  [리치유니 무인 블로그 자동화 공장] 백그라운드 구동 시작
echo ========================================================

:: 8501 포트 사용 여부 확인
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %ERRORLEVEL% equ 0 (
    echo [안내] 이미 8501 포트에서 서비스가 정상 구동 중입니다.
    echo 접속 주소: http://localhost:8501
    goto :OPEN_BROWSER
)

echo 백그라운드 프로세스로 무인 공장을 가동합니다...
powershell -NoProfile -ExecutionPolicy Bypass -File .\start_background.ps1

echo 서버 기동 상태 확인 중 (약 3초 소요)...
timeout /t 3 /nobreak >nul

netstat -ano | findstr :8501 | findstr LISTENING >nul
if %ERRORLEVEL% equ 0 (
    echo.
    echo [성공] 무인 블로그 자동화 공장이 백그라운드에서 정상 가동되었습니다!
    echo.
    echo  - 로컬 웹 조종기 접속 : http://localhost:8501
    echo  - 외부 바인딩 포트    : 0.0.0.0:8501
    echo.
    goto :OPEN_BROWSER
) else (
    echo [안내] 서버가 초기화 중입니다. 잠시 후 브라우저에서 http://localhost:8501 에 접속해 주세요.
    goto :END
)

:OPEN_BROWSER
start http://localhost:8501

:END
echo ========================================================
pause
