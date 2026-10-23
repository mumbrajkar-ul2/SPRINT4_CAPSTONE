@echo off
title Force Fab
cd /d "%~dp0"
where wsl >nul 2>&1
if errorlevel 1 (
  echo Force Fab on this PC needs WSL. run-app.cmd is the Docker path.
  exit /b 1
)
for /f "delims=" %%I in ('wsl wslpath "%CD%"') do set "WSLROOT=%%I"
echo Stopping Force Fab before copying source.
wsl -e bash -lc "cd '%WSLROOT%' && bash run_local.sh stop"
wsl -e bash -lc "cd '%WSLROOT%' && bash run_local.sh sync-source '%WSLROOT%'"
if errorlevel 1 exit /b 1
wsl -e bash -lc "cd '%WSLROOT%' && bash run_local.sh start"
if errorlevel 1 exit /b 1
start "" http://127.0.0.1:8100
start "" http://127.0.0.1:8110
exit /b 0
