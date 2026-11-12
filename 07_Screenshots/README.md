# Screenshots

## Application under test (Selenium, cycle 3 – build v1.1.0)

| Test | Screenshot |
|---|---|
| TC-UI-01 Home page / booking form | ![](selenium/cycle3_TC-UI-01_home_page.png) |
| TC-UI-02 Booking confirmed | ![](selenium/cycle3_TC-UI-02_booking_confirmed.png) |
| TC-UI-03 Invalid phone error | ![](selenium/cycle3_TC-UI-03_invalid_phone_error.png) |
| TC-UI-05 Reservation cancelled with refund | ![](selenium/cycle3_TC-UI-05_cancelled.png) |
| TC-UI-06 Staff view – seated / completed | ![](selenium/cycle3_TC-UI-06a_staff_seated.png) ![](selenium/cycle3_TC-UI-06b_staff_completed.png) |
| TC-UI-07 Weekend peak deposit ₹900 | ![](selenium/cycle3_TC-UI-07_weekend_deposit.png) |
| TC-UI-08 Unknown reservation | ![](selenium/cycle3_TC-UI-08_not_found.png) |

## Defect evidence – before and after the fix

| Defect | Cycle 1 (v1.0.0 – bug) | Cycle 2 (v1.1.0 – fixed) |
|---|---|---|
| DEF-008 Form loses input after error | ![](selenium/cycle1_TC-UI-04_form_after_error.png) | ![](selenium/cycle2_TC-UI-04_form_after_error.png) |
| DEF-009 Staff table border | ![](selenium/cycle1_TC-UI-06a_staff_seated.png) | ![](selenium/cycle2_TC-UI-06a_staff_seated.png) |

## Test reports

| Report | Cycle 1 (v1.0.0) | Cycle 3 (v1.1.0) |
|---|---|---|
| pytest console | ![](reports/cycle1_pytest_terminal.png) | ![](reports/cycle3_pytest_terminal.png) |
| pytest-html report | ![](reports/cycle1_pytest_html_report.png) | ![](reports/cycle3_pytest_html_report.png) |
| Coverage report | ![](reports/cycle1_coverage_report.png) | ![](reports/cycle3_coverage_report.png) |
| Newman (Postman) | ![](reports/cycle1_newman_terminal.png) | ![](reports/cycle3_newman_terminal.png) |

## Diagrams

Architecture and state-transition diagrams: [`01_Test_Plan/diagrams/`](../01_Test_Plan/diagrams/)
