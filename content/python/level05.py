# Learn Python, level 5: functions.
# Tasks with a `driver` are called by the driver (it receives the user's namespace `ns` plus the test arguments);
# `resolve(ns, name)` from public/harness.py fetches the user's function with a clear error if it's missing.
from _helpers import Gen, P, Q

LEVEL = dict(
    n=5,
    title="Functions",
    summary="Writing your own functions properly: defaults, flexible arguments, lambdas, comprehensions, recursion, closures, generators and decorators.",
    concepts=[
        # ------------------------------------------------------------------ defaults and keyword arguments
        dict(
            id="defaults-kwargs",
            title="Default and keyword arguments",
            builtins=[],
            intro="""
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ada")                   # 'Hello, Ada!'
greet("Ada", "Hi")             # 'Hi, Ada!'
greet("Ada", greeting="Hey")   # keyword argument: clearer
```

- Parameters with defaults go **after** the ones without.
- **Never use a mutable default** like `items=[]`: the same list is shared between calls. Use `items=None`, then `if items is None: items = []`.
""",
            problems=[
                P("py-greet-default", "Greeting with a Default", "def greet(name: str, greeting: str = ...) -> str:",
                  'Write `greet(name, greeting)` returning `"GREETING, NAME!"`, where `greeting` defaults to `"Hello"`.\n\nThe tests call it both ways: `greet("Ada")` and `greet("Ada", greeting="Hi")`.',
                  'def greet(name: str, greeting: str = "Hello") -> str:\n    return f"{greeting}, {name}!"\n',
                  [(["Ada"], ["Hello, Ada!", "Hi, Ada!"])], [["Bo"], [""]],
                  starter="def greet(name, greeting):\n    pass\n",
                  params=["name"],
                  driver='def driver(ns, name):\n    greet = resolve(ns, "greet")\n    return [greet(name), greet(name, greeting="Hi")]\n',
                  grammar="""
## Building blocks
- **A default value:** `def greet(name, greeting="Hello"):`
- **Callers can skip it** (`greet("Ada")`) **or name it** (`greet("Ada", greeting="Hi")`).
"""),
                P("py-power-default", "Square by Default", "def power(x: int, exp: int = ...) -> int:",
                  "Write `power(x, exp)` returning `x ** exp`, where `exp` defaults to 2. The tests call `power(x)` and `power(x, 3)`.",
                  "def power(x: int, exp: int = 2) -> int:\n    return x ** exp\n",
                  [([3], [9, 27])], [[0], [-2], [10]],
                  starter="def power(x, exp):\n    pass\n",
                  params=["x"],
                  driver='def driver(ns, x):\n    power = resolve(ns, "power")\n    return [power(x), power(x, 3)]\n',
                  grammar="""
## Building blocks
- **Default:** `exp=2` in the `def` line.
"""),
                P("py-fix-mutable-default", "Fix the Shared List Bug", "def add_tag(tag: str, tags: Optional[List[str]] = None) -> List[str]:",
                  "This function adds a tag to a list and returns it. With no list given it should start a **new** empty list each time, but the starter code has a famous bug: calling `add_tag(\"a\")` then `add_tag(\"b\")` returns `[\"a\", \"b\"]` the second time. Fix it.",
                  "def add_tag(tag: str, tags: Optional[List[str]] = None) -> List[str]:\n    if tags is None:\n        tags = []\n    tags.append(tag)\n    return tags\n",
                  [([["a", "b"]], [["a"], ["b"]])], [[["x", "y", "z"]]],
                  starter="def add_tag(tag, tags=[]):\n    tags.append(tag)\n    return tags\n",
                  params=["tags"],
                  driver='def driver(ns, names):\n    add_tag = resolve(ns, "add_tag")\n    return [add_tag(n) for n in names]\n',
                  difficulty="Medium",
                  hints=["The default `[]` is created once, when `def` runs, and shared by every call.", "Default to `None` and create the list inside the function."],
                  grammar="""
## Building blocks
- **Default to None:** `def add_tag(tag, tags=None):`
- **Create a fresh list per call:** `if tags is None: tags = []`
- **Why:** a default value is evaluated once, when the function is defined, not each time it's called.
"""),
            ],
            quiz=[
                Q("What does this print?", "[1, 2] [1, 2]", "[1] [1, 2]", "[1] [2]", "error", code="def f(x, acc=[]):\n    acc.append(x)\n    return acc\nprint(f(1), f(2))", predict=True,
                  why="Both calls return the same shared list object, and print shows it after both appends."),
                Q("Which `def` line is a SyntaxError?", "def f(a=1, b):", "def f(a, b=1):", "def f(a, b=1, c=2):", "def f(a=1, b=2):",
                  why="Parameters without defaults must come before those with defaults."),
            ],
        ),
        # ------------------------------------------------------------------ *args / **kwargs
        dict(
            id="args-kwargs",
            title="*args and **kwargs",
            builtins=[],
            intro="""
- `def f(*args):` collects any number of positional arguments into a **tuple**.
- `def f(**kwargs):` collects keyword arguments into a **dict**.
- The same stars **unpack** when calling: `f(*[1, 2])` is `f(1, 2)`, and `f(**{"a": 1})` is `f(a=1)`.
""",
            problems=[
                P("py-sum-all", "Add Any Number of Values", "def add_all(*nums: int) -> int:",
                  "Write `add_all` so it accepts any number of numbers and returns their sum. The tests call it with the values unpacked: `add_all(1, 2, 3)`.",
                  "def add_all(*nums: int) -> int:\n    return sum(nums)\n",
                  [([[1, 2, 3]], 6), ([[]], 0)], [[[5]], [list(range(10))]],
                  starter="def add_all():\n    pass\n",
                  params=["values"],
                  driver='def driver(ns, values):\n    return resolve(ns, "add_all")(*values)\n',
                  grammar="""
## Building blocks
- **Collect positional arguments:** `def add_all(*nums):`. `nums` is a tuple.
- **Then:** `sum(nums)`
"""),
                P("py-build-profile", "Build a Profile", "def profile(name: str, **details: str) -> Dict[str, str]:",
                  'Write `profile(name, **details)` returning a dict with `"name"` plus every keyword argument. `profile("Ada", city="London")` → `{"name": "Ada", "city": "London"}`.',
                  'def profile(name: str, **details: str) -> Dict[str, str]:\n    return {"name": name, **details}\n',
                  [(["Ada", {"city": "London"}], {"name": "Ada", "city": "London"}), (["Bo", {}], {"name": "Bo"})], [["Cy", {"a": "1", "b": "2"}]],
                  starter="def profile(name):\n    pass\n",
                  params=["name", "keyword_args"],
                  driver='def driver(ns, name, details):\n    return resolve(ns, "profile")(name, **details)\n',
                  grammar="""
## Building blocks
- **Collect keyword arguments:** `def profile(name, **details):`. `details` is a dict.
- **Merge into a new dict:** `{"name": name, **details}`
"""),
                P("py-count-arguments", "Count the Arguments", "def count_args(*args, **kwargs) -> List[int]:",
                  "Return `[number of positional arguments, number of keyword arguments]`.",
                  "def count_args(*args, **kwargs) -> List[int]:\n    return [len(args), len(kwargs)]\n",
                  [([[1, 2], {"x": 3}], [2, 1]), ([[], {}], [0, 0])], [[[None] * 5, {"a": 1, "b": 2, "c": 3}]],
                  starter="def count_args():\n    pass\n",
                  params=["positional", "keyword"],
                  driver='def driver(ns, args, kwargs):\n    return resolve(ns, "count_args")(*args, **kwargs)\n',
                  grammar="""
## Building blocks
- **Both kinds:** `def count_args(*args, **kwargs):`
- **Sizes:** `len(args)`, `len(kwargs)`
"""),
            ],
            quiz=[
                Q("What does this print?", "(1, 2) {'c': 3}", "[1, 2] {'c': 3}", "(1, 2, 3) {}", "error", code="def f(*a, **k):\n    print(a, k)\nf(1, 2, c=3)", predict=True,
                  why="`*a` collects positionals into a tuple; `**k` collects keywords into a dict."),
                Q("What does this print?", "3", "[1, 2]", "error", "12", code="def add(a, b):\n    return a + b\nprint(add(*[1, 2]))", predict=True,
                  why="`*[1, 2]` unpacks the list into two arguments."),
            ],
        ),
        # ------------------------------------------------------------------ lambda + key functions
        dict(
            id="lambda-key",
            title="lambda and key= functions",
            builtins=[],
            intro="""
A `lambda` is a tiny unnamed function: `lambda x: x * 2` is the same as a `def` that returns `x * 2`.

They're most useful as a **key** for `sorted`, `min` and `max`:

```python
sorted(words, key=len)                 # by length
sorted(people, key=lambda p: p[1])     # by the second item
max(words, key=lambda w: w.count("a"))
sorted(words, key=lambda w: (len(w), w))  # by length, then alphabetically
```

Returning a tuple from the key sorts by several things in order.
""",
            problems=[
                P("py-sort-by-last-letter", "Sort by Last Letter", "def by_last_letter(words: List[str]) -> List[str]:",
                  "Sort the words by their last letter. Words with the same last letter keep their original order. No word is empty.",
                  "def by_last_letter(words: List[str]) -> List[str]:\n    return sorted(words, key=lambda w: w[-1])\n",
                  [([["cab", "bad", "ace"]], ["cab", "bad", "ace"]), ([["zoo", "bee", "ant"]], ["bee", "zoo", "ant"])], [[[]], [["x", "y", "z", "a"]]],
                  require=["lambda"],
                  grammar="""
## Building blocks
- **A key function:** `sorted(words, key=lambda w: w[-1])`
- **Stable sort:** ties keep their original order.
"""),
                P("py-longest-word", "Longest Word", "def longest(words: List[str]) -> str:",
                  "Return the longest word (the first one, if there's a tie). The list isn't empty.",
                  "def longest(words: List[str]) -> str:\n    return max(words, key=len)\n",
                  [([["a", "abc", "ab"]], "abc"), ([["xx", "yy"]], "xx")], [[["solo"]], [["", "a"]]],
                  require=["max"],
                  grammar="""
## Building blocks
- **Max by something:** `max(words, key=len)`. Any function works as a key, including built-ins like `len`.
"""),
                P("py-sort-by-score", "Sort by Score", "def ranking(results: List[List]) -> List[str]:",
                  "`results` is a list of `[name, score]` pairs. Return the names ordered by score, highest first; equal scores in alphabetical order.",
                  "def ranking(results: List[List]) -> List[str]:\n    return [name for name, score in sorted(results, key=lambda r: (-r[1], r[0]))]\n",
                  [([[["bo", 3], ["ada", 5], ["cy", 3]]], ["ada", "bo", "cy"]), ([[]], [])], [[[["z", 1], ["a", 1]]]],
                  difficulty="Medium", require=["lambda"],
                  hints=["A tuple key sorts by its first item, then its second.", "Negating the score makes higher scores sort first."],
                  grammar="""
## Building blocks
- **Sort by several things:** return a tuple from the key: `key=lambda r: (-r[1], r[0])`
- **Highest first for numbers:** negate them in the key.
- **Pull out the names:** a loop, or `[name for name, score in ...]`.
"""),
            ],
            quiz=[
                Q("What does this print?", "['b', 'cc', 'aaa']", "['aaa', 'b', 'cc']", "['aaa', 'cc', 'b']", "error", code="print(sorted(['cc', 'aaa', 'b'], key=len))", predict=True,
                  why="Sorted by length."),
                Q("`lambda x, y: x + y` is equivalent to…", "def f(x, y): return x + y", "def f(x): return x + y", "def f(x, y): x + y", "x + y",
                  why="A lambda's single expression is automatically returned."),
            ],
        ),
        # ------------------------------------------------------------------ map / filter
        dict(
            id="map-filter",
            title="map and filter",
            builtins=["map", "filter"],
            intro="""
- `map(f, items)` applies `f` to every item.
- `filter(f, items)` keeps the items where `f(item)` is truthy.

Both are **lazy**: they give an iterator, so wrap them in `list(...)` to see the results.

```python
list(map(int, ["1", "2"]))             # [1, 2]
list(filter(lambda x: x > 0, nums))    # positives
```

Comprehensions (next lesson) do the same job and are often clearer, but `map(int, …)` is a common idiom.
""",
            problems=[
                P("py-strings-to-ints", "Text to Numbers", "def to_ints(items: List[str]) -> List[int]:",
                  'Convert every string to an int using `map`. `["1", "20"]` → `[1, 20]`.',
                  "def to_ints(items: List[str]) -> List[int]:\n    return list(map(int, items))\n",
                  [([["1", "20"]], [1, 20]), ([[]], [])], [[["-5", "0", "007"]]],
                  require=["map"],
                  grammar="""
## Building blocks
- **Apply a function to every item:** `map(int, items)`
- **Get a list:** `list(map(...))`
"""),
                P("py-squares-map", "Squares with map", "def squares(nums: List[int]) -> List[int]:",
                  "Return the square of every number, using `map` and a `lambda`.",
                  "def squares(nums: List[int]) -> List[int]:\n    return list(map(lambda x: x * x, nums))\n",
                  [([[1, 2, 3]], [1, 4, 9]), ([[]], [])], [[[-3, 0]]],
                  require=["map", "lambda"],
                  grammar="""
## Building blocks
- **A lambda as the function:** `map(lambda x: x * x, nums)`
"""),
                P("py-filter-evens", "Evens with filter", "def evens(nums: List[int]) -> List[int]:",
                  "Return only the even numbers, using `filter`.",
                  "def evens(nums: List[int]) -> List[int]:\n    return list(filter(lambda x: x % 2 == 0, nums))\n",
                  [([[1, 2, 3, 4]], [2, 4]), ([[1, 3]], [])], [[[]], [[0, -2, -3]]],
                  require=["filter"],
                  grammar="""
## Building blocks
- **Keep matching items:** `filter(lambda x: x % 2 == 0, nums)`
- **Then:** `list(...)`
"""),
                P("py-non-empty", "Drop Empty Strings", "def non_empty(items: List[str]) -> List[str]:",
                  'Remove the empty strings. `filter(None, items)` keeps only truthy items.',
                  "def non_empty(items: List[str]) -> List[str]:\n    return list(filter(None, items))\n",
                  [([["a", "", "b", ""]], ["a", "b"]), ([[""]], [])], [[[]], [[" ", "x"]]],
                  require=["filter"],
                  grammar="""
## Building blocks
- **Filter by truthiness:** `filter(None, items)`. `""` is falsy, so it's dropped (but `" "` isn't).
"""),
            ],
            quiz=[
                Q("What does this print?", "<class 'map'>", "<class 'list'>", "[2, 4]", "error", code="print(type(map(lambda x: x * 2, [1, 2])))", predict=True,
                  why="`map` is lazy. Use `list(map(...))` to get the values."),
                Q("What does this print?", "[1, 2] []", "[1, 2] [1, 2]", "[] []", "error", code="m = map(int, ['1', '2'])\nprint(list(m), list(m))", predict=True,
                  why="An iterator can only be consumed once."),
            ],
        ),
        # ------------------------------------------------------------------ comprehensions
        dict(
            id="comprehensions",
            title="Comprehensions",
            builtins=[],
            intro="""
A comprehension builds a collection in one expression:

```python
[x * x for x in nums]                 # list
[x for x in nums if x > 0]            # with a filter
{w: len(w) for w in words}            # dict
{len(w) for w in words}               # set
sum(x * x for x in nums)              # generator expression: no brackets needed inside a call
[c for row in grid for c in row]      # nested: outer loop first
```

Read them left to right as "give me `this` for each `item` in `items` if `condition`".
""",
            problems=[
                P("py-squares-comp", "Squares, Comprehension Style", "def squares(nums: List[int]) -> List[int]:",
                  "Return the square of every number, using a list comprehension.",
                  "def squares(nums: List[int]) -> List[int]:\n    return [x * x for x in nums]\n",
                  [([[1, 2, 3]], [1, 4, 9]), ([[]], [])], [[[-1, 10]]],
                  require=["listcomp"],
                  grammar="""
## Building blocks
- **List comprehension:** `[x * x for x in nums]`
"""),
                P("py-positive-doubles", "Double the Positives", "def double_positives(nums: List[int]) -> List[int]:",
                  "Return double each **positive** number, skipping the rest, in one comprehension.",
                  "def double_positives(nums: List[int]) -> List[int]:\n    return [2 * x for x in nums if x > 0]\n",
                  [([[1, -2, 3, 0]], [2, 6]), ([[-1]], [])], [[[]], [[5, 5]]],
                  require=["listcomp"],
                  grammar="""
## Building blocks
- **Filter at the end:** `[2 * x for x in nums if x > 0]`
"""),
                P("py-word-lengths", "Word Lengths", "def lengths(words: List[str]) -> Dict[str, int]:",
                  "Return a dict mapping each word to its length, using a dict comprehension.",
                  "def lengths(words: List[str]) -> Dict[str, int]:\n    return {w: len(w) for w in words}\n",
                  [([["hi", "hello"]], {"hi": 2, "hello": 5}), ([[]], {})], [[["a", "a"]]],
                  require=["dictcomp"],
                  grammar="""
## Building blocks
- **Dict comprehension:** `{w: len(w) for w in words}`
"""),
                P("py-length-set", "Distinct Lengths", "def distinct_lengths(words: List[str]) -> Set[int]:",
                  "Return the set of different word lengths, using a set comprehension.",
                  "def distinct_lengths(words: List[str]) -> Set[int]:\n    return {len(w) for w in words}\n",
                  [([["a", "bb", "cc"]], {1, 2}), ([[]], set())], [[["", "x"]]],
                  compare="strict", require=["setcomp"],
                  grammar="""
## Building blocks
- **Set comprehension:** `{len(w) for w in words}`, with no colon.
"""),
                P("py-sum-odd-squares", "Sum of Odd Squares", "def odd_square_sum(nums: List[int]) -> int:",
                  "Return the sum of the squares of the odd numbers, using a generator expression inside `sum`.",
                  "def odd_square_sum(nums: List[int]) -> int:\n    return sum(x * x for x in nums if x % 2)\n",
                  [([[1, 2, 3]], 10), ([[2, 4]], 0)], [[[]], [list(range(20))]],
                  require=["genexp"],
                  grammar="""
## Building blocks
- **Generator expression:** `sum(x * x for x in nums if x % 2)`. No square brackets: no list is built.
"""),
                P("py-flatten-comp", "Flatten a Grid", "def flatten(grid: List[List[int]]) -> List[int]:",
                  "Return every value of the grid in one list, row by row, with a single comprehension.",
                  "def flatten(grid: List[List[int]]) -> List[int]:\n    return [x for row in grid for x in row]\n",
                  [([[[1, 2], [3]]], [1, 2, 3]), ([[]], [])], [[[[], [4, 5]]]],
                  require=["listcomp"], difficulty="Medium",
                  grammar="""
## Building blocks
- **Two `for`s, outer first:** `[x for row in grid for x in row]`. Same order as nested loops.
"""),
            ],
            quiz=[
                Q("What does this print?", "[0, 4, 16]", "[0, 1, 4, 9, 16]", "[1, 9]", "[0, 2, 4]", code="print([x * x for x in range(5) if x % 2 == 0])", predict=True,
                  why="Only 0, 2 and 4 pass the filter."),
                Q("What does this print?", "{1, 2}", "[1, 2, 2]", "{'a': 1, 'bb': 2, 'cc': 2}", "(1, 2, 2)", code="print({len(w) for w in ['a', 'bb', 'cc']})", predict=True,
                  why="Braces without a colon make a set."),
            ],
        ),
        # ------------------------------------------------------------------ recursion
        dict(
            id="recursion",
            title="Recursion",
            builtins=[],
            intro="""
A **recursive** function calls itself on a smaller version of the problem.

```python
def countdown_sum(n):
    if n == 0:            # base case: stops the recursion
        return 0
    return n + countdown_sum(n - 1)   # recursive case: a smaller problem
```

- Always have a **base case**, and make each call move toward it.
- Python stops very deep recursion (about 1000 calls) with a `RecursionError`.
- Trees and backtracking problems (levels 9–10) lean on recursion heavily.
""",
            problems=[
                P("py-factorial", "Factorial", "def factorial(n: int) -> int:",
                  "Return `n!` (1 × 2 × … × n, with `0! = 1`) using recursion.",
                  "def factorial(n: int) -> int:\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n",
                  [([5], 120), ([0], 1), ([1], 1)], [[10], [20]],
                  require=["recursion"],
                  grammar="""
## Building blocks
- **Base case:** `if n <= 1: return 1`
- **Recursive case:** `return n * factorial(n - 1)`
"""),
                P("py-recursive-sum", "Sum a List Recursively", "def rsum(nums: List[int]) -> int:",
                  "Return the sum of `nums` using recursion (no loops, no `sum`).",
                  "def rsum(nums: List[int]) -> int:\n    if not nums:\n        return 0\n    return nums[0] + rsum(nums[1:])\n",
                  [([[1, 2, 3]], 6), ([[]], 0)], [[[5]], [list(range(100))]],
                  require=["recursion"], forbid=["sum", "for", "while"],
                  grammar="""
## Building blocks
- **Base case:** an empty list sums to 0: `if not nums: return 0`
- **First plus the rest:** `nums[0] + rsum(nums[1:])`
"""),
                P("py-recursive-reverse", "Reverse Recursively", "def rreverse(s: str) -> str:",
                  "Return `s` reversed, using recursion (no slicing with a step, no loops).",
                  "def rreverse(s: str) -> str:\n    if len(s) <= 1:\n        return s\n    return rreverse(s[1:]) + s[0]\n",
                  [(["abc"], "cba"), ([""], "")], [["a"], ["racecar"], ["hello world"]],
                  require=["recursion"], forbid=["for", "while", "reversed"],
                  grammar="""
## Building blocks
- **Base case:** strings of length 0 or 1 are their own reverse.
- **Reverse the rest, then put the first character last:** `rreverse(s[1:]) + s[0]`
"""),
                P("py-count-nested", "Count Nested Items", "def count_items(nested: list) -> int:",
                  "`nested` is a list whose items are numbers or more lists, to any depth. Return how many numbers it contains in total.",
                  "def count_items(nested: list) -> int:\n    total = 0\n    for x in nested:\n        total += count_items(x) if isinstance(x, list) else 1\n    return total\n",
                  [([[1, [2, [3, 4]], 5]], 5), ([[]], 0)], [[[[[[]]]]], [[[1], [2], [3, [4]]]]],
                  difficulty="Medium", require=["recursion"],
                  grammar="""
## Building blocks
- **Is it a list?** `isinstance(x, list)`
- **Recurse on lists, count numbers:** `count_items(x)` for a list, `1` for a number.
"""),
            ],
            quiz=[
                Q("What happens when you call `f(3)`?", "RecursionError", "It returns 0", "It returns 3", "It prints forever without error",
                  code="def f(n):\n    return f(n - 1)", why="There's no base case, so it recurses until Python's limit."),
                Q("What does this print?", "10", "4", "0", "error", code="def s(n):\n    return 0 if n == 0 else n + s(n - 1)\nprint(s(4))", predict=True, why="4 + 3 + 2 + 1 + 0."),
            ],
        ),
        # ------------------------------------------------------------------ closures
        dict(
            id="closures",
            title="Functions that return functions (closures)",
            builtins=["callable"],
            intro="""
Functions are values: you can store them, pass them around and return them.

```python
def make_adder(n):
    def add(x):
        return x + n      # remembers n from the outer call: a closure
    return add

add5 = make_adder(5)
add5(10)   # 15
```

- To **change** an outer variable from the inner function, declare it `nonlocal`.
- `callable(x)` tells you whether `x` can be called like a function.
""",
            problems=[
                P("py-make-adder", "Make an Adder", "def make_adder(n: int):",
                  "Write `make_adder(n)` that returns a **function**. That function takes `x` and returns `x + n`.\n\nThe tests do `make_adder(n)(x)`.",
                  "def make_adder(n: int):\n    def add(x):\n        return x + n\n    return add\n",
                  [([5, 10], 15), ([0, 0], 0)], [[-3, 3], [100, 1]],
                  params=["n", "x"],
                  driver='def driver(ns, n, x):\n    return resolve(ns, "make_adder")(n)(x)\n',
                  grammar="""
## Building blocks
- **A function inside a function:** `def add(x): return x + n`
- **Return the function itself:** `return add` (no brackets: you're not calling it).
"""),
                P("py-make-counter", "Make a Counter", "def make_counter():",
                  "Write `make_counter()` that returns a function. Each time that function is called it returns the next number: 1, then 2, then 3…\n\nTwo counters must count independently. The tests make two counters and call them in turn.",
                  "def make_counter():\n    count = 0\n\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n\n    return counter\n",
                  [([3], [[1, 2, 3], [1]])], [[1], [5]],
                  params=["calls"],
                  driver='def driver(ns, n):\n    make = resolve(ns, "make_counter")\n    a, b = make(), make()\n    first = [a() for _ in range(n)]\n    return [first, [b()]]\n',
                  require=["nonlocal"], difficulty="Medium",
                  hints=["Without `nonlocal`, `count += 1` inside the inner function raises `UnboundLocalError`."],
                  grammar="""
## Building blocks
- **State in the outer function:** `count = 0`
- **Change it from inside:** `nonlocal count`, then `count += 1`.
- **Each call to `make_counter()` creates a fresh `count`**, so counters are independent.
"""),
                P("py-call-if-callable", "Call It If You Can", "def resolve_value(x, arg):",
                  "If `x` is callable, return `x(arg)`; otherwise return `x` itself. The tests pass things like `len`, `str.upper`, `5` and `\"text\"`.",
                  "def resolve_value(x, arg):\n    return x(arg) if callable(x) else x\n",
                  [([], [3, "HI", 5, "text"])], [[]],
                  params=[],
                  driver='def driver(ns):\n    f = resolve(ns, "resolve_value")\n    return [f(len, "abc"), f(str.upper, "hi"), f(5, "ignored"), f("text", "ignored")]\n',
                  require=["callable"],
                  grammar="""
## Building blocks
- **Can it be called?** `callable(x)`
- **One-line if/else:** `x(arg) if callable(x) else x`
"""),
            ],
            quiz=[
                Q("What does this print?", "True True False", "True False False", "False True False", "True True True", code="print(callable(len), callable(lambda: 1), callable(5))", predict=True,
                  why="Functions and lambdas are callable; numbers aren't."),
                Q("Why does this raise UnboundLocalError?", "Assigning to `n` makes it local to `inc`, so it's read before it's set", "`n` is a global", "Closures can't read outer variables", "`+=` isn't allowed on ints",
                  code="def outer():\n    n = 0\n    def inc():\n        n += 1\n    inc()", why="Add `nonlocal n` inside `inc`."),
            ],
        ),
        # ------------------------------------------------------------------ iterators and generators
        dict(
            id="iterators-generators",
            title="iter, next and generators",
            builtins=["iter", "next"],
            quiz_only=["aiter", "anext"],
            intro="""
An **iterator** hands out values one at a time.

- `it = iter(items)` makes one; `next(it)` gets the next value; `next(it, default)` returns `default` when it runs out (instead of raising `StopIteration`).
- `for` loops call `iter` and `next` for you.

A **generator** is a function that uses `yield`. Each `yield` hands out a value and pauses until the next one is requested:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

list(countdown(3))   # [3, 2, 1]
```

Generators are lazy, so they can describe huge or even infinite sequences. `aiter` and `anext` are the same ideas for `async` code.
""",
            problems=[
                P("py-first-or-default", "First Item or Default", "def first(items: List[int], default: int) -> int:",
                  "Return the first item, or `default` if the list is empty, using `iter` and `next`.",
                  "def first(items: List[int], default: int) -> int:\n    return next(iter(items), default)\n",
                  [([[5, 6], 0], 5), ([[], -1], -1)], [[[0], 9]],
                  require=["next", "iter"],
                  grammar="""
## Building blocks
- **An iterator:** `iter(items)`
- **Next value, or a fallback:** `next(it, default)`
"""),
                P("py-first-match", "First Long Word", "def first_long(words: List[str], n: int) -> Optional[str]:",
                  "Return the first word longer than `n` characters, or `None`. Use `next` with a generator expression.",
                  "def first_long(words: List[str], n: int) -> Optional[str]:\n    return next((w for w in words if len(w) > n), None)\n",
                  [([["a", "abcd", "abcdef"], 3], "abcd"), ([["a"], 3], None)], [[[], 0], [["xy", "xyz"], 2]],
                  require=["next", "genexp"],
                  grammar="""
## Building blocks
- **A lazy search:** `(w for w in words if len(w) > n)`
- **Take the first, or None:** `next(that_generator, None)`. Brackets are needed around the generator when it's not the only argument.
"""),
                P("py-countdown-generator", "Countdown Generator", "def countdown(n: int):",
                  "Write a **generator** that yields `n, n-1, …, 1`.",
                  "def countdown(n: int):\n    while n > 0:\n        yield n\n        n -= 1\n",
                  [([3], Gen([3, 2, 1])), ([0], Gen([]))], [[1], [10]],
                  compare="strict", require=["yield"],
                  grammar="""
## Building blocks
- **Yield instead of return:** `yield n` hands out one value and pauses.
- **The tests check it's a generator,** so returning a list won't pass.
"""),
                P("py-chunks", "Chunks", "def chunks(items: List[int], size: int):",
                  "Write a generator that yields consecutive pieces of `items`, each `size` long (the last may be shorter). `[1, 2, 3, 4, 5], 2` yields `[1, 2]`, `[3, 4]`, `[5]`.",
                  "def chunks(items: List[int], size: int):\n    for i in range(0, len(items), size):\n        yield items[i:i + size]\n",
                  [([[1, 2, 3, 4, 5], 2], Gen([[1, 2], [3, 4], [5]])), ([[], 3], Gen([]))], [[[1, 2, 3], 3], [list(range(10)), 4]],
                  compare="strict", require=["yield"], difficulty="Medium",
                  grammar="""
## Building blocks
- **Step through the start positions:** `range(0, len(items), size)`
- **Yield a slice:** `yield items[i:i + size]`
"""),
            ],
            quiz=[
                Q("What does this print?", "1 2 done", "1 2 3", "1 1 1", "error", code="it = iter([1, 2])\nprint(next(it), next(it), next(it, 'done'))", predict=True,
                  why="The third `next` has run out, so it returns the default."),
                Q("What does this print?", "a b", "['a', 'b']", "a", "error",
                  code="import asyncio\n\nasync def letters():\n    yield 'a'\n    yield 'b'\n\nasync def main():\n    it = aiter(letters())\n    print(await anext(it), await anext(it))\n\nasyncio.run(main())", predict=True,
                  why="`aiter` and `anext` are the async versions of `iter` and `next`, used with `async` generators and `await`."),
                Q("What does `f()` return?", "A generator object", "1", "[1, 2]", "None", code="def f():\n    yield 1\n    yield 2",
                  why="Calling a generator function doesn't run its body; it returns a generator you then iterate."),
            ],
        ),
        # ------------------------------------------------------------------ decorators
        dict(
            id="decorators",
            title="Decorators",
            builtins=[],
            intro="""
A **decorator** takes a function and returns a new function that wraps it:

```python
def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@shout            # same as: greet = shout(greet)
def greet(name):
    return f"hi {name}"

greet("ada")      # 'HI ADA'
```

`@functools.cache` (level 7) is a decorator you'll use for dynamic programming.
""",
            problems=[
                P("py-double-result", "Double the Result", "def double_result(func):",
                  "Write a decorator `double_result` that makes the decorated function return twice its normal result. The tests decorate a function that adds two numbers.",
                  "def double_result(func):\n    def wrapper(*args, **kwargs):\n        return 2 * func(*args, **kwargs)\n    return wrapper\n",
                  [([1, 2], 6), ([0, 0], 0)], [[-5, 2], [10, 10]],
                  params=["a", "b"],
                  driver='def driver(ns, a, b):\n    deco = resolve(ns, "double_result")\n\n    @deco\n    def add(x, y):\n        return x + y\n\n    return add(a, b)\n',
                  grammar="""
## Building blocks
- **Take a function, return a wrapper:** `def double_result(func):` … `return wrapper`
- **Pass every argument through:** `def wrapper(*args, **kwargs): return 2 * func(*args, **kwargs)`
"""),
                P("py-count-calls", "Count the Calls", "def count_calls(func):",
                  "Write a decorator that counts how many times the decorated function has been called, storing the number in an attribute `calls` on the wrapper. The tests call the function `n` times and read `f.calls`.",
                  "def count_calls(func):\n    def wrapper(*args, **kwargs):\n        wrapper.calls += 1\n        return func(*args, **kwargs)\n    wrapper.calls = 0\n    return wrapper\n",
                  [([3], 3), ([0], 0)], [[1], [10]],
                  params=["calls"],
                  driver='def driver(ns, n):\n    deco = resolve(ns, "count_calls")\n\n    @deco\n    def f():\n        return None\n\n    for _ in range(n):\n        f()\n    return f.calls\n',
                  difficulty="Medium",
                  grammar="""
## Building blocks
- **Functions can have attributes:** `wrapper.calls = 0`
- **Update it on each call:** `wrapper.calls += 1` inside the wrapper.
"""),
            ],
            quiz=[
                Q("`@deco` above `def f(): ...` means…", "f = deco(f)", "f = f(deco)", "deco is called every time f returns", "f becomes a class",
                  why="The decorator receives the function and its return value replaces it."),
            ],
        ),
    ],
)
