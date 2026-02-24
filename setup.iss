; AI拍 - 安装程序脚本
; 使用 Inno Setup 编译
; 下载地址：https://jrsoftware.org/isdl.php

[Setup]
AppName=AI拍
AppVersion=1.0.0
AppPublisher=Dream工作室
AppPublisherURL=https://example.com
AppSupportURL=https://example.com
AppUpdatesURL=https://example.com
DefaultDirName={autopf}\AI拍
DefaultGroupName=AI拍
LicenseFile=
OutputBaseFilename=AI拍_安装程序
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\AI拍.exe
ChangesAssociations=no
ChangesEnvironment=no
InternalCompressLevel=max
CreateAppDir=yes
CreateUninstallRegKey=yes
OutputDir=output

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加图标:"; Flags: unchecked

[Files]
Source: "dist\AI拍\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\AI拍"; Filename: "{app}\AI拍.exe"
Name: "{group}\卸载 AI拍"; Filename: "{uninstallexe}"
Name: "{commondesktop}\AI拍"; Filename: "{app}\AI拍.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AI拍.exe"; Description: "启动 AI拍"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{commonappdata}\AI拍"
Type: filesandordirs; Name: "{userappdata}\AI拍"
