@echo off
setlocal

set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend\app"
set "PYTHON=%ROOT%backend\venv\Scripts\python.exe"
set "PORT=4149"

if not exist "%PYTHON%" (
    echo [!] Nie znaleziono venv w backend\venv\
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:PORT='4149'; Start-Process -FilePath '%PYTHON%' -ArgumentList 'main.py' -WorkingDirectory '%BACKEND%' -WindowStyle Hidden"

timeout /t 2 /nobreak > nul
start "" "C:\Users\Bonzo2\AppData\Local\Chromium\Application\chrome.exe" "--new-tab http://localhost:4149 --profile-directory=Default"
exit /b 0
