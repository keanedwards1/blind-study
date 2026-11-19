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
import os
import runpy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import learn  # noqa: E402
import python_levels  # noqa: E402

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

# Hints live in content/hints/*.py (HINTS = {slug: [...]}) and replace any inline `hints` on a problem or task.
HINTS = {}
for _path in sorted((ROOT / "content" / "hints").glob("*.py")):
    for _slug, _hints in runpy.run_path(str(_path))["HINTS"].items():
        assert _slug not in HINTS, f"{_path.name}: hints for {_slug} are defined twice"
        HINTS[_slug] = list(_hints)

# Edge cases live in content/edges/*.py (EDGES = {slug: [(note, args), ...]}). Each one becomes a hidden test whose expected
# value comes from the reference solution, and its note ("empty list", "all the same") is shown in the IDE so you know what
# Submit will throw at your code. A note whose args match an existing example or test labels that case instead.
# A file's EXHAUSTIVE set names tasks whose every valid input is already tested (days 1-7), so they can't reach MIN_TESTS.
EDGES, EXHAUSTIVE = {}, set()
for _path in sorted((ROOT / "content" / "edges").glob("*.py")):
    _mod = runpy.run_path(str(_path))
    EXHAUSTIVE |= set(_mod.get("EXHAUSTIVE", ()))
    for _slug, _cases in _mod["EDGES"].items():
        assert _slug not in EDGES, f"{_path.name}: edge cases for {_slug} are defined twice"
        EDGES[_slug] = [(note, list(args)) for note, args in _cases]
MIN_TESTS, MIN_EDGES = 8, 3
SHORT = []  # problems below the minimums, reported (and failed) at the end of the build

# Stress tests: extra hidden tests built from each problem's examples (see stress_cases()). A file's STRESS_SKIP names the
# kinds a task can't take ({slug: {"big", "negative", "long"}}, or "all"): a weekday can't be 10**15, a grade can't be negative.
STRESS_SKIP = {}
for _path in sorted((ROOT / "content" / "edges").glob("*.py")):
    for _slug, _kinds in runpy.run_path(str(_path)).get("STRESS_SKIP", {}).items():
        assert _slug not in STRESS_SKIP, f"{_path.name}: stress skips for {_slug} are defined twice"
        _kinds = {"big", "negative", "long"} if _kinds == "all" else set(_kinds)
        assert _kinds <= {"big", "negative", "long"}, f"{_path.name}: unknown stress kinds for {_slug}: {_kinds}"
        STRESS_SKIP[_slug] = _kinds
STRESS_STATS = {"added": 0, "dropped": 0}
STRESS_LOG = []  # (slug, kind, "added" | "dropped", why): written to $STRESS_REPORT when set, for reviewing what each task got


def _norm(s):
    return " ".join(s.replace("`", " ").split())


def check_hints(slug, hints, solution):
    """2-4 hints, none of which repeats a (non-trivial) line of the reference solution."""
    assert 2 <= len(hints) <= 4, f"{slug}: needs 2-4 hints, has {len(hints)}"
    lines = {_norm(line) for line in solution.splitlines()}
    # Signatures, returns and control-flow headers ("for x in nums:") don't give an answer away; lines that compute do.
    headers = ("def ", "class ", "return ", "for ", "while ", "if ", "elif ", "else", "try", "except", "with ", "finally")
    lines = {line for line in lines if len(line) >= 14 and not line.startswith(headers)}
    for h in hints:
        assert h.strip(), f"{slug}: empty hint"
        nh = _norm(h)
        for line in lines:
            assert line not in nh, f"{slug}: a hint gives away a solution line: {line!r}"

# ---------------------------------------------------------------- stress tests
# 10**15, not more: test data goes through JavaScript, whose numbers are exact only up to 2**53 (about 9 * 10**15).
BIG_INT, BIG_FLOAT, LONG = 10**15, 1e9, 1000
JS_SAFE = 2**53 - 1
STRESS_SECONDS = 0.25  # the reference must answer this fast in CPython; Pyodide in the browser is several times slower


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _shift(x, n, f):
    """Every number, at any depth, moved by n (ints) or f (floats): keeps order, gaps and signs-relative-to-each-other."""
    if _is_int(x):
        return x + n
    if isinstance(x, float):
        return x + f
    if isinstance(x, (list, tuple)):
        return type(x)(_shift(v, n, f) for v in x)
    if isinstance(x, dict):
        return {k: _shift(v, n, f) for k, v in x.items()}
    return x


def _has_number(x):
    if _is_int(x) or isinstance(x, float):
        return True
    if isinstance(x, (list, tuple)):
        return any(_has_number(v) for v in x)
    if isinstance(x, dict):
        return any(_has_number(v) for v in x.values())
    return False


def _repeats(n):
    """How many copies make ~LONG items: always odd, so an odd length stays odd and the middle item stays a copy of the middle."""
    k = -(-LONG // n)
    return k if k % 2 else k + 1


def _js_exact(x):
    """Every int, at any depth, is one JavaScript holds exactly."""
    if _is_int(x):
        return abs(x) <= JS_SAFE
    if isinstance(x, (list, tuple)):
        return all(_js_exact(v) for v in x)
    if isinstance(x, dict):
        return all(_js_exact(v) for v in x.values())
    return True


def _js_comparable(x):
    """An expected value still compares right after a trip through JavaScript: numbers (alone or in lists) are compared with
    a tolerance, so they may be huge; numbers inside dicts are compared exactly, so they must stay exact."""
    if isinstance(x, (list, tuple)):
        return all(_js_comparable(v) for v in x)
    if isinstance(x, dict):
        return _js_exact(x)
    return True


def _lengthen(x):
    """A ~LONG version of a string, list or dict made by repeating its own contents (so the values stay the same kind).
    One-character strings are left alone: they're usually a single letter or symbol the task looks for."""
    if isinstance(x, str) and len(x) > 1:
        return x * _repeats(len(x))
    if isinstance(x, list) and x:
        out = x * _repeats(len(x))
        if all(_is_int(v) or isinstance(v, float) for v in x) and x == sorted(x):
            out.sort()  # a sorted input stays sorted
        return out
    if isinstance(x, dict) and x and all(isinstance(k, str) for k in x):
        items = list(x.items())
        n = len(items) * _repeats(len(items))
        return {(k if i < len(items) else f"{k}{i // len(items)}"): v for i in range(n) for k, v in [items[i % len(items)]]}
    return None


def _timed(sol, args):
    """Run the reference on a stress input in a forked child, so an input that makes it allocate without limit (1 << 10**15)
    only kills the child. Returns the harness result, or {"error": ...} when the child is slow, crashes or is killed."""
    import pickle
    import select
    import signal
    import time

    rd, wr = os.pipe()
    pid = os.fork()
    if pid == 0:  # child: run with a timer, send the pickled result back, and exit without cleanup
        os.close(rd)
        try:
            signal.setitimer(signal.ITIMER_REAL, STRESS_SECONDS)
            out = sol.run(args, has_expected=False)
            signal.setitimer(signal.ITIMER_REAL, 0)
            data = pickle.dumps(out)
        except BaseException as e:  # noqa: BLE001
            data = pickle.dumps({"error": f"{type(e).__name__}: {e}"})
        with os.fdopen(wr, "wb") as f:
            f.write(data)
        os._exit(0)
    os.close(wr)
    chunks, deadline = [], time.monotonic() + STRESS_SECONDS + 2
    with os.fdopen(rd, "rb") as f:
        while time.monotonic() < deadline:
            ready, _, _ = select.select([f], [], [], max(0.0, deadline - time.monotonic()))
            if not ready:
                break
            chunk = os.read(f.fileno(), 1 << 16)
            if not chunk:
                break
            chunks.append(chunk)
        else:
            chunks = None
    if time.monotonic() >= deadline:
        os.kill(pid, signal.SIGKILL)
    _, status = os.waitpid(pid, 0)
    if not chunks or not os.WIFEXITED(status):
        return {"error": "too slow, or ran out of memory"}
    return pickle.loads(b"".join(chunks))


def stress_cases(p, run_spec, examples):
    """Candidate stress inputs for a task, built from its examples: every number moved up by 10**15, every number moved down
    by 10**15, and every top-level string / list / dict stretched to ~1000 items. Tasks with stdin, classes or tree / graph /
    linked-list inputs only get the number shifts (their shapes have rules a blind stretch would break)."""
    skip = STRESS_SKIP.get(p["slug"], set())
    if run_spec.get("kind") == "class":
        return []
    adapters = run_spec.get("in") or []
    out = []
    numeric = next((e["args"] for e in examples if _has_number(e["args"])), None)
    if numeric is not None:
        if "big" not in skip:
            out.append(("big", _shift(numeric, BIG_INT, BIG_FLOAT)))
        if "negative" not in skip:
            out.append(("negative", _shift(numeric, -BIG_INT, -BIG_FLOAT)))
    if "long" not in skip and not run_spec.get("stdin") and not any(adapters):
        for e in examples:
            args = [(_lengthen(a) if isinstance(a, (str, list, dict)) else None) for a in e["args"]]
            if any(a is not None for a in args):
                out.append(("long", [n if n is not None else a for n, a in zip(args, e["args"])]))
                break
    return out

SPEC_KEYS = ["fn", "kind", "cls", "in", "out", "compare", "mutate", "driver", "checker", "stdin", "raises", "require", "forbid"]


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
    if p.get("stdin"):
        p["params"] = ["stdin", *p["params"]]  # the first test argument is the list of lines input() returns
    for k in ("driver", "checker"):
        if p.get(k):
            p[k] = p[k].strip() + "\n"

    run_spec = {k: p[k] for k in SPEC_KEYS if p.get(k) is not None}
    try:
        sol = harness.Session(p["solution"], run_spec)
    except harness.TaskRuleError as e:
        raise AssertionError(f"{p['slug']}: the reference solution breaks its own task rule: {e}") from None

    strict = run_spec.get("compare") == "strict"

    def typed(expected):
        # Content files write real Python values; strict tasks compare their canonical text.
        if strict and not (isinstance(expected, dict) and set(expected) == {"raises"}):
            return harness.typed_repr(expected)
        return expected

    examples = []
    for args, expected in p["examples"]:
        expected = typed(expected)
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

    for note, args in EDGES.get(p["slug"], []):
        assert note.strip() and len(note) <= 60, f"{p['slug']}: edge-case notes are short labels: {note!r}"
        same = next((t for t in tests if json.dumps(t["args"]) == json.dumps(args)), None)
        if same is not None:
            assert "note" not in same, f"{p['slug']}: two edge-case notes for {args!r}"
            same["note"] = note
            continue
        r = sol.run(args, has_expected=False)
        if r["error"]:
            raise AssertionError(f"{p['slug']}: edge case {note!r} {args!r} raised {r['error']}")
        if not sol.check(args, r["result"], r["result"]):
            raise AssertionError(f"{p['slug']}: checker rejects the reference output for edge case {note!r}")
        tests.append({"args": args, "expected": r["result"], "note": note})

    # Stress tests (hidden): a reference that errors or is slow on one means the input doesn't suit the task, so it's dropped.
    for kind, args in stress_cases(p, run_spec, examples):
        if any(json.dumps(t["args"]) == json.dumps(args) for t in tests):
            continue
        r = _timed(sol, args)
        if not r["error"] and not (_js_exact(args) and (strict or _js_comparable(r["result"]))):
            r = {"error": "beyond JavaScript's exact integers"}
        if r["error"] or not sol.check(args, r["result"], r["result"]):
            STRESS_STATS["dropped"] += 1
            STRESS_LOG.append((p["slug"], kind, "dropped", str(r["error"]).splitlines()[-1][:80] if r["error"] else "checker"))
            continue
        STRESS_STATS["added"] += 1
        STRESS_LOG.append((p["slug"], kind, "added", ""))
        tests.append({"args": args, "expected": r["result"]})
    notes = [t["note"] for t in tests if t.get("note")]
    assert len(set(notes)) == len(notes), f"{p['slug']}: repeated edge-case note"
    if (len(tests) < MIN_TESTS and p["slug"] not in EXHAUSTIVE) or len(notes) < MIN_EDGES:
        SHORT.append(f"{p['slug']}: {len(tests)} tests, {len(notes)} edge cases")

    # The starter must at least compile and run through the harness without crashing it.
    starter = harness.Session(p["starter"], run_spec, rules=False)
    for t in tests:
        starter.run(t["args"], t["expected"])

    hints = HINTS.get(p["slug"], p.get("hints", []))
    if not p["slug"].startswith("py-place-"):  # placement tasks are a test, so they have no hints
        check_hints(p["slug"], hints, p["solution"])

    return {
        "slug": p["slug"],
        "title": p["title"],
        "difficulty": p["difficulty"],
        "category": category,
        "desc": p["desc"].strip(),
        "params": p["params"],
        "starter": p["starter"],
        "hints": hints,
        "solution": p["solution"].strip() + "\n",
        "explanation": p["explanation"].strip(),
        "spec": run_spec,
        "examples": examples,
        "tests": tests,
    }


def _python_slugs():
    data = json.loads((ROOT / "data" / "python.json").read_text())
    return [p["slug"] for p in data["problems"]]


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
    python_levels.build_python(out, categories, build_one)
    print(f"OK: stress tests {STRESS_STATS['added']} added, {STRESS_STATS['dropped']} dropped (the reference errored or was slow)")
    if os.environ.get("STRESS_REPORT"):
        Path(os.environ["STRESS_REPORT"]).write_text("\n".join("\t".join(row) for row in STRESS_LOG) + "\n")
    unknown = set(EDGES) - {p["slug"] for p in out} - set(_python_slugs())
    assert not unknown, f"edge cases for unknown slugs: {sorted(unknown)}"
    if SHORT:
        limit = int(os.environ.get("EDGE_REPORT", "40"))
        print("\n".join(SHORT[:limit]) + (f"\n... and {len(SHORT) - limit} more" if len(SHORT) > limit else ""))
        raise SystemExit(f"{len(SHORT)} problems need at least {MIN_TESTS} tests and {MIN_EDGES} labelled edge cases (content/edges/)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
