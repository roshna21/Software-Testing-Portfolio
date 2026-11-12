#!/usr/bin/env bash
# Runs one full test cycle and stores every report.
#   bash run_tests.sh cycle1 "Cycle 1"
#   bash run_tests.sh cycle2 "Cycle 2"
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
CYCLE="${1:-cycle1}"
TITLE="${2:-Cycle 1}"
OUT="$ROOT/06_Test_Reports/$CYCLE"
mkdir -p "$OUT"
VERSION=$(cd "$ROOT/application" && python3 -c "import reservation_system as r; print(r.__version__)")

echo "== $TITLE: pytest (unit + API + Selenium UI) on build v$VERSION =="
cd "$HERE"
TEST_CYCLE="$CYCLE" python3 -m pytest \
  --junitxml="$OUT/junit.xml" \
  --html="$OUT/test_report.html" --self-contained-html \
  --cov="$ROOT/application/reservation_system" --cov-branch \
  --cov-report=html:"$OUT/coverage" --cov-report=term \
  -p no:cacheprovider -o log_cli=false 2>&1 | grep -v "werkzeug" | tee "$OUT/pytest_console.txt"

rm -f "$OUT/coverage/.gitignore"   # coverage.py hides its HTML report from git by default

echo "== $TITLE: Postman collection via Newman =="
bash "$HERE/postman/run_postman.sh" "$CYCLE" > /dev/null
tail -25 "$ROOT/06_Test_Reports/postman/$CYCLE.txt"

echo "== Generating execution log =="
python3 "$HERE/tools/generate_execution_log.py" "$CYCLE" "$TITLE" "$VERSION"
