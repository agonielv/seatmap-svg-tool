@echo off
setlocal
cd /d "%~dp0\.."

if exist "SeatmapSVGTool.exe" (
  "SeatmapSVGTool.exe" --config configs\default.yaml || goto :error
) else if exist "dist\SeatmapSVGTool.exe" (
  "dist\SeatmapSVGTool.exe" --config configs\default.yaml || goto :error
) else (
  if not exist .venv (
    py -3.11 -m venv .venv || py -3 -m venv .venv || goto :error
  )
  call .venv\Scripts\activate.bat || goto :error
  python -m pip install -r requirements.txt || goto :error
  python seatmap_svg.py --config configs\default.yaml || goto :error
)

echo Generated output\seatmap.svg and output\report.json
pause
exit /b 0

:error
echo.
echo [ERROR] Sample run failed. Please review the messages above.
pause
exit /b 1
