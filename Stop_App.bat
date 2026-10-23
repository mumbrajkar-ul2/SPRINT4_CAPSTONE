@echo off
title Force Fab
cd /d "%~dp0"
where wsl >nul 2>&1
if errorlevel 1 (
  echo Force Fab on this PC needs WSL.
  exit /b 1
)
for /f "delims=" %%I in ('wsl wslpath "%CD%"') do set "WSLROOT=%%I"
wsl -e bash -lc "cd '%WSLROOT%' && bash run_local.sh stop"
exit /b 0
