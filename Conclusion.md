# Conclusion

## What we did

We took the **Restaurant Table Reservation System** through a complete testing life cycle:

1. **Understood the application.** We listed 8 modules and wrote 13 testable requirements (R1–R13).
2. **Planned.** We wrote a test plan with scope, approach, environment, entry and exit criteria, and risks.
3. **Designed 128 test cases** using Equivalence Partitioning, Boundary Value Analysis, Decision Tables and State Transition testing, plus scenario tests for table allocation, the REST API and the web UI. A traceability matrix links every requirement to its tests.
4. **Automated every test case** with pytest (unit and API), Selenium WebDriver (UI, headless Chrome) and a Postman collection run by Newman.
5. **Executed three cycles.** Cycle 1 on v1.0.0, then retest and regression on v1.1.0 (Cycle 2), then a final regression after improving the tests (Cycle 3).
6. **Logged, tracked and closed 9 defects.** Each has steps to reproduce, evidence, root cause, fix commit and retest result.
7. **Measured test quality** with code coverage (93%) and mutation testing (100% after improvement).

## What we found

| | Cycle 1 (v1.0.0) | Cycle 3 (v1.1.0) |
|---|---|---|
| Test cases passed | 114 / 127 (89.8%) | 128 / 128 (100%) |
| Postman assertions passed | 25 / 31 | 31 / 31 |
| Open defects | 9 | 0 |

The most serious defect was **DEF-003: double booking**. If a group booked a table for 18:30 and another group already had it at 19:00, the system gave the same table to both. The overlap check only looked in one direction. A customer would never notice this while booking. It would only show up when two groups arrived for the same table. Boundary value tests at 30-minute steps around the existing booking found it immediately.

Other defects were classic edge mistakes: 8 guests rejected (`<` instead of `<=`), 11-digit phone numbers accepted (regex not anchored), 31 days allowed instead of 30, and Friday counted as the weekend. There was also a missing guard that let a finished meal be "cancelled", and a usability bug where the form erased the user's input after an error.

## What we learned

* **Each technique finds a different kind of bug.** BVA found the off-by-one errors, decision tables found the wrong combination (Friday + peak), state transition found the forbidden move (COMPLETED → CANCELLED), and only the browser test found the form-clearing problem.
* **Boundary value analysis gave the best return:** it was involved in 5 of the 9 defects.
* **Automation pays off during regression.** Re-running all 128 test cases after the fixes took about 10 seconds. The same check by hand would have taken hours.
* **High coverage does not mean strong tests.** At 99% coverage of the booking engine, mutation testing still found 3 assertions that would have missed real bugs.
* **Repeatable tests need control over time and data.** We used a frozen clock, a fresh application for every test, and explicit waits in Selenium.
* **Good defect reports speed up fixing.** Each report named the requirement, the failing test and the evidence, so every fix was small and targeted (one commit per defect).

## Final verdict

All exit criteria in the test plan are met. Build **v1.1.0 is recommended for release**. Next steps would be a persistent database with integration tests, load testing for peak dinner hours, and security testing of the API.
