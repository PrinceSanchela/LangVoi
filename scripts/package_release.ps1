<#
.SYNOPSIS
    Packages LangVoi Voice Studio Pro into a clean distribution ZIP archive.
    Excludes private keys (.pfx), Python caches (__pycache__), and temporary build files.
#>

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

$ProgressPreference = 'SilentlyContinue'

$ZipName = "LangVoi_Studio_v2.2_Package.zip"
$ZipPath = Join-Path $RootDir $ZipName

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Packaging LangVoi Voice Studio Pro for Public Release     " -ForegroundColor Yellow
Write-Host "             Architect: Prince Sanchela                     " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Clean old cache and build files
Write-Host "`n[1/3] Cleaning bytecode caches and temporary files..." -ForegroundColor Gray
Get-ChildItem -Path $RootDir -Recurse -Include "__pycache__", "*.pyc", "*.pyo" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 2. Files and Directories to include in public release
$ItemsToInclude = @(
    "LangVoi_Studio.exe",
    "LangVoi_Setup.exe",
    "LangVoi_Studio.bat",
    "Install_LangVoi.bat",
    "Run_Setup.bat",
    "install.ps1",
    "run.py",
    "main.py",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "README.md",
    "LICENSE.txt",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "installer_script.iss",
    "app",
    "core",
    "assets",
    "samples",
    "scripts"
)

# 3. Create fresh zip archive
Write-Host "[2/3] Compressing release package to: $ZipName..." -ForegroundColor Green
if (Test-Path $ZipPath) {
    Remove-Item -Force $ZipPath
}

Compress-Archive -Path $ItemsToInclude -DestinationPath $ZipPath -CompressionLevel Optimal

$ZipSize = (Get-Item $ZipPath).Length / 1MB
Write-Host "[3/3] Package created successfully!" -ForegroundColor Green
Write-Host "File: $ZipPath" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($ZipSize, 2)) MB" -ForegroundColor Yellow
Write-Host "`nReady for upload to GitHub Releases, Google Drive, or your website!`n" -ForegroundColor Green
