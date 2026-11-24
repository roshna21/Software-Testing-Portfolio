# Test Case Design

| Document | Technique | Test cases |
|---|---|---|
| [01_Equivalence_Partitioning.md](01_Equivalence_Partitioning.md) | Equivalence Partitioning | 29 (TC-EP-01 … 29) |
| [02_Boundary_Value_Analysis.md](02_Boundary_Value_Analysis.md) | Boundary Value Analysis | 38 (TC-BVA-01 … 38) |
| [03_Decision_Table.md](03_Decision_Table.md) | Decision Table | 17 (TC-DT-01 … 17) |
| [04_State_Transition.md](04_State_Transition.md) | State Transition | 16 (TC-ST-01 … 16) |
| [05_Use_Case_UI_API_Tests.md](05_Use_Case_UI_API_Tests.md) | Use-case / scenario (allocation, API, UI) | 7 + 13 + 8 = 28 |
| **Total (black-box + scenario)** | | **128** (+ 15 Postman requests) |
| [06_White_Box_Testing.md](06_White_Box_Testing.md) | **White-box:** statement coverage + branch coverage | 6 (TC-WB-01 … 06) |

## Requirement traceability matrix

Shows that every requirement is covered by at least one test.

| Req | Description | Test cases |
|---|---|---|
| R1 | Name 2–50 letters | EP-01…05, BVA-07…13 |
| R2 | 10-digit mobile 6–9 | EP-06…10, BVA-14…16, API-04, UI-03, PM-05 |
| R3 | Optional email | EP-11…13 |
| R4 | Party 1–8 | EP-14…18, BVA-01…06, PM-06, WB-03…06 |
| R5 | Date window 30 days | EP-19…22, BVA-17…22 |
| R6 | Time 11:00–21:30, :00/:30, not passed | EP-23…27, BVA-23…28, BVA-38 |
| R7 | Smallest free table, 90 min, no overlap | BVA-29…34, TA-01…07, ST-15, ST-16, API-12, UI-02, PM-07, PM-08, PM-14 |
| R8 | Deposit rule | DT-01…11, UI-07, WB-01, WB-02 |
| R9 | Status life cycle | ST-01…14, API-09, API-10, UI-06, PM-10…12 |
| R10 | Cancellation refund | BVA-35…37, DT-12…17, API-11, UI-05 |
| R11 | One booking per phone per day | EP-28, EP-29, API-13, PM-09 |
| R12 | API status codes | API-01…13, PM-01…14 |
| R13 | Form shows error and keeps input | UI-03, UI-04 |

Each test case ID appears in the automated test's name, so `pytest -k TC-BVA-05` runs exactly that case.
