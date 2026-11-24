#!/usr/bin/env bash
# One-command helper for running and demonstrating the project.
#
#   bash demo.sh setup      # first time only: installs everything into .venv
#   bash demo.sh app        # starts the website  -> http://127.0.0.1:5000
#   bash demo.sh selenium   # Selenium opens Chrome and runs the 8 UI tests (visible, slowed down)
#   bash demo.sh tests      # runs all 128 test cases with names, pass/fail
#   bash demo.sh bva        # runs only the Boundary Value Analysis tests (any group: ep, bva, dt, st)
#   bash demo.sh postman    # runs the Postman collection with Newman (needs Node.js)
#   bash demo.sh coverage   # runs all 128 tests with coverage and opens the coverage report
#   bash demo.sh reports    # opens the summary PDF and the HTML test report
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"
PY="$VENV/bin/python"

open_file() {   # open a file with the default app on macOS, Linux or Windows (Git Bash)
  if command -v open >/dev/null 2>&1; then open "$1"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$1" >/dev/null 2>&1 &
  else start "" "$1"; fi
}

need_setup() {
  if [ ! -x "$PY" ]; then echo "Run 'bash demo.sh setup' first."; exit 1; fi
}

case "${1:-help}" in
  setup)
    command -v python3 >/dev/null || { echo "Python 3 is not installed. Install it from python.org first."; exit 1; }
    python3 -m venv "$VENV"
    "$PY" -m pip install --quiet --upgrade pip
    "$PY" -m pip install --quiet -r "$ROOT/application/requirements.txt" -r "$ROOT/05_Test_Automation/requirements.txt"
    echo "Setup done. Next:  bash demo.sh app"
    ;;
  app)
    need_setup
    echo "Starting the Restaurant Table Reservation System at http://127.0.0.1:5000  (Ctrl+C to stop)"
    ( sleep 2; open_file "http://127.0.0.1:5000" ) &
    cd "$ROOT/application" && "$PY" run.py
    ;;
  selenium)
    need_setup
    cd "$ROOT/05_Test_Automation"
    SHOW_BROWSER=1 DEMO_DELAY="${DEMO_DELAY:-1.5}" TEST_CYCLE=demo "$PY" -m pytest ui -v -p no:cacheprovider
    rm -f "$ROOT"/07_Screenshots/selenium/demo_*.png
    ;;
  tests)
    need_setup
    cd "$ROOT/05_Test_Automation" && TEST_CYCLE=demo "$PY" -m pytest -v -p no:cacheprovider -m "not ui" unit api
    rm -f "$ROOT"/07_Screenshots/selenium/demo_*.png
    ;;
  ep|bva|dt|st)
    need_setup
    cd "$ROOT/05_Test_Automation" && "$PY" -m pytest unit -v -p no:cacheprovider -k "TC-$(echo "$1" | tr a-z A-Z)- or TC_$(echo "$1" | tr a-z A-Z)_"
    ;;
  postman)
    command -v newman >/dev/null || { echo "Newman is not installed. Run: npm install -g newman"; exit 1; }
    need_setup
    PATH="$VENV/bin:$PATH" bash "$ROOT/05_Test_Automation/postman/run_postman.sh" demo
    rm -f "$ROOT"/06_Test_Reports/postman/demo.*
    ;;
  coverage)
    need_setup
    cd "$ROOT/05_Test_Automation"
    echo "Running all 128 tests (Selenium in the background) and measuring coverage..."
    TEST_CYCLE=demo "$PY" -m pytest unit api ui -q -p no:cacheprovider \
      --cov="$ROOT/application/reservation_system" --cov-branch \
      --cov-report=term --cov-report=html:"$ROOT/.coverage_demo"
    rm -f "$ROOT"/07_Screenshots/selenium/demo_*.png
    open_file "$ROOT/.coverage_demo/index.html"
    ;;
  reports)
    open_file "$ROOT/06_Test_Reports/Test_Summary_Report.pdf"
    open_file "$ROOT/06_Test_Reports/cycle3/test_report.html"
    ;;
  *)
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac
