# Extra practice for Learn Python level 3 (Loops & lists), merged into level03.py by scripts/python_levels.py.
#
# EXTRA[concept_id]:
#   warmup   - easier tasks placed before the concept's existing ones
#   practice - tasks placed after them, usually mixing in an earlier idea
#   reps     - predict-the-output questions for the rep room (answers are checked at build time)
# REVIEW is a mixed review group added at the end of the world, before the guardian.
from _helpers import P, Q

EXTRA = {
    "for-loops": dict(
        warmup=[
            P("py-say-each", "Roll Call", "def roll_call(names: List[str]) -> None:",
              """
Every morning the orchard keeper calls out each picker's name.

- **You get:** `names`, a list of names.
- **Print:** each name on its own line, in order.
- **Example:** `["Ada", "Bo"]` prints `Ada` then `Bo`.

_This task checks what you print._
""",
              "def roll_call(names: List[str]) -> None:\n    for name in names:\n        print(name)\n",
              [([["Ada", "Bo"]], "Ada\nBo\n"), ([[]], "")], [[["x"]], [["a", "b", "c"]]],
              out="stdout",
              hints=["A `for` loop runs its indented lines once for each item in a list.",
                     "Inside the loop, the loop variable holds the current item.",
                     "Print the loop variable each time round. An empty list prints nothing."],
              grammar="""
## Building blocks
- **Loop over a list:** `for fruit in basket:`
- **Print one thing:** `print(word)`
"""),
        ],
        practice=[
            P("py-loop-longest-name", "The Longest Ladder", "def longest_name(names: List[str]) -> str:",
              """
The picker with the longest name gets the tallest ladder (it's tradition). Find them without using `max`.

- **You get:** `names` (at least one).
- **Return:** the longest name; if there's a tie, the first one.
- **Example:** `["Bo", "Ada", "Cy"]` → `"Ada"`.
""",
              "def longest_name(names: List[str]) -> str:\n    best = names[0]\n    for name in names:\n        if len(name) > len(best):\n            best = name\n    return best\n",
              [([["Bo", "Ada", "Cy"]], "Ada"), ([["Al", "Bo"]], "Al")], [[["x"]], [["aa", "b", "ccc", "ddd"]]],
              forbid=["max"],
              hints=["Keep track of the best name found so far, starting with the first one.",
                     "Compare lengths with `len(...)`, not the names themselves.",
                     "Replace the best only when a name is strictly longer, so ties keep the first one."],
              grammar="""
## Building blocks
- **Length of text:** `len(word)`
- **Strictly bigger:** `>`
- **Start from the first item:** `items[0]`
"""),
        ],
        reps=[
            Q("What does this print?", "6", "3", "123", "0", code="t = 0\nfor x in [1, 2, 3]:\n    t += x\nprint(t)", predict=True,
              why="The loop adds 1, then 2, then 3 to the total."),
            Q("What does this print?", "a-b-c-", "abc", "a-b-c", "-a-b-c", code="for ch in 'abc':\n    print(ch, end='-')", predict=True,
              why="Looping over a string gives one character at a time; `end='-'` replaces each new line with a dash."),
            Q("What does this print?", "2", "3", "1", "0", code="n = 0\nfor w in ['hi', 'x', 'yes']:\n    if len(w) > 1:\n        n += 1\nprint(n)", predict=True,
              why="Only `hi` and `yes` have more than one character."),
        ],
    ),
    "range": dict(
        warmup=[
            P("py-count-to-n", "Count the Rows", "def rows(n: int) -> None:",
              """
The orchard has `n` rows of trees, numbered from 1. Print each row number.

- **You get:** `n` (0 or more).
- **Print:** the numbers 1 to `n`, one per line.
- **Example:** `3` prints `1`, `2`, `3`.

_This task checks what you print._
""",
              "def rows(n: int) -> None:\n    for i in range(1, n + 1):\n        print(i)\n",
              [([3], "1\n2\n3\n"), ([0], "")], [[1], [5]],
              out="stdout",
              hints=["`range(start, stop)` counts from `start` up to but not including `stop`.",
                     "To finish at `n`, the stop has to be one more than `n`.",
                     "Print each number the loop gives you."],
              grammar="""
## Building blocks
- **Count from a start:** `range(1, 6)` gives 1, 2, 3, 4, 5.
- **Print a value:** `print(x)`
"""),
        ],
        practice=[
            P("py-every-third-tree", "Every Third Tree", "def marked(trees: List[str]) -> List[str]:",
              """
The keeper ties a ribbon on every third tree, starting with the first.

- **You get:** `trees`, a list of tree names.
- **Return:** the names at positions 0, 3, 6, …, using `range` with a step.
- **Example:** `["a", "b", "c", "d", "e"]` → `["a", "d"]`.
""",
              "def marked(trees: List[str]) -> List[str]:\n    out = []\n    for i in range(0, len(trees), 3):\n        out.append(trees[i])\n    return out\n",
              [([["a", "b", "c", "d", "e"]], ["a", "d"]), ([[]], [])], [[["x"]], [list("abcdefghij")]],
              forbid=["slicing"],
              hints=["You want positions 0, 3, 6, … up to the end of the list.",
                     "`range` takes a third number, the step, and the stop can be the list's length.",
                     "Loop over those positions and collect the tree at each one (no slicing allowed here)."],
              grammar="""
## Building blocks
- **Count in steps:** `range(0, 10, 4)` gives 0, 4, 8.
- **Read by position:** `items[k]`
- **Add to a list:** `out.append(x)`
"""),
        ],
        reps=[
            Q("What does this print?", "[2, 3, 4]", "[2, 3, 4, 5]", "[1, 2, 3, 4]", "[3, 4]", code="print(list(range(2, 5)))", predict=True,
              why="`range(2, 5)` starts at 2 and stops before 5."),
            Q("What does this print?", "[10, 7, 4, 1]", "[10, 7, 4]", "[10, 7, 4, 1, -2]", "[1, 4, 7, 10]", code="print(list(range(10, 0, -3)))", predict=True,
              why="A step of -3 counts down; it stops before reaching 0."),
            Q("What does this print?", "0", "3", "[]", "None", code="print(len(range(5, 5)))", predict=True,
              why="Start and stop are equal, so the range is empty."),
        ],
    ),
    "while-break": dict(
        warmup=[
            P("py-double-until", "Doubling Seeds", "def days_to_reach(target: int) -> int:",
              """
A magic seed pod starts with 1 seed and doubles every day. How many days until it has **at least** `target` seeds?

- **You get:** `target` (1 or more).
- **Return:** the number of days. On day 0 there is 1 seed.
- **Example:** `8` → `3` (1, 2, 4, 8).
""",
              "def days_to_reach(target: int) -> int:\n    seeds, days = 1, 0\n    while seeds < target:\n        seeds *= 2\n        days += 1\n    return days\n",
              [([8], 3), ([1], 0)], [[2], [9], [1000]],
              hints=["You don't know in advance how many days it takes, which is exactly when a `while` loop fits.",
                     "Keep two numbers: the seeds and the days so far.",
                     "While there are still too few seeds, double them and count a day. A target of 1 needs 0 days."],
              grammar="""
## Building blocks
- **Repeat while something is true:** `while level < 10:`
- **Double in place:** `x *= 2`
- **Add one in place:** `n += 1`
"""),
        ],
        practice=[
            P("py-first-rotten", "Find the Rotten Apple", "def first_rotten(apples: List[str]) -> int:",
              """
Apples are checked in order. Stop at the first rotten one (`"rotten"`) and report its position.

- **You get:** `apples`, a list of words like `"good"` or `"rotten"`.
- **Return:** the index of the first `"rotten"`, or `-1` if they're all fine. Use `break`.
- **Example:** `["good", "rotten", "rotten"]` → `1`.
""",
              "def first_rotten(apples: List[str]) -> int:\n    found = -1\n    for i, a in enumerate(apples):\n        if a == \"rotten\":\n            found = i\n            break\n    return found\n",
              [([["good", "rotten", "rotten"]], 1), ([["good"]], -1)], [[[]], [["rotten"]], [["good"] * 5 + ["rotten"]]],
              require=["break"],
              hints=["Start your answer as -1, meaning \"not found yet\".",
                     "Loop with positions (`enumerate`), and when you meet a rotten apple, remember its position.",
                     "Then `break` straight away, so a later rotten apple can't overwrite the first."],
              grammar="""
## Building blocks
- **Position and item:** `for k, item in enumerate(things):`
- **Leave the loop now:** `break`
- **Compare text:** `word == "x"`
"""),
        ],
        reps=[
            Q("What does this print?", "3", "4", "2", "8", code="n, steps = 8, 0\nwhile n > 1:\n    n //= 2\n    steps += 1\nprint(steps)", predict=True,
              why="8 → 4 → 2 → 1 takes three halvings."),
            Q("What does this print?", "[1, 2]", "[1, 2, 3]", "[1]", "[3]", code="out = []\nfor x in [1, 2, 3]:\n    if x == 3:\n        break\n    out.append(x)\nprint(out)", predict=True,
              why="`break` stops the loop before 3 is printed."),
            Q("What does this print?", "[1, 3]", "[1, 2, 3]", "[2]", "[1]", code="out = []\nfor x in [1, 2, 3]:\n    if x == 2:\n        continue\n    out.append(x)\nprint(out)", predict=True,
              why="`continue` skips the rest of that round only, so 2 isn't printed but 3 is."),
        ],
    ),
    "list-methods": dict(
        warmup=[
            P("py-pick-basket", "Fill the Basket", "def basket(apples: int) -> List[str]:",
              """
Build a basket by adding one `"apple"` at a time.

- **You get:** `apples`, how many to add (0 or more).
- **Return:** a list with that many `"apple"` strings, built with `append` in a loop.
- **Example:** `2` → `["apple", "apple"]`.
""",
              "def basket(apples: int) -> List[str]:\n    out = []\n    for _ in range(apples):\n        out.append(\"apple\")\n    return out\n",
              [([2], ["apple", "apple"]), ([0], [])], [[1], [5]],
              require=[".append"],
              hints=["Start with an empty list.",
                     "Loop `apples` times with `range`; the loop variable isn't needed, so `_` is a fine name.",
                     "Each time round, `append` one `\"apple\"`."],
              grammar="""
## Building blocks
- **Empty list:** `[]`
- **Add to the end:** `bag.append("pear")`
- **Repeat n times:** `for _ in range(3):`
"""),
        ],
        practice=[
            P("py-sorted-copy-top", "Best Three Harvests", "def best_three(harvests: List[int]) -> List[int]:",
              """
Pick the three biggest harvests, biggest first, **without** changing the original list.

- **You get:** `harvests`, a list of numbers.
- **Return:** a new list of the three largest, largest first (fewer if there aren't three).
- **Example:** `[5, 1, 9, 7]` → `[9, 7, 5]`.
- **Watch out:** `.sort()` changes the list you were given; copy it first.
""",
              "def best_three(harvests: List[int]) -> List[int]:\n    copy = harvests[:]\n    copy.sort(reverse=True)\n    return copy[:3]\n",
              [([[5, 1, 9, 7]], [9, 7, 5]), ([[2]], [2])], [[[]], [[3, 3, 3, 3]], [[1, 2, 3, 4, 5, 6]]],
              hints=["You need a copy so the original isn't sorted too. A full slice makes one.",
                     "Sort the copy largest first with `reverse=True`.",
                     "Return the first three items with a slice, which is safe for short lists."],
              grammar="""
## Building blocks
- **Copy a list:** `dup = things[:]`
- **Sort in place, largest first:** `nums.sort(reverse=True)`
- **First few items:** `xs[:2]`
"""),
        ],
        reps=[
            Q("What does this print?", "[1, 2, 3]", "[3, 2, 1]", "None", "[1, 2]", code="a = [3, 1, 2]\na.sort()\nprint(a)", predict=True,
              why="`sort()` changes the list itself."),
            Q("What does this print?", "None", "[1, 2, 3]", "[3, 1, 2]", "error", code="a = [3, 1, 2]\nprint(a.sort())", predict=True,
              why="`sort()` returns `None`; it sorts in place instead of giving you a new list."),
            Q("What does this print?", "[1, [2, 3]] [1, 2, 3]", "[1, 2, 3] [1, 2, 3]", "[1, [2, 3]] [1, [2, 3]]", "error",
              code="a = [1]\nb = [1]\na.append([2, 3])\nb.extend([2, 3])\nprint(a, b)", predict=True,
              why="`append` adds the whole list as one item; `extend` adds its items one by one."),
        ],
    ),
    "list-slicing": dict(
        warmup=[
            P("py-first-two-trees", "First Two Rows", "def first_two(rows: List[str]) -> List[str]:",
              """
The tour only visits the first two rows of the orchard.

- **You get:** `rows`, a list of row names.
- **Return:** the first two (or fewer, if there aren't two), using a slice.
- **Example:** `["oak", "ash", "elm"]` → `["oak", "ash"]`.
""",
              "def first_two(rows: List[str]) -> List[str]:\n    return rows[:2]\n",
              [([["oak", "ash", "elm"]], ["oak", "ash"]), ([["fir"]], ["fir"])], [[[]], [["a", "b"]]],
              require=["slicing"],
              hints=["A slice `xs[a:b]` takes items from position `a` up to but not including `b`.",
                     "Leaving `a` out means \"from the start\".",
                     "Slices never crash past the end of a list, so short lists are fine."],
              grammar="""
## Building blocks
- **From the start up to a position:** `xs[:4]`
"""),
        ],
        practice=[
            P("py-middle-rows", "The Middle Rows", "def middle(rows: List[int]) -> List:",
              """
The first and last rows are fences, not trees. Return everything in between, then count how many trees that is.

- **You get:** `rows`.
- **Return:** `[the rows without the first and last, how many that is]`.
- **Example:** `[0, 5, 6, 7, 0]` → `[[5, 6, 7], 3]`.
""",
              "def middle(rows: List[int]) -> List:\n    inner = rows[1:-1]\n    return [inner, len(inner)]\n",
              [([[0, 5, 6, 7, 0]], [[5, 6, 7], 3]), ([[0, 0]], [[], 0])], [[[]], [[1]], [[1, 2, 3]]],
              hints=["A slice can start at 1 and stop at -1 (just before the last item).",
                     "That slice is empty for lists with fewer than 3 items, which is what you want.",
                     "Then return the slice together with its length, inside a list."],
              grammar="""
## Building blocks
- **Skip the first and last:** `xs[1:-1]`
- **How many:** `len(xs)`
"""),
        ],
        reps=[
            Q("What does this print?", "[2, 3]", "[1, 2, 3]", "[2, 3, 4]", "[1, 2]", code="a = [1, 2, 3, 4]\nprint(a[1:3])", predict=True,
              why="The slice starts at position 1 and stops before position 3."),
            Q("What does this print?", "[4, 3, 2, 1]", "[1, 2, 3, 4]", "[4]", "[1]", code="a = [1, 2, 3, 4]\nprint(a[::-1])", predict=True,
              why="A step of -1 walks backwards over the whole list."),
            Q("What does this print?", "[1, 2] [0, 2]", "[0, 2] [0, 2]", "[1, 2] [1, 2]", "error",
              code="a = [1, 2]\nb = a[:]\nb[0] = 0\nprint(a, b)", predict=True,
              why="`a[:]` makes a separate copy, so changing `b` leaves `a` alone."),
            Q("What does this print?", "[0, 2] [0, 2]", "[1, 2] [0, 2]", "[1, 2] [1, 2]", "error",
              code="a = [1, 2]\nb = a\nb[0] = 0\nprint(a, b)", predict=True,
              why="`b = a` doesn't copy: both names point at the same list."),
        ],
    ),
    "enumerate-zip": dict(
        warmup=[
            P("py-numbered-rows", "Label the Rows", "def labels(rows: List[str]) -> None:",
              """
Print each row with its position, starting from 0, like `0 oak`.

- **You get:** `rows`.
- **Print:** one line per row: the position, a space, the name.
- **Example:** `["oak", "ash"]` prints `0 oak` then `1 ash`.

_This task checks what you print._
""",
              "def labels(rows: List[str]) -> None:\n    for i, name in enumerate(rows):\n        print(i, name)\n",
              [([["oak", "ash"]], "0 oak\n1 ash\n"), ([[]], "")], [[["x"]], [["a", "b", "c"]]],
              out="stdout", require=["enumerate"],
              hints=["`enumerate(list)` gives `(position, item)` pairs.",
                     "Unpack each pair into two names in the `for` line.",
                     "`print(a, b)` puts one space between the two values."],
              grammar="""
## Building blocks
- **Position and item together:** `for k, item in enumerate(things):`
- **Print two values with a space:** `print(a, b)`
"""),
        ],
        practice=[
            P("py-heaviest-day", "Heaviest Picking Day", "def heaviest_day(days: List[str], kilos: List[int]) -> str:",
              """
Two lists: the days of the week, and the kilos picked on each day, in the same order. Which day was heaviest?

- **You get:** `days` and `kilos`, the same length (at least one).
- **Return:** the day with the most kilos (the first one if tied).
- **Example:** `["mon", "tue"]` and `[3, 5]` → `"tue"`.
""",
              "def heaviest_day(days: List[str], kilos: List[int]) -> str:\n    best_day, best = days[0], kilos[0]\n    for d, k in zip(days, kilos):\n        if k > best:\n            best_day, best = d, k\n    return best_day\n",
              [([["mon", "tue"], [3, 5]], "tue"), ([["sun"], [1]], "sun")], [[["a", "b", "c"], [5, 5, 1]], [["a", "b"], [1, 9]]],
              hints=["`zip(a, b)` pairs each day with its kilos.",
                     "Keep the best day and its kilos so far, starting with the first pair.",
                     "Replace them only when a day is strictly heavier, so ties keep the first day."],
              grammar="""
## Building blocks
- **Walk two lists together:** `for a, b in zip(xs, ys):`
- **Two names at once:** `p, q = 1, 2`
"""),
        ],
        reps=[
            Q("What does this print?", "[(0, 'a'), (1, 'b')]", "[('a', 0), ('b', 1)]", "[0, 1]", "['a', 'b']", code="print(list(enumerate('ab')))", predict=True,
              why="`enumerate` pairs each item with its position, position first."),
            Q("What does this print?", "[(1, 'x'), (2, 'y')]", "[(1, 'x'), (2, 'y'), (3, None)]", "error", "[1, 2, 3]",
              code="print(list(zip([1, 2, 3], 'xy')))", predict=True, why="`zip` stops at the shorter input."),
            Q("What does this print?", "1 a\n2 b", "0 a\n1 b", "a 1\nb 2", "1 2", code="for i, ch in enumerate('ab', start=1):\n    print(i, ch)", predict=True,
              why="`start=1` makes the counting begin at 1."),
        ],
    ),
    "list-builtins": dict(
        warmup=[
            P("py-total-apples", "Total Apples", "def total(baskets: List[int]) -> int:",
              """
Add up the apples in every basket, the quick way.

- **You get:** `baskets`, a list of counts.
- **Return:** the total, using `sum`.
- **Example:** `[3, 4, 5]` → `12`; `[]` → `0`.
""",
              "def total(baskets: List[int]) -> int:\n    return sum(baskets)\n",
              [([[3, 4, 5]], 12), ([[]], 0)], [[[1]], [[10, -2]]],
              require=["sum"],
              hints=["Python has a built-in that adds up a whole list.",
                     "It returns 0 for an empty list, so there's no special case.",
                     "Return its result directly."],
              grammar="""
## Building blocks
- **Add up a list:** `sum(xs)`
"""),
        ],
        practice=[
            P("py-ranked-pickers", "Ranked Pickers", "def ranked(kilos: List[int]) -> List[int]:",
              """
Rank the pickers' totals from most to least, and leave the original record alone.

- **You get:** `kilos`.
- **Return:** a new list sorted from largest to smallest, using `sorted`.
- **Example:** `[3, 9, 1]` → `[9, 3, 1]`.
""",
              "def ranked(kilos: List[int]) -> List[int]:\n    return sorted(kilos, reverse=True)\n",
              [([[3, 9, 1]], [9, 3, 1]), ([[]], [])], [[[1, 1, 2]], [[5]]],
              require=["sorted"],
              hints=["`sorted(...)` returns a brand-new sorted list and leaves the original as it was.",
                     "By default it sorts smallest first.",
                     "Pass `reverse=True` to get largest first."],
              grammar="""
## Building blocks
- **A new sorted list:** `sorted(xs)`
- **Largest first:** `reverse=True`
"""),
        ],
        reps=[
            Q("What does this print?", "[1, 2, 3] [3, 1, 2]", "[1, 2, 3] [1, 2, 3]", "None [3, 1, 2]", "error",
              code="a = [3, 1, 2]\nb = sorted(a)\nprint(b, a)", predict=True, why="`sorted` returns a new list and leaves `a` unchanged."),
            Q("What does this print?", "6", "[1, 2, 3]", "123", "3", code="print(sum([1, 2, 3]))", predict=True, why="`sum` adds the items."),
            Q("What does this print?", "[3, 2, 1]", "[1, 2, 3]", "<list_reverseiterator>", "None", code="print(list(reversed([1, 2, 3])))", predict=True,
              why="`reversed` walks backwards; `list(...)` collects the result."),
        ],
    ),
    "any-all": dict(
        warmup=[
            P("py-any-ripe", "Anything Ripe?", "def any_ripe(apples: List[bool]) -> bool:",
              """
Each apple is `True` if it's ripe. Is at least one ready to pick?

- **You get:** `apples`, a list of booleans.
- **Return:** `True` if any is ripe, using `any`.
- **Example:** `[False, True]` → `True`; `[]` → `False`.
""",
              "def any_ripe(apples: List[bool]) -> bool:\n    return any(apples)\n",
              [([[False, True]], True), ([[]], False)], [[[False]], [[True, True]]],
              require=["any"],
              hints=["`any(list)` is `True` when at least one item is true.",
                     "It's `False` for an empty list.",
                     "Return its result."],
              grammar="""
## Building blocks
- **At least one is true:** `any(flags)`
"""),
        ],
        practice=[
            P("py-all-labelled", "Every Crate Labelled?", "def all_labelled(labels: List[str]) -> bool:",
              """
A crate is labelled if its label isn't empty. Is every crate labelled, and is the first letter of each label upper case?

- **You get:** `labels`.
- **Return:** `True` if every label is non-empty and starts with a capital letter.
- **Example:** `["Apples", "Pears"]` → `True`; `["Apples", ""]` → `False`; `["apples"]` → `False`.
""",
              "def all_labelled(labels: List[str]) -> bool:\n    return all(lab != \"\" and lab[0].isupper() for lab in labels)\n",
              [([["Apples", "Pears"]], True), ([["Apples", ""]], False), ([["apples"]], False)], [[[]], [["A"]], [["Ab", "b"]]],
              require=["all"],
              hints=["Two checks per label: it isn't empty, and its first character is upper case.",
                     "Check the empty case first and join the two checks with `and`, so you never read `[0]` of an empty label.",
                     "`all(...)` over a generator gives one answer for every label. An empty list counts as `True`."],
              grammar="""
## Building blocks
- **Every item passes:** `all(...)`
- **Upper-case letter?** `ch.isupper()`
- **First character:** `word[0]`
"""),
        ],
        reps=[
            Q("What does this print?", "True False", "False True", "True True", "False False", code="print(all([]), any([]))", predict=True,
              why="With nothing to check, `all` is `True` (nothing failed) and `any` is `False` (nothing passed)."),
            Q("What does this print?", "False", "True", "0", "error", code="print(all([1, 2, 0]))", predict=True, why="`0` is falsy, so not all items are true."),
            Q("What does this print?", "True", "False", "2", "error", code="print(any(x > 1 for x in [0, 1, 2]))", predict=True,
              why="2 is greater than 1, so at least one item passes."),
        ],
    ),
    "nested": dict(
        warmup=[
            P("py-print-grid", "Print the Orchard Map", "def show(grid: List[List[str]]) -> None:",
              """
The orchard map is a grid of letters. Print each row as one line with no spaces.

- **You get:** `grid`, a list of rows (each a list of letters).
- **Print:** each row's letters joined together, one row per line.
- **Example:** `[["a", "b"], ["c", "d"]]` prints `ab` then `cd`.

_This task checks what you print._
""",
              "def show(grid: List[List[str]]) -> None:\n    for row in grid:\n        print(\"\".join(row))\n",
              [([[["a", "b"], ["c", "d"]]], "ab\ncd\n"), ([[]], "")], [[[["x"]]], [[["a", "b", "c"]]]],
              out="stdout",
              hints=["Loop over the rows; each row is a list of letters.",
                     "`\"\".join(list)` glues a list of strings together with nothing between them.",
                     "Print the joined row each time round."],
              grammar="""
## Building blocks
- **Loop over rows:** `for line in table:`
- **Glue letters together:** `"".join(["x", "y"])`
"""),
        ],
        practice=[
            P("py-count-trees-grid", "Count the Trees", "def count_trees(grid: List[List[str]]) -> int:",
              """
On the orchard map, `"T"` is a tree and `"."` is grass. How many trees are there?

- **You get:** `grid`, rows of `"T"` and `"."`.
- **Return:** how many `"T"` cells there are.
- **Example:** `[["T", "."], [".", "T"]]` → `2`.
""",
              "def count_trees(grid: List[List[str]]) -> int:\n    n = 0\n    for row in grid:\n        for cell in row:\n            if cell == \"T\":\n                n += 1\n    return n\n",
              [([[["T", "."], [".", "T"]]], 2), ([[]], 0)], [[[["."]]], [[["T", "T", "T"]]]],
              hints=["A loop inside a loop visits every cell: rows on the outside, cells on the inside.",
                     "Keep one counter for the whole grid.",
                     "Add one whenever a cell is `\"T\"`."],
              grammar="""
## Building blocks
- **Loop inside a loop:** an inner `for` indented under an outer `for`.
- **Compare text:** `spot == "x"`
- **Add one:** `total += 1`
"""),
        ],
        reps=[
            Q("What does this print?", "4", "2", "[1, 2, 3, 4]", "3", code="g = [[1, 2], [3, 4]]\nprint(g[1][1])", predict=True,
              why="`g[1]` is the second row `[3, 4]`, and `[1]` is its second item."),
            Q("What does this print?", "[[1, 0], [1, 0]]", "[[1, 0], [0, 0]]", "[[0, 0], [0, 0]]", "error",
              code="g = [[0, 0]] * 2\ng[0][0] = 1\nprint(g)", predict=True,
              why="`[[0, 0]] * 2` repeats the *same* inner list, so changing one row changes both."),
            Q("What does this print?", "6", "3", "9", "4", code="n = 0\nfor i in range(2):\n    for j in range(3):\n        n += 1\nprint(n)", predict=True,
              why="The inner loop runs 3 times for each of the 2 outer rounds."),
        ],
    ),
}

REVIEW = dict(
    id="review-3", title="Review: loops & lists",
    intro="""
Time to mix it all together. These stages combine loops, `range`, list methods, slicing, `enumerate`/`zip` and the list built-ins. There's no new idea here, just practice choosing the right tool.
""",
    problems=[
        P("py-review-harvest-report", "Harvest Report", "def report(names: List[str], kilos: List[int]) -> List[str]:",
          """
Write the end-of-day report: one line per picker who picked **more than 5** kilos, numbered from 1, biggest picker first.

- **You get:** `names` and `kilos`, the same length.
- **Return:** lines like `"1. Ada (9)"`, ordered by kilos from most to least (equal kilos keep their original order).
- **Example:** `["Bo", "Ada", "Cy"]` and `[6, 9, 2]` → `["1. Ada (9)", "2. Bo (6)"]`.
""",
          "def report(names: List[str], kilos: List[int]) -> List[str]:\n    pairs = [(k, n) for n, k in zip(names, kilos) if k > 5]\n    pairs = sorted(pairs, key=lambda p: -p[0])\n    return [f\"{i}. {n} ({k})\" for i, (k, n) in enumerate(pairs, start=1)]\n",
          [([["Bo", "Ada", "Cy"], [6, 9, 2]], ["1. Ada (9)", "2. Bo (6)"]), ([[], []], [])],
          [[["a", "b"], [6, 6]], [["x"], [1]], [["p", "q", "r"], [10, 7, 8]]],
          hints=["Three steps: keep only the big pickers, sort them, then number the lines.",
                 "`zip` pairs each name with its kilos; keep the pairs where the kilos are more than 5.",
                 "Sort by kilos largest first (sorting is stable, so ties keep their order), then use `enumerate(..., start=1)` to number them.",
                 "Build each line with an f-string: number, dot, space, name, then the kilos in brackets."],
          grammar="""
## Building blocks
- **Walk two lists together:** `zip(xs, ys)`
- **Sort by something:** `sorted(words, key=len)`
- **Turn largest-first into smallest-first:** sort by `-x` instead of `x`.
- **Part of a pair:** `pair[0]`
- **Number from 1:** `enumerate(things, start=1)`
- **Text with values in it:** `f"{a}. {b}"`
"""),
        P("py-review-fence-repair", "Fence Repair", "def broken_sections(fence: List[int]) -> List[int]:",
          """
Each fence section has a strength from 0 to 9. A section needs repair if it's weaker than **both** its neighbours. The two end sections only have one neighbour, so they never count.

- **You get:** `fence`, a list of strengths.
- **Return:** the positions that need repair, in order.
- **Example:** `[5, 2, 6, 6, 1, 3]` → `[1, 4]`.
""",
          "def broken_sections(fence: List[int]) -> List[int]:\n    out = []\n    for i in range(1, len(fence) - 1):\n        if fence[i] < fence[i - 1] and fence[i] < fence[i + 1]:\n            out.append(i)\n    return out\n",
          [([[5, 2, 6, 6, 1, 3]], [1, 4]), ([[1, 2]], [])], [[[]], [[3, 1, 3, 1, 3]], [[2, 2, 2]]],
          hints=["Only the inner positions (not the first or last) can need repair.",
                 "`range(1, len(fence) - 1)` gives exactly the inner positions.",
                 "For each one, compare it with the section before (`i - 1`) and after (`i + 1`); it must be smaller than both."],
          grammar="""
## Building blocks
- **Count from 1 up to a stop:** `range(1, stop)`
- **One less than the length:** `len(xs) - 1`
- **Neighbours:** `xs[k - 1]`, `xs[k + 1]`
- **Both must hold:** `and`
"""),
        P("py-review-picking-rounds", "Picking Rounds", "def rounds(trees: List[int], per_round: int) -> int:",
          """
Each tree has some apples. A picker can take at most `per_round` apples from one tree per round. How many rounds does the slowest tree need?

- **You get:** `trees` (apples on each tree) and `per_round` (at least 1).
- **Return:** the largest number of rounds any tree needs (0 if there are no trees).
- **Example:** `[5, 9, 2]` with `4` → `3` (9 apples need 3 rounds of up to 4).
""",
          "def rounds(trees: List[int], per_round: int) -> int:\n    most = 0\n    for apples in trees:\n        needed = (apples + per_round - 1) // per_round\n        most = max(most, needed)\n    return most\n",
          [([[5, 9, 2], 4], 3), ([[], 3], 0)], [[[0], 2], [[8], 4], [[1, 1, 1], 1], [[10, 3], 3]],
          hints=["For one tree, the rounds needed is the apples divided by `per_round`, rounded **up**.",
                 "Rounding up with whole numbers: add `per_round - 1` before using `//`. (9 apples, 4 per round: (9 + 3) // 4 = 3.)",
                 "Work this out for every tree and keep the largest."],
          grammar="""
## Building blocks
- **Whole-number division:** `17 // 5` is `3`.
- **Larger of two:** `max(a, b)`
- **Loop over a list:** `for x in xs:`
"""),
    ],
    quiz=[
        Q("What does this print?", "[1, 3]", "[1, 2, 3]", "[2]", "[3, 1]", code="a = [1, 2, 3]\nprint(a[::2])", predict=True,
          why="A step of 2 takes every other item, starting at position 0."),
        Q("Which line adds every item of `b` to the end of `a`?", "`a.extend(b)`", "`a.append(b)`", "`a + b`", "`a.insert(b)`",
          why="`extend` adds items one by one; `a + b` builds a new list without changing `a`."),
    ],
)
