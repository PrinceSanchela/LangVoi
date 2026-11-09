<#
.SYNOPSIS
    LangVoi Voice Studio Pro - Native Windows Installer Script
    Installs software to %LOCALAPPDATA%\Programs\LangVoi, creates Desktop & Start Menu shortcuts,
    and registers an Uninstaller in Windows Installed Apps.
#>

$AppName = "LangVoi Voice Studio Pro"
$AppVersion = "2.2"
$Publisher = "Prince Sanchela"
$SourceDir = $PSScriptRoot
if (-not $SourceDir) { $SourceDir = Get-Location }

$InstallDir = "$env:LOCALAPPDATA\Programs\LangVoi"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       LangVoi Voice Studio Pro - Windows Installer Wizard  " -ForegroundColor Yellow
Write-Host "              Created & Engineered by Prince Sanchela       " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Target Directory: $InstallDir" -ForegroundColor Gray

# -------------------------------------------------------------
# 1. CREATE TARGET INSTALLATION DIRECTORY
# -------------------------------------------------------------
try {
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    }
} catch {
    Write-Host "[ERROR] Could not create installation directory: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# -------------------------------------------------------------
# 2. COPY APPLICATION FILES & ASSETS
# -------------------------------------------------------------
Write-Host "`n[1/4] Copying application files..." -ForegroundColor Green
$FilesToCopy = @("LangVoi_Studio.exe", "LangVoi_Studio.bat", "Install_LangVoi.bat", "run.py", "main.py", "requirements.txt", "README.md", "LICENSE.txt")
foreach ($f in $FilesToCopy) {
    $src = Join-Path $SourceDir $f
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $InstallDir -Force -ErrorAction SilentlyContinue
    }
}

$DirsToCopy = @("app", "core", "samples", "assets")
foreach ($d in $DirsToCopy) {
    $src = Join-Path $SourceDir $d
    $dst = Join-Path $InstallDir $d
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# -------------------------------------------------------------
# 3. CREATE UNINSTALLER SCRIPT
# -------------------------------------------------------------
$UninstallScript = Join-Path $InstallDir "Uninstall.bat"
$UninstallContent = @"
@echo off
title Uninstalling LangVoi Voice Studio Pro...
echo Removing shortcuts and files...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Remove-Item -Force -ErrorAction SilentlyContinue '`$env:USERPROFILE\Desktop\LangVoi Voice Studio Pro.lnk'; Remove-Item -Force -ErrorAction SilentlyContinue '`$env:OneDrive\Desktop\LangVoi Voice Studio Pro.lnk'; Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '`$env:APPDATA\Microsoft\Windows\Start Menu\Programs\LangVoi'; Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '$InstallDir'; Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\LangVoi' -ErrorAction SilentlyContinue"
echo LangVoi Voice Studio Pro has been completely uninstalled.
pause
"@
Set-Content -Path $UninstallScript -Value $UninstallContent -ErrorAction SilentlyContinue

# -------------------------------------------------------------
# 4. RESOLVE ACCURATE DESKTOP PATH & CREATE SHORTCUTS
# -------------------------------------------------------------
Write-Host "[2/4] Creating Windows Shortcuts..." -ForegroundColor Green

function Get-ActualDesktopPath {
    # 1. Check SpecialFolder DesktopDirectory
    try {
        $p = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::DesktopDirectory)
        if ($p -and (Test-Path $p)) { return $p }
    } catch {}

    # 2. Check User Shell Folders registry
    try {
        $regP = (Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' -ErrorAction SilentlyContinue).Desktop
        if ($regP) {
            $expanded = [System.Environment]::ExpandEnvironmentVariables($regP)
            if (Test-Path $expanded) { return $expanded }
        }
    } catch {}

    # 3. Check OneDrive Desktop
    if ($env:OneDrive -and (Test-Path "$env:OneDrive\Desktop")) {
        return "$env:OneDrive\Desktop"
    }
    if ($env:USERPROFILE -and (Test-Path "$env:USERPROFILE\OneDrive\Desktop")) {
        return "$env:USERPROFILE\OneDrive\Desktop"
    }

    # 4. Check Standard Desktop
    if ($env:USERPROFILE -and (Test-Path "$env:USERPROFILE\Desktop")) {
        return "$env:USERPROFILE\Desktop"
    }

    # 5. Check Public Desktop
    if ($env:PUBLIC -and (Test-Path "$env:PUBLIC\Desktop")) {
        return "$env:PUBLIC\Desktop"
    }

    # 6. Fallback: Create directory at $env:USERPROFILE\Desktop
    $fb = "$env:USERPROFILE\Desktop"
    try {
        New-Item -ItemType Directory -Force -Path $fb -ErrorAction SilentlyContinue | Out-Null
        return $fb
    } catch {
        return $null
    }
}

try {
    $WshShell = New-Object -ComObject WScript.Shell

    # A. Desktop Shortcut
    $DesktopDir = Get-ActualDesktopPath
    if ($DesktopDir) {
        if (-not (Test-Path $DesktopDir)) {
            New-Item -ItemType Directory -Force -Path $DesktopDir -ErrorAction SilentlyContinue | Out-Null
        }
        $DesktopShortcutPath = Join-Path $DesktopDir "LangVoi Voice Studio Pro.lnk"
        try {
            $Shortcut = $WshShell.CreateShortcut($DesktopShortcutPath)
            $Shortcut.TargetPath = "$InstallDir\LangVoi_Studio.exe"
            $Shortcut.WorkingDirectory = "$InstallDir"
            $Shortcut.Description = "LangVoi Voice Studio Pro - HD Audio Engineering & Worldwide Language Detection"
            if (Test-Path "$InstallDir\assets\app_icon.ico") {
                $Shortcut.IconLocation = "$InstallDir\assets\app_icon.ico,0"
            }
            $Shortcut.Save()
            Write-Host "  + Created Desktop Shortcut: $DesktopShortcutPath" -ForegroundColor Gray
        } catch {
            Write-Host "  ! Note: Could not write to desktop path ($($_.Exception.Message))" -ForegroundColor Yellow
        }
    }

    # B. Start Menu Shortcut
    $StartMenuDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\LangVoi"
    if (-not (Test-Path $StartMenuDir)) {
        New-Item -ItemType Directory -Force -Path $StartMenuDir -ErrorAction SilentlyContinue | Out-Null
    }
    $StartMenuShortcutPath = Join-Path $StartMenuDir "LangVoi Voice Studio Pro.lnk"
    try {
        $StartShortcut = $WshShell.CreateShortcut($StartMenuShortcutPath)
        $StartShortcut.TargetPath = "$InstallDir\LangVoi_Studio.exe"
        $StartShortcut.WorkingDirectory = "$InstallDir"
        $StartShortcut.Description = "LangVoi Voice Studio Pro"
        if (Test-Path "$InstallDir\assets\app_icon.ico") {
            $StartShortcut.IconLocation = "$InstallDir\assets\app_icon.ico,0"
        }
        $StartShortcut.Save()
        Write-Host "  + Created Start Menu Shortcut: $StartMenuShortcutPath" -ForegroundColor Gray
    } catch {
        Write-Host "  ! Note: Could not write Start Menu shortcut ($($_.Exception.Message))" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ! Non-fatal shortcut notice: $($_.Exception.Message)" -ForegroundColor Yellow
}

# -------------------------------------------------------------
# 5. REGISTER IN WINDOWS SETTINGS / CONTROL PANEL (UNINSTALL ENTRY)
# -------------------------------------------------------------
Write-Host "[3/4] Registering in Windows Add/Remove Programs..." -ForegroundColor Green
try {
    $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\LangVoi"
    if (-not (Test-Path $RegPath)) {
        New-Item -Path $RegPath -Force -ErrorAction SilentlyContinue | Out-Null
    }
    Set-ItemProperty -Path $RegPath -Name "DisplayName" -Value "$AppName" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path $RegPath -Name "DisplayVersion" -Value "$AppVersion" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path $RegPath -Name "Publisher" -Value "$Publisher" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path $RegPath -Name "InstallLocation" -Value "$InstallDir" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path $RegPath -Name "UninstallString" -Value "`"$UninstallScript`"" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path $RegPath -Name "DisplayIcon" -Value "$InstallDir\assets\app_icon.ico" -ErrorAction SilentlyContinue
} catch {
    Write-Host "  ! Non-fatal registry notice: $($_.Exception.Message)" -ForegroundColor Yellow
}

# -------------------------------------------------------------
# 6. VERIFY PYTHON ENVIRONMENT & DEPENDENCIES
# -------------------------------------------------------------
Write-Host "[4/4] Verifying Python Environment..." -ForegroundColor Green
try {
    Start-Process -FilePath "python" -ArgumentList "-m pip install -r `"$InstallDir\requirements.txt`"" -Wait -NoNewWindow -ErrorAction SilentlyContinue
} catch {
    Write-Host "  ! Note: Please verify requirements.txt manually if needed." -ForegroundColor Yellow
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host " [SUCCESS] LangVoi Voice Studio Pro Installed Successfully! " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "• Publisher: Prince Sanchela"
Write-Host "• Installed Directory: $InstallDir"
Write-Host "• Registered in Windows Settings: Installed Apps"
Write-Host "`nLaunching LangVoi Voice Studio Pro..." -ForegroundColor Yellow

try {
    Start-Process -FilePath "$InstallDir\LangVoi_Studio.exe" -ErrorAction SilentlyContinue
} catch {
    Write-Host "Launch command initiated."
}
