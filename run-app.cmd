@echo off
title Force Fab
setlocal
cd /d "%~dp0"

where docker >nul 2>&1
if errorlevel 1 (
  echo Docker is not available in this command prompt.
  echo Install Docker Desktop and open a new command prompt.
  exit /b 1
)

if not exist ".env" (
  echo This folder has no .env file.
  echo Copy .env.example to .env, then run this script again.
  exit /b 1
)

rem A variable already set in this window replaces the same name in .env.
set "MODEL_MODE="
set "FABPULSE_API_KEY="

echo Starting the applications from %CD%
docker compose up -d --build
if errorlevel 1 (
  echo Docker Compose did not start the stack.
  exit /b 1
)

echo Waiting for identity on port 8095, Application A on port 8100, and Application B on port 8110.
set /a TRIES=0
:wait
set /a TRIES+=1
if %TRIES% GTR 30 (
  echo The health pages did not answer in time.
  echo Run: docker compose ps
  exit /b 1
)
curl -fsS http://127.0.0.1:8095/health >nul 2>&1
if errorlevel 1 (
  ping -n 3 127.0.0.1 >nul
  goto :wait
)
curl -fsS http://127.0.0.1:8100/health >nul 2>&1
if errorlevel 1 (
  ping -n 3 127.0.0.1 >nul
  goto :wait
)
curl -fsS http://127.0.0.1:8110/health >nul 2>&1
if errorlevel 1 (
  ping -n 3 127.0.0.1 >nul
  goto :wait
)

echo.
echo Identity        http://127.0.0.1:8095
echo Application A   http://127.0.0.1:8100
echo Application B   http://127.0.0.1:8110
echo Lake REST       http://127.0.0.1:8091/health
echo Lake MCP        http://127.0.0.1:8092/health
echo Legacy          http://127.0.0.1:8080/health
echo Source gateway  http://127.0.0.1:8090/health
exit /b 0
