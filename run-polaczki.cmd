@echo off
title VOLTAGENT - POLACZKI DEVS ORCHESTRATOR
cd /d "%~dp0knowledge_mood\the_deal_BOYS\app"
echo ====================================================================
echo [VoltAgent] Starting Polaczki Devs Supervisor...
echo [VoltAgent] Listening on http://localhost:3141
echo ====================================================================
npm run dev
pause
