# Mutation Testing Report

## What is mutation testing? (plain English)

Code coverage tells you *which lines ran* during the tests. It doesn't tell you whether the tests would **notice if a line were wrong**.

Mutation testing checks exactly that. A tool makes one tiny change to the code (a *mutant*): for example `<` becomes `<=`, `and` becomes `or`, or `8` becomes `9`. Then the whole test suite runs:

* a test fails → the mutant is **killed** ✅ (the tests caught the "bug")
* every test still passes → the mutant **survived** ⚠️ (the tests have a blind spot)

Some mutants can't be killed by *any* test because the change makes no difference to behaviour. These are **equivalent mutants** and are excluded from the score.

> **Mutation score = killed ÷ (total − equivalent) × 100**

## Setup

| Item | Detail |
|---|---|
| Tool | `05_Test_Automation/mutation/mutation_test.py` – an AST-based mutation tool written for this project (same operator families as mutmut / PIT) |
| Code mutated | `validators.py` and `service.py` (all business rules) on build v1.1.0 |
| Tests run per mutant | Unit + API suites (`pytest unit api -x`) |
| Mutants generated | 71 (30 in validators, 41 in service) |

| Operator | Meaning | Mutants | Killed | Survived |
|---|---|---:|---:|---:|
| ROR | Relational operator replacement (< ↔ <=, == ↔ !=, in ↔ not in) | 26 | 26 | 0 |
| AOR | Arithmetic operator replacement (+ ↔ -, * → +) | 5 | 5 | 0 |
| LCR | Logical connector replacement (and ↔ or) | 9 | 9 | 0 |
| UOI | Remove `not` | 8 | 8 | 0 |
| CRP | Integer constant + 1 | 23 | 19 | 4 |

## Results

| | Pass 1 (original tests) | Pass 2 (after strengthening tests) |
|---|---:|---:|
| Mutants | 71 | 71 |
| Killed | 64 | 67 |
| Survived | 7 | 4 |
| Equivalent (excluded) | 4 | 4 |
| **Raw score** (killed ÷ total) | 90.1% | 94.4% |
| **Mutation score** (excluding equivalent) | **95.5%** | **100.0%** |

## Analysis of every surviving mutant (pass 1)

| Location | Original code | Mutation | Verdict | Why it survived | Action |
|---|---|---|---|---|---|
| `validators.py`:5 | `MIN_PARTY, MAX_PARTY = 1, 8` | CRP: 8 -> 9 | Real gap → fixed | Limit raised to 9 guests, but TC-BVA-06 still passed because 9 guests were rejected with *no table available* instead of a validation error. | TC-BVA-01/06 now also check the rejection **reason** ("Party size…"). |
| `validators.py`:8 | `LAST_SLOT = time(21, 30)` | CRP: 30 -> 31 | Equivalent | Last slot 21:30 → 21:31. Slots must be on :00/:30, so 21:31 can never be requested – behaviour is identical. | None possible |
| `service.py`:11 | `PEAK_START, PEAK_END = time(19, 0), time(21, 30)` | CRP: 21 -> 22 | Equivalent | Peak end 21:30 → 21:31 / 22:30. No booking can start after 21:30, so the peak result never changes. | None possible |
| `service.py`:11 | `PEAK_START, PEAK_END = time(19, 0), time(21, 30)` | CRP: 30 -> 31 | Equivalent | Peak end 21:30 → 21:31 / 22:30. No booking can start after 21:30, so the peak result never changes. | None possible |
| `service.py`:119 | `if start <= now:` | ROR: <= -> < | Real gap → fixed | `start <= now` → `start < now` lets a guest book a slot that starts at this exact minute. No test used slot = now. | New test **TC-BVA-38**: clock 13:00, book 13:00 today → rejected. |
| `service.py`:72 | `self._ids = count(1001)` | CRP: 1001 -> 1002 | Equivalent | Reservation numbers start at R1002 instead of R1001. Numbering is not a requirement; tests rightly don't depend on it. | None needed |
| `service.py`:104 | `busy = any(r.table_id == table.table_id and r.is_active and ` | LCR: and -> or | Real gap → fixed | `and` → `or` in the availability check marks *every* table busy once any booking exists. TC-API-12 only looked at T1. | TC-API-12 now also asserts the other 7 tables are available. |

## What we learned

* **Coverage alone was misleading.** Statement coverage of `service.py` was already ~99%, yet 3 mutants survived. The lines *ran*, but the tests didn't check the right thing.
* **Check the reason, not just the outcome.** A "rejected" result can come from the wrong rule (TC-BVA-06). Assertions should check *why*.
* **Test the "other side".** When checking that something is busy, also check that the rest is still free (TC-API-12).
* **Boundaries again.** The missing case (slot = now) was another boundary. Mutation testing is effectively an automatic boundary-value review.

Raw data: [`mutation/mutation_results_pass1.json`](mutation/mutation_results_pass1.json), [`mutation/mutation_results_pass2.json`](mutation/mutation_results_pass2.json)
