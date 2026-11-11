"""Learning content: Python-concept detection, self-quiz generation and validation.

Used by build_problems.py. Content lives in content/learn/*.py.
"""
import ast
import contextlib
import io
import random
import re
import runpy
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "content" / "learn"

CALLS = {
    "dict": "dict", "get": "dict", "setdefault": "dict", "items": "dict", "values": "dict", "keys": "dict",
    "set": "set", "add": "set",
    "append": "list-stack",
    "enumerate": "enumerate-zip", "zip": "enumerate-zip",
    "sorted": "sorting", "sort": "sorting",
    "Counter": "counter", "defaultdict": "counter",
    "deque": "deque", "popleft": "deque", "appendleft": "deque",
    "heappush": "heapq", "heappop": "heapq", "heapify": "heapq", "nlargest": "heapq", "nsmallest": "heapq",
    "bisect_left": "bisect", "bisect_right": "bisect", "insort": "bisect",
    "isalnum": "strings", "lower": "strings", "ord": "strings", "chr": "strings", "join": "strings", "split": "strings",
    "any": "any-all", "all": "any-all",
    "iter": "iterators", "next": "iterators",
    "max": "min-max", "min": "min-max",
    "range": "loops-range",
}
# Fix-ups where syntax alone is ambiguous (e.g. `a & b` on sets looks like a bit operation).
TAG_OVERRIDES = {"pacific-atlantic-water-flow": {"bits": "set"}}

BIT_OPS = (ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift, ast.Invert)


def detect_concepts(code: str) -> dict[int, list[str]]:
    """Map line number -> concept ids used on that line."""
    tree = ast.parse(code)
    tags: dict[int, set[str]] = defaultdict(set)

    def tag(node, cid):
        tags[node.lineno].add(cid)

    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        for child in ast.walk(fn):
            if child is not fn and isinstance(child, ast.FunctionDef):
                tag(child, "closures")
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == fn.name:
                tag(child, "recursion")

    for n in ast.walk(tree):
        if isinstance(n, ast.Nonlocal):
            tag(n, "closures")
        elif isinstance(n, ast.ClassDef):
            tag(n, "classes")
        if isinstance(n, (ast.Dict, ast.DictComp)):
            tag(n, "dict")
        if isinstance(n, (ast.Set, ast.SetComp)):
            tag(n, "set")
        if isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            tag(n, "comprehensions")
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
            tag(n, "slicing")
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Tuple) for t in n.targets):
            tag(n, "unpacking")
        if isinstance(n, (ast.For, ast.comprehension)) and isinstance(n.target, ast.Tuple):
            tag(n.target, "unpacking")
        if isinstance(n, (ast.For, ast.While)) and n.orelse:
            tag(n, "loop-else")
        if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, BIT_OPS):
            tag(n, "bits")
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Invert):
            tag(n, "bits")
        if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, (ast.FloorDiv, ast.Mod)):
            tag(n, "int-division")
        if isinstance(n, ast.Attribute) and n.attr in ("next", "left", "right", "neighbors"):
            tag(n, "node-refs")
        if isinstance(n, ast.Compare) and any(isinstance(op, (ast.In, ast.NotIn)) for op in n.ops):
            tag(n, "membership")
        if isinstance(n, ast.Name) and n.id == "inf":
            tag(n, "infinity")
        if isinstance(n, ast.Lambda):
            tag(n, "sorting")
        if isinstance(n, ast.Call):
            f = n.func
            name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
            if name == "float" and n.args and isinstance(n.args[0], ast.Constant) and "inf" in str(n.args[0].value):
                tag(n, "infinity")
            elif name == "pop":
                # dict.pop(key) with a string key vs list.pop()
                is_dict = bool(n.args) and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)
                tag(n, "dict" if is_dict else "list-stack")
            elif name in CALLS:
                tag(n, CALLS[name])
    return {line: sorted(ids) for line, ids in sorted(tags.items())}


def run_snippet(code: str) -> str:
    buf = io.StringIO()
    env: dict = {"__name__": "__main__"}
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<snippet>", "exec"), env)
    return buf.getvalue().rstrip("\n")


def _check_question(q: dict, where: str) -> dict:
    q = dict(q)
    assert q.get("q") and isinstance(q.get("options"), list) and len(q["options"]) >= 2, f"{where}: malformed question"
    assert 0 <= q["answer"] < len(q["options"]), f"{where}: answer index out of range"
    assert len(set(q["options"])) == len(q["options"]), f"{where}: duplicate options"
    if q.pop("predict", False):
        actual = run_snippet(q["code"])
        assert q["options"][q["answer"]] == actual, f"{where}: predicted output {q['options'][q['answer']]!r} but code prints {actual!r}"
    q.setdefault("why", "")
    return q


BIG_O = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2^n)"]


def _first_big_o(text: str, label: str):
    m = re.search(rf"\*\*{label}:\*\*\s*(.*)", text)
    if not m:
        return None
    line = m.group(1)
    start = line.find("O(")
    if start < 0:
        return None
    depth, i = 0, start + 1
    while i < len(line):
        depth += {"(": 1, ")": -1}.get(line[i], 0)
        if depth == 0:
            return line[start : i + 1]
        i += 1
    return None


def problem_quiz(p: dict, categories: list[str], insight: dict | None) -> list[dict]:
    rng = random.Random(p["slug"])
    qs = []
    if insight:
        qs.append({"id": f"{p['slug']}:insight", "kind": "insight", **_check_question(insight, p["slug"])})

    others = rng.sample([c for c in categories if c != p["category"]], 3)
    opts = others + [p["category"]]
    rng.shuffle(opts)
    qs.append({
        "id": f"{p['slug']}:pattern", "kind": "pattern",
        "q": f"Which technique does the standard solution to **{p['title']}** use?",
        "options": opts, "answer": opts.index(p["category"]),
        "why": f"The standard solution uses the **{p['category']}** pattern. The pattern guide explains how to recognise it.",
    })

    for label, kind in (("Time", "time"), ("Space", "space")):
        ans = _first_big_o(p["explanation"], label)
        if not ans:
            continue
        if re.fullmatch(r"O\(\d+\)", ans):
            ans = "O(1)"  # O(26), O(32): constant
        ans = ans.replace("O(sz)", "O(n)")
        if not re.fullmatch(r"O\((?:[nmkhVENL\d\s·+²^()α]|log)+\)", ans):
            continue  # unusual wording would stand out among the options
        pool = [o for o in BIG_O if o != ans]
        opts = rng.sample(pool, 3) + [ans]
        rng.shuffle(opts)
        line = re.search(rf"\*\*{label}:\*\*\s*(.*)", p["explanation"]).group(1)
        qs.append({
            "id": f"{p['slug']}:{kind}", "kind": kind,
            "q": f"What is the **{label.lower()} complexity** of the optimal solution to **{p['title']}**?",
            "options": opts, "answer": opts.index(ans),
            "why": f"The optimal solution's {label.lower()} complexity is {line.rstrip('.')}.",
        })
    return qs


def load_learn(problems: list[dict], categories: list[str]):
    """Validate concept + pattern content, annotate problems in place, return learn.json payload."""
    concepts = runpy.run_path(str(LEARN / "concepts.py"))["CONCEPTS"]
    patterns = runpy.run_path(str(LEARN / "patterns.py"))["PATTERNS"]
    insights = runpy.run_path(str(LEARN / "insights.py"))["INSIGHTS"]
    drills = runpy.run_path(str(LEARN / "python_drills.py"))["DRILLS"]

    concept_ids = {c["id"] for c in concepts}
    assert not set(drills) - concept_ids, f"python_drills.py has unknown concept ids {set(drills) - concept_ids}"
    used_in = defaultdict(list)
    for p in problems:
        tags = detect_concepts(p["solution"])
        for wrong, right in TAG_OVERRIDES.get(p["slug"], {}).items():
            tags = {ln: sorted({right if c == wrong else c for c in ids}) for ln, ids in tags.items()}
        unknown = {c for ids in tags.values() for c in ids} - concept_ids
        assert not unknown, f"{p['slug']}: detector produced unknown concept ids {unknown}"
        p["lineTags"] = {str(k): v for k, v in tags.items()}
        p["concepts"] = sorted({c for ids in tags.values() for c in ids})
        for c in p["concepts"]:
            used_in[c].append(p["slug"])
        p["quiz"] = problem_quiz(p, categories, insights.get(p["slug"]))
    missing = [p["slug"] for p in problems if p["slug"] not in insights]
    assert not missing, f"missing insight questions for: {missing}"

    out_concepts = []
    for c in concepts:
        c = dict(c)
        c["output"] = run_snippet(c["snippet"])
        qs = [*c.get("quiz", []), *drills.get(c["id"], [])]
        c["quiz"] = [{"id": f"py:{c['id']}:{i}", "kind": "python", **_check_question(q, c["id"])} for i, q in enumerate(qs)]
        c["usedIn"] = used_in.get(c["id"], [])
        out_concepts.append(c)

    by_cat = {pt["category"]: pt for pt in patterns}
    assert set(by_cat) == set(categories), f"pattern guides don't match categories: {set(categories) ^ set(by_cat)}"
    out_patterns = []
    for cat in categories:
        pt = dict(by_cat[cat])
        pt["id"] = re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")
        compile(pt["template"], f"<template {pt['id']}>", "exec")
        pt["quiz"] = [{"id": f"pattern:{pt['id']}:{i}", "kind": "pattern-guide", **_check_question(q, pt["id"])} for i, q in enumerate(pt.get("quiz", []))]
        pt["problems"] = [p["slug"] for p in problems if p["category"] == cat]
        out_patterns.append(pt)
    pattern_id = {pt["category"]: pt["id"] for pt in out_patterns}
    for p in problems:
        p["pattern"] = pattern_id[p["category"]]
    return {"concepts": out_concepts, "patterns": out_patterns}
