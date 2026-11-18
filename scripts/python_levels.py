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
    learn.check_grammar(built["slug"], built["grammar"], built["solution"])
    built["category"] = category
    return built


def _quiz(questions: list[dict], prefix: str) -> list[dict]:
    return [{"id": f"{prefix}:{i}", "kind": "python-basics", **learn._check_question(q, prefix)} for i, q in enumerate(questions)]


def _boss_env() -> dict:
    """What a guardian expression may use: the built-ins plus the tools pre-imported in the editor."""
    import bisect, collections, functools, heapq, itertools, math
    env = {"__builtins__": builtins, "math": math}
    for mod in (collections, itertools, functools, heapq, bisect):
        env.update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("_")})
    return env


def _boss_data(n: int, boss: dict, quiz: list[dict], reps: list[dict], problems: list[dict]) -> dict:
    """Guardian mini-game content for one world: falling expressions, lightning facts, match pairs and coding strikes."""
    env = _boss_env()
    exprs = []
    for e in boss.get("exprs", []):
        value = eval(e, dict(env))  # noqa: S307 - our own content, run at build time
        alts = {repr(value)}
        if isinstance(value, str):
            alts |= {value, f'"{value}"'}
        exprs.append({"expr": e, "answer": repr(value), "alts": sorted(alts)})
    facts = []
    for text, check in boss.get("facts", []):
        truth = eval(check, dict(env))  # noqa: S307
        assert isinstance(truth, bool), f"world {n} fact {text!r}: check must give True/False, got {truth!r}"
        facts.append({"text": text, "truth": truth})
    # Match pairs: short one-line predict questions, shown as `expression` → output.
    pairs, seen = [], set()
    for q in [*quiz, *reps]:
        code, out = q.get("code", ""), q["options"][q["answer"]]
        if "\n" in code or not code.startswith("print(") or not code.endswith(")") or "\n" in out or len(out) > 22 or out in seen:
            continue
        inner = code[len("print("):-1]
        if len(inner) > 34 or "," in inner and inner.count("(") == 0:
            continue
        seen.add(out)
        pairs.append({"left": inner, "right": out})
    for e in exprs:  # the falling expressions make good pairs too
        if e["answer"] not in seen and len(e["answer"]) <= 22 and len(e["expr"]) <= 34:
            seen.add(e["answer"])
            pairs.append({"left": e["expr"], "right": e["answer"]})
    # Coding strikes: the world's shortest plain-function tasks (at most 3 lines in the body).
    strikes = []
    for p in problems:
        spec = p.get("spec", {})
        body = [line for line in p["solution"].strip().splitlines()[1:] if line.strip()]
        if p["solution"].lstrip().startswith("def ") and len(body) <= 3 and not set(spec) & {"driver", "out", "stdin", "kind", "raises", "compare", "checker"}:
            strikes.append(p["slug"])
    return {"exprs": exprs, "facts": facts, "pairs": pairs, "strikes": strikes}


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
    boss_mod = runpy.run_path(str(CONTENT / "boss.py"))
    BOSS, AUDIT = boss_mod["BOSS"], boss_mod["AUDIT"]
    audited: set[str] = set()
    for n in PY_LEVELS:
        path = CONTENT / f"level{n:02d}.py"
        if not path.exists():
            levels.append({"n": n, "kind": "python", "title": f"Level {n}", "summary": "", "ready": False, "concepts": [], "problems": [], "quiz": []})
            continue
        lv = runpy.run_path(str(path))["LEVEL"]
        assert lv["n"] == n, f"{path.name} says it is level {lv['n']}"
        category = f"Level {n}: {lv['title']}"
        concepts, quiz_pool = [], []
        # Extra practice (content/python/extra_levelNN.py): warm-ups before a concept's tasks, practice after them, rep
        # questions for the rep room, whole new concepts, and a mixed review group at the end of the world.
        extra_path = CONTENT / f"extra_level{n:02d}.py"
        extra = runpy.run_path(str(extra_path)) if extra_path.exists() else {}
        more = extra.get("EXTRA", {})
        concept_list = list(lv["concepts"])
        for nc in extra.get("NEW_CONCEPTS", []):
            ids = [c["id"] for c in concept_list]
            assert nc["after"] in ids, f"{extra_path.name}: {nc['id']} goes after unknown concept {nc['after']}"
            concept_list.insert(ids.index(nc["after"]) + 1, nc)
        if extra.get("REVIEW"):
            concept_list.append({**extra["REVIEW"], "review": True})
        # Beginner lessons (content/lessons/python_levelNN.py) replace the concepts' original intros.
        lessons_path = ROOT / "content" / "lessons" / f"python_level{n:02d}.py"
        lessons = runpy.run_path(str(lessons_path))["LESSONS"] if lessons_path.exists() else {}
        no_lesson = [c["id"] for c in lv["concepts"] if c["id"] not in lessons]
        assert not lessons or not no_lesson, f"{lessons_path.name}: missing lessons for {no_lesson}"
        assert set(lessons) <= {c["id"] for c in lv["concepts"]}, f"{lessons_path.name}: lessons for unknown concepts {sorted(set(lessons) - {c['id'] for c in lv['concepts']})}"
        concept_list = [{**c, "intro": lessons.get(c["id"], c["intro"])} for c in concept_list]
        unknown_extra = set(more) - {c["id"] for c in concept_list}
        assert not unknown_extra, f"{extra_path.name}: extras for unknown concepts {sorted(unknown_extra)}"
        for c in concept_list:
            e = more.get(c["id"], {})
            c = {**c, "problems": [*e.get("warmup", []), *c.get("problems", []), *e.get("practice", [])],
                 "reps": [*c.get("reps", []), *e.get("reps", [])]}
            where = f"level {n} / {c['id']}"
            names = set(c.get("builtins", [])) | set(c.get("quiz_only", []))
            unknown = names - all_builtins()
            assert not unknown, f"{where}: not built-ins: {sorted(unknown)}"
            bad_quiz_only = set(c.get("quiz_only", [])) - UNTESTABLE
            assert not bad_quiz_only, f"{where}: {sorted(bad_quiz_only)} can be tested with code, so they need a problem, not quiz_only"
            assert c.get("problems") or c.get("quiz_only"), f"{where}: a concept needs at least one problem"
            covered |= names
            raw_quiz = []
            for i, q in enumerate(c.get("quiz", [])):
                key = f"{n}:{c['id']}:{i}"
                if key in AUDIT:
                    audited.add(key)
                    if AUDIT[key] is None:
                        continue
                    q = AUDIT[key]
                raw_quiz.append(q)
            qs = _quiz(raw_quiz, f"py:{n}:{c['id']}")
            assert qs, f"{where}: needs quiz questions for the level quiz"
            quiz_pool += qs
            concepts.append({
                "id": c["id"], "title": c["title"], "intro": c["intro"].strip(),
                "builtins": sorted(names),
                "problems": [add(p, category) for p in c.get("problems", [])],
                "reps": _quiz(c["reps"], f"py:{n}:{c['id']}:rep"),
                "review": bool(c.get("review")),
            })
        level_slugs = [s for c in concepts for s in c["problems"]]
        by = {p["slug"]: p for p in problems}
        boss = _boss_data(n, BOSS.get(n, {}), quiz_pool, [q for c in concepts for q in c["reps"]], [by[s] for s in level_slugs])
        levels.append({
            "n": n, "kind": "python", "title": lv["title"], "summary": lv["summary"].strip(), "ready": True,
            "concepts": concepts, "problems": level_slugs, "quiz": quiz_pool, "boss": boss,
        })

    unused = set(AUDIT) - audited
    assert not unused, f"boss.py AUDIT has keys that match no question: {sorted(unused)}"
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
