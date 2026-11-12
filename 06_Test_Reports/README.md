# Test Reports

| Report | Description |
|---|---|
| [**Test_Summary_Report.pdf**](Test_Summary_Report.pdf) / [.md](Test_Summary_Report.md) | Overall test execution summary: results, defects, coverage, mutation score, exit criteria, recommendation |
| [Mutation_Testing_Report.md](Mutation_Testing_Report.md) | Mutation testing method, score and analysis of every surviving mutant |
| `cycle1/`, `cycle2/`, `cycle3/` | Per cycle: `test_report.html` (pytest-html), `coverage/index.html` (coverage), `junit.xml`, `pytest_console.txt` |
| `postman/` | Newman output for each cycle (`.txt` console, `.xml` JUnit, `.json` full run) |
| `mutation/` | Raw mutation results (pass 1 and pass 2) |
| `charts/` | Charts used in the summary report |

The HTML reports are self-contained. Download and open them in a browser, or view them in the screenshots under `07_Screenshots/reports/`.
