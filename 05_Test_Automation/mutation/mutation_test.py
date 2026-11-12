"""Mutation testing for the business-logic modules.

Idea: make one small change ("mutant") to the code, e.g. turn `<` into `<=`,
then run the test suite. If a test fails, the mutant is KILLED (good - the
tests noticed). If every test still passes, the mutant SURVIVED (the tests
have a blind spot there).

    Mutation score = killed / (total - equivalent) x 100

Operators used (the same families as mutmut / PIT):
  ROR  relational operator replacement   <  <=  >  >=  ==  !=  in / not in
  AOR  arithmetic operator replacement   +  -  *
  LCR  logical connector replacement     and <-> or
  UOI  remove `not`
  CRP  integer constant +1

Usage:
    python mutation/mutation_test.py                 # from 05_Test_Automation/
    python mutation/mutation_test.py --report out.md
"""
import argparse
import ast
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
ROOT = SUITE.parent
APP = ROOT / "application"
TARGETS = ["reservation_system/validators.py", "reservation_system/service.py"]

ROR = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
       ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.In: ast.NotIn, ast.NotIn: ast.In}
AOR = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add}
SYMBOL = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=", ast.Eq: "==", ast.NotEq: "!=",
          ast.In: "in", ast.NotIn: "not in", ast.Add: "+", ast.Sub: "-", ast.Mult: "*",
          ast.And: "and", ast.Or: "or"}


def find_sites(tree):
    """List every place a mutation can be applied: (node index, kind, detail, line)."""
    sites = []
    nodes = list(ast.walk(tree))
    docstrings = {id(n.body[0].value) for n in nodes
                  if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body
                  and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
    for i, node in enumerate(nodes):
        if isinstance(node, ast.Compare):
            for j, op in enumerate(node.ops):
                if type(op) in ROR:
                    sites.append((i, "ROR", j, node.lineno,
                                  f"{SYMBOL[type(op)]} -> {SYMBOL[ROR[type(op)]]}"))
        elif isinstance(node, ast.BinOp) and type(node.op) in AOR:
            sites.append((i, "AOR", None, node.lineno, f"{SYMBOL[type(node.op)]} -> {SYMBOL[AOR[type(node.op)]]}"))
        elif isinstance(node, ast.BoolOp):
            other = "or" if isinstance(node.op, ast.And) else "and"
            sites.append((i, "LCR", None, node.lineno, f"{SYMBOL[type(node.op)]} -> {other}"))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            sites.append((i, "UOI", None, node.lineno, "remove `not`"))
        elif (isinstance(node, ast.Constant) and type(node.value) is int and id(node) not in docstrings):
            sites.append((i, "CRP", None, node.lineno, f"{node.value} -> {node.value + 1}"))
    return sites


def apply(tree, site):
    mutant = copy.deepcopy(tree)
    node = list(ast.walk(mutant))[site[0]]
    kind = site[1]
    if kind == "ROR":
        node.ops[site[2]] = ROR[type(node.ops[site[2]])]()
    elif kind == "AOR":
        node.op = AOR[type(node.op)]()
    elif kind == "LCR":
        node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
    elif kind == "UOI":
        return mutant, node                      # replaced by parent below
    elif kind == "CRP":
        node.value = node.value + 1
    return mutant, None


def remove_not(tree, target):
    class Strip(ast.NodeTransformer):
        def visit_UnaryOp(self, node):
            self.generic_visit(node)
            return node.operand if node is target else node
    return Strip().visit(tree)


def run_tests(app_copy):
    env = dict(os.environ, RTRS_APP_DIR=str(app_copy), PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", "unit", "api", "-x", "-q", "-p", "no:cacheprovider"],
                          cwd=SUITE, env=env, capture_output=True, text=True, timeout=120)
    return proc.returncode != 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(ROOT / "06_Test_Reports" / "mutation" / "mutation_results.json"))
    args = parser.parse_args()

    results, start = [], time.time()
    work = Path(tempfile.mkdtemp(prefix="mutants_"))
    try:
        for rel in TARGETS:
            source = (APP / rel).read_text()
            lines = source.splitlines()
            tree = ast.parse(source)
            sites = find_sites(tree)
            print(f"{rel}: {len(sites)} mutants")
            for n, site in enumerate(sites, 1):
                mutant, not_node = apply(tree, site)
                if not_node is not None:
                    mutant = remove_not(mutant, not_node)
                app_copy = work / "app"
                if app_copy.exists():
                    shutil.rmtree(app_copy)
                shutil.copytree(APP, app_copy, ignore=shutil.ignore_patterns("__pycache__"))
                (app_copy / rel).write_text(ast.unparse(ast.fix_missing_locations(mutant)))
                killed = run_tests(app_copy)
                results.append({"file": rel, "line": site[3], "operator": site[1], "change": site[4],
                                "code": lines[site[3] - 1].strip(), "status": "killed" if killed else "survived"})
                print(f"  [{n:3}/{len(sites)}] line {site[3]:4} {site[1]} {site[4]:<14} {'KILLED' if killed else 'SURVIVED'}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    killed = sum(r["status"] == "killed" for r in results)
    out = Path(args.report)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"total": len(results), "killed": killed,
                               "seconds": round(time.time() - start, 1), "mutants": results}, indent=2))
    print(f"\n{killed}/{len(results)} mutants killed ({100 * killed / len(results):.1f}%). Results: {out}")


if __name__ == "__main__":
    main()
