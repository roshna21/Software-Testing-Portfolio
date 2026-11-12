#!/usr/bin/env bash
# Starts the app in test mode, runs the Postman collection with Newman, then stops the app.
# Usage:  bash run_postman.sh [report-name]
# Needs:  npm install -g newman newman-reporter-htmlextra   (htmlextra is optional)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
NAME="${1:-newman_report}"
OUT="$ROOT/06_Test_Reports/postman"
mkdir -p "$OUT"

cd "$ROOT/application"
RESERVATION_FIXED_NOW=2026-11-16T10:00 RESERVATION_ENABLE_RESET=1 PORT=5000 python3 run.py >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
for _ in $(seq 1 30); do curl -s http://127.0.0.1:5000/api/health >/dev/null && break; sleep 0.3; done

REPORTERS="cli,junit,json"
newman run "$HERE/Restaurant_Reservation_API.postman_collection.json" \
  -e "$HERE/local.postman_environment.json" \
  -r "$REPORTERS" \
  --reporter-junit-export "$OUT/$NAME.xml" \
  --reporter-json-export "$OUT/$NAME.json" \
  --color off | sed "s/\x1b\[[0-9;]*m//g" | tee "$OUT/$NAME.txt" || true
