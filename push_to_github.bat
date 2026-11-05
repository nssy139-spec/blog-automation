@echo off
cd /d "%~dp0"

echo ========================================================
echo  GitHub Upload Start...
echo ========================================================
echo.

git push -u origin main

echo.
echo ========================================================
echo  Done! Please press any key to close this window.
echo ========================================================
pause
