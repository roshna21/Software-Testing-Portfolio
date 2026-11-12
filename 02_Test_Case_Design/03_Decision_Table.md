# Decision Table Testing

## What it is (plain English)

When the result depends on a **combination** of conditions, we list every combination in a table and write one test per column (called a *rule*). With 3 yes/no conditions there are 2 × 2 × 2 = **8 rules**. This makes sure no combination is forgotten.

---

## Decision Table 1 – Deposit (R8)

**Conditions**
- C1: Party size is 6 or more?
- C2: Booking is on a weekend (Saturday or Sunday)?
- C3: Booking time is peak (19:00 – 21:30)?

**Actions**
- A1: Charge ₹100 per guest
- A2: Charge ₹300 flat
- A3: No deposit

| | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **C1** Party ≥ 6 | Y | Y | Y | Y | N | N | N | N |
| **C2** Weekend | Y | Y | N | N | Y | Y | N | N |
| **C3** Peak time | Y | N | Y | N | Y | N | Y | N |
| **A1** ₹100 × guests | ✔ | ✔ | ✔ | ✔ | | | | |
| **A2** ₹300 flat | ✔ | | | | ✔ | | | |
| **A3** No deposit | | | | | | ✔ | ✔ | ✔ |
| **Deposit (party 6 / party 2)** | **₹900** | **₹600** | **₹600** | **₹600** | **₹300** | **₹0** | **₹0** | **₹0** |
| Test case | TC-DT-01 | TC-DT-02 | TC-DT-03 | TC-DT-04 | TC-DT-05 | TC-DT-06 | TC-DT-07 | TC-DT-08 |

### Test cases

| TC ID | Rule | Party | Day | Time | Expected deposit |
|---|---|---|---|---|---|
| TC-DT-01 | 1 | 6 | Sat 21 Nov | 19:00 | ₹900 |
| TC-DT-02 | 2 | 6 | Sat 21 Nov | 13:00 | ₹600 |
| TC-DT-03 | 3 | 6 | Wed 18 Nov | 19:00 | ₹600 |
| TC-DT-04 | 4 | 6 | Wed 18 Nov | 13:00 | ₹600 |
| TC-DT-05 | 5 | 2 | Sat 21 Nov | 20:00 | ₹300 |
| TC-DT-06 | 6 | 2 | Sat 21 Nov | 13:00 | ₹0 |
| TC-DT-07 | 7 | 2 | Wed 18 Nov | 19:30 | ₹0 |
| TC-DT-08 | 8 | 2 | Wed 18 Nov | 13:00 | ₹0 |

Extra checks on the edges of each condition (EP/BVA applied inside the decision table):

| TC ID | What it checks | Party | Day | Time | Expected |
|---|---|---|---|---|---|
| TC-DT-09 | Friday is **not** a weekend (C2 = N) | 2 | Fri 20 Nov | 19:00 | ₹0 |
| TC-DT-10 | Sunday + last peak slot (C2 = Y, C3 = Y) | 2 | Sun 22 Nov | 21:30 | ₹300 |
| TC-DT-11 | Just before peak (C3 = N) | 2 | Sat 21 Nov | 18:30 | ₹0 |

---

## Decision Table 2 – Cancellation and refund (R10)

**Conditions**
- C1: Reservation status is CONFIRMED?
- C2: Cancelled 2 hours or more before the slot?
- C3: A deposit was paid?

| | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
|---|:-:|:-:|:-:|:-:|:-:|
| **C1** Status CONFIRMED | Y | Y | Y | Y | N |
| **C2** Notice ≥ 2 h | Y | N | Y | N | – |
| **C3** Deposit > 0 | Y | Y | N | N | – |
| Cancel the booking | ✔ | ✔ | ✔ | ✔ | |
| Refund full deposit | ✔ | | | | |
| Refund ₹0 | | ✔ | ✔ | ✔ | |
| Refuse cancellation | | | | | ✔ |

"–" means "doesn't matter". Rule 5 collapses 4 combinations because a non-confirmed booking is always refused.

| TC ID | Rule | Setup (slot today 15:00) | Cancel at | Expected |
|---|---|---|---|---|
| TC-DT-12 | 1 | Party 6, deposit ₹600 | 12:00 (3 h notice) | CANCELLED, refund ₹600 |
| TC-DT-13 | 2 | Party 6, deposit ₹600 | 14:00 (1 h notice) | CANCELLED, refund ₹0 |
| TC-DT-14 | 3 | Party 2, no deposit | 12:00 | CANCELLED, refund ₹0 |
| TC-DT-15 | 4 | Party 2, no deposit | 14:00 | CANCELLED, refund ₹0 |
| TC-DT-16 | 5 | Booking already SEATED | any | Refused |
| TC-DT-17 | 5 | Booking already CANCELLED | any | Refused |

**Automation:** `05_Test_Automation/unit/test_decision_tables.py`
