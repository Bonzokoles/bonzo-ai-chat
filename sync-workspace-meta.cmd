@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync-workspace-meta.ps1"
exit /b 0
