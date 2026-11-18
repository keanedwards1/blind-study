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
            P("py-say-each", 'Print Each Name', "def roll_call(names: List[str]) -> None:",
              """
A command-line tool lists every user on its own line. Write `roll_call(names)` to print each name in order.

Example: `roll_call(["Ada", "Bo"])` prints `Ada` and then `Bo`. An empty list prints nothing.

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
- **Loop over a list:** `for item in cart:`
- **Print one thing:** `print(word)`
"""),
        ],
        practice=[
            P("py-loop-longest-name", 'Longest Name Without max', "def longest_name(names: List[str]) -> str:",
              """
A table needs to be as wide as its longest name. Write `longest_name(names)` to return the longest name, or the first one if several tie, without using `max`. The list has at least one name.

Example: `longest_name(["Bo", "Ada", "Cy"])` returns `"Ada"`.
""",
              "def longest_name(names: List[str]) -> str:\n    best = names[0]\n    for name in names:\n        if len(name) > len(best):\n            best = name\n    return best\n",
              [([["Bo", "Ada", "Cy"]], "Ada"), ([["Al", "Bo"]], "Al")], [[["x"]], [["aa", "b", "ccc", "ddd"]]],
              forbid=["max"],
              hints=["Keep track of the best name found so far, starting with the first one.",
                     "Compare the lengths with `len(...)`, not the names themselves.",
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
            P("py-count-to-n", 'Print 1 to N', "def rows(n: int) -> None:",
              """
A progress log prints each step number as it runs. Write `rows(n)` to print the numbers from 1 to `n`, one per line.

Example: `rows(3)` prints `1`, `2` and `3`. `rows(0)` prints nothing.

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
            P("py-every-third", "Every Third Item", "def every_third(items: List[str]) -> List[str]:",
              """
A sampling script keeps every third record from a log, starting with the first. Write `every_third(items)` to return the items at positions 0, 3, 6 and so on, using `range` with a step (no slicing).

Example: `every_third(["a", "b", "c", "d", "e"])` returns `["a", "d"]`.
""",
              "def every_third(items: List[str]) -> List[str]:\n    out = []\n    for i in range(0, len(items), 3):\n        out.append(items[i])\n    return out\n",
              [([["a", "b", "c", "d", "e"]], ["a", "d"]), ([[]], [])], [[["x"]], [list("abcdefghij")]],
              forbid=["slicing"],
              hints=["You want positions 0, 3, 6, and so on, up to the end of the list.",
                     "`range` takes a third number, the step, and the stop can be the list's length.",
                     "Loop over those positions and collect the item at each one."],
              grammar="""
## Building blocks
- **Count in steps:** `range(0, 10, 4)` gives 0, 4, 8.
- **Read by position:** `things[k]`
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
            P("py-double-until", 'Doubling Until a Target', "def days_to_reach(target: int) -> int:",
              """
A cache doubles its capacity every time it fills up, starting from 1 slot. Write `days_to_reach(target)` to return how many doublings it takes to have at least `target` slots.

Example: `days_to_reach(8)` returns `3` (1, 2, 4, 8). `days_to_reach(1)` returns `0`.
""",
              "def days_to_reach(target: int) -> int:\n    seeds, days = 1, 0\n    while seeds < target:\n        seeds *= 2\n        days += 1\n    return days\n",
              [([8], 3), ([1], 0)], [[2], [9], [1000]],
              hints=["You don't know in advance how many doublings it takes, which is exactly when a `while` loop fits.",
                     "Keep two numbers: the current size and the number of doublings so far.",
                     "While the size is still below the target, double it and count one doubling. A target of 1 needs 0 doublings."],
              grammar="""
## Building blocks
- **Repeat while something is true:** `while level < 10:`
- **Double in place:** `x *= 2`
- **Add one in place:** `n += 1`
"""),
        ],
        practice=[
            P("py-first-failure", "First Failed Check", "def first_failure(results: List[str]) -> int:",
              """
A CI script runs its checks in order and reports the first one that failed. Write `first_failure(results)` to return the index of the first `"fail"`, or `-1` if every check passed. Use `break` to stop looking once you find it.

Example: `first_failure(["pass", "fail", "fail"])` returns `1`, and `first_failure(["pass"])` returns `-1`.
""",
              "def first_failure(results: List[str]) -> int:\n    found = -1\n    for i, r in enumerate(results):\n        if r == \"fail\":\n            found = i\n            break\n    return found\n",
              [([["pass", "fail", "fail"]], 1), ([["pass"]], -1)], [[[]], [["fail"]], [["pass"] * 5 + ["fail"]]],
              require=["break"],
              hints=["Start your answer as -1, meaning \"not found yet\".",
                     "Loop with positions (`enumerate`), and when you meet a failure, remember its position.",
                     "Then `break` straight away, so a later failure can't overwrite the first one."],
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
            P("py-pending-list", "A List of Placeholders", "def pending(n: int) -> List[str]:",
              """
A task tracker creates `n` empty slots marked `"pending"` before any work starts. Write `pending(n)` to build that list by appending one `"pending"` at a time in a loop.

Example: `pending(2)` returns `["pending", "pending"]`, and `pending(0)` returns `[]`.
""",
              "def pending(n: int) -> List[str]:\n    out = []\n    for _ in range(n):\n        out.append(\"pending\")\n    return out\n",
              [([2], ["pending", "pending"]), ([0], [])], [[1], [5]],
              require=[".append"],
              hints=["Start with an empty list.",
                     "Loop `n` times with `range`; the loop variable isn't needed, so `_` is a fine name.",
                     "Each time round, `append` one `\"pending\"`."],
              grammar="""
## Building blocks
- **Empty list:** `[]`
- **Add to the end:** `bag.append("x")`
- **Repeat n times:** `for _ in range(3):`
"""),
        ],
        practice=[
            P("py-sorted-copy-top", 'Top Three Without Changing the List', "def best_three(scores: List[int]) -> List[int]:",
              """
A leaderboard shows the three best scores, largest first, but the original list is shared with other code and must not change. Write `best_three(scores)` to return a new list of the three largest values (fewer if there aren't three).

Example: `best_three([5, 1, 9, 7])` returns `[9, 7, 5]`. `.sort()` would change the list you were given, so copy it first.
""",
              "def best_three(scores: List[int]) -> List[int]:\n    copy = scores[:]\n    copy.sort(reverse=True)\n    return copy[:3]\n",
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
            P("py-first-two-trees", 'First Two Items', "def first_two(rows: List[str]) -> List[str]:",
              """
A preview card shows only the first two tags of a post. Write `first_two(rows)` to return the first two items (or fewer, if there aren't two), using a slice.

Example: `first_two(["oak", "ash", "elm"])` returns `["oak", "ash"]`.
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
            P("py-middle-rows", 'Drop the First and Last', "def middle(rows: List[int]) -> List:",
              """
A CSV export wraps its data with a header row and a footer row. Write `middle(rows)` to return `[the rows without the first and last, how many that is]`.

Example: `middle([0, 5, 6, 7, 0])` returns `[[5, 6, 7], 3]`, and `middle([0, 0])` returns `[[], 0]`.
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
            P("py-numbered-rows", 'Print with Positions', "def labels(rows: List[str]) -> None:",
              """
A debugging helper prints each item with its index. Write `labels(rows)` to print one line per item: the position (starting at 0), a space, then the item.

Example: `labels(["oak", "ash"])` prints `0 oak` and then `1 ash`.

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
            P("py-busiest-day", "Busiest Day", "def busiest_day(days: List[str], visits: List[int]) -> str:",
              """
A traffic report has the days of the week in one list and the number of site visits on each day in another, in the same order. Write `busiest_day(days, visits)` to return the day with the most visits (the first one if there's a tie). Both lists have at least one item.

Example: `busiest_day(["mon", "tue"], [3, 5])` returns `"tue"`.
""",
              "def busiest_day(days: List[str], visits: List[int]) -> str:\n    best_day, best = days[0], visits[0]\n    for d, v in zip(days, visits):\n        if v > best:\n            best_day, best = d, v\n    return best_day\n",
              [([["mon", "tue"], [3, 5]], "tue"), ([["sun"], [1]], "sun")], [[["a", "b", "c"], [5, 5, 1]], [["a", "b"], [1, 9]]],
              hints=["`zip(a, b)` pairs each day with its visit count.",
                     "Keep the best day and its count so far, starting with the first pair.",
                     "Replace them only when a day has strictly more visits, so ties keep the first day."],
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
            P("py-total-amounts", 'Add Up a List', "def total(amounts: List[int]) -> int:",
              """
An invoice totals its line amounts. Write `total(amounts)` to return the sum of the list, using `sum`.

Example: `total([3, 4, 5])` returns `12`, and `total([])` returns `0`.
""",
              "def total(amounts: List[int]) -> int:\n    return sum(amounts)\n",
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
            P("py-sorted-scores", 'Sort Without Changing the Original', "def ranked(scores: List[int]) -> List[int]:",
              """
A report shows scores from highest to lowest, and the original list must stay as it is. Write `ranked(scores)` to return a new list sorted largest first, using `sorted`.

Example: `ranked([3, 9, 1])` returns `[9, 3, 1]`.
""",
              "def ranked(scores: List[int]) -> List[int]:\n    return sorted(scores, reverse=True)\n",
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
            P("py-any-done", "Is Any Job Finished?", "def any_done(jobs: List[bool]) -> bool:",
              """
A dashboard lights up as soon as at least one background job has finished. Each job is `True` when it's done. Write `any_done(jobs)` using `any`.

Example: `any_done([False, True])` returns `True`, and `any_done([])` returns `False`.
""",
              "def any_done(jobs: List[bool]) -> bool:\n    return any(jobs)\n",
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
            P("py-all-labelled", 'Check Every Label', "def all_labelled(labels: List[str]) -> bool:",
              """
Before saving, a form checks that every label is filled in and starts with a capital letter. Write `all_labelled(labels)` to return `True` only if every label is non-empty and its first character is upper case.

Example: `all_labelled(["Apples", "Pears"])` returns `True`; `all_labelled(["Apples", ""])` and `all_labelled(["apples"])` both return `False`. An empty list counts as `True`.
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
            P("py-print-grid", 'Print a Grid', "def show(grid: List[List[str]]) -> None:",
              """
A terminal game draws its map from a grid of single characters. Write `show(grid)` to print each row as one line, with the characters joined together and no spaces.

Example: `show([["a", "b"], ["c", "d"]])` prints `ab` and then `cd`.

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
            P("py-count-walls", "Count the Walls", "def count_walls(grid: List[List[str]]) -> int:",
              """
A maze is stored as a grid where `"#"` is a wall and `"."` is open floor. Write `count_walls(grid)` to return how many wall cells there are.

Example: `count_walls([["#", "."], [".", "#"]])` returns `2`, and an empty grid returns `0`.
""",
              "def count_walls(grid: List[List[str]]) -> int:\n    n = 0\n    for row in grid:\n        for cell in row:\n            if cell == \"#\":\n                n += 1\n    return n\n",
              [([[["#", "."], [".", "#"]]], 2), ([[]], 0)], [[[["."]]], [[["#", "#", "#"]]]],
              hints=["A loop inside a loop visits every cell: rows on the outside, cells on the inside.",
                     "Keep one counter for the whole grid.",
                     "Add one whenever a cell is `\"#\"`."],
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
        P("py-review-sales-report", "Sales Report", "def report(names: List[str], sales: List[int]) -> List[str]:",
              """
A weekly email lists every salesperson who closed **more than 5** sales, numbered from 1, best seller first. Write `report(names, sales)`, where the two lists line up by position, to return lines like `"1. Ada (9)"`. People with equal sales keep their original order.

Example: `report(["Bo", "Ada", "Cy"], [6, 9, 2])` returns `["1. Ada (9)", "2. Bo (6)"]`.
""",
              "def report(names: List[str], sales: List[int]) -> List[str]:\n    pairs = [(s, n) for n, s in zip(names, sales) if s > 5]\n    pairs = sorted(pairs, key=lambda p: -p[0])\n    return [f\"{i}. {n} ({s})\" for i, (s, n) in enumerate(pairs, start=1)]\n",
              [([["Bo", "Ada", "Cy"], [6, 9, 2]], ["1. Ada (9)", "2. Bo (6)"]), ([[], []], [])],
              [[["a", "b"], [6, 6]], [["x"], [1]], [["p", "q", "r"], [10, 7, 8]]],
              hints=["Three steps: keep only the people with more than 5 sales, sort them, then number the lines.",
                     "`zip` pairs each name with its sales; keep the pairs where the sales are more than 5.",
                     "Sort by sales largest first (sorting is stable, so ties keep their order), then use `enumerate(..., start=1)` to number them.",
                     "Build each line with an f-string: number, dot, space, name, then the sales in brackets."],
              grammar="""
## Building blocks
- **Walk two lists together:** `zip(xs, ys)`
- **Sort by something:** `sorted(words, key=len)`
- **Turn largest-first into smallest-first:** sort by `-x` instead of `x`.
- **Part of a pair:** `pair[0]`
- **Number from 1:** `enumerate(things, start=1)`
- **Text with values in it:** `f"{a}. {b}"`
"""),
        P("py-review-local-dips", "Find the Dips", "def dips(readings: List[int]) -> List[int]:",
              """
A monitoring script flags sensor readings that are lower than **both** of their neighbours. The first and last readings only have one neighbour, so they're never flagged. Write `dips(readings)` to return the positions of the flagged readings, in order.

Example: `dips([5, 2, 6, 6, 1, 3])` returns `[1, 4]`.
""",
              "def dips(readings: List[int]) -> List[int]:\n    out = []\n    for i in range(1, len(readings) - 1):\n        if readings[i] < readings[i - 1] and readings[i] < readings[i + 1]:\n            out.append(i)\n    return out\n",
              [([[5, 2, 6, 6, 1, 3]], [1, 4]), ([[1, 2]], [])], [[[]], [[3, 1, 3, 1, 3]], [[2, 2, 2]]],
              hints=["Only the inner positions (not the first or last) can be flagged.",
                     "`range(1, len(readings) - 1)` gives exactly the inner positions.",
                     "For each one, compare it with the reading before (`i - 1`) and after (`i + 1`); it must be smaller than both."],
              grammar="""
## Building blocks
- **Count from 1 up to a stop:** `range(1, stop)`
- **One less than the length:** `len(xs) - 1`
- **Neighbours:** `xs[k - 1]`, `xs[k + 1]`
- **Both must hold:** `and`
"""),
        P("py-review-batches-needed", "How Many Batches?", "def batches_needed(queues: List[int], per_batch: int) -> int:",
              """
Several work queues are drained in batches, and each batch can take at most `per_batch` items from one queue. Write `batches_needed(queues, per_batch)` to return how many batches the longest queue needs (0 if there are no queues). `per_batch` is at least 1.

Example: `batches_needed([5, 9, 2], 4)` returns `3`, because the queue of 9 needs three batches of up to 4.
""",
              "def batches_needed(queues: List[int], per_batch: int) -> int:\n    most = 0\n    for items in queues:\n        needed = (items + per_batch - 1) // per_batch\n        most = max(most, needed)\n    return most\n",
              [([[5, 9, 2], 4], 3), ([[], 3], 0)], [[[0], 2], [[8], 4], [[1, 1, 1], 1], [[10, 3], 3]],
              hints=["For one queue, the batches needed is its length divided by `per_batch`, rounded **up**.",
                     "Rounding up with whole numbers: add `per_batch - 1` before using `//`. (9 items, 4 per batch: (9 + 3) // 4 = 3.)",
                     "Work this out for every queue and keep the largest."],
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
