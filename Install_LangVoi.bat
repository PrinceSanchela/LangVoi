@echo off
title LangVoi Voice Studio Pro Setup Wizard
cd /d "%~dp0"
if exist "%~dp0LangVoi_Setup.exe" (
    start "" "%~dp0LangVoi_Setup.exe"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
)
