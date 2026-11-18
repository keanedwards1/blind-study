# Extra practice for Learn Python level 5 (Functions): the spellbook. See extra_level03.py for the format.
from _helpers import P, Q

EXTRA = {
    "defaults-kwargs": dict(
        warmup=[
            P("py-candle-default", "One Candle by Default", "def light(candles: int = 1) -> str:",
              """
The lighting spell lights candles. Most of the time the wizard wants just one.

- **Write:** `light(candles)`, returning `"lit N"`, where `candles` defaults to `1`.
- **Example:** `light()` → `"lit 1"`; `light(3)` → `"lit 3"`.
""",
              "def light(candles: int = 1) -> str:\n    return f\"lit {candles}\"\n",
              [([None], ["lit 1", "lit 1"]), ([3], ["lit 1", "lit 3"])], [[0], [10]],
              params=["n"],
              driver='def driver(ns, n):\n    f = resolve(ns, "light")\n    return [f(), f() if n is None else f(n)]\n',
              hints=["A default value goes in the function's first line: `def f(x=5):`.",
                     "When the caller leaves the argument out, the default is used.",
                     "Build the text with an f-string."],
              grammar="""
## Building blocks
- **A parameter with a default:** `def brew(cups=2):`
- **Text with a value in it:** `f"made {cups}"`
"""),
        ],
        practice=[
            P("py-scroll-format", "Format a Scroll", "def scroll(title: str, *, upper: bool = False, border: str = \"*\") -> str:",
              """
Format a scroll title between two borders. The options must be given **by name** (keyword-only).

- **Write:** `scroll(title, *, upper=False, border="*")`, returning border + title + border, with the title in capitals when `upper` is true.
- **Example:** `scroll("fire")` → `"*fire*"`; `scroll("fire", upper=True, border="~")` → `"~FIRE~"`.
""",
              "def scroll(title: str, *, upper: bool = False, border: str = \"*\") -> str:\n    text = title.upper() if upper else title\n    return border + text + border\n",
              [(["fire", False, "*"], "*fire*"), (["fire", True, "~"], "~FIRE~")], [["a", False, "#"], ["", True, "!"]],
              params=["title", "upper", "border"],
              driver='def driver(ns, title, upper, border):\n    return resolve(ns, "scroll")(title, upper=upper, border=border)\n',
              hints=["A bare `*` in the parameter list means everything after it must be passed by name.",
                     "Give both options their defaults in the signature.",
                     "Choose the title text first (upper-cased or not), then glue the border on both sides."],
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
            P("py-count-spells", "How Many Ingredients?", "def ingredients(*items: str) -> int:",
              """
A potion can take any number of ingredients.

- **Write:** `ingredients(*items)`, returning how many were passed.
- **Example:** `ingredients("newt", "moss")` → `2`; `ingredients()` → `0`.
""",
              "def ingredients(*items: str) -> int:\n    return len(items)\n",
              [([["newt", "moss"]], 2), ([[]], 0)], [[["a"]], [["x", "y", "z"]]],
              params=["items"],
              driver='def driver(ns, items):\n    return resolve(ns, "ingredients")(*items)\n',
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
            P("py-potion-label", "Potion Label", "def label(name: str, *ingredients: str, **notes: str) -> str:",
              """
Make a potion label: the name, the ingredients joined with `" + "`, then any notes as `key=value`, all separated by ` | `.

- **Write:** `label(name, *ingredients, **notes)`.
- **Example:** `label("Glow", "moss", "dew", strength="mild")` → `"Glow | moss + dew | strength=mild"`.
- **Watch out:** leave out a section entirely if it's empty: `label("Plain")` → `"Plain"`.
""",
              "def label(name: str, *ingredients: str, **notes: str) -> str:\n    parts = [name]\n    if ingredients:\n        parts.append(\" + \".join(ingredients))\n    if notes:\n        parts.append(\", \".join(f\"{k}={v}\" for k, v in notes.items()))\n    return \" | \".join(parts)\n",
              [(["Glow", ["moss", "dew"], {"strength": "mild"}], "Glow | moss + dew | strength=mild"), (["Plain", [], {}], "Plain")],
              [["X", ["a"], {}], ["Y", [], {"k": "v", "z": "w"}]],
              params=["name", "ingredients", "notes"],
              driver='def driver(ns, name, ingredients, notes):\n    return resolve(ns, "label")(name, *ingredients, **notes)\n',
              hints=["`*ingredients` arrives as a tuple and `**notes` as a dict.",
                     "Build a list of the label's parts, adding each section only if it isn't empty.",
                     "Join the ingredients with `\" + \"`, the notes as `k=v` with `\", \"`, and finally everything with `\" | \"`."],
              grammar="""
## Building blocks
- **Collect keyword arguments:** `def f(**opts):`
- **Key and value pairs:** `for k, v in d.items():`
- **Join with a separator:** `" + ".join(words)`
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
            P("py-shortest-spell", "Shortest Spell First", "def by_length(spells: List[str]) -> List[str]:",
              """
Sort the spells from shortest to longest. Spells of the same length keep their order.

- **You get:** `spells`.
- **Return:** a new list sorted by length, using `key=len`.
- **Example:** `["blaze", "go", "rain"]` → `["go", "rain", "blaze"]`.
""",
              "def by_length(spells: List[str]) -> List[str]:\n    return sorted(spells, key=len)\n",
              [([["blaze", "go", "rain"]], ["go", "rain", "blaze"]), ([[]], [])], [[["bb", "a", "cc"]]],
              hints=["`sorted` can sort by whatever a `key` function returns.",
                     "`len` is a function, so it can be the key directly (no brackets after it).",
                     "Python's sort is stable, so equal lengths keep their order."],
              grammar="""
## Building blocks
- **Sort by a key:** `sorted(items, key=abs)`
"""),
        ],
        practice=[
            P("py-strongest-familiar", "The Strongest Familiar", "def strongest(familiars: Dict[str, List[int]]) -> str:",
              """
Each familiar has a list of training scores. The strongest has the highest **average**.

- **You get:** `familiars`, name → scores (each list has at least one score).
- **Return:** the name with the highest average (the first in the dict if tied).
- **Example:** `{"owl": [3, 5], "cat": [6], "toad": [1, 9]}` → `"cat"` (averages 4, 6, 5).
""",
              "def strongest(familiars: Dict[str, List[int]]) -> str:\n    return max(familiars, key=lambda name: sum(familiars[name]) / len(familiars[name]))\n",
              [([{"owl": [3, 5], "cat": [6], "toad": [1, 9]}], "cat"), ([{"x": [1]}], "x")], [[{"a": [2, 2], "b": [1, 3]}]],
              require=["lambda"],
              hints=["`max` over a dict looks at its keys (the names).",
                     "Give `max` a `key`: a `lambda` that takes a name and works out that familiar's average.",
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
            P("py-upper-runes", "Shout the Runes", "def shout(runes: List[str]) -> List[str]:",
              """
Turn every rune name into capitals, using `map`.

- **You get:** `runes`.
- **Return:** the names in upper case.
- **Example:** `["fire", "ice"]` → `["FIRE", "ICE"]`.
""",
              "def shout(runes: List[str]) -> List[str]:\n    return list(map(str.upper, runes))\n",
              [([["fire", "ice"]], ["FIRE", "ICE"]), ([[]], [])], [[["a"]]],
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
            P("py-strong-potions", "Strong Potions Only", "def strong(potions: List[str]) -> List[int]:",
              """
Potion strengths are written as text. Convert them to numbers and keep only the ones of 50 or more, in order.

- **You get:** `potions`, strength strings.
- **Return:** the strong ones as ints, using `map` and `filter`.
- **Example:** `["20", "75", "50"]` → `[75, 50]`.
""",
              "def strong(potions: List[str]) -> List[int]:\n    return list(filter(lambda n: n >= 50, map(int, potions)))\n",
              [([["20", "75", "50"]], [75, 50]), ([[]], [])], [[["1"]], [["99", "100"]]],
              require=["map", "filter"],
              hints=["Two steps: convert every string with `map`, then keep the big ones with `filter`.",
                     "`filter` can work directly on what `map` gives back; there's no need to make a list in between.",
                     "Give `filter` a `lambda` that checks the strength is at least 50, and wrap the final result in `list(...)`."],
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
            P("py-add-one-comp", "Level Up Everyone", "def level_up(levels: List[int]) -> List[int]:",
              """
Every apprentice goes up one level.

- **You get:** `levels`.
- **Return:** each level plus one, using a list comprehension.
- **Example:** `[1, 4]` → `[2, 5]`.
""",
              "def level_up(levels: List[int]) -> List[int]:\n    return [lv + 1 for lv in levels]\n",
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
            P("py-initials-dict", "Apprentice Initials", "def initials(names: List[str]) -> Dict[str, str]:",
              """
Map each apprentice to their initials, skipping any blank names.

- **You get:** `names`, full names like `"ada lovelace"`.
- **Return:** a dict from each non-blank name to its initials in capitals, using a dict comprehension.
- **Example:** `["ada lovelace", "", "bo"]` → `{"ada lovelace": "AL", "bo": "B"}`.
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
            P("py-countdown-recursive", "Countdown Chant", "def chant(n: int) -> List[int]:",
              """
Chant the numbers from `n` down to 1, recursively.

- **You get:** `n` (0 or more).
- **Return:** the list `[n, n-1, …, 1]`, built with recursion (no loops).
- **Example:** `3` → `[3, 2, 1]`; `0` → `[]`.
""",
              "def chant(n: int) -> List[int]:\n    if n == 0:\n        return []\n    return [n] + chant(n - 1)\n",
              [([3], [3, 2, 1]), ([0], [])], [[1], [6]],
              require=["recursion"], forbid=["for", "while"],
              hints=["The chant for `n` is `n` followed by the chant for `n - 1`.",
                     "Base case: the chant for 0 is an empty list.",
                     "Join a one-item list and the smaller chant with `+`."],
              grammar="""
## Building blocks
- **Call yourself on something smaller:** `f(k - 1)`
- **Join two lists:** `[a] + rest`
- **Stop at the bottom:** `if k == 0: return []`
"""),
        ],
        practice=[
            P("py-power-tower", "Power Tower", "def power(base: int, exp: int) -> int:",
              """
Raise `base` to the power `exp` by recursion, using the fast trick: x to the power 2k is (x to the power k) squared.

- **You get:** `base` and `exp` (0 or more).
- **Return:** `base ** exp`, worked out recursively (no `**`, no `pow`).
- **Example:** `2, 10` → `1024`; `5, 0` → `1`.
""",
              "def power(base: int, exp: int) -> int:\n    if exp == 0:\n        return 1\n    half = power(base, exp // 2)\n    if exp % 2 == 0:\n        return half * half\n    return half * half * base\n",
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
            P("py-make-greeter", "Forge a Greeter", "def make_greeter(word: str):",
              """
Forge greeting spells: each one remembers its own greeting word.

- **Write:** `make_greeter(word)`, returning a function that takes `name` and returns `"WORD NAME"`.
- **Example:** `make_greeter("Hi")("Ada")` → `"Hi Ada"`.
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
            P("py-make-limited", "A Spell with Three Charges", "def make_wand(charges: int):",
              """
A wand holds a number of charges. Each wave uses one and returns `"zap"`; once it's empty, it returns `"fizzle"`.

- **Write:** `make_wand(charges)`, returning a function with no parameters that behaves like that.
- **Example:** a wand with 2 charges waved 3 times gives `"zap"`, `"zap"`, `"fizzle"`.
""",
              "def make_wand(charges: int):\n    left = charges\n\n    def wave():\n        nonlocal left\n        if left == 0:\n            return \"fizzle\"\n        left -= 1\n        return \"zap\"\n\n    return wave\n",
              [([2, 3], ["zap", "zap", "fizzle"]), ([0, 1], ["fizzle"])], [[1, 2], [3, 3]],
              params=["charges", "waves"],
              driver='def driver(ns, charges, waves):\n    w = resolve(ns, "make_wand")(charges)\n    return [w() for _ in range(waves)]\n',
              require=["nonlocal"],
              hints=["The inner function must change a number that lives in the outer function.",
                     "Declare it `nonlocal` inside the inner function before changing it.",
                     "Check for zero first and return `\"fizzle\"`; otherwise use a charge and return `\"zap\"`."],
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
            P("py-yield-evens", "Even Sparks", "def sparks(n: int):",
              """
A generator of sparks: yield the even numbers from 0 up to (but not including) `n`.

- **Write:** a generator `sparks(n)`.
- **Example:** `sparks(7)` yields `0, 2, 4, 6`.
""",
              "def sparks(n: int):\n    for i in range(0, n, 2):\n        yield i\n",
              [([7], [0, 2, 4, 6]), ([0], [])], [[1], [10]],
              driver='def driver(ns, n):\n    return list(resolve(ns, "sparks")(n))\n',
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
            P("py-take-while-lit", "Lit Torches", "def lit_prefix(torches: List[int]) -> List[int]:",
              """
Torches burn in a row. Read them from the start and stop at the first one that's out (strength 0).

- **You get:** `torches`, strengths.
- **Return:** the strengths before the first 0, using `iter` and `next` (no `for` loop).
- **Example:** `[3, 5, 0, 4]` → `[3, 5]`.
""",
              "def lit_prefix(torches: List[int]) -> List[int]:\n    it = iter(torches)\n    out = []\n    while (t := next(it, 0)) != 0:\n        out.append(t)\n    return out\n",
              [([[3, 5, 0, 4]], [3, 5]), ([[]], [])], [[[0, 1]], [[1, 2, 3]]],
              require=["iter", "next"], forbid=["for"],
              hints=["`iter(list)` gives an iterator; `next(iterator, default)` takes the next item or returns the default at the end.",
                     "Using 0 as the default means \"run out\" and \"torch is out\" look the same, so one check stops both.",
                     "Loop with `while`, taking the next strength each time, until it's 0."],
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
            P("py-shout-decorator", "The Loud Rune", "def loud(func):",
              """
Carve the loud rune on a spell, and its text result comes out in capitals.

- **Write:** a decorator `loud` whose wrapper returns the original result upper-cased.
- **Example:** a spell returning `"hi " + name`, decorated with `@loud`, called with `"bo"` → `"HI BO"`.
""",
              "def loud(func):\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs).upper()\n    return wrapper\n",
              [(["bo"], "HI BO"), ([""], "HI ")], [["x"]],
              params=["name"],
              driver='def driver(ns, name):\n    deco = resolve(ns, "loud")\n\n    @deco\n    def hello(n):\n        return "hi " + n\n\n    return hello(name)\n',
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
            P("py-retry-decorator", "Try the Spell Twice", "def retry_once(func):",
              """
Some spells fail the first time. The retry rune catches a `ValueError` and tries once more; if that fails too, the error escapes.

- **Write:** a decorator `retry_once`.
- **Example:** a spell that fails on its first call then succeeds returns its result (`"ok"`); one that fails twice still raises `ValueError` (the tests report that as `"ValueError escaped"`).
""",
              "def retry_once(func):\n    def wrapper(*args, **kwargs):\n        try:\n            return func(*args, **kwargs)\n        except ValueError:\n            return func(*args, **kwargs)\n    return wrapper\n",
              [([1], "ok"), ([2], "ValueError escaped")], [[0]],
              params=["fails"],
              driver='def driver(ns, fails):\n    deco = resolve(ns, "retry_once")\n    calls = [0]\n\n    @deco\n    def spell():\n        calls[0] += 1\n        if calls[0] <= fails:\n            raise ValueError("fizzle")\n        return "ok"\n\n    try:\n        return spell()\n    except ValueError:\n        return "ValueError escaped"\n',
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
    id="review-5", title="Review: the spellbook exam",
    intro="""
The spellbook exam mixes everything in this world: defaults, `*args`/`**kwargs`, `lambda` keys, comprehensions, recursion, closures, generators and decorators.
""",
    problems=[
        P("py-review-spell-ranking", "Rank the Spells", "def rank(spells: List[str], power: Dict[str, int]) -> List[str]:",
          """
Rank the spells by power, strongest first. Spells missing from `power` have power 0. Ties go alphabetically.

- **You get:** `spells` and `power` (spell → power).
- **Return:** the spells ranked, using `sorted` with a `lambda` key.
- **Example:** `["fog", "fire", "ice"]` with `{"fire": 9, "ice": 9}` → `["fire", "ice", "fog"]`.
""",
          "def rank(spells: List[str], power: Dict[str, int]) -> List[str]:\n    return sorted(spells, key=lambda s: (-power.get(s, 0), s))\n",
          [([["fog", "fire", "ice"], {"fire": 9, "ice": 9}], ["fire", "ice", "fog"]), ([[], {}], [])], [[["b", "a"], {}], [["x", "y"], {"y": 1}]],
          require=["lambda"],
          hints=["Two sorting rules: higher power first, then alphabetical.",
                 "A key can return a tuple; tuples compare item by item. Negate the power so higher comes first.",
                 "Read missing spells' power with `.get(spell, 0)`."],
          grammar="""
## Building blocks
- **Sort by two things:** a key that returns a tuple, like `(-score, name)`.
- **Read with a default:** `d.get(k, 0)`
"""),
        P("py-review-flatten-scrolls", "Unroll Nested Scrolls", "def unroll(scroll: list) -> List[str]:",
          """
A scroll holds words and smaller scrolls (lists), nested to any depth. Read every word in order, skipping empty words.

- **You get:** `scroll`.
- **Return:** all the non-empty words, in reading order.
- **Example:** `["a", ["b", ["", "c"]], "d"]` → `["a", "b", "c", "d"]`.
""",
          "def unroll(scroll: list) -> List[str]:\n    out = []\n    for part in scroll:\n        if isinstance(part, list):\n            out += unroll(part)\n        elif part:\n            out.append(part)\n    return out\n",
          [([["a", ["b", ["", "c"]], "d"]], ["a", "b", "c", "d"]), ([[]], [])], [[[[[["x"]]]]], [["", ""]]],
          require=["recursion"],
          hints=["Each item is either a word or another scroll (a list).",
                 "For a list, call your own function on it and add everything it returns.",
                 "For a word, add it only if it isn't empty (empty strings are falsy)."],
          grammar="""
## Building blocks
- **Is it a list?** `isinstance(x, list)`
- **Add several items:** `out += more`
- **Call yourself on a smaller part:** `f(part)`
"""),
        P("py-review-cooldowns", "Spell Cooldowns", "def make_caster(cooldown: int):",
          """
A caster can only cast once every `cooldown` ticks. Build a caster function that takes the current `tick` and returns `True` if the cast happens (and starts the cooldown), or `False` if it's still cooling down.

- **Write:** `make_caster(cooldown)`, returning a function `cast(tick)`.
- **Example:** with cooldown `3`, casting at ticks `0, 1, 3, 4, 6` gives `True, False, True, False, True`.
""",
          "def make_caster(cooldown: int):\n    ready_at = 0\n\n    def cast(tick):\n        nonlocal ready_at\n        if tick < ready_at:\n            return False\n        ready_at = tick + cooldown\n        return True\n\n    return cast\n",
          [([3, [0, 1, 3, 4, 6]], [True, False, True, False, True]), ([1, [0, 0, 1]], [True, False, True])], [[5, [0, 4, 5, 9, 10]], [2, []]],
          params=["cooldown", "ticks"],
          driver='def driver(ns, cooldown, ticks):\n    cast = resolve(ns, "make_caster")(cooldown)\n    return [cast(t) for t in ticks]\n',
          hints=["The caster needs to remember the tick when it's next ready, between calls: a closure.",
                 "Store that tick in the outer function, starting at 0, and use `nonlocal` to update it.",
                 "If the tick is earlier than the ready tick, refuse; otherwise cast and set the next ready tick to now plus the cooldown."],
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
