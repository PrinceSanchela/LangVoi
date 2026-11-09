@echo off
title Launching LangVoi Studio Setup...
cd /d "%~dp0"

:: Redirect TEMP to local folder to bypass Windows Smart App Control User Temp policy (Error 4551)
set "CUSTOM_TEMP=%LOCALAPPDATA%\Programs\LangVoiInstallerTemp"
if not exist "%CUSTOM_TEMP%" mkdir "%CUSTOM_TEMP%"
set "TEMP=%CUSTOM_TEMP%"
set "TMP=%CUSTOM_TEMP%"

if exist "installer_output\LangVoi_Studio_Setup_v2.2.exe" (
    start "" "installer_output\LangVoi_Studio_Setup_v2.2.exe"
) else if exist "LangVoi_Studio_Setup_v2.2.exe" (
    start "" "LangVoi_Studio_Setup_v2.2.exe"
) else (
    echo [INFO] LangVoi_Studio_Setup_v2.2.exe not found in current directory.
    echo Please compile installer_script.iss using Inno Setup Compiler.
    pause
)
