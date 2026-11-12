# Test Execution

Each log lists every test case with its input, **expected result**, **actual result**, pass/fail status and the defect it exposed. The logs are generated from the automated runs (`05_Test_Automation/tools/generate_execution_log.py`). CSV copies open directly in Excel.

| Cycle | Build | Purpose | Result | Log |
|---|---|---|---|---|
| 1 | v1.0.0 | First full execution | 114 / 127 passed, 13 failed → 9 defects | [Markdown](Cycle_1_Execution_Log.md) · [CSV](Cycle_1_Execution_Log.csv) |
| 2 | v1.1.0 | Retest of fixed defects + full regression | 127 / 127 passed | [Markdown](Cycle_2_Execution_Log.md) · [CSV](Cycle_2_Execution_Log.csv) |
| 3 | v1.1.0 | Final regression after mutation-testing improvements (+TC-BVA-38) | 128 / 128 passed | [Markdown](Cycle_3_Execution_Log.md) · [CSV](Cycle_3_Execution_Log.csv) |

All runs use a frozen clock (**Mon 16 Nov 2026, 10:00**), so date-based results are the same on any day.
