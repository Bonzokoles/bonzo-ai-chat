@echo off
setlocal
set "ROOT=Z:\36_chambers\The_Buch"
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%ROOT%\START_EASTWOOD_OPS.ps1"
exit /b 0
