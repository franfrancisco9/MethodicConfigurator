; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
; This file should be run from ardupilot_methodic_configuratorWinBuild.bat

#define MyAppName "ardupilot_methodic_configurator"
; Note MyAppVersion is defined in ardupilot_methodic_configuratorWinBuild.bat
; #define MyAppVersion {code:GetVersion}
#define MyAppPublisher "Amilcar do Carmo Lucas"
#define MyAppURL "https://github.com/ArduPilot/MethodicConfigurator"
#define MyAppExeName "ardupilot_methodic_configurator.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{F13FF76D-C9FC-47F0-BCE3-A2E0ED2859F6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=..\LICENSE.md
OutputBaseFilename=ardupilot_methodic_configurator_setup_{#MyAppVersion}
Compression=lzma
SolidCompression=yes
ChangesEnvironment=yes

[InstallDelete]
Type: filesandordirs; Name: {commonpf}\{#MyAppName}
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.3.8-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.4.4-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.5.1-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.5.2-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.5.3-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.6.0-DEV-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.5.x-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\diatone_taycan_mxc\4.6.x-params"
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\X11_plus";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\Marmotte5v2";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\Chimera7";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\ReadyToSkyZD550";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\FETtec-5";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\Tarot_X4";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\GazeboIrisWithTargetFollow";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\ArduCopter\Hoverit_X11+";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\Heli\Allister";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\Heli\OMP_M4";
Type: filesandordirs; Name: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates\Rover\AION_R1";
Type: filesandordirs; Name: "{app}\_internal\ardupilot_methodic_configurator\ArduCopter_configuration_steps.json";
Type: filesandordirs; Name: "{app}\_internal\ardupilot_methodic_configurator\ArduPlane_configuration_steps.json";

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "zh_CN"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "it"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\ardupilot_methodic_configurator\dist\ardupilot_methodic_configurator\ardupilot_methodic_configurator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\ardupilot_methodic_configurator\dist\ardupilot_methodic_configurator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "..\ardupilot_methodic_configurator\vehicle_templates\*.*"; DestDir: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\git_hash.txt"; DestDir: "{commonappdata}\.ardupilot_methodic_configurator"; Flags: ignoreversion
Source: "..\windows\ardupilot_methodic_configurator.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\ardupilot_methodic_configurator\ArduPilot_icon.png"; DestDir: "{app}\_internal\ardupilot_methodic_configurator"; Flags: ignoreversion
Source: "..\ardupilot_methodic_configurator\ArduPilot_logo.png"; DestDir: "{app}\_internal\ardupilot_methodic_configurator"; Flags: ignoreversion
Source: "..\ardupilot_methodic_configurator\configuration_steps_*.json"; DestDir: "{app}\_internal\ardupilot_methodic_configurator"; Flags: ignoreversion
Source: "..\LICENSES\*.*"; DestDir: "{app}\LICENSES"; Flags: ignoreversion
Source: "..\credits\*.*"; DestDir: "{app}\credits"; Flags: ignoreversion
Source: "..\ardupilot_methodic_configurator\locale\*.mo"; DestDir: "{app}\_internal\ardupilot_methodic_configurator\locale"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{userappdata}\.ardupilot_methodic_configurator\vehicles"; Flags: uninsneveruninstall

[Icons]
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{userappdata}\.ardupilot_methodic_configurator"; Tasks: desktopicon; IconFilename: "{app}\ardupilot_methodic_configurator.ico"; Languages: en
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{userappdata}\.ardupilot_methodic_configurator"; Tasks: desktopicon; IconFilename: "{app}\ardupilot_methodic_configurator.ico"; Parameters: "--language {language}"; Languages: zh_CN pt de it
Name: "{group}\Documentation"; Filename: "https://github.com/ArduPilot/MethodicConfigurator/blob/master/USERMANUAL.md"
Name: "{group}\Vehicle Templates"; Filename: "{commonappdata}\.ardupilot_methodic_configurator\vehicle_templates"
Name: "{group}\ArduPilot Methodic Configurator Forum"; Filename: "https://discuss.ardupilot.org/t/new-ardupilot-methodic-configurator-gui/115038/"
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{userappdata}\.ardupilot_methodic_configurator"; IconFilename: "{app}\ardupilot_methodic_configurator.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; Parameters: "--language {language}"

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "PATH"; ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath('{app}')
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment";  ValueName: "PATH"; ValueData: "{app}"; Flags: uninsdeletevalue

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(
    HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result :=
    (Pos(';' + UpperCase(Param) + ';', ';' + UpperCase(OrigPath) + ';') = 0) and
    (Pos(';' + UpperCase(Param) + '\;', ';' + UpperCase(OrigPath) + ';') = 0);
end;

var
  Paths: string;

const
  EnvironmentKey = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment';
  SMTO_ABORTIFHUNG = 2;
  WM_WININICHANGE = $001A;
  WM_SETTINGCHANGE = WM_WININICHANGE;

type
  WPARAM = UINT_PTR;
  LPARAM = INT_PTR;
  LRESULT = INT_PTR;

function SendTextMessageTimeout(hWnd: HWND; Msg: UINT;
  wParam: WPARAM; lParam: PAnsiChar; fuFlags: UINT;
  uTimeout: UINT; out lpdwResult: DWORD): LRESULT;
  external 'SendMessageTimeoutA@user32.dll stdcall';

procedure SaveOldPath();
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE, EnvironmentKey, 'Path', Paths) then
  begin
    Log('PATH not found');
  end else begin
    Log(Format('Old Path saved as [%s]', [Paths]));
  end;
end;

procedure RemovePath(Path: string);
var
  P: Integer;
begin
  Log(Format('Prepare to remove from Old PATH [%s]', [Paths]));

  P := Pos(';' + Uppercase(Path) + ';', ';' + Uppercase(Paths) + ';');
  if P = 0 then
  begin
    Log(Format('Path [%s] not found in PATH', [Path]));
  end
    else
  begin
    Delete(Paths, P - 1, Length(Path) + 1);
    Log(Format('Path [%s] removed from PATH => [%s]', [Path, Paths]));

    if RegWriteExpandStringValue(HKEY_LOCAL_MACHINE, EnvironmentKey, 'Path', Paths) then
    begin
      Log('PATH written');
    end
      else
    begin
      Log('Error writing PATH');
    end;
  end;
end;

procedure RefreshEnvironment;
var
  S: AnsiString;
  MsgResult: DWORD;
begin
  S := 'Environment';
  SendTextMessageTimeout(HWND_BROADCAST, WM_SETTINGCHANGE, 0,
    PAnsiChar(S), SMTO_ABORTIFHUNG, 5000, MsgResult);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep =  usUninstall then
  begin
    SaveOldPath();
  end;
  if CurUninstallStep = usPostUninstall then
  begin
    RemovePath(ExpandConstant('{app}'));
    RefreshEnvironment();
  end;
end;
