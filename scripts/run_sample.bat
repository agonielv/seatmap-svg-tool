@echo off
setlocal
cd /d "%~dp0\.."
if not exist .venv (
  py -3.11 -m venv .venv || py -3 -m venv .venv || exit /b 1
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt || exit /b 1
python seatmap_svg.py --config configs\default.yaml || exit /b 1
echo Generated output\seatmap.svg and output\report.json
pause
