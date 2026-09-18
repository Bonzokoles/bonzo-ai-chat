@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "LOGDIR=%~dp0logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%" >nul 2>&1
set "LOG=%LOGDIR%\autostart.log"

echo.>>"%LOG%"
echo [%date% %time%] ===== run-jimbo-always start =====>>"%LOG%"
echo [%date% %time%] Script dir: %~dp0>>"%LOG%"

rem Wait after login so Podman/network drives/env have time to initialize.
timeout /t 60 /nobreak >nul

set "PYTHON=%~dp0backend\venv\Scripts\python.exe"
set "READY=0"
for /L %%I in (1,1,12) do (
  if exist "%PYTHON%" (
    set "READY=1"
    echo [%date% %time%] Dependency ready on attempt %%I>>"%LOG%"
    goto :ready
  )
  echo [%date% %time%] Attempt %%I: waiting for %PYTHON%>>"%LOG%"
  timeout /t 5 /nobreak >nul
)

:ready
if "%READY%"=="0" (
  echo [%date% %time%] ERROR: Python venv not found after retries: %PYTHON%>>"%LOG%"
  exit /b 1
)

if exist "%~dp0sync-workspace-meta.cmd" (
  echo [%date% %time%] Running sync-workspace-meta.cmd>>"%LOG%"
  call "%~dp0sync-workspace-meta.cmd" >>"%LOG%" 2>&1
) else (
  echo [%date% %time%] sync-workspace-meta.cmd not found, skipping.>>"%LOG%"
)

echo [%date% %time%] Starting start.bat (backend + browser)>>"%LOG%"
call "%~dp0start.bat" >>"%LOG%" 2>&1

set "EXITCODE=%ERRORLEVEL%"
echo [%date% %time%] start.bat exited with code %EXITCODE%>>"%LOG%"
echo [%date% %time%] ===== run-jimbo-always end =====>>"%LOG%"
exit /b %EXITCODE%
