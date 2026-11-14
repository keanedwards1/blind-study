"""Learn Python: build the 10-level curriculum and the placement test into data/python.json.

Levels 1-7 are authored in content/python/levelNN.py; levels 8-10 are the Blind 75 split by difficulty.
The placement test (content/python/placement.py) is 20 coding tasks, two per level.
Used by build_problems.py, which passes in its build_one() so every task is validated the same way as the Blind 75.
"""
import builtins
import json
import runpy
import sys
from pathlib import Path

import learn

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "python"
sys.path.insert(0, str(CONTENT))  # lets level files `from _helpers import P, Q`
PY_LEVELS = range(1, 8)
QUIZ_KINDS = ("insight", "time", "space")

# Built-ins whose effect no test can observe (interactive, identity-based, or site helpers).
# They may only be covered by quiz questions; everything else needs a coding problem.
UNTESTABLE = {"help", "breakpoint", "id", "exit", "quit", "copyright", "credits", "license", "globals", "locals",
              "__import__", "aiter", "anext"}


def all_builtins() -> set[str]:
    """Every built-in function and type a learner can call: lowercase names, plus __import__."""
    names = {n for n in dir(builtins) if n[0].islower()}
    return names | {"__import__"}


def blind_levels(blind: list[dict], categories: list[str]) -> dict[int, list[str]]:
    """L8 = Easy; L9 = the first half of the Mediums in category order; L10 = the rest of the Mediums + Hard."""
    order = {c: i for i, c in enumerate(categories)}
    by_cat = sorted(blind, key=lambda p: order[p["category"]])
    mediums = [p["slug"] for p in by_cat if p["difficulty"] == "Medium"]
    half = (len(mediums) + 1) // 2
    return {
        8: [p["slug"] for p in by_cat if p["difficulty"] == "Easy"],
        9: mediums[:half],
        10: mediums[half:] + [p["slug"] for p in by_cat if p["difficulty"] == "Hard"],
    }


def _finish_problem(built: dict, raw: dict, category: str) -> dict:
    """Fill in the Problem fields the workspace expects (Blind 75 problems get these from learn.load_learn)."""
    tags = learn.detect_concepts(built["solution"])
    built["lineTags"] = {str(k): v for k, v in tags.items()}
    built["concepts"] = sorted({c for ids in tags.values() for c in ids})
    built["quiz"] = []
    built["pattern"] = ""
    built["grammar"] = learn.parse_grammar(built["slug"], raw["grammar"]) if raw.get("grammar") else []
    built["category"] = category
    return built


def _quiz(questions: list[dict], prefix: str) -> list[dict]:
    return [{"id": f"{prefix}:{i}", "kind": "python-basics", **learn._check_question(q, prefix)} for i, q in enumerate(questions)]


def build_python(blind: list[dict], categories: list[str], build_one) -> dict:
    slugs: set[str] = set()
    problems: list[dict] = []

    def add(raw: dict, category: str) -> str:
        slug = raw["slug"]
        assert slug.startswith("py-"), f"Learn Python slugs must start with 'py-': {slug}"
        assert slug not in slugs, f"duplicate Learn Python slug {slug}"
        slugs.add(slug)
        problems.append(_finish_problem(build_one(raw, category), raw, category))
        return slug

    levels = []
    covered: set[str] = set()
    for n in PY_LEVELS:
        path = CONTENT / f"level{n:02d}.py"
        if not path.exists():
            levels.append({"n": n, "kind": "python", "title": f"Level {n}", "summary": "", "ready": False, "concepts": [], "problems": [], "quiz": []})
            continue
        lv = runpy.run_path(str(path))["LEVEL"]
        assert lv["n"] == n, f"{path.name} says it is level {lv['n']}"
        category = f"Level {n}: {lv['title']}"
        concepts, quiz_pool = [], []
        for c in lv["concepts"]:
            where = f"level {n} / {c['id']}"
            names = set(c.get("builtins", [])) | set(c.get("quiz_only", []))
            unknown = names - all_builtins()
            assert not unknown, f"{where}: not built-ins: {sorted(unknown)}"
            bad_quiz_only = set(c.get("quiz_only", [])) - UNTESTABLE
            assert not bad_quiz_only, f"{where}: {sorted(bad_quiz_only)} can be tested with code, so they need a problem, not quiz_only"
            assert c.get("problems") or c.get("quiz_only"), f"{where}: a concept needs at least one problem"
            covered |= names
            qs = _quiz(c.get("quiz", []), f"py:{n}:{c['id']}")
            assert qs, f"{where}: needs quiz questions for the level quiz"
            quiz_pool += qs
            concepts.append({
                "id": c["id"], "title": c["title"], "intro": c["intro"].strip(),
                "builtins": sorted(names),
                "problems": [add(p, category) for p in c.get("problems", [])],
            })
        levels.append({
            "n": n, "kind": "python", "title": lv["title"], "summary": lv["summary"].strip(), "ready": True,
            "concepts": concepts, "problems": [s for c in concepts for s in c["problems"]], "quiz": quiz_pool,
        })

    by_slug = {p["slug"]: p for p in blind}
    titles = {8: ("Blind 75: Easy", "All 19 Easy problems from the Blind 75."),
              9: ("Blind 75: Medium I", "The first half of the Medium problems: arrays and hashing through trees."),
              10: ("Blind 75: Medium II & Hard", "The remaining Medium problems and all of the Hard ones.")}
    for n, level_slugs in blind_levels(blind, categories).items():
        pool = [q for s in level_slugs for q in by_slug[s]["quiz"] if q["kind"] in QUIZ_KINDS]
        levels.append({"n": n, "kind": "blind", "title": titles[n][0], "summary": titles[n][1], "ready": True,
                       "concepts": [], "problems": level_slugs, "quiz": pool})

    placement = []
    for i, task in enumerate(runpy.run_path(str(CONTENT / "placement.py"))["PLACEMENT"]):
        assert task["level"] in range(1, 11), f"placement task {i}: bad level"
        placement.append({"level": task["level"], "slug": add(task["problem"], f"Placement · level {task['level']}")})
    counts = {lv: sum(t["level"] == lv for t in placement) for lv in range(1, 11)}
    assert all(c == 2 for c in counts.values()), f"placement needs exactly 2 tasks per level, got {counts}"
    placement.sort(key=lambda t: t["level"])

    missing = all_builtins() - covered
    if all(lv["ready"] for lv in levels):
        assert not missing, f"built-ins not covered by any level: {sorted(missing)}"
    elif missing:
        print(f"  note: {len(missing)} built-ins not covered yet (levels {[lv['n'] for lv in levels if not lv['ready']]} unwritten)")

    data = {"levels": levels, "placement": placement, "problems": problems}
    dest = ROOT / "data" / "python.json"
    dest.write_text(json.dumps(data, separators=(",", ":")))
    print(f"OK: Learn Python {sum(lv['ready'] for lv in levels)}/10 levels, {len(problems)} tasks "
          f"({len(placement)} placement) -> {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")
    return data
