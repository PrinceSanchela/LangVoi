; =====================================================================
; LangVoi Voice Studio Pro - Inno Setup Professional Installer Script
; Created & Engineered by: Prince Sanchela
; Compiles: LangVoi_Setup.exe (Classic Step-by-Step Setup Wizard)
; =====================================================================

#define MyAppName "LangVoi Voice Studio Pro"
#define MyAppVersion "2.2.0"
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

; Classic Step-by-Step Wizard Pages (Welcome -> License -> Folder -> Start Menu -> Tasks -> Install -> Finish)
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=LICENSE.txt

; Flexible user privileges: Works for both standard users and administrators
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Output configuration
OutputDir=.
OutputBaseFilename=LangVoi_Setup
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\assets\app_icon.ico
UninstallDisplayName={#MyAppName}

; Compression & Modern Styling
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardSizePercent=100
ArchitecturesInstallIn64BitMode=x64compatible

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
Source: "launcher.cs"; DestDir: "{app}"; Flags: ignoreversion

; Codebase Modules & Assets
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "app\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "samples\*"; DestDir: "{app}\samples"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu Shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
; Desktop Shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
; Auto-Launch after installation completes with checkbox
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
