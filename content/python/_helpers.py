# Shared helpers for content/python/levelNN.py (scripts/python_levels.py puts this folder on sys.path).


def P(slug, title, sig, desc, solution, examples, tests, *, hints=(), grammar="", explanation="", difficulty="Easy", **spec):
    """One Learn Python task, in the same dict format as the Blind 75 problems (see README).

    Pass sig=None for class tasks and give `starter=` instead. Extra keyword arguments are spec keys
    (out, stdin, compare, raises, require, forbid, mutate, kind, cls, driver, checker, in).
    """
    d = dict(slug=slug, title=title, difficulty=difficulty, desc=desc, hints=list(hints), solution=solution,
             explanation=explanation or "See the solution above.", examples=examples, tests=tests, grammar=grammar, **spec)
    if sig:
        d["sig"] = sig
    return d


def Q(q, right, *wrong, why="", code=None, predict=False):
    """A multiple-choice question. The correct option comes first; the UI shuffles them.
    predict=True runs `code` at build time and checks that it prints exactly the correct option."""
    d = dict(q=q, options=[right, *wrong], answer=0, why=why)
    if code:
        d["code"] = code
    if predict:
        d["predict"] = True
    return d


class Gen:
    """Expected value for a generator task (with compare="strict"): Gen([3, 2, 1]) means "a generator yielding 3, 2, 1"."""

    def __init__(self, items):
        self.items = list(items)

    def __repr__(self):
        return f"<generator yielding {self.items!r}>"
