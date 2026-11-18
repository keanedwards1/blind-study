# Learn Python, level 1: first steps.
# Every problem uses the same dict format as the Blind 75 (see README), plus `grammar` (Learn mode building blocks).
# Quiz questions: the correct option comes first (answer=0); the UI shuffles them. predict=True questions are run at build time.


from _helpers import P, Q


LEVEL = dict(
    n=1,
    title="First steps",
    summary="Functions that take values in and give one back: arithmetic, comparisons, `if`, and converting between numbers and text.",
    concepts=[
        # ------------------------------------------------------------------ return + arithmetic
        dict(
            id="return-arithmetic",
            title="Returning a value, and + − *",
            builtins=[],
            intro="""
Every task here is a **function**: Python calls it with some inputs, and whatever you `return` is the answer.

```python
def add_two(n):
    return n + 2
```

- The inputs (here `n`) are called **parameters**. Use them like normal variables.
- `return` sends a value back and ends the function immediately.
- `+`, `-` and `*` work as you'd expect. Brackets control the order: `(a + b) * 2`.
- Forgetting `return` is the most common first mistake. The function then gives back `None`.
""",
            problems=[
                P("py-one-less", "One Less", "def one_less(n: int) -> int:",
                  "Given a whole number `n`, return the number that comes **just before** it.\n\nFor example, the number just before `5` is `4`.",
                  "def one_less(n: int) -> int:\n    return n - 1\n",
                  [([5], 4), ([1], 0), ([0], -1)], [[100], [-7], [2]],
                  hints=["Subtract 1 from `n` and return the result."],
                  grammar="""
## Building blocks
- **Return a value:** `return something` sends `something` back as the answer.
- **Subtract:** `n - 1`
- **Indentation:** the `return` line sits 4 spaces in from `def`.
"""),
                P("py-double-it", "Double It", "def double(n: int) -> int:",
                  "Return twice the value of `n`.",
                  "def double(n: int) -> int:\n    return n * 2\n",
                  [([3], 6), ([0], 0), ([-4], -8)], [[50], [1], [-1]],
                  hints=["Multiplication in Python is `*`."],
                  grammar="""
## Building blocks
- **Multiply:** `n * 2`
- **Return it:** `return num * 2`
"""),
                P("py-rectangle-area", "Rectangle Area", "def area(width: int, height: int) -> int:",
                  "Return the area of a rectangle that is `width` wide and `height` tall (width × height).",
                  "def area(width: int, height: int) -> int:\n    return width * height\n",
                  [([3, 4], 12), ([5, 5], 25), ([1, 9], 9)], [[0, 7], [10, 10], [12, 3]],
                  grammar="""
## Building blocks
- **Two parameters:** use both names, `width` and `height`, directly.
- **Multiply:** `width * height`
"""),
                P("py-change-due", "Change Due", "def change_due(price: int, paid: int, items: int) -> int:",
                  "You buy `items` things that each cost `price`, and hand over `paid`. Return the change you get back.\n\nYou always pay enough.",
                  "def change_due(price: int, paid: int, items: int) -> int:\n    return paid - price * items\n",
                  [([3, 10, 2], 4), ([5, 5, 1], 0)], [[2, 20, 7], [1, 100, 99], [10, 50, 5]],
                  hints=["Work out the total cost first. `*` happens before `-`, just like in maths."],
                  grammar="""
## Building blocks
- **Order of operations:** `*` and `/` happen before `+` and `-`, so `paid - price * items` multiplies first.
- **Brackets:** `(price * items)` makes the order obvious, if you prefer.
- **A variable for a step:** `acc = cost * elems` then `return handed - acc`.
"""),
            ],
            quiz=[
                Q("What does this function return when called as `f(3)`?", "None", "4", "3", "An error", code="def f(n):\n    n + 1",
                  why="There is no `return`, so the function gives back `None`. Calculating `n + 1` doesn't send it anywhere."),
                Q("What does this print?", "14", "20", "11", "24", code="print(2 + 3 * 4)", predict=True,
                  why="`*` happens before `+`: 3 × 4 = 12, then 2 + 12 = 14."),
                Q("What does `return` do?", "Sends a value back and ends the function", "Prints a value to the screen",
                  "Saves a value for the next call", "Restarts the function", why="Code after a `return` that runs doesn't execute."),
            ],
        ),
        # ------------------------------------------------------------------ division
        dict(
            id="division",
            title="Division: /, //, % and **",
            builtins=[],
            intro="""
Python has three kinds of division, and they're used constantly:

| Operator | Meaning | `7 ? 2` |
|---|---|---|
| `/` | normal division, **always a float** | `3.5` |
| `//` | floor division: how many whole times | `3` |
| `%` | remainder (modulo) | `1` |

- `n % 2 == 0` is the standard "is `n` even?" test.
- `**` is "to the power of": `2 ** 3` is `8`.
- `6 / 2` is `3.0`, not `3`. Use `//` when you need a whole number.
""",
            problems=[
                P("py-average-of-two", "Average of Two", "def average(a: int, b: int) -> float:",
                  "Return the average of `a` and `b` as a **float** (a number with a decimal point). For example, the average of `2` and `4` is `3.0`.",
                  "def average(a: int, b: int) -> float:\n    return (a + b) / 2\n",
                  [([2, 4], 3.0), ([1, 2], 1.5), ([5, 5], 5.0)], [[0, 0], [-3, 3], [7, 10], [100, 1]],
                  compare="strict",
                  hints=["Add them, then divide by 2. Which division operator always gives a float?", "Brackets: `(a + b) / 2`, not `a + b / 2`."],
                  grammar="""
## Building blocks
- **True division:** `/` always gives a float: `4 / 2` is `2.0`.
- **Brackets first:** `(a + b) / 2`. Without them, only `b` is divided.
- **This task checks the type:** returning `3` instead of `3.0` counts as wrong.
"""),
                P("py-share-sweets", "Share the Sweets", "def share(sweets: int, kids: int) -> List[int]:",
                  "Share `sweets` equally between `kids`, giving each child as many **whole** sweets as possible. Return a list `[each, left_over]`: how many each child gets, and how many are left.",
                  "def share(sweets: int, kids: int) -> List[int]:\n    return [sweets // kids, sweets % kids]\n",
                  [([7, 2], [3, 1]), ([10, 5], [2, 0]), ([3, 4], [0, 3])], [[100, 7], [0, 3], [1, 1], [29, 10]],
                  require=["op://", "op:%"],
                  hints=["`//` gives the whole-number part of a division.", "`%` gives what's left over."],
                  grammar="""
## Building blocks
- **Whole times:** `sweets // kids`
- **Left over:** `sweets % kids`
- **Return a list of two values:** `return [first, second]`
"""),
                P("py-is-even", "Is It Even?", "def is_even(n: int) -> bool:",
                  "Return `True` if `n` is even, otherwise `False`.",
                  "def is_even(n: int) -> bool:\n    return n % 2 == 0\n",
                  [([4], True), ([7], False), ([0], True)], [[-2], [-3], [1], [1000001]],
                  require=["op:%"],
                  hints=["An even number leaves no remainder when divided by 2."],
                  grammar="""
## Building blocks
- **Remainder:** `n % 2` is `0` for even numbers and `1` for odd ones.
- **Compare:** `==` gives `True` or `False`, so you can return a comparison directly.
"""),
                P("py-power-of", "Power Of", "def power(base: int, exp: int) -> int:",
                  "Return `base` raised to the power `exp`. `exp` is never negative.",
                  "def power(base: int, exp: int) -> int:\n    return base ** exp\n",
                  [([2, 3], 8), ([5, 0], 1), ([10, 2], 100)], [[3, 4], [1, 50], [-2, 3], [7, 1]],
                  require=["op:**"],
                  grammar="""
## Building blocks
- **Power:** `base ** exp`. (`^` is *not* power in Python; it's a bit operation.)
"""),
            ],
            quiz=[
                Q("What does this print?", "3.5 3 1", "3.5 3.5 1", "3 3 1", "3.5 3 0.5", code="print(7 / 2, 7 // 2, 7 % 2)", predict=True,
                  why="`/` gives a float, `//` the whole part, `%` the remainder."),
                Q("What does this print?", "2.0", "2", "2.00", "error", code="print(6 / 3)", predict=True, why="`/` always returns a float, even when it divides evenly."),
                Q("Which expression is `True` exactly when `n` is odd?", "n % 2 == 1", "n / 2 == 1", "n // 2 == 1", "n ** 2 == 1",
                  why="The remainder after dividing by 2 is 1 for odd numbers. (For negative odd numbers, Python also gives 1.)"),
            ],
        ),
        # ------------------------------------------------------------------ comparisons + bool
        dict(
            id="comparisons",
            title="Comparisons and True/False",
            builtins=["bool"],
            intro="""
Comparisons give back `True` or `False` (a **bool**):

`==` equal · `!=` not equal · `<` · `>` · `<=` · `>=`

- One `=` **assigns** (`x = 5`); two `==` **compares** (`x == 5`).
- You can return a comparison directly: `return age >= 18`. No `if` needed.
- `bool(x)` converts anything to `True`/`False`. Zero, empty text `""`, empty lists and `None` are `False`; almost everything else is `True`.
""",
            problems=[
                P("py-can-vote", "Can Vote", "def can_vote(age: int) -> bool:",
                  "People can vote from age 18. Return `True` if someone aged `age` can vote.",
                  "def can_vote(age: int) -> bool:\n    return age >= 18\n",
                  [([18], True), ([17], False), ([40], True)], [[0], [19], [100], [5]],
                  grammar="""
## Building blocks
- **At least:** `>=`
- **Return the comparison itself:** `return years >= 18` already is `True` or `False`.
"""),
                P("py-not-equal", "Different Values", "def different(a: int, b: int) -> bool:",
                  "Return `True` if `a` and `b` are different numbers.",
                  "def different(a: int, b: int) -> bool:\n    return a != b\n",
                  [([1, 2], True), ([3, 3], False)], [[0, 0], [-1, 1], [5, 6]],
                  require=["op:!="],
                  grammar="""
## Building blocks
- **Not equal:** `a != b`
"""),
                P("py-is-nonzero", "Truthy or Falsy", "def is_truthy(n: int) -> bool:",
                  "Return what `bool` says about `n`: `False` for `0`, `True` for any other number.",
                  "def is_truthy(n: int) -> bool:\n    return bool(n)\n",
                  [([0], False), ([3], True), ([-1], True)], [[100], [1], [-50]],
                  require=["bool"],
                  grammar="""
## Building blocks
- **Convert to True/False:** `bool(n)` is `False` only for zero.
"""),
            ],
            quiz=[
                Q("What does this print?", "False True", "True False", "False False", "error", code="x = 5\nprint(x == 4, x != 4)", predict=True,
                  why="`==` checks equality, `!=` checks inequality."),
                Q("What does this print?", "False False True", "True True True", "False True True", "False False False",
                  code="print(bool(0), bool(''), bool('0'))", predict=True,
                  why="`0` and `''` are falsy. `'0'` is a non-empty string, so it's truthy."),
                Q("Which line *assigns* rather than compares?", "x = 3", "x == 3", "x >= 3", "x != 3", why="A single `=` stores a value in a variable."),
            ],
        ),
        # ------------------------------------------------------------------ if / elif / else
        dict(
            id="if-else",
            title="if, elif, else",
            builtins=[],
            intro="""
`if` runs a block only when a condition is true. Add `elif` ("else if") for more cases and `else` for everything left over.

```python
def describe(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"
```

- Only the **first** branch whose condition is true runs.
- Every block is indented 4 spaces past its `if`/`elif`/`else` line, which ends with a colon `:`.
- Order matters: check the most specific case first.
""",
            problems=[
                P("py-sign", "Sign of a Number", "def sign(n: int) -> int:",
                  "Return `1` if `n` is positive, `-1` if it's negative, and `0` if it's zero.",
                  "def sign(n: int) -> int:\n    if n > 0:\n        return 1\n    elif n < 0:\n        return -1\n    else:\n        return 0\n",
                  [([5], 1), ([-3], -1), ([0], 0)], [[1], [-1], [999], [-999]],
                  require=["if"],
                  grammar="""
## Building blocks
- **Three cases:** `if num > 0:` … `elif num < 0:` … `else:`
- **Colons and indentation:** each condition line ends with `:`, and its block is indented 4 more spaces.
- **Return inside a branch:** `return 1` ends the function right there.
"""),
                P("py-grade", "Letter Grade", "def grade(score: int) -> str:",
                  'Turn a test `score` (0–100) into a letter: 90 and above is `"A"`, 80–89 `"B"`, 70–79 `"C"`, and anything lower `"F"`.',
                  'def grade(score: int) -> str:\n    if score >= 90:\n        return "A"\n    elif score >= 80:\n        return "B"\n    elif score >= 70:\n        return "C"\n    return "F"\n',
                  [([95], "A"), ([85], "B"), ([70], "C"), ([12], "F")], [[90], [89], [80], [79], [69], [100], [0]],
                  hints=["Check from the highest grade down, so `>= 80` only runs for scores that weren't already an A."],
                  grammar="""
## Building blocks
- **Several cases:** one `if`, then as many `elif` as you need.
- **Order matters:** check `score >= 90` before `score >= 80`, since 95 is also `>= 80`.
- **Return text:** `return "A"` (quotes make a string).
- **Fallback:** a final `return "F"` (or an `else:`) catches everything else.
"""),
                P("py-fizzbuzz-one", "FizzBuzz (One Number)", "def fizzbuzz(n: int) -> str:",
                  'Return `"FizzBuzz"` if `n` is divisible by both 3 and 5, `"Fizz"` if only by 3, `"Buzz"` if only by 5, and otherwise `n` as text (for example `"7"`).',
                  'def fizzbuzz(n: int) -> str:\n    if n % 15 == 0:\n        return "FizzBuzz"\n    if n % 3 == 0:\n        return "Fizz"\n    if n % 5 == 0:\n        return "Buzz"\n    return str(n)\n',
                  [([15], "FizzBuzz"), ([9], "Fizz"), ([10], "Buzz"), ([7], "7")], [[1], [3], [5], [30], [98], [45]],
                  difficulty="Medium",
                  hints=["Check the both-3-and-5 case first.", "`str(n)` turns a number into text."],
                  grammar="""
## Building blocks
- **Divisible by:** `n % 3 == 0`
- **Both at once:** `n % 3 == 0 and n % 5 == 0`, or simply `n % 15 == 0`.
- **Most specific first:** check FizzBuzz before Fizz and Buzz.
- **Number to text:** `str(n)`
"""),
            ],
            quiz=[
                Q("What does this print?", "B", "A\nB", "A", "C", code="x = 7\nif x > 5:\n    print('B')\nelif x > 3:\n    print('A')\nelse:\n    print('C')", predict=True,
                  why="Only the first true branch runs. `x > 5` is true, so the `elif` is never checked."),
                Q("What's wrong with this code?", "The `if` line is missing a colon", "`==` should be `=`", "`return` can't go inside an `if`", "Nothing",
                  code="def f(x):\n    if x == 1\n        return 'one'",
                  why="Every `if`, `elif`, `else`, `for`, `while` and `def` line must end with `:`."),
            ],
        ),
        # ------------------------------------------------------------------ and / or / not
        dict(
            id="boolean-logic",
            title="and, or, not",
            builtins=[],
            intro="""
Combine conditions with:

- `a and b`: true only if **both** are true.
- `a or b`: true if **at least one** is true.
- `not a`: flips true and false.

Python also lets you chain comparisons: `lo <= x <= hi` means `lo <= x and x <= hi`.
""",
            problems=[
                P("py-in-range", "In Range", "def in_range(x: int, lo: int, hi: int) -> bool:",
                  "Return `True` if `x` is between `lo` and `hi`, **including** both ends.",
                  "def in_range(x: int, lo: int, hi: int) -> bool:\n    return lo <= x <= hi\n",
                  [([5, 1, 10], True), ([1, 1, 10], True), ([11, 1, 10], False)], [[0, 1, 10], [10, 1, 10], [-5, -10, -1], [3, 3, 3]],
                  grammar="""
## Building blocks
- **Both conditions:** `x >= lo and x <= hi`
- **Chained shortcut:** `lo <= x <= hi` means the same thing.
"""),
                P("py-is-weekend", "Is It the Weekend?", "def is_weekend(day: int) -> bool:",
                  "Days are numbered 1 (Monday) to 7 (Sunday). Return `True` for Saturday (6) or Sunday (7).",
                  "def is_weekend(day: int) -> bool:\n    return day == 6 or day == 7\n",
                  [([6], True), ([7], True), ([1], False)], [[2], [3], [4], [5]],
                  require=["op:or"],
                  grammar="""
## Building blocks
- **Either one:** `or`. Each side needs its own full comparison: `x == 1 or x == 2`, never `x == 1 or 2`.
"""),
                P("py-exactly-one", "Exactly One", "def exactly_one(a: bool, b: bool) -> bool:",
                  "Return `True` if exactly one of `a` and `b` is `True` (not both, not neither).",
                  "def exactly_one(a: bool, b: bool) -> bool:\n    return (a or b) and not (a and b)\n",
                  [([True, False], True), ([True, True], False), ([False, False], False)], [[False, True]],
                  require=["op:not"],
                  hints=["At least one is true, and not both are true."],
                  grammar="""
## Building blocks
- **At least one:** `a or b`
- **Not both:** `not (a and b)`
- **Group with brackets:** `(p or q)` is worked out before whatever is outside the brackets.
- **Shortcut you'll see later:** `a != b` gives the same answer for bools.
"""),
            ],
            quiz=[
                Q("What does this print?", "7", "False", "True", "error", code="day = 3\nprint(day == 6 or 7)", predict=True,
                  why="A classic bug. `or` doesn't compare `7` with `day`: `day == 6` is `False`, so `False or 7` gives back `7`. Write `day == 6 or day == 7`."),
                Q("What does this print?", "True", "False", "error", "None", code="x = 5\nprint(1 <= x <= 10)", predict=True,
                  why="Chained comparison: `1 <= x and x <= 10`."),
                Q("`not (a and b)` is the same as…", "(not a) or (not b)", "(not a) and (not b)", "not a and b", "a or b",
                  why="De Morgan's law: \"not both\" means \"at least one is false\"."),
            ],
        ),
        # ------------------------------------------------------------------ conversions
        dict(
            id="conversions",
            title="Converting between int, float and str",
            builtins=["int", "float", "str"],
            intro="""
Numbers and text are different types. `"5" + 1` is an error, because Python won't guess what you mean.

- `int("42")` → `42`, `int(3.9)` → `3` (cuts off the decimals, toward zero).
- `float("2.5")` → `2.5`, `float(3)` → `3.0`.
- `str(42)` → `"42"`.
- Text from `input()` is always a string, so you'll convert it a lot.
""",
            problems=[
                P("py-add-one-text", "Add One to Text", "def add_one(text: str) -> int:",
                  'You get a number written as text, like `"41"`. Return that number plus one, as an **int** (`42`).',
                  "def add_one(text: str) -> int:\n    return int(text) + 1\n",
                  [(["41"], 42), (["0"], 1), (["-5"], -4)], [["999"], ["7"], ["-1"]],
                  require=["int"],
                  grammar="""
## Building blocks
- **Text to whole number:** `int(text)`
- **Then add:** `int(text) + 1`. Adding `1` to the text itself is an error.
"""),
                P("py-number-to-text", "Number to Text", "def to_text(n: int) -> str:",
                  "Return the number `n` written as text. For example `12` becomes `\"12\"`.",
                  "def to_text(n: int) -> str:\n    return str(n)\n",
                  [([12], "12"), ([0], "0"), ([-3], "-3")], [[1000], [7]],
                  require=["str"],
                  grammar="""
## Building blocks
- **Anything to text:** `str(n)`
"""),
                P("py-chop-decimals", "Chop the Decimals", "def chop(x: float) -> int:",
                  "Return `x` with everything after the decimal point removed, as an int. `3.9` becomes `3` and `-2.7` becomes `-2`.",
                  "def chop(x: float) -> int:\n    return int(x)\n",
                  [([3.9], 3), ([-2.7], -2), ([5.0], 5)], [[0.5], [-0.5], [100.99]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Float to int:** `int(x)` drops the decimals, moving toward zero (so `-2.7` → `-2`).
- **Not the same as `//`:** `-2.7 // 1` is `-3.0`, which rounds down instead.
"""),
                P("py-text-times-two", "Decimal Text Doubled", "def doubled(text: str) -> float:",
                  'You get a decimal number as text, like `"2.5"`. Return twice its value as a float (`5.0`).',
                  "def doubled(text: str) -> float:\n    return float(text) * 2\n",
                  [(["2.5"], 5.0), (["1"], 2.0), (["-0.25"], -0.5)], [["0"], ["10.1"], ["3"]],
                  compare="strict", require=["float"],
                  grammar="""
## Building blocks
- **Text to decimal number:** `float(text)`
- **Float times int is a float:** `2.5 * 2` is `5.0`.
"""),
            ],
            quiz=[
                Q("What does this print?", "3 -3", "4 -4", "3 -4", "4 -3", code="print(int(3.7), int(-3.7))", predict=True,
                  why="`int()` drops the decimal part, moving toward zero."),
                Q("What happens here?", "TypeError", "6", "\"51\"", "51", code='print("5" + 1)',
                  why="You can't add text and a number. Convert first: `int(\"5\") + 1` or `\"5\" + str(1)`."),
                Q("What does this print?", "12", "3", "1 2", "error", code='print("1" + "2")', predict=True, why="`+` on two strings joins them."),
            ],
        ),
        # ------------------------------------------------------------------ abs round min max
        dict(
            id="number-builtins",
            title="abs, round, min and max",
            builtins=["abs", "round", "min", "max"],
            intro="""
Handy built-in functions for numbers:

- `abs(-4)` → `4`: distance from zero.
- `round(2.567, 2)` → `2.57`; `round(2.5)` → `2` (Python rounds halves to the nearest **even** number).
- `min(3, 8)` → `3`, `max(3, 8, 5)` → `8`. They take any number of values.
""",
            problems=[
                P("py-distance", "Distance Apart", "def distance(a: int, b: int) -> int:",
                  "Return how far apart `a` and `b` are on the number line (always zero or positive).",
                  "def distance(a: int, b: int) -> int:\n    return abs(a - b)\n",
                  [([2, 7], 5), ([7, 2], 5), ([-3, 3], 6)], [[0, 0], [-10, -2], [100, -100]],
                  require=["abs"],
                  grammar="""
## Building blocks
- **Difference:** `a - b` (it might be negative).
- **Make it positive:** `abs(a - b)`
"""),
                P("py-round-price", "Round the Price", "def round_price(x: float) -> float:",
                  "Return `x` rounded to 2 decimal places.",
                  "def round_price(x: float) -> float:\n    return round(x, 2)\n",
                  [([2.567], 2.57), ([10.0], 10.0), ([0.123], 0.12)], [[3.14159], [99.999], [1.005]],
                  require=["round"],
                  grammar="""
## Building blocks
- **Round to places:** `round(x, 2)`. The second argument is the number of decimal places.
"""),
                P("py-largest-of-three", "Largest of Three", "def largest(a: int, b: int, c: int) -> int:",
                  "Return the largest of the three numbers.",
                  "def largest(a: int, b: int, c: int) -> int:\n    return max(a, b, c)\n",
                  [([1, 5, 3], 5), ([-1, -5, -3], -1), ([4, 4, 4], 4)], [[9, 2, 9], [0, -1, 1], [100, 50, 75]],
                  require=["max"],
                  grammar="""
## Building blocks
- **Biggest of several values:** `max(a, b, c)`
"""),
                P("py-clamp", "Clamp", "def clamp(x: int, lo: int, hi: int) -> int:",
                  "Return `x`, but forced into the range `lo`…`hi`: if it's below `lo` return `lo`, if it's above `hi` return `hi`.",
                  "def clamp(x: int, lo: int, hi: int) -> int:\n    return max(lo, min(x, hi))\n",
                  [([5, 0, 10], 5), ([-3, 0, 10], 0), ([42, 0, 10], 10)], [[0, 0, 10], [10, 0, 10], [-50, -10, -5], [7, 7, 7]],
                  require=["min", "max"], difficulty="Medium",
                  hints=["`min(x, hi)` stops `x` going above `hi`.", "Then wrap that in `max(lo, …)`."],
                  grammar="""
## Building blocks
- **Cap from above:** `min(x, hi)`
- **Cap from below:** `max(lo, something)`
- **Nest calls:** `max(lo, min(x, hi))`. The inner call runs first.
"""),
            ],
            quiz=[
                Q("What does this print?", "2 4", "3 4", "2 3", "3 3", code="print(round(2.5), round(3.5))", predict=True,
                  why="Python rounds exact halves to the nearest even number (\"banker's rounding\")."),
                Q("What does this print?", "-7", "7", "-2", "error", code="print(min(-2, 5, -7))", predict=True, why="`min` returns the smallest value."),
            ],
        ),
        # ------------------------------------------------------------------ print
        dict(
            id="print",
            title="print: showing output",
            builtins=["print"],
            intro="""
`print` shows text on the screen. It's how scripts talk to people, and it's great for debugging.

- `print("hi")` shows `hi` and then moves to a new line.
- Several values are separated by a space: `print("a", 1)` shows `a 1`.
- `sep=` changes the separator: `print(1, 2, 3, sep="-")` shows `1-2-3`.
- `end=` changes what comes after (normally a new line): `print("a", end="")` stays on the same line.
- **`print` is not `return`.** It shows something but the function still returns `None`. In these tasks, the tests check exactly what you print.
""",
            problems=[
                P("py-say-hello", "Say Hello", "def greet(name: str) -> None:",
                  'Print `Hello, NAME!` using the given `name`. For `"Ada"` that is `Hello, Ada!`.\n\n_This task checks what you **print**, not what you return._',
                  'def greet(name: str) -> None:\n    print("Hello, " + name + "!")\n',
                  [(["Ada"], "Hello, Ada!\n"), (["Bob"], "Hello, Bob!\n")], [["Z"], ["Grace Hopper"]],
                  out="stdout", require=["print"],
                  grammar="""
## Building blocks
- **Show text:** `print(...)`
- **Join text pieces:** `"Hello, " + name + "!"` (`+` on strings glues them).
- **Why not `print("Hello,", name, "!")`?** Commas add spaces, giving `Hello, Ada !`.
"""),
                P("py-two-lines", "Two Lines", "def two_lines(a: str, b: str) -> None:",
                  "Print `a` on one line and `b` on the next line.\n\n_This task checks what you print._",
                  "def two_lines(a: str, b: str) -> None:\n    print(a)\n    print(b)\n",
                  [(["top", "bottom"], "top\nbottom\n")], [["1", "2"], ["x", ""]],
                  out="stdout",
                  grammar="""
## Building blocks
- **One `print` per line:** each `print` ends with a new line.
"""),
                P("py-dashed", "Dashed Numbers", "def dashed(a: int, b: int, c: int) -> None:",
                  "Print the three numbers on one line with dashes between them. For `1, 2, 3` print `1-2-3`.\n\n_This task checks what you print._",
                  'def dashed(a: int, b: int, c: int) -> None:\n    print(a, b, c, sep="-")\n',
                  [([1, 2, 3], "1-2-3\n"), ([10, 0, -5], "10-0--5\n")], [[7, 7, 7], [100, 200, 300]],
                  out="stdout",
                  grammar="""
## Building blocks
- **Several values:** `print(a, b, c)` puts spaces between them.
- **Change the separator:** `between="-"`
"""),
                P("py-same-line", "Same Line", "def same_line(a: str, b: str) -> None:",
                  "Print `a` and then `b` using **two** `print` calls, so they appear together on one line with nothing between them, followed by a single new line.\n\nFor `\"ab\"` and `\"cd\"` the output is `abcd`.",
                  'def same_line(a: str, b: str) -> None:\n    print(a, end="")\n    print(b)\n',
                  [(["ab", "cd"], "abcd\n")], [["x", "y"], ["", "solo"]],
                  out="stdout", require=["print"], difficulty="Medium",
                  grammar="""
## Building blocks
- **Stay on the same line:** `print(p, end="")`. The next `print` continues right after it.
- **The second print** ends normally with a new line.
"""),
            ],
            quiz=[
                Q("What does this print?", "1 2 3", "123", "1,2,3", "[1, 2, 3]", code="print(1, 2, 3)", predict=True, why="Commas in `print` add a space between values."),
                Q("What does `f(2)` return?", "None", "4", "\"4\"", "2", code="def f(x):\n    print(x * 2)",
                  why="`print` shows `4` but nothing is returned, so the call evaluates to `None`."),
                Q("What does this print?", "a b.", "a b\n.", "ab.", "a.b.", code="print('a', 'b', end='.')", predict=True,
                  why="`end='.'` replaces the usual new line."),
            ],
        ),
        # ------------------------------------------------------------------ input
        dict(
            id="input",
            title="input: reading what someone types",
            builtins=["input"],
            intro="""
`input()` pauses, waits for a line of typed text, and returns it **as a string**.

```python
name = input()
age = int(input())   # convert, because input() is always text
```

- `input("Your name? ")` shows a prompt first.
- In these tasks, the tests type for you: each `input()` call gets the next line from the test's `stdin` list.
""",
            problems=[
                P("py-echo-name", "Echo the Name", "def main() -> None:",
                  "Read one line (a name) with `input()`, then print `Hello NAME`.\n\nFor the input `Ada`, print `Hello Ada`.",
                  'def main() -> None:\n    name = input()\n    print("Hello", name)\n',
                  [([["Ada"]], "Hello Ada\n"), ([["Bob"]], "Hello Bob\n")], [[["Grace"]], [["x"]]],
                  out="stdout", stdin=True, require=["input"],
                  grammar="""
## Building blocks
- **Read a line:** `person_name = input()`
- **Print two values with a space:** `print("Hello", person)`
"""),
                P("py-add-inputs", "Add Two Inputs", "def main() -> None:",
                  "Read two whole numbers, one per line, and print their sum.",
                  "def main() -> None:\n    a = int(input())\n    b = int(input())\n    print(a + b)\n",
                  [([["3", "4"]], "7\n"), ([["-1", "1"]], "0\n")], [[["100", "250"]], [["0", "0"]], [["-5", "-6"]]],
                  out="stdout", stdin=True, require=["input", "int"],
                  hints=["`input()` gives text. `\"3\" + \"4\"` is `\"34\"`, not 7."],
                  grammar="""
## Building blocks
- **Read a line:** `input()` gives the typed text as a string.
- **Text to number:** `int("7")` gives `7`.
- **Call `input()` once per line.**
- **Print a value:** `print(x)`
"""),
            ],
            quiz=[
                Q("If someone types `5`, what is `type(input())`?", "str", "int", "float", "It depends on what they type",
                  why="`input()` always returns a string. Convert with `int()` or `float()`."),
                Q("Someone types `2` and then `3`. What does this print?", "23", "5", "2 3", "error", code="a = input()\nb = input()\nprint(a + b)",
                  why="Both values are strings, so `+` joins them."),
            ],
        ),
    ],
)
