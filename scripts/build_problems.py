#!/usr/bin/env python3
"""Validate every problem in content/ and write data/problems.json.

For each problem:
  * the reference solution must pass every example (examples carry hand-written expected values)
  * hidden tests list only inputs; their expected outputs are produced by the reference solution
  * the starter code must compile

Usage: python3 scripts/build_problems.py
"""
import ast
import importlib.util
import json
import runpy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import learn  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("harness", ROOT / "public" / "harness.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)

COMMENTS = {
    "list": "# Definition for singly-linked list (pre-defined):\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n",
    "tree": "# Definition for a binary tree node (pre-defined):\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n",
    "graph": "# Definition for a graph node (pre-defined):\n# class Node:\n#     def __init__(self, val=0, neighbors=None):\n#         self.val = val\n#         self.neighbors = neighbors if neighbors is not None else []\n",
}
DIFFICULTIES = {"Easy", "Medium", "Hard"}
SPEC_KEYS = ["fn", "kind", "cls", "in", "out", "compare", "mutate", "driver", "checker"]


def parse_sig(sig):
    tree = ast.parse(sig.strip() + "\n    pass\n")
    fn = tree.body[0]
    return fn.name, [a.arg for a in fn.args.args if a.arg != "self"]


def build_one(p, category):
    p = dict(p)
    assert p["difficulty"] in DIFFICULTIES, p["slug"]
    uses = set(p.pop("uses", []))
    for key in ("in", "out"):
        val = p.get(key)
        for a in val if isinstance(val, list) else [val]:
            if a:
                uses.add("list" if a == "lists" else a)
    header = "".join(COMMENTS[u] for u in ("list", "tree", "graph") if u in uses)

    if "sig" in p:
        fn, params = parse_sig(p["sig"])
        p.setdefault("fn", fn)
        p.setdefault("params", params)
        p.setdefault("starter", p["sig"].strip() + "\n    pass\n")
    if header:
        p["starter"] = header + "\n" + p["starter"]
    if p.get("kind") == "class":
        p.setdefault("params", ["operations", "arguments"])
    for k in ("driver", "checker"):
        if p.get(k):
            p[k] = p[k].strip() + "\n"

    run_spec = {k: p[k] for k in SPEC_KEYS if p.get(k) is not None}
    sol = harness.Session(p["solution"], run_spec)

    examples = []
    for args, expected in p["examples"]:
        r = sol.run(args, expected)
        if r["error"] or not r["ok"]:
            raise AssertionError(f"{p['slug']}: example {args!r} expected {expected!r}, solution gave {r['result']!r} {r['error'] or ''}")
        examples.append({"args": args, "expected": expected})

    tests = list(examples)
    for args in p.get("tests", []):
        r = sol.run(args, has_expected=False)
        if r["error"]:
            raise AssertionError(f"{p['slug']}: test {args!r} raised {r['error']}")
        if not sol.check(args, r["result"], r["result"]):
            raise AssertionError(f"{p['slug']}: checker rejects the reference output for {args!r}")
        tests.append({"args": args, "expected": r["result"]})

    # The starter must at least compile and run through the harness without crashing it.
    starter = harness.Session(p["starter"], run_spec)
    for t in tests:
        starter.run(t["args"], t["expected"])

    return {
        "slug": p["slug"],
        "title": p["title"],
        "difficulty": p["difficulty"],
        "category": category,
        "desc": p["desc"].strip(),
        "params": p["params"],
        "starter": p["starter"],
        "hints": p.get("hints", []),
        "solution": p["solution"].strip() + "\n",
        "explanation": p["explanation"].strip(),
        "spec": run_spec,
        "examples": examples,
        "tests": tests,
    }


def main():
    out, slugs, categories = [], set(), []
    for path in sorted((ROOT / "content").glob("[0-9]*.py")):
        mod = runpy.run_path(str(path))
        category = mod["CATEGORY"]
        categories.append(category)
        for p in mod["PROBLEMS"]:
            if p["slug"] in slugs:
                raise AssertionError(f"duplicate slug {p['slug']}")
            slugs.add(p["slug"])
            out.append(build_one(p, category))
        print(f"  {category:<22} {len(mod['PROBLEMS'])} problems")
    learn_data = learn.load_learn(out, categories)
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "learn.json").write_text(json.dumps(learn_data, separators=(",", ":")))
    nq = sum(len(p["quiz"]) for p in out) + sum(len(c["quiz"]) for c in learn_data["concepts"]) + sum(len(x["quiz"]) for x in learn_data["patterns"])
    print(f"OK: {len(learn_data['concepts'])} Python concepts, {len(learn_data['patterns'])} pattern guides, {nq} quiz questions -> data/learn.json")
    dest = ROOT / "data" / "problems.json"
    dest.write_text(json.dumps({"categories": categories, "problems": out}, separators=(",", ":")))
    print(f"OK: {len(out)} problems, {sum(len(p['tests']) for p in out)} test cases -> {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
