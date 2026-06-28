@echo off
setlocal EnableExtensions

REM SeatmapSVGTool Windows packaging script.
REM Run from project root or double-click this file.
cd /d "%~dp0\.."

set "APP_NAME=SeatmapSVGTool"
set "EXE_PATH=dist\%APP_NAME%.exe"
set "ZIP_PATH=release\%APP_NAME%-windows-x64.zip"
set "PYINSTALLER_ADD_DATA=configs;configs"

call :main
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo.
  echo [ERROR] Build failed with exit code %EXIT_CODE%.
  echo Please review the messages above.
  pause
  exit /b %EXIT_CODE%
)

echo.
echo [OK] Build finished successfully.
echo [OK] Executable: %EXE_PATH%
echo [OK] Release zip: %ZIP_PATH%
pause
exit /b 0

:main
echo [INFO] Working directory: %CD%

if not exist "requirements.txt" (
  echo [ERROR] requirements.txt not found. Please run this script from the project checkout.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creating virtual environment .venv ...
  py -3.11 -m venv .venv
  if errorlevel 1 (
    echo [WARN] Python 3.11 launcher failed; trying default py -3 ...
    py -3 -m venv .venv
    if errorlevel 1 (
      echo [WARN] py launcher failed; trying python ...
      python -m venv .venv
      if errorlevel 1 exit /b 1
    )
  )
) else (
  echo [INFO] Reusing existing .venv.
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

REM requirements.txt already lists pytest and pyinstaller, but install them explicitly too
REM so the packaging contract remains true even if requirements.txt is customized.
python -m pip install -r requirements.txt pytest pyinstaller
if errorlevel 1 exit /b 1

python -m pytest
if errorlevel 1 exit /b 1

if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if not exist "release" mkdir "release"
if exist "release\package" rmdir /s /q "release\package"
if exist "%ZIP_PATH%" del /f /q "%ZIP_PATH%"

pyinstaller --clean --windowed --onefile --name "%APP_NAME%" --add-data "%PYINSTALLER_ADD_DATA%" seatmap_svg_gui.py
if errorlevel 1 exit /b 1

if not exist "%EXE_PATH%" (
  echo [ERROR] Expected executable was not created: %EXE_PATH%
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop'; " ^
  "New-Item -ItemType Directory -Force release\package\configs,release\package\scripts,release\package\output | Out-Null; " ^
  "Copy-Item '%EXE_PATH%' 'release\package\SeatmapSVGTool.exe' -Force; " ^
  "Copy-Item 'configs\default.yaml' 'release\package\configs\default.yaml' -Force; " ^
  "Copy-Item 'README.md' 'release\package\README.md' -Force; " ^
  "Copy-Item 'scripts\run_sample.bat' 'release\package\scripts\run_sample.bat' -Force; " ^
  "New-Item -ItemType File -Force release\package\output\.gitkeep | Out-Null; " ^
  "Compress-Archive -Path 'release\package\*' -DestinationPath '%ZIP_PATH%' -Force"
if errorlevel 1 exit /b 1

exit /b 0
