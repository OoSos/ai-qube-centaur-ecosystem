@echo off
REM Create Desktop Shortcut for AI Qube Centaur Ecosystem

echo Creating desktop shortcut for Centaur Control Center...

set "SCRIPT_DIR=%~dp0"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\🏛️ Centaur Control Center.lnk"

REM Create VBScript to generate shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT_PATH%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%Launch_Centaur.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "AI Qube Centaur Ecosystem Control Center" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,21" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Execute VBScript
cscript CreateShortcut.vbs >nul

REM Clean up
del CreateShortcut.vbs

echo ✅ Desktop shortcut created successfully!
echo 🚀 Double-click "🏛️ Centaur Control Center" on your desktop to launch the application.
pause
