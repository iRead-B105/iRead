@echo off
setlocal
cd /d "%~dp0"

where docker >nul 2>nul || (
  echo [ERROR] Docker Desktop is required.
  exit /b 1
)

docker compose ps --status running backend | findstr /i "backend" >nul || (
  echo [ERROR] The backend container is not running. Run start-all-local.bat first.
  exit /b 1
)

echo Restoring the QA demo database and persistent assets...
docker compose exec backend ./gradlew qaDemoReset --no-daemon
if errorlevel 1 (
  echo [ERROR] QA demo reset failed.
  exit /b 1
)

echo [OK] QA demo reset completed. Login: test@test.com / qwer1234
