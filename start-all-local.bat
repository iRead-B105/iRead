@echo off
setlocal
title iRead local launcher
cd /d "%~dp0"

set "AUTH_JWT_SECRET=iread-local-demo-only-jwt-secret-2026-07-29"
set "BACKEND_URL=http://127.0.0.1:8080"

echo [1/5] Checking required commands...
where docker >nul 2>nul || (
  echo [ERROR] Docker was not found. Install or start Docker Desktop first.
  pause
  exit /b 1
)
where npm >nul 2>nul || (
  echo [ERROR] Node.js/npm was not found.
  pause
  exit /b 1
)

echo Cleaning old local app processes on ports 5173, 5174, and 8765...
for %%P in (5173 5174 8765) do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$listeners = Get-NetTCPConnection -State Listen -LocalPort %%P -ErrorAction SilentlyContinue; foreach ($listener in $listeners) { Write-Host ('Stopping PID {0} on port %%P' -f $listener.OwningProcess); Stop-Process -Id $listener.OwningProcess -Force -ErrorAction SilentlyContinue }"
)

echo [2/5] Starting MySQL, Redis, AI mock, and Spring backend in Docker...
docker compose -f "services\backend\docker-compose.yml" --profile demo up -d --build
if errorlevel 1 (
  echo [ERROR] Docker services failed to start. Check that Docker Desktop is running.
  pause
  exit /b 1
)

echo [3/5] Preparing the local eye-tracking FastAPI server...
if not exist "services\eyetracking\.venv\Scripts\python.exe" (
  where py >nul 2>nul || (
    echo [ERROR] Python launcher was not found.
    pause
    exit /b 1
  )
  py -3 -m venv "services\eyetracking\.venv"
  if errorlevel 1 (
    echo [ERROR] Failed to create the eye-tracking Python environment.
    pause
    exit /b 1
  )
  "services\eyetracking\.venv\Scripts\python.exe" -m pip install -r "services\eyetracking\requirements.txt"
  if errorlevel 1 (
    echo [ERROR] Failed to install eye-tracking Python dependencies.
    pause
    exit /b 1
  )
)

echo [4/5] Checking frontend dependencies...
if not exist "services\frontend-app\node_modules\.bin\vite.cmd" (
  pushd "services\frontend-app"
  call npm install
  if errorlevel 1 (
    popd
    echo [ERROR] Failed to install learner frontend dependencies.
    pause
    exit /b 1
  )
  popd
)
if not exist "services\frontend-web\node_modules\.bin\vite.cmd" (
  pushd "services\frontend-web"
  where pnpm >nul 2>nul
  if errorlevel 1 (
    call npm install
  ) else (
    call pnpm install
  )
  if errorlevel 1 (
    popd
    echo [ERROR] Failed to install teacher frontend dependencies.
    pause
    exit /b 1
  )
  popd
)

echo [5/5] Opening local application windows...
pushd "services\eyetracking"
start "iRead Eye Tracker - 8765" cmd /k "".venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8765"
popd

pushd "services\frontend-app"
start "iRead Learner Vue - 5173" cmd /k "set VITE_LEARNER_DATA_SOURCE=api&& set VITE_BACKEND_URL=%BACKEND_URL%&& npm run dev -- --host 127.0.0.1 --port 5173 --strictPort"
popd

pushd "services\frontend-web"
start "iRead Teacher Vue - 5174" cmd /k "set VITE_AUTH_SOURCE=api&& set VITE_DATA_SOURCE=api&& set VITE_BACKEND_URL=%BACKEND_URL%&& npm run dev -- --host 127.0.0.1 --port 5174 --strictPort"
popd

echo.
echo iRead local stack launch requested:
echo   Learner UI : http://127.0.0.1:5173/learner/login
echo   Teacher UI : http://127.0.0.1:5174/
echo   Backend    : http://127.0.0.1:8080/
echo   Eye tracker: http://127.0.0.1:8765/
echo.
echo Each non-Docker application runs in its own terminal window.
echo Close those windows to stop the local apps.
echo To stop Docker services, run:
echo   docker compose -f services\backend\docker-compose.yml --profile demo down
pause
