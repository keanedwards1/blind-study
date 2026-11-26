# Extra practice for Learn Python level 5 (Functions). See extra_level03.py for the format.
from _helpers import P, Q

EXTRA = {
    "defaults-kwargs": dict(
        warmup=[
            P("py-default-limit", "A Default Page Size", "def fetch(limit: int = 10) -> str:",
              """
An API client builds the query for paged results, and most callers want the default page size of 10. Write `fetch(limit=10)` to return `"limit=N"`.

The tests call `fetch()`, then `fetch(limit)`.

**Constraints**
- `limit` is a whole number
""",
              "def fetch(limit: int = 10) -> str:\n    return f\"limit={limit}\"\n",
              [([None], ["limit=10", "limit=10"]), ([25], ["limit=10", "limit=25"])], [[0], [100]],
              params=["limit"],
              driver='def driver(ns, limit):\n    f = resolve(ns, "fetch")\n    return [f(), f() if limit is None else f(limit)]\n',
              hints=["A default value goes in the function's first line: `def f(x=5):`.",
                     "When the caller leaves the argument out, the default is used.",
                     "Build the text with an f-string."],
              grammar="""
## Building blocks
- **A parameter with a default:** `def resize(width=800):`
- **Text with a value in it:** `f"{width}px"`
"""),
        ],
        practice=[
            P("py-format-heading", "Format a Heading", "def heading(title: str, *, upper: bool = False, border: str = \"*\") -> str:",
              """
A command-line tool prints each section heading between two border characters. The options must be passed **by name** (keyword-only). Write `heading(title, *, upper=False, border="*")` to return border + title + border, with the title in capitals when `upper` is true.

**Constraints**
- `0 <= len(title), len(border) <= 10^4`
""",
              "def heading(title: str, *, upper: bool = False, border: str = \"*\") -> str:\n    text = title.upper() if upper else title\n    return border + text + border\n",
              [(["setup", False, "*"], "*setup*"), (["setup", True, "="], "=SETUP=")], [["a", False, "#"], ["", True, "!"]],
              params=["title", "upper", "border"],
              driver='def driver(ns, title, upper, border):\n    return resolve(ns, "heading")(title, upper=upper, border=border)\n',
              hints=["A bare `*` in the parameter list means everything after it must be passed by name.",
                     "Give both options their defaults in the signature.",
                     "Choose the title text first (upper-cased or not), then put the border on both sides."],
              grammar="""
## Building blocks
- **Keyword-only parameters:** `def f(a, *, b=1):`
- **One-line if/else:** `x if flag else y`
- **Capitals:** `word.upper()`
"""),
        ],
        reps=[
            Q("What does this print?", "Hello, Bo", "Hi, Bo", "Bo", "error", code="def greet(name, word='Hello'):\n    return f'{word}, {name}'\nprint(greet('Bo'))", predict=True,
              why="The default is used when the argument is left out."),
            Q("What does this print?", "[1] [1, 1]", "[1] [1]", "[1, 1] [1, 1]", "error",
              code="def add(x, bag=[]):\n    bag.append(x)\n    return bag\nprint(add(1), end=' ')\nprint(add(1))", predict=True,
              why="A default list is created once and shared between calls. (The first print shows `[1]` before the second call adds to it.)"),
            Q("What does this print?", "3", "error", "None", "1", code="def f(a, *, b=1):\n    return a + b\nprint(f(1, b=2))", predict=True,
              why="`b` is passed by name, as the `*` requires."),
        ],
    ),
    "args-kwargs": dict(
        warmup=[
            P("py-count-tags", "Count the Tags", "def count_tags(*tags: str) -> int:",
              """
A logging helper accepts any number of tags on each call. Write `count_tags(*tags)` to return how many tags were passed.

The tests pass each item of `tags` as a separate argument.

**Constraints**
- `0 <= len(tags) <= 10^4`
""",
              "def count_tags(*tags: str) -> int:\n    return len(tags)\n",
              [([["db", "slow"]], 2), ([[]], 0)], [[["a"]], [["x", "y", "z"]]],
              params=["tags"],
              driver='def driver(ns, tags):\n    return resolve(ns, "count_tags")(*tags)\n',
              hints=["A star before a parameter collects all the positional arguments into a tuple.",
                     "A tuple has a length like any other sequence.",
                     "Return its `len`."],
              grammar="""
## Building blocks
- **Collect any number of arguments:** `def f(*things):`
- **How many:** `len(xs)`
"""),
        ],
        practice=[
            P("py-log-line", "Build a Log Line", "def log_line(level: str, *words: str, **fields: str) -> str:",
              """
A logger writes one line per event: the level, then the message words joined with spaces, then any extra fields as `key=value` separated by `", "`. The sections are separated by `" | "`, and an empty section is left out entirely. Write `log_line(level, *words, **fields)`.

The tests call `log_line(level, *words, **fields)`.

**Constraints**
- `0 <= len(level) <= 10^4`
- Up to `10^4` words and `10^4` fields
- Every word and field value is a non-empty string
""",
              "def log_line(level: str, *words: str, **fields: str) -> str:\n    parts = [level]\n    if words:\n        parts.append(\" \".join(words))\n    if fields:\n        parts.append(\", \".join(f\"{k}={v}\" for k, v in fields.items()))\n    return \" | \".join(parts)\n",
              [(["INFO", ["user", "login"], {"user": "ada"}], "INFO | user login | user=ada"), (["WARN", [], {}], "WARN")],
              [["X", ["a"], {}], ["Y", [], {"k": "v", "z": "w"}]],
              params=["level", "words", "fields"],
              driver='def driver(ns, level, words, fields):\n    return resolve(ns, "log_line")(level, *words, **fields)\n',
              hints=["`*words` arrives as a tuple and `**fields` as a dict.",
                     "Build a list of the line's sections, adding each one only if it isn't empty.",
                     "Join the words with a space, the fields as `k=v` with `\", \"`, and finally everything with `\" | \"`."],
              grammar="""
## Building blocks
- **Collect keyword arguments:** `def f(**opts):`
- **Key and value pairs:** `for k, v in d.items():`
- **Join with a separator:** `"-".join(names)`
"""),
        ],
        reps=[
            Q("What does this print?", "(1, 2, 3)", "[1, 2, 3]", "1 2 3", "6", code="def f(*args):\n    return args\nprint(f(1, 2, 3))", predict=True,
              why="`*args` collects positional arguments into a tuple."),
            Q("What does this print?", "{'a': 1, 'b': 2}", "[('a', 1), ('b', 2)]", "(1, 2)", "error", code="def f(**kw):\n    return kw\nprint(f(a=1, b=2))", predict=True,
              why="`**kwargs` collects keyword arguments into a dict."),
            Q("What does this print?", "6", "[1, 2, 3]", "error", "123", code="def add(a, b, c):\n    return a + b + c\nnums = [1, 2, 3]\nprint(add(*nums))", predict=True,
              why="A star in a call unpacks the list into separate arguments."),
        ],
    ),
    "lambda-key": dict(
        warmup=[
            P("py-sort-by-length", "Shortest Suggestions First", "def by_length(words: List[str]) -> List[str]:",
              """
An autocomplete box shows shorter suggestions first. Write `by_length(words)` to return a new list sorted from shortest to longest with `key=len`. Words of the same length keep their order.

**Constraints**
- `0 <= len(words) <= 10^4`
""",
              "def by_length(words: List[str]) -> List[str]:\n    return sorted(words, key=len)\n",
              [([["search", "go", "save"]], ["go", "save", "search"]), ([[]], [])], [[["bb", "a", "cc"]]],
              hints=["`sorted` can sort by whatever a `key` function returns.",
                     "`len` is a function, so it can be the key directly (no brackets after it).",
                     "Python's sort is stable, so equal lengths keep their order."],
              grammar="""
## Building blocks
- **Sort by a key:** `sorted(items, key=abs)`
"""),
        ],
        practice=[
            P("py-best-average", "Best Average Score", "def best(players: Dict[str, List[int]]) -> str:",
              """
A leaderboard keeps a list of scores for each player. Write `best(players)` to return the player with the highest **average** score. If players tie, return the one that comes first in the dict.

**Constraints**
- `1 <= len(players) <= 10^4`
- `1 <= len(players[name]) <= 10^4`
- `-10^16 <= players[name][j] <= 10^16`
""",
              "def best(players: Dict[str, List[int]]) -> str:\n    return max(players, key=lambda name: sum(players[name]) / len(players[name]))\n",
              [([{"ada": [3, 5], "bo": [6], "cy": [1, 9]}], "bo"), ([{"x": [1]}], "x")], [[{"a": [2, 2], "b": [1, 3]}]],
              require=["lambda"],
              hints=["`max` over a dict looks at its keys (the names).",
                     "Give `max` a `key`: a `lambda` that takes a name and works out that player's average.",
                     "An average is the sum of the scores divided by how many there are. `max` keeps the first on a tie."],
              grammar="""
## Building blocks
- **Biggest by a key:** `max(items, key=...)`
- **A tiny function:** `lambda w: len(w)`
- **Average:** total ÷ count, with `sum` and `len`.
"""),
        ],
        reps=[
            Q("What does this print?", "['a', 'bb', 'ccc']", "['bb', 'a', 'ccc']", "['ccc', 'bb', 'a']", "error",
              code="print(sorted(['a', 'ccc', 'bb'], key=lambda w: w[-1]))", predict=True,
              why="The key is each word's last letter (a, c, b), so the order by key is a, b, c: `'a'`, `'bb'`, `'ccc'`."),
            Q("What does this print?", "-5", "3", "5", "-1", code="print(max([3, -5, 1], key=abs))", predict=True, why="`abs(-5)` is the biggest, but `max` returns the original item."),
            Q("What does this print?", "9", "6", "error", "lambda", code="sq = lambda x: x * x\nprint(sq(3))", predict=True, why="A lambda is a function written in one expression."),
        ],
    ),
    "map-filter": dict(
        warmup=[
            P("py-upper-codes", "Normalise Country Codes", "def upper_all(codes: List[str]) -> List[str]:",
              """
A signup form sends country codes in whatever case people typed. Write `upper_all(codes)` to return them all in capitals, using `map`.

**Constraints**
- `0 <= len(codes) <= 10^4`
""",
              "def upper_all(codes: List[str]) -> List[str]:\n    return list(map(str.upper, codes))\n",
              [([["us", "Fr"]], ["US", "FR"]), ([[]], [])], [[["a"]]],
              require=["map"],
              hints=["`map(function, items)` applies the function to every item.",
                     "`str.upper` is the method itself, usable as a function: `str.upper(\"a\")` is `\"A\"`.",
                     "Wrap the result in `list(...)`."],
              grammar="""
## Building blocks
- **Apply a function to every item:** `map(fn, xs)`
- **A method used as a function:** `str.lower`
- **Collect into a list:** `list(...)`
"""),
        ],
        practice=[
            P("py-passing-scores", "Passing Scores Only", "def passing(scores: List[str]) -> List[int]:",
              """
A CSV import gives test scores as strings. Write `passing(scores)` to convert them to ints and keep only the ones of 50 or more, in their original order, using `map` and `filter`.

**Constraints**
- `0 <= len(scores) <= 10^4`
- Each score is 1 to 3 digits
""",
              "def passing(scores: List[str]) -> List[int]:\n    return list(filter(lambda n: n >= 50, map(int, scores)))\n",
              [([["20", "75", "50"]], [75, 50]), ([[]], [])], [[["1"]], [["99", "100"]]],
              require=["map", "filter"],
              hints=["Two steps: convert every string with `map`, then keep the high ones with `filter`.",
                     "`filter` can work directly on what `map` gives back; there's no need to make a list in between.",
                     "Give `filter` a `lambda` that checks the score is at least 50, and wrap the final result in `list(...)`."],
              grammar="""
## Building blocks
- **Convert every item:** `map(float, xs)`
- **Keep matching items:** `filter(lambda v: v > 0, xs)`
"""),
        ],
        reps=[
            Q("What does this print?", "[2, 4]", "[1, 2, 3, 4]", "[True, False]", "<filter object>", code="print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))", predict=True,
              why="`filter` keeps items where the function returns true."),
            Q("What does this print?", "[1, 4, 9]", "[2, 4, 6]", "[1, 2, 3]", "<map object>", code="print(list(map(lambda x: x * x, [1, 2, 3])))", predict=True,
              why="`map` applies the function to each item."),
            Q("What does this print?", "['a', 'b']", "['a', '', 'b']", "[True, True]", "[]", code="print(list(filter(None, ['a', '', 'b'])))", predict=True,
              why="`filter(None, ...)` keeps only truthy items, and empty strings are falsy."),
        ],
    ),
    "comprehensions": dict(
        warmup=[
            P("py-bump-builds", "Bump Every Build Number", "def bump(builds: List[int]) -> List[int]:",
              """
A release script raises every package's build number by one. Write `bump(builds)` to return the new numbers, using a list comprehension.

**Constraints**
- `0 <= len(builds) <= 10^4`
- `-10^16 <= builds[i] <= 10^16`
""",
              "def bump(builds: List[int]) -> List[int]:\n    return [b + 1 for b in builds]\n",
              [([[1, 4]], [2, 5]), ([[]], [])], [[[0, 0]]],
              require=["listcomp"],
              hints=["A list comprehension has the shape `[new_value for item in items]`.",
                     "The new value here is the item plus one.",
                     "Return the comprehension."],
              grammar="""
## Building blocks
- **List comprehension:** `[x * 10 for x in xs]`
"""),
        ],
        practice=[
            P("py-initials-dict", 'Initials for Each Name', "def initials(names: List[str]) -> Dict[str, str]:",
              """
A user directory shows initials next to each person. Write `initials(names)`, where each name looks like `"ada lovelace"`, to return a dict from every non-blank name to its initials in capitals. Use a dict comprehension and skip blank names.

**Constraints**
- `0 <= len(names) <= 10^4`
""",
              "def initials(names: List[str]) -> Dict[str, str]:\n    return {n: \"\".join(w[0].upper() for w in n.split()) for n in names if n}\n",
              [([["ada lovelace", "", "bo"]], {"ada lovelace": "AL", "bo": "B"}), ([[]], {})], [[["x y z"]]],
              require=["dictcomp"],
              hints=["A dict comprehension has the shape `{key: value for item in items if condition}`.",
                     "The condition `if n` skips empty strings, because they're falsy.",
                     "For the value, split the name into words and join each word's first letter, upper-cased."],
              grammar="""
## Building blocks
- **Dict comprehension:** `{w: len(w) for w in words}`
- **Skip some items:** add `if test` at the end.
- **Words of a name:** `text.split()`
"""),
        ],
        reps=[
            Q("What does this print?", "[0, 2, 4]", "[0, 1, 2]", "[2, 4]", "[0, 4, 16]", code="print([x * 2 for x in range(3)])", predict=True, why="Each of 0, 1, 2 is doubled."),
            Q("What does this print?", "[1, 3]", "[0, 2]", "[1, 2, 3]", "[True, False]", code="print([x for x in range(4) if x % 2])", predict=True,
              why="Only odd numbers (where `x % 2` is 1, which is truthy) are kept."),
            Q("What does this print?", "{'a': 1, 'bb': 2}", "{1: 'a', 2: 'bb'}", "['a', 'bb']", "{1, 2}", code="print({w: len(w) for w in ['a', 'bb']})", predict=True,
              why="A dict comprehension builds key: value pairs."),
        ],
    ),
    "recursion": dict(
        warmup=[
            P("py-countdown", "Count Down Recursively", "def countdown(start: int) -> List[int]:",
              """
A launch screen counts down from `start` to 1. Write `countdown(start)` to return `[start, start-1, ..., 1]` using recursion and no loops.

**Constraints**
- `0 <= start <= 100`
""",
              "def countdown(start: int) -> List[int]:\n    if start == 0:\n        return []\n    return [start] + countdown(start - 1)\n",
              [([3], [3, 2, 1]), ([0], [])], [[1], [6]],
              require=["recursion"], forbid=["for", "while"],
              hints=["The countdown from `start` is `start` followed by the countdown from `start - 1`.",
                     "Base case: the countdown from 0 is an empty list.",
                     "Join a one-item list and the shorter countdown with `+`."],
              grammar="""
## Building blocks
- **Call yourself on something smaller:** `f(k - 1)`
- **Join two lists:** `[a] + rest`
- **Stop at the bottom:** `if k == 0: return []`
"""),
        ],
        practice=[
            P("py-power-tower", 'Fast Power', "def power(base: int, exponent: int) -> int:",
              """
Write `power(base, exponent)` to return `base ** exponent` without using `**` or `pow`. Do it recursively with the halving trick: x to the power 2k is (x to the power k) squared, so each call halves the exponent.

**Constraints**
- `-100 <= base <= 100`
- `0 <= exponent <= 100`
""",
              "def power(base: int, exponent: int) -> int:\n    if exponent == 0:\n        return 1\n    half = power(base, exponent // 2)\n    if exponent % 2 == 0:\n        return half * half\n    return half * half * base\n",
              [([2, 10], 1024), ([5, 0], 1)], [[3, 5], [2, 1], [7, 12]],
              require=["recursion"], forbid=["pow", "op:**"],
              hints=["Anything to the power 0 is 1: that's the base case.",
                     "Work out the power for half the exponent (whole-number division) just once, and store it.",
                     "Square that result; if the exponent was odd, multiply by the base once more."],
              grammar="""
## Building blocks
- **Half, rounded down:** `k // 2`
- **Is it even?** `k % 2 == 0`
- **Store a result to reuse it:** `half = f(...)`
"""),
        ],
        reps=[
            Q("What does this print?", "6", "3", "0", "error", code="def f(n):\n    if n == 0:\n        return 0\n    return n + f(n - 1)\nprint(f(3))", predict=True,
              why="3 + 2 + 1 + 0 = 6."),
            Q("What does this print?", "olleh", "hello", "h", "error", code="def r(s):\n    return s if len(s) <= 1 else r(s[1:]) + s[0]\nprint(r('hello'))", predict=True,
              why="Each call moves the first letter to the end of the reversed rest."),
            Q("What happens if a recursive function has no base case?", "It keeps calling itself until Python raises a `RecursionError`.",
              "It returns `None`.", "It returns 0.", "It runs forever without any error.",
              why="Python limits how deep calls can go, and raises `RecursionError` when the limit is reached."),
        ],
    ),
    "closures": dict(
        warmup=[
            P("py-make-greeter", 'Make a Greeter', "def make_greeter(word: str):",
              """
An email template system needs greeting functions that each remember their own greeting word. Write `make_greeter(word)` to return a function that takes `name` and returns `"<word> <name>"`.

The tests call `make_greeter(word)(name)`.

**Constraints**
- `0 <= len(word), len(name) <= 10^4`
""",
              "def make_greeter(word: str):\n    def greet(name):\n        return f\"{word} {name}\"\n    return greet\n",
              [(["Hi", "Ada"], "Hi Ada"), (["Yo", "Bo"], "Yo Bo")], [["", "x"]],
              params=["word", "name"],
              driver='def driver(ns, word, name):\n    return resolve(ns, "make_greeter")(word)(name)\n',
              hints=["Define a small function inside `make_greeter` that takes `name`.",
                     "The inner function can use `word` from the outer function: it remembers it.",
                     "Return the inner function itself, without calling it."],
              grammar="""
## Building blocks
- **A function inside a function:** `def outer(a):` then an indented `def inner(b):`
- **Return the function itself:** `return inner` (no brackets)
"""),
        ],
        practice=[
            P("py-rate-limiter", "A Simple Rate Limiter", "def make_limiter(limit: int):",
              """
An API gives each client a fixed number of requests. Write `make_limiter(limit)` to return a function with no parameters. Each call uses up one request and returns `"ok"`; once none are left, it returns `"blocked"`.

The tests call the limiter `calls` times.

**Constraints**
- `0 <= limit <= 100`
- `0 <= calls <= 100`
""",
              "def make_limiter(limit: int):\n    left = limit\n\n    def request():\n        nonlocal left\n        if left == 0:\n            return \"blocked\"\n        left -= 1\n        return \"ok\"\n\n    return request\n",
              [([2, 3], ["ok", "ok", "blocked"]), ([0, 1], ["blocked"])], [[1, 2], [3, 3]],
              params=["limit", "calls"],
              driver='def driver(ns, limit, calls):\n    r = resolve(ns, "make_limiter")(limit)\n    return [r() for _ in range(calls)]\n',
              require=["nonlocal"],
              hints=["The inner function must change a number that lives in the outer function.",
                     "Declare it `nonlocal` inside the inner function before changing it.",
                     "Check for zero first and return `\"blocked\"`; otherwise use one up and return `\"ok\"`."],
              grammar="""
## Building blocks
- **Change an outer variable:** `nonlocal total`
- **Subtract one in place:** `k -= 1`
"""),
        ],
        reps=[
            Q("What does this print?", "15", "10", "5", "error", code="def make(n):\n    def add(x):\n        return x + n\n    return add\nprint(make(5)(10))", predict=True,
              why="The inner function remembers `n = 5`."),
            Q("What does this print?", "1 2 1", "1 2 3", "1 1 1", "error",
              code="def counter():\n    c = 0\n    def step():\n        nonlocal c\n        c += 1\n        return c\n    return step\na, b = counter(), counter()\nprint(a(), a(), b())", predict=True,
              why="Each call to `counter()` makes a separate count."),
            Q("Why does `count += 1` inside an inner function fail without `nonlocal count`?",
              "Python treats `count` as a new local variable that has no value yet.",
              "Inner functions can't do arithmetic.", "`count` is read-only in Python.", "It doesn't fail; it works the same.",
              why="Assigning to a name makes it local unless you say `nonlocal`."),
        ],
    ),
    "iterators-generators": dict(
        warmup=[
            P("py-yield-evens", "Yield Even Numbers", "def evens(limit: int):",
              """
A test-data helper hands out even ids one at a time instead of building a big list. Write a generator `evens(limit)` that yields the even numbers from 0 up to, but not including, `limit`.

**Constraints**
- `0 <= limit <= 1000`
""",
              "def evens(limit: int):\n    for i in range(0, limit, 2):\n        yield i\n",
              [([7], [0, 2, 4, 6]), ([0], [])], [[1], [10]],
              driver='def driver(ns, limit):\n    return list(resolve(ns, "evens")(limit))\n',
              require=["yield"],
              hints=["A generator uses `yield` to hand out values one at a time.",
                     "Loop over the even numbers with a `range` that steps by 2.",
                     "Yield each one; don't build or return a list."],
              grammar="""
## Building blocks
- **Hand out a value:** `yield x`
- **Count in steps:** `range(0, stop, 3)`
"""),
        ],
        practice=[
            P("py-read-until-zero", "Read Until the Stop Marker", "def until_zero(readings: List[int]) -> List[int]:",
              """
A sensor sends a stream of readings and marks the end with a 0. Write `until_zero(readings)` to return the readings before the first 0, using `iter` and `next` and no `for` loop. If there's no 0, return them all.

**Constraints**
- `0 <= len(readings) <= 10^4`
- `-10^16 <= readings[i] <= 10^16`
""",
              "def until_zero(readings: List[int]) -> List[int]:\n    it = iter(readings)\n    out = []\n    while (r := next(it, 0)) != 0:\n        out.append(r)\n    return out\n",
              [([[3, 5, 0, 4]], [3, 5]), ([[]], [])], [[[0, 1]], [[1, 2, 3]]],
              require=["iter", "next"], forbid=["for"],
              hints=["`iter(list)` gives an iterator; `next(iterator, default)` takes the next item or returns the default at the end.",
                     "Using 0 as the default means \"ran out\" and \"hit the stop marker\" look the same, so one check stops both.",
                     "Loop with `while`, taking the next reading each time, until it's 0."],
              grammar="""
## Building blocks
- **Make an iterator:** `stream = iter(xs)`
- **Next item, or a default:** `next(stream, -1)`
- **Loop while a condition holds:** `while ...:`
"""),
        ],
        reps=[
            Q("What does this print?", "1 2 None", "1 2 3", "1 2", "error", code="it = iter([1, 2])\nprint(next(it), next(it), next(it, None))", predict=True,
              why="With a default, `next` returns it instead of raising when the iterator is used up."),
            Q("What does this print?", "[3, 2, 1]", "<generator>", "3", "[1, 2, 3]", code="def down(n):\n    while n:\n        yield n\n        n -= 1\nprint(list(down(3)))", predict=True,
              why="`list` pulls every yielded value out of the generator."),
            Q("What does this print?", "[1, 2] []", "[1, 2] [1, 2]", "[] []", "error", code="g = (x for x in [1, 2])\nprint(list(g), list(g))", predict=True,
              why="A generator can only be used up once."),
        ],
    ),
    "decorators": dict(
        warmup=[
            P("py-upper-decorator", "An Uppercase Decorator", "def uppercase(func):",
              """
A command-line tool wants some commands to print their output in capitals. Write a decorator `uppercase` whose wrapper calls the original function and returns its text result upper-cased.

The tests decorate a function that returns `"hi " + name`, then call it with `name`.

**Constraints**
- `0 <= len(name) <= 10^4`
""",
              "def uppercase(func):\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs).upper()\n    return wrapper\n",
              [(["bo"], "HI BO"), ([""], "HI ")], [["x"]],
              params=["name"],
              driver='def driver(ns, name):\n    deco = resolve(ns, "uppercase")\n\n    @deco\n    def hello(n):\n        return "hi " + n\n\n    return hello(name)\n',
              hints=["A decorator takes a function and returns a new wrapper function.",
                     "The wrapper accepts any arguments and passes them straight on to the original.",
                     "Upper-case what the original returns, and return that."],
              grammar="""
## Building blocks
- **A wrapper that takes anything:** `def inner(*args, **kwargs):`
- **Call the original with the same arguments:** `fn(*args, **kwargs)`
- **Capitals:** `text.upper()`
"""),
        ],
        practice=[
            P("py-retry-decorator", 'Retry Once', "def retry_once(func):",
              """
Network calls sometimes fail once and then work. Write a decorator `retry_once` that catches a `ValueError`, calls the function one more time, and lets the error through if the second call fails too.

The tests decorate a function that raises `ValueError` on its first `fails` calls and returns `"ok"` after that. If the error gets out of your decorator, they report `"ValueError escaped"`.

**Constraints**
- `0 <= fails <= 10^16`
""",
              "def retry_once(func):\n    def wrapper(*args, **kwargs):\n        try:\n            return func(*args, **kwargs)\n        except ValueError:\n            return func(*args, **kwargs)\n    return wrapper\n",
              [([1], "ok"), ([2], "ValueError escaped")], [[0]],
              params=["fails"],
              driver='def driver(ns, fails):\n    deco = resolve(ns, "retry_once")\n    calls = [0]\n\n    @deco\n    def fetch():\n        calls[0] += 1\n        if calls[0] <= fails:\n            raise ValueError("timeout")\n        return "ok"\n\n    try:\n        return fetch()\n    except ValueError:\n        return "ValueError escaped"\n',
              hints=["Put the call to the original inside `try`.",
                     "In `except ValueError:`, call the original once more and return its result.",
                     "Don't catch the second failure: if the retry also raises, the error leaves the wrapper on its own."],
              grammar="""
## Building blocks
- **Try something:** `try:` … `except ValueError:`
- **Call the original:** `fn(*args, **kwargs)`
"""),
        ],
        reps=[
            Q("What does this print?", "4", "2", "error", "None", code="def twice(f):\n    def w(x):\n        return f(f(x))\n    return w\n@twice\ndef inc(x):\n    return x + 1\nprint(inc(2))", predict=True,
              why="`@twice` replaces `inc` with a wrapper that calls it two times."),
            Q("`@deco` above `def f(): ...` is the same as…", "`f = deco(f)`", "`deco = f(deco)`", "`f = deco`", "`deco(f())`",
              why="The decorator receives the function and its return value replaces it."),
        ],
    ),
}

REVIEW = dict(
    id="review-5", title="Review: functions",
    intro="""
This review mixes everything in this world: defaults, `*args`/`**kwargs`, `lambda` keys, comprehensions, recursion, closures, generators and decorators.
""",
    problems=[
        P("py-review-rank-results", "Rank Search Results", "def rank(results: List[str], score: Dict[str, int]) -> List[str]:",
          """
A search page ranks results by relevance score, highest first. Results missing from `score` count as 0, and ties go alphabetically. Write `rank(results, score)` using `sorted` with a `lambda` key.

**Constraints**
- `0 <= len(results), len(score) <= 10^4`
- `-10^16 <= score[name] <= 10^16`
""",
          "def rank(results: List[str], score: Dict[str, int]) -> List[str]:\n    return sorted(results, key=lambda r: (-score.get(r, 0), r))\n",
          [([["faq", "docs", "blog"], {"docs": 9, "faq": 9}], ["docs", "faq", "blog"]), ([[], {}], [])], [[["b", "a"], {}], [["x", "y"], {"y": 1}]],
          require=["lambda"],
          hints=["Two sorting rules: higher score first, then alphabetical.",
                 "A key can return a tuple; tuples compare item by item. Negate the score so higher comes first.",
                 "Read a missing result's score with `.get(result, 0)`."],
          grammar="""
## Building blocks
- **Sort by two things:** a key that returns a tuple, like `(-points, name)`.
- **Read with a default:** `d.get(k, 0)`
"""),
        P("py-review-flatten-menu", "Flatten a Nested Menu", "def flatten(menu: list) -> List[str]:",
          """
A site's navigation config holds labels and nested submenus (lists), to any depth. Write `flatten(menu)` to return every non-empty label in reading order.

**Constraints**
- `0 <= len(menu) <= 10^4`
- `menu` holds strings and lists
""",
          "def flatten(menu: list) -> List[str]:\n    out = []\n    for item in menu:\n        if isinstance(item, list):\n            out += flatten(item)\n        elif item:\n            out.append(item)\n    return out\n",
          [([["Home", ["Docs", ["", "API"]], "Blog"]], ["Home", "Docs", "API", "Blog"]), ([[]], [])], [[[[[["x"]]]]], [["", ""]]],
          require=["recursion"],
          hints=["Each item is either a label or a submenu (a list).",
                 "For a list, call your own function on it and add everything it returns.",
                 "For a label, add it only if it isn't empty (empty strings are falsy)."],
          grammar="""
## Building blocks
- **Is it a list?** `isinstance(x, list)`
- **Add several items:** `out += more`
- **Call yourself on a smaller part:** `f(part)`
"""),
        P("py-review-throttle", "Throttle Clicks", "def make_throttle(cooldown: int):",
          """
A button handler ignores clicks that come too soon after the last accepted one. Write `make_throttle(cooldown)` to return a function `allow(tick)`. It returns `True` and starts a new cooldown when the click is accepted, or `False` while it's still cooling down.

The first click is always accepted. After that, a click is accepted once at least `cooldown` ticks have passed since the last accepted one.

**Constraints**
- `0 <= cooldown <= 10^16`
- `0 <= len(ticks) <= 10^4`
- `0 <= ticks[i] <= 10^16`
- `ticks` never goes down
""",
          "def make_throttle(cooldown: int):\n    ready_at = 0\n\n    def allow(tick):\n        nonlocal ready_at\n        if tick < ready_at:\n            return False\n        ready_at = tick + cooldown\n        return True\n\n    return allow\n",
          [([3, [0, 1, 3, 4, 6]], [True, False, True, False, True]), ([1, [0, 0, 1]], [True, False, True])], [[5, [0, 4, 5, 9, 10]], [2, []]],
          params=["cooldown", "ticks"],
          driver='def driver(ns, cooldown, ticks):\n    allow = resolve(ns, "make_throttle")(cooldown)\n    return [allow(t) for t in ticks]\n',
          hints=["The handler needs to remember, between calls, the tick when it's next ready: a closure.",
                 "Store that tick in the outer function, starting at 0, and use `nonlocal` to update it.",
                 "If the tick is earlier than the ready tick, refuse; otherwise accept and set the next ready tick to now plus the cooldown."],
          grammar="""
## Building blocks
- **Change an outer variable:** `nonlocal ready`
- **Compare ticks:** `now < later`
"""),
    ],
    quiz=[
        Q("What does this print?", "[2, 3]", "[1, 2, 3]", "[1]", "error", code="print([x + 1 for x in [1, 2]])", predict=True, why="Each item gets 1 added."),
        Q("What does a generator give you that a list doesn't?", "Values produced one at a time, only when asked for",
          "Faster sorting", "Automatic duplicate removal", "A fixed size",
          why="Generators are lazy: they don't build the whole list in memory."),
    ],
)
