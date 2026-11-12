# Test Automation

| Folder / file | Tool | What it tests | Count |
|---|---|---|---|
| `unit/test_equivalence_partitioning.py` | pytest | Input classes (R1–R6, R11) | 29 |
| `unit/test_boundary_value_analysis.py` | pytest | Range edges, overlap, refund window | 38 |
| `unit/test_decision_tables.py` | pytest | Deposit and cancellation rules | 17 |
| `unit/test_state_transition.py` | pytest | Reservation life cycle | 16 |
| `unit/test_table_allocation.py` | pytest | Table selection | 7 |
| `api/test_api.py` | pytest + Flask test client | REST endpoints and status codes | 13 |
| `ui/test_ui_selenium.py` | **Selenium WebDriver** (Chrome headless) | Booking, errors, cancellation, staff flow | 8 |
| `postman/` | **Postman + Newman** | API contract from outside the app | 15 requests / 31 assertions |
| `mutation/mutation_test.py` | **Mutation testing** (custom AST tool) | Strength of the unit + API tests | 71 mutants |
| `tools/generate_execution_log.py` | Python | Turns JUnit/Newman XML into the execution log | – |
| `run_tests.sh` | Bash | Runs a full cycle and stores every report | – |

## Run

```bash
pip install -r requirements.txt
cd 05_Test_Automation

pytest                         # all 128 tests
pytest unit                    # unit only
pytest -k "TC-BVA-05"          # one test case by ID
pytest -m ui                   # Selenium only

bash postman/run_postman.sh    # Postman collection via Newman
python mutation/mutation_test.py
bash run_tests.sh cycle3 "Cycle 3"   # everything + reports
```

You can also import `postman/Restaurant_Reservation_API.postman_collection.json` and `local.postman_environment.json` into the Postman app. Start the server in test mode first:
`RESERVATION_FIXED_NOW=2026-11-16T10:00 RESERVATION_ENABLE_RESET=1 python application/run.py`

## Design choices

* **Test ID in every test name.** Each test maps 1-to-1 to a designed test case.
* **Expected and actual results recorded** with `record_property`, so the execution log is generated, never typed by hand.
* **Frozen clock** (`conftest.py`) so date rules are repeatable.
* **Fresh app per test**, so no test depends on another test's data.
* **Explicit waits** (`staleness_of`) in Selenium. These fixed early flaky failures where the old page was read before the reload.
