#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

if ! docker compose ps --status running backend | grep -q backend; then
  echo "[ERROR] The backend container is not running. Run docker compose up -d first." >&2
  exit 1
fi

echo "Restoring the QA demo database and persistent assets..."
docker compose exec backend ./gradlew qaDemoReset --no-daemon
echo "[OK] QA demo reset completed. Login: test@test.com / qwer1234"
