# 윈도우 UTF-8 인코딩 강제
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $baseDir

$pythonExe = Join-Path $baseDir ".venv\Scripts\python.exe"
$appPath = Join-Path $baseDir "app.py"

$argList = "-m streamlit run `"$appPath`" --server.headless true --server.port 8501 --server.address 0.0.0.0"

Start-Process -FilePath $pythonExe -ArgumentList $argList -WindowStyle Hidden
