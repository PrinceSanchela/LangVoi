@echo off
title Build LangVoi Studio Native Executables
cd /d "%~dp0\.."

set "CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%CSC%" (
    set "CSC=C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
)

if not exist "%CSC%" (
    echo [ERROR] Microsoft .NET C# Compiler csc.exe was not found.
    pause
    exit /b 1
)

echo =====================================================================
echo   Compiling LangVoi Studio Native Win32 Launchers and Installers
echo                 Architect: Prince Sanchela
echo =====================================================================
echo.

echo [1/2] Compiling LangVoi_Studio.exe (Native Windows Launcher)...
"%CSC%" /target:winexe /win32icon:assets\app_icon.ico /out:LangVoi_Studio.exe launcher.cs
if errorlevel 1 (
    echo [ERROR] Failed to compile LangVoi_Studio.exe
    pause
    exit /b 1
)
echo [OK] LangVoi_Studio.exe compiled successfully.

echo.
echo [2/2] Compiling LangVoi_Setup.exe (Native Desktop Setup Wizard)...
"%CSC%" /target:winexe /win32icon:assets\app_icon.ico /out:LangVoi_Setup.exe installer.cs
if errorlevel 1 (
    echo [ERROR] Failed to compile LangVoi_Setup.exe
    pause
    exit /b 1
)
echo [OK] LangVoi_Setup.exe compiled successfully.

echo.
echo =====================================================================
echo All native binaries compiled successfully!
echo =====================================================================
