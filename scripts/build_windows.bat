@echo off
setlocal
cd /d "%~dp0\.."
if not exist .venv (
  py -3.11 -m venv .venv || py -3 -m venv .venv || exit /b 1
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip || exit /b 1
python -m pip install -r requirements.txt || exit /b 1
python -m pytest || exit /b 1
pyinstaller --onefile --name SeatmapSVGTool seatmap_svg.py || exit /b 1
if not exist release mkdir release
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path dist\SeatmapSVGTool.exe,configs,samples,README.md -DestinationPath release\SeatmapSVGTool-windows-x64.zip -Force" || exit /b 1
echo Built dist\SeatmapSVGTool.exe and release\SeatmapSVGTool-windows-x64.zip
pause
