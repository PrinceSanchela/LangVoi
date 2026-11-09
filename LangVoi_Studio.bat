@echo off
title LangVoi Voice Studio Pro - Native Desktop Edition
cd /d "%~dp0"
echo =====================================================================
echo           Starting LangVoi Voice Studio Pro (Native Desktop)
echo        Worldwide Language Detection & Acoustic Voice Analyzer
echo =====================================================================
echo.
python run.py
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while launching LangVoi Voice Studio.
    echo Please make sure Python 3.10+ is installed and on your PATH.
    pause
)
