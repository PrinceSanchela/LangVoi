@echo off
title Launching LangVoi Studio Setup...
cd /d "%~dp0"

:: Redirect TEMP to local folder to bypass Windows Smart App Control User Temp policy (Error 4551)
set "CUSTOM_TEMP=%LOCALAPPDATA%\Programs\LangVoiInstallerTemp"
if not exist "%CUSTOM_TEMP%" mkdir "%CUSTOM_TEMP%"
set "TEMP=%CUSTOM_TEMP%"
set "TMP=%CUSTOM_TEMP%"

if exist "%~dp0LangVoi_Setup.exe" (
    start "" "%~dp0LangVoi_Setup.exe"
) else if exist "%~dp0installer_output\LangVoi_Studio_Setup_v2.2.exe" (
    start "" "%~dp0installer_output\LangVoi_Studio_Setup_v2.2.exe"
) else (
    echo [INFO] LangVoi_Setup.exe not found in current directory.
    pause
)
