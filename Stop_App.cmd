@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Force Fab
cd /d "%~dp0"

rem Stops the Windows processes started by Start_App.cmd. Leaves any other program on these ports alone.
if exist ".run\*.pid" (
  for %%F in (.run\*.pid) do (
    set "PID="
    set /p PID=<"%%F"
    if defined PID taskkill /F /T /PID !PID! >nul 2>&1
    del /f "%%F" >nul 2>&1
  )
)

powershell -NoProfile -Command "$ports=8095,8091,8092,8100,8110; $needles=@('apps.identity.server:app','rest_server:app','mcp_server:app','apps.app_a.server:app','apps.app_b.server:app'); $conns=Get-NetTCPConnection -LocalPort $ports -State Listen -ErrorAction SilentlyContinue; foreach ($c in $conns) { $proc=Get-CimInstance Win32_Process -Filter ('ProcessId=' + $c.OwningProcess); if ($proc) { $line=[string]$proc.CommandLine; foreach ($n in $needles) { if ($line.Contains($n)) { taskkill /F /T /PID $c.OwningProcess | Out-Null; break } } } }"

echo Stopped.
exit /b 0
