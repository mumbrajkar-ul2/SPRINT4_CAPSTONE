@echo off
setlocal EnableExtensions
title Force Fab
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo Python is not available in this command prompt.
  pause
  exit /b 1
)

if not exist ".run" mkdir ".run"

echo Stopping Force Fab before starting it.
call "%~dp0Stop_App.cmd"
if errorlevel 1 goto :fail

if not exist ".run\cookie_secret" (
  python -c "import secrets; print(secrets.token_hex(32), end='')" > ".run\cookie_secret"
  if errorlevel 1 goto :fail
)
set /p FF_COOKIE_SECRET=<".run\cookie_secret"
set "FF_IDP_PUBLIC_URL=http://127.0.0.1:8095"
set "FF_IDP_URL=%FF_IDP_PUBLIC_URL%"
set "FF_STATE_DIR=%CD%\.run\identity"
set "FF_DEMO_HINTS=1"
set "FF_ENV=local"
if not defined FABPULSE_API_KEY set "FABPULSE_API_KEY=local-demo-only"
if not defined MODEL_MODE set "MODEL_MODE=replay"

call :start_one identity 8095 apps.identity.server:app "%CD%;%CD%\context-lake"
if errorlevel 1 goto :fail
call :start_one lake-rest 8091 rest_server:app "%CD%;%CD%\context-lake"
if errorlevel 1 goto :fail
call :start_one lake-mcp 8092 mcp_server:app "%CD%;%CD%\context-lake"
if errorlevel 1 goto :fail
call :start_one app-a 8100 apps.app_a.server:app "%CD%;%CD%\context-lake;%CD%\fabpulse-legacy-workshop-v8-Semiconductor\fabpulse-legacy"
if errorlevel 1 goto :fail
call :start_one app-b 8110 apps.app_b.server:app "%CD%;%CD%\context-lake"
if errorlevel 1 goto :fail

echo Force Fab is up.
echo Application A  http://127.0.0.1:8100
echo Application B  http://127.0.0.1:8110
echo Identity       http://127.0.0.1:8095
start "" http://127.0.0.1:8100
start "" http://127.0.0.1:8110
exit /b 0

:start_one
python -c "import socket,sys; s=socket.socket(); s.settimeout(0.2); r=s.connect_ex(('127.0.0.1', int(sys.argv[1]))); s.close(); sys.exit(0 if r==0 else 1)" %~2
if not errorlevel 1 (
  echo Port %~2 is already in use. Stop the stack before starting %~1.
  exit /b 1
)
set "PYTHONPATH=%~4"
start "Force Fab %~1" /MIN /D "%~dp0" cmd /c "python -m uvicorn %~3 --host 127.0.0.1 --port %~2 > .run\%~1.log 2>&1"
call :wait_port %~2 %~1
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "$p = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -like '*uvicorn %~3 --host 127.0.0.1 --port %~2*' } | Select-Object -First 1; if (-not $p) { exit 1 }; Set-Content -Path '%~dp0.run\%~1.pid' -Value $p.ProcessId"
if errorlevel 1 (
  echo %~1 is listening on port %~2, but the process id was not saved.
  exit /b 1
)
echo %~1 is listening on port %~2.
exit /b 0

:wait_port
set /a TRIES=0
:wait_loop
set /a TRIES+=1
if %TRIES% GTR 40 (
  echo %~2 did not open port %~1. The log is .run\%~2.log.
  exit /b 1
)
python -c "import socket,sys; s=socket.socket(); s.settimeout(0.2); r=s.connect_ex(('127.0.0.1', int(sys.argv[1]))); s.close(); sys.exit(0 if r==0 else 1)" %~1
if errorlevel 1 (
  ping -n 2 127.0.0.1 >nul
  goto :wait_loop
)
exit /b 0

:fail
echo Force Fab did not start.
pause
exit /b 1
