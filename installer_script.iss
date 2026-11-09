; =====================================================================
; LangVoi Voice Studio Pro - Inno Setup 7 Standalone Installer Script
; Architect: Prince Sanchela
; Outputs: release_binaries\LangVoi_Setup.exe
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

; Classic Inno Setup Multi-Step Wizard
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=LICENSE.txt

; Flexible Privileges (works without admin or with admin)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Output directly to the git-ignored release_binaries folder
OutputDir=release_binaries
OutputBaseFilename=LangVoi_Setup
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Compression & 64-bit native styling
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Standalone compiled binaries (ZERO source code files)
Source: "dist\LangVoi_Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
