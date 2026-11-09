; =====================================================================
; LangVoi Voice Studio Pro - Inno Setup 6 Professional Installer Script
; Created & Engineered by: Prince Sanchela
; Compiles: LangVoi_Studio_Setup_v2.2.exe
; =====================================================================

#define MyAppName "LangVoi Voice Studio Pro"
#define MyAppVersion "2.2"
#define MyAppPublisher "Prince Sanchela"
#define MyAppCopyright "Copyright (C) 2026 Prince Sanchela. All Rights Reserved."
#define MyAppURL "https://github.com/PrinceSanchela/LangVoi"
#define MyAppExeName "LangVoi_Studio.exe"

[Setup]
AppId={{F4D2A83C-112E-497B-9B21-081977C38E22}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppCopyright={#MyAppCopyright}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
PrivilegesRequired=admin
OutputDir=installer_output
OutputBaseFilename=LangVoi_Studio_Setup_v2.2
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\assets\app_icon.ico
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Main Executable & Launchers
Source: "{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LangVoi_Studio.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "Install_LangVoi.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "install.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "run.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "Prince_Sanchela.cer"; DestDir: "{app}"; Flags: ignoreversion
Source: "launcher.cs"; DestDir: "{app}"; Flags: ignoreversion

; Codebase Modules & Assets
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "app\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "samples\*"; DestDir: "{app}\samples"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu Shortcut
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; WorkingDir: "{app}"
; Desktop Shortcut (Asks the user via the desktopicon task, checked by default)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
; Auto-Launch after installation completes
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
