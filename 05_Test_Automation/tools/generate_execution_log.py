"""Build the test execution log (Markdown + CSV) from the raw test results.

Inputs
  06_Test_Reports/<cycle>/junit.xml          - pytest results (expected/actual recorded per test)
  06_Test_Reports/postman/<cycle>.xml        - Newman results
  02_Test_Case_Design/*.md                   - test case descriptions (looked up by TC ID)
  04_Defect_Reports/defect_map.json          - optional: which defect each failing TC exposed

Output
  03_Test_Execution/<Cycle>_Execution_Log.md and .csv

Usage:  python tools/generate_execution_log.py cycle1 "Cycle 1" 1.0.0
"""
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TC_RE = re.compile(r"TC[-_](EP|BVA|DT|ST|TA|API|UI)[-_](\d+)")
TECHNIQUES = OrderedDict([
    ("EP", "Equivalence Partitioning"), ("BVA", "Boundary Value Analysis"),
    ("DT", "Decision Table"), ("ST", "State Transition"), ("TA", "Table Allocation"),
    ("API", "REST API (pytest)"), ("UI", "Web UI (Selenium)"),
])


def load_descriptions():
    """TC ID -> short description taken from the design documents."""
    out = {}
    for md in sorted((ROOT / "02_Test_Case_Design").glob("0*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.fullmatch(r"TC-[A-Z]+-\d+", cells[0]) and len(cells) >= 3:
                out[cells[0]] = " · ".join(c for c in cells[1:-1] if c)
    return out


def load_pytest(path):
    rows = []
    for case in ET.parse(path).getroot().iter("testcase"):
        match = TC_RE.search(case.get("name", ""))
        if not match:
            continue
        tc_id = f"TC-{match.group(1)}-{int(match.group(2)):02d}"
        props = {p.get("name"): p.get("value") for p in case.iter("property")}
        if case.find("failure") is not None or case.find("error") is not None:
            status = "FAIL"
        elif case.find("skipped") is not None:
            status = "SKIP"
        else:
            status = "PASS"
        actual = props.get("actual", "")
        if status == "FAIL" and not actual:
            node = case.find("failure") if case.find("failure") is not None else case.find("error")
            actual = (node.get("message") or "error")[:120]
        rows.append({"tc_id": tc_id, "group": match.group(1), "expected": props.get("expected", ""),
                     "actual": actual, "status": status, "time": float(case.get("time", 0))})
    order = list(TECHNIQUES)
    return sorted(rows, key=lambda r: (order.index(r["group"]), r["tc_id"]))


def load_newman(path):
    if not path.exists():
        return []
    rows = []
    for suite in ET.parse(path).getroot().iter("testsuite"):
        name = suite.get("name", "")
        pm_id = name.split(" ")[0]
        cases = list(suite.iter("testcase"))
        failed = [c.get("name") for c in cases if c.find("failure") is not None]
        rows.append({"pm_id": pm_id, "name": name[len(pm_id):].strip(), "total": len(cases),
                     "passed": len(cases) - len(failed), "failed": failed,
                     "status": "FAIL" if failed else "PASS"})
    return rows


def main(cycle, title, version):
    reports = ROOT / "06_Test_Reports" / cycle
    rows = load_pytest(reports / "junit.xml")
    newman = load_newman(ROOT / "06_Test_Reports" / "postman" / f"{cycle}.xml")
    desc = load_descriptions()
    defect_file = ROOT / "04_Defect_Reports" / "defect_map.json"
    defects = json.loads(defect_file.read_text()) if defect_file.exists() else {}

    total = Counter(r["status"] for r in rows)
    executed = len(rows)
    pass_rate = 100 * total["PASS"] / executed if executed else 0
    icon = {"PASS": "✅ Pass", "FAIL": "❌ Fail", "SKIP": "⏭ Skip"}

    lines = [
        f"# {title} – Test Execution Log", "",
        "| Item | Detail |", "|---|---|",
        f"| Build under test | Restaurant Table Reservation System **v{version}** |",
        f"| Executed on | {datetime.now():%d %b %Y, %H:%M} |",
        "| Test clock | Mon 16 Nov 2026, 10:00 (frozen) |",
        "| Environment | Python 3, Flask, pytest, Selenium 4 + Chrome (headless), Newman |",
        f"| Executed | **{executed}** test cases + **{len(newman)}** Postman requests |",
        f"| Result | **{total['PASS']} passed**, **{total['FAIL']} failed**, {total['SKIP']} skipped "
        f"→ pass rate **{pass_rate:.1f}%** |", "",
        "## Summary by technique", "",
        "| Technique | Executed | Passed | Failed | Pass % |", "|---|---:|---:|---:|---:|",
    ]
    csv_rows = []
    for group, label in TECHNIQUES.items():
        sub = [r for r in rows if r["group"] == group]
        if not sub:
            continue
        p = sum(r["status"] == "PASS" for r in sub)
        lines.append(f"| {label} | {len(sub)} | {p} | {len(sub) - p} | {100 * p / len(sub):.0f}% |")
    if newman:
        assertions = sum(n["total"] for n in newman)
        passed = sum(n["passed"] for n in newman)
        lines.append(f"| Postman / Newman (assertions) | {assertions} | {passed} | {assertions - passed} | "
                     f"{100 * passed / assertions:.0f}% |")
    lines.append(f"| **Total (test cases)** | **{executed}** | **{total['PASS']}** | **{total['FAIL']}** | "
                 f"**{pass_rate:.0f}%** |")

    failed = [r for r in rows if r["status"] == "FAIL"]
    if failed:
        lines += ["", "## Failed test cases", "",
                  "| TC ID | Expected | Actual | Defect |", "|---|---|---|---|"]
        for r in failed:
            lines.append(f"| {r['tc_id']} | {r['expected']} | {r['actual']} | {defects.get(r['tc_id'], 'to be logged')} |")

    for group, label in TECHNIQUES.items():
        sub = [r for r in rows if r["group"] == group]
        if not sub:
            continue
        lines += ["", f"## {label}", "",
                  "| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |",
                  "|---|---|---|---|---|---|"]
        for r in sub:
            d = desc.get(r["tc_id"], "")
            defect = defects.get(r["tc_id"], "") if r["status"] == "FAIL" else ""
            lines.append(f"| {r['tc_id']} | {d} | {r['expected']} | {r['actual']} | {icon[r['status']]} | {defect} |")
            csv_rows.append([r["tc_id"], label, d, r["expected"], r["actual"], r["status"], defect])

    if newman:
        lines += ["", "## Postman collection (Newman)", "",
                  "| ID | Request | Assertions passed | Status | Failed assertions | Defect |",
                  "|---|---|---|---|---|---|"]
        for n in newman:
            defect = defects.get(n["pm_id"], "") if n["failed"] else ""
            lines.append(f"| {n['pm_id']} | {n['name']} | {n['passed']}/{n['total']} | {icon[n['status']]} | "
                         f"{'; '.join(n['failed'])} | {defect} |")
            csv_rows.append([n["pm_id"], "Postman", n["name"], f"{n['total']} assertions pass",
                             f"{n['passed']}/{n['total']} passed", n["status"], defect])

    out = ROOT / "03_Test_Execution" / f"{title.replace(' ', '_')}_Execution_Log"
    out.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with out.with_suffix(".csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Test ID", "Technique", "Input / scenario", "Expected", "Actual", "Status", "Defect"])
        writer.writerows(csv_rows)
    print(f"Wrote {out.with_suffix('.md').relative_to(ROOT)}: {total['PASS']} passed, {total['FAIL']} failed")


if __name__ == "__main__":
    main(*sys.argv[1:4])
