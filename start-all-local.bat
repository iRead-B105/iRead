@echo off
setlocal
title iRead full local stack
cd /d "%~dp0"

where docker >nul 2>nul || (
  echo [ERROR] Docker Desktop is required.
  pause
  exit /b 1
)

echo [1/3] Starting database, backend, AI, learner UI, and teacher UI...
docker compose up -d --build
if errorlevel 1 (
  echo [ERROR] Docker stack failed to start.
  pause
  exit /b 1
)

echo [2/3] Preparing the Windows eye-tracker bridge...
if not exist "services\eyetracking\.venv\Scripts\python.exe" (
  where py >nul 2>nul || (
    echo [ERROR] Python launcher was not found.
    pause
    exit /b 1
  )
  py -3 -m venv "services\eyetracking\.venv"
  "services\eyetracking\.venv\Scripts\python.exe" -m pip install -r "services\eyetracking\requirements.txt"
  if errorlevel 1 (
    echo [ERROR] Eye-tracker dependencies failed to install.
    pause
    exit /b 1
  )
)

echo [3/3] Starting the eye-tracker bridge on port 8765...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":8765 .*LISTENING"') do taskkill /PID %%P /F >nul 2>nul
pushd "services\eyetracking"
start "iRead Eye Tracker - 8765" cmd /k "".venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8765"
popd

echo.
echo Learner UI : http://127.0.0.1:5174/learner/login
echo Teacher UI : http://127.0.0.1:5173/
echo Backend    : http://127.0.0.1:8080/
echo AI         : http://127.0.0.1:8081/health
echo Eye tracker: http://127.0.0.1:8765/api/status
echo.
echo The eye tracker bridge auto-starts native Tobii mode when the learner app connects.
echo If Tobii is not available, the learner app can still use mouse fallback.
pause
