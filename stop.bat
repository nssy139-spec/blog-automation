@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================================
echo  [리치유니 무인 블로그 자동화 공장] 백그라운드 프로세스 종료
echo ========================================================

set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (
    echo [종료 중] 8501 포트 PID %%a 프로세스를 종료합니다...
    taskkill /F /PID %%a >nul 2>&1
    set FOUND=1
)

if %FOUND% equ 1 (
    echo [완료] 무인 블로그 자동화 공장 서버가 성공적으로 종료되었습니다.
) else (
    echo [안내] 8501 포트에서 실행 중인 프로세스가 없습니다.
)

echo ========================================================
pause
