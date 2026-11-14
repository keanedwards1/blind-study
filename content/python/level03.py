# Learn Python, level 3: loops and lists.
from _helpers import P, Q

LEVEL = dict(
    n=3,
    title="Loops & lists",
    summary="Repeating work with `for` and `while`, and the list: Python's everyday container. Plus the built-ins that loop for you.",
    concepts=[
        # ------------------------------------------------------------------ for loops
        dict(
            id="for-loops",
            title="for loops",
            builtins=[],
            intro="""
A `for` loop runs its block once for each item:

```python
total = 0
for x in [3, 1, 4]:
    total += x      # runs 3 times: x is 3, then 1, then 4
```

- The **accumulator pattern**: start a variable before the loop (`total = 0`, `best = …`, `result = []`), update it inside, use it after.
- `total += x` is short for `total = total + x`.
- Looping over a string gives one character at a time.
""",
            problems=[
                P("py-loop-sum", "Add Them Up", "def total(nums: List[int]) -> int:",
                  "Return the sum of `nums` using a loop (the built-in `sum` comes later in this level).",
                  "def total(nums: List[int]) -> int:\n    t = 0\n    for x in nums:\n        t += x\n    return t\n",
                  [([[3, 1, 4]], 8), ([[]], 0), ([[-5, 5]], 0)], [[[10]], [list(range(100))], [[-1, -2, -3]]],
                  require=["for"], forbid=["sum"],
                  grammar="""
## Building blocks
- **Start a running total:** `t = 0` before the loop.
- **Loop over values:** `for x in nums:`
- **Add as you go:** `t += x`
- **Return after the loop:** `return t`, at the function's indentation level.
"""),
                P("py-count-negatives", "Count the Negatives", "def negatives(nums: List[int]) -> int:",
                  "Return how many numbers in `nums` are below zero.",
                  "def negatives(nums: List[int]) -> int:\n    count = 0\n    for x in nums:\n        if x < 0:\n            count += 1\n    return count\n",
                  [([[1, -2, 3, -4]], 2), ([[]], 0), ([[0]], 0)], [[[-1, -1, -1]], [[5, 6]], [list(range(-50, 50))]],
                  require=["for"],
                  grammar="""
## Building blocks
- **Counter:** `count = 0`
- **An `if` inside the loop:** indent it one more level than the `for`.
- **Count one:** `count += 1`
"""),
                P("py-loop-max", "Largest Without max", "def largest(nums: List[int]) -> int:",
                  "Return the largest number in `nums` (which isn't empty) without using `max`.",
                  "def largest(nums: List[int]) -> int:\n    best = nums[0]\n    for x in nums:\n        if x > best:\n            best = x\n    return best\n",
                  [([[3, 9, 2]], 9), ([[-5, -2, -8]], -2), ([[7]], 7)], [[[1, 1, 1]], [list(range(1000))], [[0, -1]]],
                  forbid=["max", "sorted", ".sort"],
                  hints=["Start with the first item as the best so far, not with 0 (all the numbers could be negative)."],
                  grammar="""
## Building blocks
- **Best so far:** `best = nums[0]`. Starting at `0` breaks on all-negative lists.
- **Replace when bigger:** `if x > best: best = x`
"""),
                P("py-count-letter", "Count a Letter", "def count_letter(s: str, letter: str) -> int:",
                  "Count how many times `letter` appears in `s`, using a loop over the characters.",
                  "def count_letter(s: str, letter: str) -> int:\n    n = 0\n    for c in s:\n        if c == letter:\n            n += 1\n    return n\n",
                  [(["banana", "a"], 3), (["", "a"], 0), (["xyz", "a"], 0)], [["aaaa", "a"], ["Mississippi", "s"]],
                  forbid=[".count"],
                  grammar="""
## Building blocks
- **Loop over a string:** `for c in s:` gives one character at a time.
- **Compare:** `c == letter`
"""),
            ],
            quiz=[
                Q("What does this print?", "6", "3", "123", "0", code="t = 0\nfor x in [1, 2, 3]:\n    t += x\nprint(t)", predict=True,
                  why="The accumulator grows by each item: 1, 3, 6."),
                Q("What does this print?", "3", "6", "1", "0", code="t = 0\nfor x in [1, 2, 3]:\n    t = x\nprint(t)", predict=True,
                  why="`t = x` replaces the value each time instead of adding, so only the last one is left."),
            ],
        ),
        # ------------------------------------------------------------------ range
        dict(
            id="range",
            title="range: counting loops",
            builtins=["range", "list"],
            intro="""
`range` produces a sequence of numbers:

- `range(5)` → 0, 1, 2, 3, 4 (stop is **not** included)
- `range(2, 6)` → 2, 3, 4, 5
- `range(0, 10, 3)` → 0, 3, 6, 9 (a step)
- `range(5, 0, -1)` → 5, 4, 3, 2, 1 (counting down)

`for i in range(n):` repeats something `n` times. `list(range(3))` turns it into the list `[0, 1, 2]`.
""",
            problems=[
                P("py-one-to-n", "One to N", "def one_to_n(n: int) -> List[int]:",
                  "Return the list `[1, 2, …, n]` (empty if `n` is 0).",
                  "def one_to_n(n: int) -> List[int]:\n    return list(range(1, n + 1))\n",
                  [([5], [1, 2, 3, 4, 5]), ([0], []), ([1], [1])], [[10], [2]],
                  require=["range", "list"],
                  grammar="""
## Building blocks
- **Start and stop:** `range(1, n + 1)`. The `+ 1` is because the stop isn't included.
- **Turn it into a list:** `list(range(...))`
"""),
                P("py-evens-up-to", "Even Numbers up to N", "def evens(n: int) -> List[int]:",
                  "Return every even number from 0 up to and including `n`.",
                  "def evens(n: int) -> List[int]:\n    return list(range(0, n + 1, 2))\n",
                  [([6], [0, 2, 4, 6]), ([7], [0, 2, 4, 6]), ([0], [0])], [[1], [20]],
                  require=["range"], forbid=["op:%"],
                  hints=["`range` takes a third argument: the step."],
                  grammar="""
## Building blocks
- **A step:** `range(0, n + 1, 2)`
"""),
                P("py-countdown-list", "Countdown", "def countdown(n: int) -> List[int]:",
                  "Return `[n, n-1, …, 1]`.",
                  "def countdown(n: int) -> List[int]:\n    return list(range(n, 0, -1))\n",
                  [([3], [3, 2, 1]), ([1], [1]), ([0], [])], [[10]],
                  require=["range"], forbid=["reversed", "slicing", ".reverse"],
                  grammar="""
## Building blocks
- **Count down:** `range(n, 0, -1)` stops *before* 0.
"""),
                P("py-sum-of-squares", "Sum of Squares", "def sum_squares(n: int) -> int:",
                  "Return `1² + 2² + … + n²` using a loop.",
                  "def sum_squares(n: int) -> int:\n    total = 0\n    for i in range(1, n + 1):\n        total += i * i\n    return total\n",
                  [([3], 14), ([1], 1), ([0], 0)], [[10], [100]],
                  require=["for", "range"],
                  grammar="""
## Building blocks
- **Loop over numbers:** `for i in range(1, n + 1):`
- **Square:** `i * i` or `i ** 2`
"""),
                P("py-multiplication-row", "Times Table Row", "def times_row(n: int) -> None:",
                  "Print the `n` times table from 1 to 5, one line each, as `1 x n = …`.\n\nFor `n = 3` the first line is `1 x 3 = 3`.",
                  'def times_row(n: int) -> None:\n    for i in range(1, 6):\n        print(f"{i} x {n} = {i * n}")\n',
                  [([3], "1 x 3 = 3\n2 x 3 = 6\n3 x 3 = 9\n4 x 3 = 12\n5 x 3 = 15\n")], [[0], [7], [12]],
                  out="stdout",
                  grammar="""
## Building blocks
- **Five rounds:** `for i in range(1, 6):`
- **One line each round:** `print(f"{i} x {n} = {i * n}")`
"""),
            ],
            quiz=[
                Q("What does this print?", "[2, 4, 6, 8]", "[2, 4, 6, 8, 10]", "[0, 2, 4, 6, 8]", "[2, 3, 4, 5, 6, 7, 8, 9]", code="print(list(range(2, 10, 2)))", predict=True,
                  why="Start at 2, step by 2, stop before 10."),
                Q("How many times does the body of `for i in range(3, 7):` run?", "4", "3", "5", "7", why="3, 4, 5, 6."),
                Q("What does this print?", "[]", "[5, 4, 3, 2, 1]", "[0, 1, 2, 3, 4, 5]", "error", code="print(list(range(5, 0)))", predict=True,
                  why="Counting down needs a negative step: `range(5, 0, -1)`."),
            ],
        ),
        # ------------------------------------------------------------------ while, break, continue
        dict(
            id="while-break",
            title="while, break and continue",
            builtins=[],
            intro="""
`while condition:` repeats as long as the condition is true. Use it when you don't know in advance how many rounds you need.

```python
while n > 0:
    n //= 10      # something must change, or it loops forever
```

- `break` leaves the loop immediately.
- `continue` skips the rest of this round and starts the next.
- Both work in `for` loops too.
""",
            problems=[
                P("py-digit-sum", "Digit Sum", "def digit_sum(n: int) -> int:",
                  "Return the sum of the digits of `n` (which is 0 or more), using arithmetic rather than converting to text.",
                  "def digit_sum(n: int) -> int:\n    total = 0\n    while n > 0:\n        total += n % 10\n        n //= 10\n    return total\n",
                  [([123], 6), ([0], 0), ([9999], 36)], [[10], [505], [1234567890]],
                  require=["while"], forbid=["str"],
                  hints=["`n % 10` is the last digit; `n // 10` removes it."],
                  grammar="""
## Building blocks
- **Last digit:** `n % 10`
- **Drop the last digit:** `n //= 10`
- **Until nothing's left:** `while n > 0:`
"""),
                P("py-first-negative", "First Negative", "def first_negative(nums: List[int]) -> int:",
                  "Return the index of the first negative number, or `-1` if there isn't one. Stop looking as soon as you find it.",
                  "def first_negative(nums: List[int]) -> int:\n    i = 0\n    while i < len(nums):\n        if nums[i] < 0:\n            break\n        i += 1\n    return i if i < len(nums) else -1\n",
                  [([[3, 1, -4, -1]], 2), ([[1, 2]], -1), ([[-1]], 0)], [[[]], [[0, 0, -0, -7]]],
                  grammar="""
## Building blocks
- **Index-based loop:** `i = 0`, `while i < len(nums):`, `i += 1`
- **Stop early:** `break`
- **Or return early:** `return i` inside the loop, and `return -1` after it.
"""),
                P("py-halvings", "How Many Halvings", "def halvings(n: int) -> int:",
                  "How many times can you halve `n` (with `//`) before it reaches 0? `8` → `4` (8, 4, 2, 1, 0).",
                  "def halvings(n: int) -> int:\n    steps = 0\n    while n > 0:\n        n //= 2\n        steps += 1\n    return steps\n",
                  [([8], 4), ([1], 1), ([0], 0)], [[1000], [2 ** 30]],
                  require=["while"],
                  grammar="""
## Building blocks
- **Repeat until zero:** `while n > 0:`
- **Halve:** `n //= 2`
- **Count rounds:** `steps += 1`
"""),
                P("py-sum-skip-negatives", "Skip the Negatives", "def positive_total(nums: List[int]) -> int:",
                  "Add up the numbers in `nums`, skipping negatives, using `continue`.",
                  "def positive_total(nums: List[int]) -> int:\n    total = 0\n    for x in nums:\n        if x < 0:\n            continue\n        total += x\n    return total\n",
                  [([[1, -2, 3]], 4), ([[-1]], 0), ([[]], 0)], [[[5, 5, -5]], [list(range(-10, 11))]],
                  grammar="""
## Building blocks
- **Skip to the next item:** `continue`
- **Then the normal work:** `total += x` runs only for items that weren't skipped.
"""),
            ],
            quiz=[
                Q("What does this print?", "0 1 2", "0 1 2 3", "0 1 2 4", "0 1", code="for i in range(5):\n    if i == 3:\n        break\n    print(i, end=' ')", predict=False,
                  why="`break` leaves the loop when i is 3."),
                Q("What does this print?", "1 3", "0 2 4", "1 2 3", "0 1 2 3 4", code="for i in range(5):\n    if i % 2 == 0:\n        continue\n    print(i, end=' ')",
                  why="Even numbers are skipped by `continue`."),
                Q("What's wrong with this loop?", "n never changes, so it runs forever", "while needs a colon", "n > 0 is invalid", "Nothing", code="n = 5\nwhile n > 0:\n    print(n)",
                  why="Something in the loop must move the condition toward false: `n -= 1`."),
            ],
        ),
        # ------------------------------------------------------------------ list methods
        dict(
            id="list-methods",
            title="List methods",
            builtins=[],
            intro="""
Lists can change (they're **mutable**). The main methods:

| Method | Does |
|---|---|
| `a.append(x)` | add `x` at the end |
| `a.extend([x, y])` | add every item of another list |
| `a.insert(0, x)` | add `x` at a position |
| `a.pop()` / `a.pop(i)` | remove and **return** the last item / item `i` |
| `a.remove(x)` | remove the first `x` (error if missing) |
| `a.index(x)` | position of the first `x` |
| `a.count(x)` | how many times `x` appears |
| `a.sort()` / `a.reverse()` | reorder in place |

Most of these change the list and return `None`. `a = a.sort()` is a classic bug: `a` becomes `None`.

In tasks marked **in place**, change the list you're given. The tests look at that list afterwards.
""",
            problems=[
                P("py-add-to-end", "Add to the End (in place)", "def add_item(items: List[int], x: int) -> None:",
                  "Add `x` to the end of `items`, changing the list itself. Don't return anything.",
                  "def add_item(items: List[int], x: int) -> None:\n    items.append(x)\n",
                  [([[1, 2], 3], [1, 2, 3]), ([[], 5], [5])], [[[9, 9], 9]],
                  mutate=0, require=[".append"],
                  grammar="""
## Building blocks
- **Add at the end:** `items.append(x)`
- **Nothing to return:** the tests check `items` itself afterwards.
"""),
                P("py-add-to-front", "Add to the Front (in place)", "def push_front(items: List[int], x: int) -> None:",
                  "Put `x` at the start of `items`, in place.",
                  "def push_front(items: List[int], x: int) -> None:\n    items.insert(0, x)\n",
                  [([[2, 3], 1], [1, 2, 3]), ([[], 7], [7])], [[[0], -1]],
                  mutate=0, require=[".insert"],
                  grammar="""
## Building blocks
- **Insert at a position:** `items.insert(0, x)`. Position 0 is the front.
"""),
                P("py-join-lists", "Join Two Lists (in place)", "def extend_with(a: List[int], b: List[int]) -> None:",
                  "Add every item of `b` to the end of `a`, in place.",
                  "def extend_with(a: List[int], b: List[int]) -> None:\n    a.extend(b)\n",
                  [([[1, 2], [3, 4]], [1, 2, 3, 4]), ([[], []], [])], [[[1], []], [[], [5, 6, 7]]],
                  mutate=0, require=[".extend"],
                  grammar="""
## Building blocks
- **Add many items:** `a.extend(b)`
- **Compare:** `a.append(b)` would add the whole list `b` as one item.
"""),
                P("py-remove-value", "Remove a Value (in place)", "def remove_value(items: List[int], x: int) -> None:",
                  "Remove the first `x` from `items`, in place. If `x` isn't there, leave the list alone.",
                  "def remove_value(items: List[int], x: int) -> None:\n    if x in items:\n        items.remove(x)\n",
                  [([[1, 2, 3, 2], 2], [1, 3, 2]), ([[1], 5], [1])], [[[], 1], [[4, 4, 4], 4]],
                  mutate=0, require=[".remove"],
                  grammar="""
## Building blocks
- **Remove the first match:** `items.remove(x)`. It raises `ValueError` if `x` is missing.
- **Check first:** `if x in items:`
"""),
                P("py-pop-last", "Take the Last One", "def take_last(items: List[int]) -> int:",
                  "Remove the last item from `items` and return it. `items` isn't empty.",
                  "def take_last(items: List[int]) -> int:\n    return items.pop()\n",
                  [([[1, 2, 3]], 3), ([[7]], 7)], [[[0, -1]]],
                  require=[".pop"],
                  grammar="""
## Building blocks
- **Remove and get back the last item:** `items.pop()`
"""),
                P("py-sort-in-place", "Sort in Place", "def sort_desc(items: List[int]) -> None:",
                  "Sort `items` from largest to smallest, in place.",
                  "def sort_desc(items: List[int]) -> None:\n    items.sort(reverse=True)\n",
                  [([[3, 1, 2]], [3, 2, 1]), ([[]], [])], [[[5, 5, 1, 9]], [[-1, -3, -2]]],
                  mutate=0, require=[".sort"],
                  grammar="""
## Building blocks
- **Sort the list itself:** `items.sort()`
- **Largest first:** `items.sort(reverse=True)`
- **Don't write `items = items.sort()`:** `.sort()` returns `None`.
"""),
                P("py-position-and-count", "Position and Count", "def find_and_count(items: List[int], x: int) -> List[int]:",
                  "Return `[first position of x, how many times x appears]`. `x` is always in the list.",
                  "def find_and_count(items: List[int], x: int) -> List[int]:\n    return [items.index(x), items.count(x)]\n",
                  [([[5, 3, 5, 5], 5], [0, 3]), ([[1, 2, 3], 3], [2, 1])], [[[0, 0, 1], 1]],
                  require=[".index", ".count"],
                  grammar="""
## Building blocks
- **First position:** `items.index(x)`
- **How many:** `items.count(x)`
"""),
            ],
            quiz=[
                Q("What does this print?", "None", "[1, 2, 3]", "[3, 2, 1]", "error", code="a = [3, 1, 2]\na = a.sort()\nprint(a)", predict=True,
                  why="`.sort()` sorts in place and returns `None`. Use `a.sort()` alone, or `a = sorted(a)`."),
                Q("What does this print?", "[1, 2, [3, 4]]", "[1, 2, 3, 4]", "[[1, 2], [3, 4]]", "error", code="a = [1, 2]\na.append([3, 4])\nprint(a)", predict=True,
                  why="`append` adds one item (here, a list). `extend` adds each item."),
                Q("What does this print?", "3 [1, 2]", "[1, 2] 3", "3 [1, 2, 3]", "1 [2, 3]", code="a = [1, 2, 3]\nx = a.pop()\nprint(x, a)", predict=True,
                  why="`pop()` removes the last item and returns it."),
            ],
        ),
        # ------------------------------------------------------------------ list slicing + slice()
        dict(
            id="list-slicing",
            title="Slicing lists, copies and slice()",
            builtins=["slice"],
            intro="""
Lists slice just like strings: `a[1:3]`, `a[::-1]`, `a[-2:]`.

- A slice is a **new list**. `b = a[:]` is a quick copy, so changing `b` won't change `a`.
- `b = a` is **not** a copy: both names point to the same list.
- The built-in `slice(start, stop, step)` builds a slice you can store and reuse: `a[slice(1, 3)]` is the same as `a[1:3]`. Missing parts are `None`.
- Gotcha: `a[-0:]` is the whole list, because `-0` is just `0`.
""",
            problems=[
                P("py-last-n", "Last N Items", "def last_n(items: List[int], n: int) -> List[int]:",
                  "Return the last `n` items of the list (all of them if `n` is larger). `n` may be 0.",
                  "def last_n(items: List[int], n: int) -> List[int]:\n    return items[len(items) - n:] if n else []\n",
                  [([[1, 2, 3, 4], 2], [3, 4]), ([[1, 2], 0], []), ([[1, 2], 5], [1, 2])], [[[], 3], [[9], 1]],
                  hints=["`items[-n:]` works, except when `n` is 0."],
                  grammar="""
## Building blocks
- **From a position to the end:** `items[start:]`
- **The usual trick:** `items[-n:]`, but `items[-0:]` is the *whole* list, so handle `n == 0` separately.
- **Or compute the start:** `items[max(len(items) - n, 0):]` works for every `n`, including 0.
"""),
                P("py-copy-then-change", "Copy, Then Change", "def with_first_zeroed(items: List[int]) -> List[List[int]]:",
                  "Make a copy of `items`, set the copy's first item to 0, and return `[items, copy]`. The original must be unchanged. `items` isn't empty.",
                  "def with_first_zeroed(items: List[int]) -> List[List[int]]:\n    copy = items[:]\n    copy[0] = 0\n    return [items, copy]\n",
                  [([[5, 6, 7]], [[5, 6, 7], [0, 6, 7]]), ([[1]], [[1], [0]])], [[[0, 0]]],
                  hints=["`copy = items` doesn't copy anything; both names would share one list."],
                  grammar="""
## Building blocks
- **A real copy:** `items[:]` or `list(items)`
- **Change one item:** `copy[0] = 0`
- **Why not `copy = items`?** Both names would point at the same list, so changing one changes "both".
"""),
                P("py-apply-slice", "Use a slice Object", "def take(items: List[int], start: Optional[int], stop: Optional[int], step: Optional[int]) -> List[int]:",
                  "Return the part of `items` described by `start`, `stop` and `step`, any of which may be `None` (meaning \"use the default\"). Use the built-in `slice`.",
                  "def take(items: List[int], start: Optional[int], stop: Optional[int], step: Optional[int]) -> List[int]:\n    return items[slice(start, stop, step)]\n",
                  [([[0, 1, 2, 3, 4, 5], 1, 4, None], [1, 2, 3]), ([[0, 1, 2, 3], None, None, -1], [3, 2, 1, 0])], [[[1, 2, 3], None, None, None], [list(range(10)), 2, None, 3], [[], 0, 5, 1]],
                  require=["slice"],
                  grammar="""
## Building blocks
- **Build a slice from values:** `slice(start, stop, step)`. `None` means "default", just like leaving a gap in `a[::2]`.
- **Use it:** `items[slice(...)]`
"""),
                P("py-rotate-left", "Rotate Left", "def rotate_left(items: List[int], k: int) -> List[int]:",
                  "Move the first `k` items to the end. `[1, 2, 3, 4, 5]`, `2` → `[3, 4, 5, 1, 2]`. `k` may be larger than the list, in which case it wraps around.",
                  "def rotate_left(items: List[int], k: int) -> List[int]:\n    if not items:\n        return []\n    k %= len(items)\n    return items[k:] + items[:k]\n",
                  [([[1, 2, 3, 4, 5], 2], [3, 4, 5, 1, 2]), ([[1, 2, 3], 3], [1, 2, 3]), ([[1, 2, 3], 4], [2, 3, 1])], [[[], 2], [[7], 100], [[1, 2], 1]],
                  difficulty="Medium",
                  grammar="""
## Building blocks
- **Wrap k:** `k %= len(items)` (check for an empty list first, or you'll divide by zero).
- **Two slices joined:** `items[k:] + items[:k]`
"""),
            ],
            quiz=[
                Q("What does this print?", "[9, 2]", "[1, 2]", "error", "[9]", code="a = [1, 2]\nb = a\nb[0] = 9\nprint(a)", predict=True,
                  why="`b = a` makes a second name for the same list. Use `a[:]` for a copy."),
                Q("What does this print?", "[1, 2]", "[9, 2]", code="a = [1, 2]\nb = a[:]\nb[0] = 9\nprint(a)", predict=True, why="The slice made a new list."),
                Q("What does this print?", "[1, 3]", "[0, 2]", "[1, 2, 3]", "[0, 1]", code="print([0, 1, 2, 3][slice(1, None, 2)])", predict=True,
                  why="Start at 1, go to the end, step 2."),
            ],
        ),
        # ------------------------------------------------------------------ enumerate + zip
        dict(
            id="enumerate-zip",
            title="enumerate and zip",
            builtins=["enumerate", "zip"],
            intro="""
- `for i, x in enumerate(items):` gives each position **and** item. `enumerate(items, start=1)` counts from 1.
- `for a, b in zip(xs, ys):` walks two lists side by side, stopping at the shorter one.

Both save you from writing `for i in range(len(items)):` and indexing by hand.
""",
            problems=[
                P("py-numbered-list", "Numbered List", "def numbered(items: List[str]) -> List[str]:",
                  'Return each item prefixed with its number, starting at 1. `["tea", "jam"]` → `["1. tea", "2. jam"]`.',
                  'def numbered(items: List[str]) -> List[str]:\n    out = []\n    for i, x in enumerate(items, start=1):\n        out.append(f"{i}. {x}")\n    return out\n',
                  [([["tea", "jam"]], ["1. tea", "2. jam"]), ([[]], [])], [[["a", "b", "c"]]],
                  require=["enumerate"],
                  grammar="""
## Building blocks
- **Position and item:** `for i, x in enumerate(items, start=1):`
- **Build a new list:** `out = []`, then `out.append(...)`.
"""),
                P("py-even-positions", "Even Positions", "def even_positions(items: List[int]) -> List[int]:",
                  "Return the items at even positions (0, 2, 4, …) using `enumerate`.",
                  "def even_positions(items: List[int]) -> List[int]:\n    out = []\n    for i, x in enumerate(items):\n        if i % 2 == 0:\n            out.append(x)\n    return out\n",
                  [([[10, 11, 12, 13]], [10, 12]), ([[]], [])], [[[5]], [list(range(9))]],
                  require=["enumerate"], forbid=["slicing"],
                  grammar="""
## Building blocks
- **Position and item:** `for i, x in enumerate(items):`
- **Even position:** `i % 2 == 0`
"""),
                P("py-pairwise-sum", "Add Side by Side", "def add_lists(a: List[int], b: List[int]) -> List[int]:",
                  "Return a list where each item is `a[i] + b[i]`. Stop at the end of the shorter list.",
                  "def add_lists(a: List[int], b: List[int]) -> List[int]:\n    out = []\n    for x, y in zip(a, b):\n        out.append(x + y)\n    return out\n",
                  [([[1, 2, 3], [10, 20, 30]], [11, 22, 33]), ([[1, 2, 3], [1]], [2])], [[[], [1]], [[-1, -1], [1, 1]]],
                  require=["zip"],
                  grammar="""
## Building blocks
- **Two lists at once:** `for x, y in zip(a, b):`. It stops at the shorter list.
"""),
                P("py-count-matches", "Count Matching Positions", "def matches(a: str, b: str) -> int:",
                  'Count the positions where `a` and `b` have the same character (compare up to the shorter length). `"karolin", "kathrin"` → `4`.',
                  "def matches(a: str, b: str) -> int:\n    return sum(1 for x, y in zip(a, b) if x == y)\n",
                  [(["karolin", "kathrin"], 4), (["abc", "xyz"], 0), (["", "a"], 0)], [["same", "same"], ["ab", "abba"]],
                  require=["zip"],
                  grammar="""
## Building blocks
- **Walk both strings:** `for x, y in zip(a, b):`
- **Count matches:** `if x == y: count += 1`
"""),
                P("py-index-pairs", "Name and Score", "def report(names: List[str], scores: List[int]) -> List[str]:",
                  'Return `"NAME: SCORE"` for each pair. `["Ada"], [90]` → `["Ada: 90"]`. The lists are the same length.',
                  'def report(names: List[str], scores: List[int]) -> List[str]:\n    return [f"{n}: {s}" for n, s in zip(names, scores)]\n',
                  [([["Ada", "Bo"], [90, 75]], ["Ada: 90", "Bo: 75"]), ([[], []], [])], [[["x"], [0]]],
                  require=["zip"],
                  grammar="""
## Building blocks
- **Pair them up:** `zip(names, scores)`
- **Format each pair:** `f"{n}: {s}"`
"""),
            ],
            quiz=[
                Q("What does this print?", "[(0, 'a'), (1, 'b')]", "[('a', 0), ('b', 1)]", "[0, 1]", "['a', 'b']", code="print(list(enumerate('ab')))", predict=True,
                  why="enumerate yields (index, item) pairs."),
                Q("What does this print?", "[(1, 'x'), (2, 'y')]", "[(1, 'x'), (2, 'y'), (3, None)]", "error", "[1, 2, 3]", code="print(list(zip([1, 2, 3], 'xy')))", predict=True,
                  why="zip stops at the shorter input."),
            ],
        ),
        # ------------------------------------------------------------------ sum / sorted / reversed
        dict(
            id="list-builtins",
            title="sum, sorted and reversed",
            builtins=["sum", "sorted", "reversed"],
            intro="""
Built-ins that do common loops for you:

- `sum(nums)` adds everything (0 for an empty list).
- `sorted(items)` returns a **new** sorted list; `sorted(items, reverse=True)` sorts largest first. The original is untouched.
- `reversed(items)` gives the items backwards (wrap it in `list(...)` to get a list).
- `min(items)` / `max(items)` work on whole lists too (but raise an error if it's empty).

`sorted` vs `.sort()`: `sorted` makes a new list and works on anything; `.sort()` changes a list in place and returns `None`.
""",
            problems=[
                P("py-average-list", "Average of a List", "def average(nums: List[int]) -> float:",
                  "Return the average of `nums`, or `0.0` if the list is empty.",
                  "def average(nums: List[int]) -> float:\n    return sum(nums) / len(nums) if nums else 0.0\n",
                  [([[1, 2, 3, 4]], 2.5), ([[]], 0.0), ([[5]], 5.0)], [[[-2, 2]], [list(range(101))]],
                  require=["sum"],
                  grammar="""
## Building blocks
- **Total:** `sum(nums)`
- **Average:** `sum(nums) / len(nums)`
- **Avoid dividing by zero:** check `if nums` first (an empty list counts as false).
"""),
                P("py-top-three", "Top Three Scores", "def top_three(scores: List[int]) -> List[int]:",
                  "Return the three highest scores, highest first (fewer if there aren't three). Don't change the input list.",
                  "def top_three(scores: List[int]) -> List[int]:\n    return sorted(scores, reverse=True)[:3]\n",
                  [([[50, 90, 70, 80]], [90, 80, 70]), ([[1]], [1]), ([[]], [])], [[[5, 5, 5, 5]], [list(range(20))]],
                  require=["sorted"], forbid=[".sort"],
                  grammar="""
## Building blocks
- **A sorted copy, largest first:** `sorted(scores, reverse=True)`
- **The first three:** `[:3]`
"""),
                P("py-reversed-list", "Backwards Copy", "def backwards(items: List[int]) -> List[int]:",
                  "Return a new list with the items in reverse order, using the built-in `reversed`.",
                  "def backwards(items: List[int]) -> List[int]:\n    return list(reversed(items))\n",
                  [([[1, 2, 3]], [3, 2, 1]), ([[]], [])], [[[7]], [[1, 1, 2]]],
                  require=["reversed"],
                  grammar="""
## Building blocks
- **Backwards:** `reversed(items)` gives an iterator...
- **...so make it a list:** `list(reversed(items))`
- **Same result:** `items[::-1]`
"""),
                P("py-median", "Median", "def median(nums: List[int]) -> float:",
                  "Return the median of `nums` (which isn't empty): the middle value once sorted, or the average of the two middle values if the length is even.",
                  "def median(nums: List[int]) -> float:\n    s = sorted(nums)\n    mid = len(s) // 2\n    if len(s) % 2:\n        return s[mid]\n    return (s[mid - 1] + s[mid]) / 2\n",
                  [([[3, 1, 2]], 2), ([[4, 1, 3, 2]], 2.5), ([[7]], 7)], [[[1, 1, 1, 1]], [[10, -10]], [list(range(100, 0, -1))]],
                  difficulty="Medium", require=["sorted"],
                  grammar="""
## Building blocks
- **Sort a copy:** `s = sorted(nums)`
- **Middle index:** `mid = len(s) // 2`
- **Odd length:** `s[mid]`; **even length:** `(s[mid - 1] + s[mid]) / 2`
"""),
                P("py-range-of-values", "Spread", "def spread(nums: List[int]) -> int:",
                  "Return the difference between the largest and smallest numbers in `nums` (which isn't empty).",
                  "def spread(nums: List[int]) -> int:\n    return max(nums) - min(nums)\n",
                  [([[3, 9, 1]], 8), ([[5]], 0)], [[[-5, 5]], [[2, 2, 2]]],
                  require=["max", "min"],
                  grammar="""
## Building blocks
- **On a whole list:** `max(nums)` and `min(nums)`
"""),
            ],
            quiz=[
                Q("What does this print?", "[1, 2, 3] [3, 1, 2]", "[1, 2, 3] [1, 2, 3]", "None [3, 1, 2]", "[3, 1, 2] [1, 2, 3]", code="a = [3, 1, 2]\nb = sorted(a)\nprint(b, a)", predict=True,
                  why="`sorted` returns a new list and leaves the original alone."),
                Q("What does this print?", "0", "None", "error", "[]", code="print(sum([]))", predict=True, why="The sum of nothing is 0."),
                Q("What does `max([])` do?", "Raises ValueError", "Returns 0", "Returns None", "Returns -inf", why="Pass `default=` to handle empty lists: `max(items, default=0)`."),
            ],
        ),
        # ------------------------------------------------------------------ any / all
        dict(
            id="any-all",
            title="any and all",
            builtins=["any", "all"],
            intro="""
- `all(items)` is `True` if **every** item is truthy (and `True` for an empty list).
- `any(items)` is `True` if **at least one** item is truthy (and `False` for an empty list).

They shine with a **generator expression** (you'll study these in level 5):

```python
all(x > 0 for x in nums)      # every number positive?
any(c.isdigit() for c in s)   # any digit in the text?
```
""",
            problems=[
                P("py-no-zeros", "No Zeros", "def no_zeros(nums: List[int]) -> bool:",
                  "Return `True` if none of the numbers is 0. Use `all` (remember: 0 is falsy).",
                  "def no_zeros(nums: List[int]) -> bool:\n    return all(nums)\n",
                  [([[1, 2, 3]], True), ([[1, 0]], False), ([[]], True)], [[[-1]], [[0]]],
                  require=["all"],
                  grammar="""
## Building blocks
- **Every item truthy:** `all(nums)`. 0 is the only falsy number.
"""),
                P("py-all-positive", "All Positive", "def all_positive(nums: List[int]) -> bool:",
                  "Return `True` if every number is greater than 0.",
                  "def all_positive(nums: List[int]) -> bool:\n    return all(x > 0 for x in nums)\n",
                  [([[1, 2]], True), ([[1, -2]], False), ([[]], True)], [[[0]], [[5, 5, 5]]],
                  require=["all"],
                  grammar="""
## Building blocks
- **A condition for every item:** `all(x > 0 for x in nums)`
"""),
                P("py-has-digit", "Has a Digit", "def has_digit(s: str) -> bool:",
                  "Return `True` if `s` contains at least one digit.",
                  "def has_digit(s: str) -> bool:\n    return any(c.isdigit() for c in s)\n",
                  [(["abc1"], True), (["abc"], False), ([""], False)], [["9"], ["no digits here!"]],
                  require=["any"],
                  grammar="""
## Building blocks
- **At least one:** `any(c.isdigit() for c in s)`
"""),
                P("py-strong-password", "Strong Password", "def strong(pw: str) -> bool:",
                  "A password is strong if it has at least 8 characters, at least one digit, at least one upper-case letter, and at least one lower-case letter.",
                  "def strong(pw: str) -> bool:\n    return (len(pw) >= 8 and any(c.isdigit() for c in pw)\n            and any(c.isupper() for c in pw) and any(c.islower() for c in pw))\n",
                  [(["Passw0rd"], True), (["password"], False), (["Sh0rt"], False)], [["ALLUPPER1"], ["alllower1"], ["NoDigitsHere"], ["G00dEnough"]],
                  difficulty="Medium", require=["any"],
                  grammar="""
## Building blocks
- **Length:** `len(pw) >= 8`
- **Each requirement:** `any(c.isdigit() for c in pw)`, then the same with `isupper` and `islower`.
- **All of them:** join with `and`. Brackets let one expression span several lines.
"""),
            ],
            quiz=[
                Q("What does this print?", "True False", "False True", "True True", "False False", code="print(all([]), any([]))", predict=True,
                  why="Nothing fails `all`, and nothing passes `any`."),
                Q("What does this print?", "False", "True", code="print(all([1, 2, 0]))", predict=True, why="0 is falsy."),
            ],
        ),
        # ------------------------------------------------------------------ nested loops / lists of lists
        dict(
            id="nested",
            title="Nested loops and lists of lists",
            builtins=[],
            intro="""
A grid is a list of rows, and each row is a list: `grid[r][c]` is row `r`, column `c`.

```python
for row in grid:
    for value in row:
        ...
```

- Number of rows: `len(grid)`; number of columns: `len(grid[0])`.
- To build a grid, use a loop or comprehension: `[[0] * cols for _ in range(rows)]`. **Not** `[[0] * cols] * rows`, which repeats one row.
""",
            problems=[
                P("py-grid-total", "Grid Total", "def grid_total(grid: List[List[int]]) -> int:",
                  "Return the sum of every number in the grid.",
                  "def grid_total(grid: List[List[int]]) -> int:\n    total = 0\n    for row in grid:\n        for x in row:\n            total += x\n    return total\n",
                  [([[[1, 2], [3, 4]]], 10), ([[]], 0), ([[[5]]], 5)], [[[[1, 1, 1], [1, 1, 1]]], [[[], []]]],
                  grammar="""
## Building blocks
- **Rows, then values:** `for row in grid:` with `for x in row:` inside.
"""),
                P("py-row-sums", "Row Sums", "def row_sums(grid: List[List[int]]) -> List[int]:",
                  "Return a list with the sum of each row.",
                  "def row_sums(grid: List[List[int]]) -> List[int]:\n    return [sum(row) for row in grid]\n",
                  [([[[1, 2], [3, 4]]], [3, 7]), ([[]], [])], [[[[0], [5, 5, 5]]]],
                  grammar="""
## Building blocks
- **One total per row:** loop over rows and `append(sum(row))`.
"""),
                P("py-column-sums", "Column Sums", "def column_sums(grid: List[List[int]]) -> List[int]:",
                  "Return a list with the sum of each column. The grid has at least one row, and all rows are the same length.",
                  "def column_sums(grid: List[List[int]]) -> List[int]:\n    sums = [0] * len(grid[0])\n    for row in grid:\n        for c, x in enumerate(row):\n            sums[c] += x\n    return sums\n",
                  [([[[1, 2], [3, 4]]], [4, 6]), ([[[1, 2, 3]]], [1, 2, 3])], [[[[1], [1], [1]]], [[[]]]],
                  difficulty="Medium",
                  grammar="""
## Building blocks
- **One counter per column:** `sums = [0] * len(grid[0])`
- **Column index while looping:** `for c, x in enumerate(row):`
- **Add into the right column:** `sums[c] += x`
"""),
                P("py-make-grid", "Make a Grid", "def make_grid(rows: int, cols: int) -> List[List[int]]:",
                  "Return a `rows` × `cols` grid where each cell holds `row * col`. For `2, 3` that's `[[0, 0, 0], [0, 1, 2]]`.",
                  "def make_grid(rows: int, cols: int) -> List[List[int]]:\n    grid = []\n    for r in range(rows):\n        row = []\n        for c in range(cols):\n            row.append(r * c)\n        grid.append(row)\n    return grid\n",
                  [([2, 3], [[0, 0, 0], [0, 1, 2]]), ([0, 5], []), ([1, 1], [[0]])], [[3, 3], [4, 2]],
                  grammar="""
## Building blocks
- **Build a row, then add it:** `row = []` inside the outer loop, fill it, then `grid.append(row)`.
- **A fresh row each time:** creating `row` inside the outer loop is what keeps the rows separate.
"""),
            ],
            quiz=[
                Q("What does this print?", "[[9, 0], [9, 0]]", "[[9, 0], [0, 0]]", "[[9, 9], [0, 0]]", "error", code="g = [[0, 0]] * 2\ng[0][0] = 9\nprint(g)", predict=True,
                  why="`[[0, 0]] * 2` repeats the *same* row twice. Use `[[0] * 2 for _ in range(2)]`."),
                Q("For `grid = [[1, 2, 3], [4, 5, 6]]`, what is `grid[1][2]`?", "6", "2", "5", "3", why="Row 1 is [4, 5, 6]; column 2 is 6."),
            ],
        ),
    ],
)
