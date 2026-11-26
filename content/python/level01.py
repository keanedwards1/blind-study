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
                P("py-one-less", "One Less", "def one_less(number: int) -> int:",
                  """Given a whole number `number`, return the number that comes **just before** it.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def one_less(number: int) -> int:\n    return number - 1\n",
                  [([5], 4), ([1], 0), ([0], -1)], [[100], [-7], [2]],
                  hints=["Subtract 1 from `number` and return the result."],
                  grammar="""
## Building blocks
- **Return a value:** `return something` sends `something` back as the answer.
- **Subtract:** `number - 1`
- **Indentation:** the `return` line sits 4 spaces in from `def`.
"""),
                P("py-double-it", "Double It", "def double(number: int) -> int:",
                  """Return twice the value of `number`.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def double(number: int) -> int:\n    return number * 2\n",
                  [([3], 6), ([0], 0), ([-4], -8)], [[50], [1], [-1]],
                  hints=["Multiplication in Python is `*`."],
                  grammar="""
## Building blocks
- **Multiply:** `number * 2`
- **Return it:** `return num * 2`
"""),
                P("py-rectangle-area", "Rectangle Area", "def area(width: int, height: int) -> int:",
                  """Return the area of a rectangle that is `width` wide and `height` tall (width × height).

**Constraints**
- `0 <= width, height <= 10^16`
""",
                  "def area(width: int, height: int) -> int:\n    return width * height\n",
                  [([3, 4], 12), ([5, 5], 25), ([1, 9], 9)], [[0, 7], [10, 10], [12, 3]],
                  grammar="""
## Building blocks
- **Two parameters:** use both names, `width` and `height`, directly.
- **Multiply:** `width * height`
"""),
                P("py-change-due", "Change Due", "def change_due(price: int, paid: int, items: int) -> int:",
                  """You buy `items` things that each cost `price`, and hand over `paid`. Return the change you get back.

You always pay enough.

**Constraints**
- `0 <= price, items <= 1000`
- `0 <= paid <= 10^5`
- `paid >= price * items`
""",
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
                P("py-average-of-two", "Average of Two", "def average(first: int, second: int) -> float:",
                  """Return the average of `first` and `second` as a **float** (a number with a decimal point).

**Constraints**
- `-1000 <= first, second <= 1000`
""",
                  "def average(first: int, second: int) -> float:\n    return (first + second) / 2\n",
                  [([2, 4], 3.0), ([1, 2], 1.5), ([5, 5], 5.0)], [[0, 0], [-3, 3], [7, 10], [100, 1]],
                  compare="strict",
                  hints=["Add them, then divide by 2. Which division operator always gives a float?", "Brackets: `(first + second) / 2`, not `first + second / 2`."],
                  grammar="""
## Building blocks
- **True division:** `/` always gives a float: `4 / 2` is `2.0`.
- **Brackets first:** `(first + second) / 2`. Without them, only `second` is divided.
- **This task checks the type:** returning `3` instead of `3.0` counts as wrong.
"""),
                P("py-share-sweets", "Share the Sweets", "def share(sweets: int, kids: int) -> List[int]:",
                  """Share `sweets` equally between `kids`, giving each child as many **whole** sweets as possible. Return a list `[each, left_over]`: how many each child gets, and how many are left.

**Constraints**
- `0 <= sweets <= 10^16`
- `1 <= kids <= 10^16`
""",
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
                P("py-is-even", "Is It Even?", "def is_even(number: int) -> bool:",
                  """Return `True` if `number` is even, otherwise `False`.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def is_even(number: int) -> bool:\n    return number % 2 == 0\n",
                  [([4], True), ([7], False), ([0], True)], [[-2], [-3], [1], [1000001]],
                  require=["op:%"],
                  hints=["An even number leaves no remainder when divided by 2."],
                  grammar="""
## Building blocks
- **Remainder:** `number % 2` is `0` for even numbers and `1` for odd ones.
- **Compare:** `==` gives `True` or `False`, so you can return a comparison directly.
"""),
                P("py-power-of", "Power Of", "def power(base: int, exponent: int) -> int:",
                  """Return `base` raised to the power `exponent`.

**Constraints**
- `-100 <= base <= 100`
- `0 <= exponent <= 100`
""",
                  "def power(base: int, exponent: int) -> int:\n    return base ** exponent\n",
                  [([2, 3], 8), ([5, 0], 1), ([10, 2], 100)], [[3, 4], [1, 50], [-2, 3], [7, 1]],
                  require=["op:**"],
                  grammar="""
## Building blocks
- **Power:** `base ** exponent`. (`^` is *not* power in Python; it's a bit operation.)
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
                  """People can vote from age 18. Return `True` if someone aged `age` can vote.

**Constraints**
- `0 <= age <= 150`
""",
                  "def can_vote(age: int) -> bool:\n    return age >= 18\n",
                  [([18], True), ([17], False), ([40], True)], [[0], [19], [100], [5]],
                  grammar="""
## Building blocks
- **At least:** `>=`
- **Return the comparison itself:** `return years >= 18` already is `True` or `False`.
"""),
                P("py-not-equal", "Different Values", "def different(first: int, second: int) -> bool:",
                  """Return `True` if `first` and `second` are different numbers.

**Constraints**
- `-10^16 <= first, second <= 10^16`
""",
                  "def different(first: int, second: int) -> bool:\n    return first != second\n",
                  [([1, 2], True), ([3, 3], False)], [[0, 0], [-1, 1], [5, 6]],
                  require=["op:!="],
                  grammar="""
## Building blocks
- **Not equal:** `first != second`
"""),
                P("py-is-nonzero", "Truthy or Falsy", "def is_truthy(number: int) -> bool:",
                  """Return what `bool` says about `number`: `False` for `0`, `True` for any other number.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def is_truthy(number: int) -> bool:\n    return bool(number)\n",
                  [([0], False), ([3], True), ([-1], True)], [[100], [1], [-50]],
                  require=["bool"],
                  grammar="""
## Building blocks
- **Convert to True/False:** `bool(number)` is `False` only for zero.
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
                P("py-sign", "Sign of a Number", "def sign(number: int) -> int:",
                  """Return `1` if `number` is positive, `-1` if it's negative, and `0` if it's zero.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def sign(number: int) -> int:\n    if number > 0:\n        return 1\n    elif number < 0:\n        return -1\n    else:\n        return 0\n",
                  [([5], 1), ([-3], -1), ([0], 0)], [[1], [-1], [999], [-999]],
                  require=["if"],
                  grammar="""
## Building blocks
- **Three cases:** `if num > 0:` … `elif num < 0:` … `else:`
- **Colons and indentation:** each condition line ends with `:`, and its block is indented 4 more spaces.
- **Return inside a branch:** `return 1` ends the function right there.
"""),
                P("py-grade", "Letter Grade", "def grade(score: int) -> str:",
                  """Turn a test `score` into a letter: 90 and above is `"A"`, 80–89 `"B"`, 70–79 `"C"`, and anything lower `"F"`.

**Constraints**
- `0 <= score <= 100`
""",
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
                P("py-fizzbuzz-one", "FizzBuzz (One Number)", "def fizzbuzz(number: int) -> str:",
                  """Return `"FizzBuzz"` if `number` is divisible by both 3 and 5, `"Fizz"` if only by 3, `"Buzz"` if only by 5, and otherwise `number` as text.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  'def fizzbuzz(number: int) -> str:\n    if number % 15 == 0:\n        return "FizzBuzz"\n    if number % 3 == 0:\n        return "Fizz"\n    if number % 5 == 0:\n        return "Buzz"\n    return str(number)\n',
                  [([15], "FizzBuzz"), ([9], "Fizz"), ([10], "Buzz"), ([7], "7")], [[1], [3], [5], [30], [98], [45]],
                  difficulty="Medium",
                  hints=["Check the both-3-and-5 case first.", "`str(number)` turns a number into text."],
                  grammar="""
## Building blocks
- **Divisible by:** `number % 3 == 0`
- **Both at once:** `number % 3 == 0 and number % 5 == 0`, or simply `number % 15 == 0`.
- **Most specific first:** check FizzBuzz before Fizz and Buzz.
- **Number to text:** `str(number)`
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
                P("py-in-range", "In Range", "def in_range(value: int, low: int, high: int) -> bool:",
                  """Return `True` if `value` is between `low` and `high`, **including** both ends.

**Constraints**
- `-10^16 <= value, low, high <= 10^16`
- `low <= high`
""",
                  "def in_range(value: int, low: int, high: int) -> bool:\n    return low <= value <= high\n",
                  [([5, 1, 10], True), ([1, 1, 10], True), ([11, 1, 10], False)], [[0, 1, 10], [10, 1, 10], [-5, -10, -1], [3, 3, 3]],
                  grammar="""
## Building blocks
- **Both conditions:** `value >= low and value <= high`
- **Chained shortcut:** `low <= value <= high` means the same thing.
"""),
                P("py-is-weekend", "Is It the Weekend?", "def is_weekend(day: int) -> bool:",
                  """Days are numbered 1 (Monday) to 7 (Sunday). Return `True` for Saturday (6) or Sunday (7).

**Constraints**
- `1 <= day <= 7`
""",
                  "def is_weekend(day: int) -> bool:\n    return day == 6 or day == 7\n",
                  [([6], True), ([7], True), ([1], False)], [[2], [3], [4], [5]],
                  require=["op:or"],
                  grammar="""
## Building blocks
- **Either one:** `or`. Each side needs its own full comparison: `x == 1 or x == 2`, never `x == 1 or 2`.
"""),
                P("py-exactly-one", "Exactly One", "def exactly_one(first: bool, second: bool) -> bool:",
                  """Return `True` if exactly one of `first` and `second` is `True` (not both, not neither).

**Constraints**
- `first` and `second` are each `True` or `False`
""",
                  "def exactly_one(first: bool, second: bool) -> bool:\n    return (first or second) and not (first and second)\n",
                  [([True, False], True), ([True, True], False), ([False, False], False)], [[False, True]],
                  require=["op:not"],
                  hints=["At least one is true, and not both are true."],
                  grammar="""
## Building blocks
- **At least one:** `first or second`
- **Not both:** `not (first and second)`
- **Group with brackets:** `(p or q)` is worked out before whatever is outside the brackets.
- **Shortcut you'll see later:** `first != second` gives the same answer for bools.
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
                  """You get a whole number written as text. Return that number plus one, as an **int**.

**Constraints**
- `1 <= len(text) <= 20`
- `text` is digits, with an optional `-` in front
""",
                  "def add_one(text: str) -> int:\n    return int(text) + 1\n",
                  [(["41"], 42), (["0"], 1), (["-5"], -4)], [["999"], ["7"], ["-1"]],
                  require=["int"],
                  grammar="""
## Building blocks
- **Text to whole number:** `int(text)`
- **Then add:** `int(text) + 1`. Adding `1` to the text itself is an error.
"""),
                P("py-number-to-text", "Number to Text", "def to_text(number: int) -> str:",
                  """Return the number `number` written as text.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def to_text(number: int) -> str:\n    return str(number)\n",
                  [([12], "12"), ([0], "0"), ([-3], "-3")], [[1000], [7]],
                  require=["str"],
                  grammar="""
## Building blocks
- **Anything to text:** `str(number)`
"""),
                P("py-chop-decimals", "Chop the Decimals", "def chop(number: float) -> int:",
                  """Return `number` with everything after the decimal point removed, as an int.

**Constraints**
- `-10^10 <= number <= 10^10`
""",
                  "def chop(number: float) -> int:\n    return int(number)\n",
                  [([3.9], 3), ([-2.7], -2), ([5.0], 5)], [[0.5], [-0.5], [100.99]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Float to int:** `int(number)` drops the decimals, moving toward zero (so `-2.7` → `-2`).
- **Not the same as `//`:** `-2.7 // 1` is `-3.0`, which rounds down instead.
"""),
                P("py-text-times-two", "Decimal Text Doubled", "def doubled(text: str) -> float:",
                  """You get a decimal number written as text. Return twice its value as a float.

**Constraints**
- `1 <= len(text) <= 20`
- `text` is digits with an optional `-` in front and an optional decimal point
""",
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
                P("py-distance", "Distance Apart", "def distance(first: int, second: int) -> int:",
                  """Return how far apart `first` and `second` are on the number line (always zero or positive).

**Constraints**
- `-10^16 <= first, second <= 10^16`
""",
                  "def distance(first: int, second: int) -> int:\n    return abs(first - second)\n",
                  [([2, 7], 5), ([7, 2], 5), ([-3, 3], 6)], [[0, 0], [-10, -2], [100, -100]],
                  require=["abs"],
                  grammar="""
## Building blocks
- **Difference:** `first - second` (it might be negative).
- **Make it positive:** `abs(first - second)`
"""),
                P("py-round-price", "Round the Price", "def round_price(price: float) -> float:",
                  """Return `price` rounded to 2 decimal places.

**Constraints**
- `-10^10 <= price <= 10^10`
""",
                  "def round_price(price: float) -> float:\n    return round(price, 2)\n",
                  [([2.567], 2.57), ([10.0], 10.0), ([0.123], 0.12)], [[3.14159], [99.999], [1.005]],
                  require=["round"],
                  grammar="""
## Building blocks
- **Round to places:** `round(price, 2)`. The second argument is the number of decimal places.
"""),
                P("py-largest-of-three", "Largest of Three", "def largest(first: int, second: int, third: int) -> int:",
                  """Return the largest of the three numbers.

**Constraints**
- `-10^16 <= first, second, third <= 10^16`
""",
                  "def largest(first: int, second: int, third: int) -> int:\n    return max(first, second, third)\n",
                  [([1, 5, 3], 5), ([-1, -5, -3], -1), ([4, 4, 4], 4)], [[9, 2, 9], [0, -1, 1], [100, 50, 75]],
                  require=["max"],
                  grammar="""
## Building blocks
- **Biggest of several values:** `max(first, second, third)`
"""),
                P("py-clamp", "Clamp", "def clamp(value: int, low: int, high: int) -> int:",
                  """Return `value`, but forced into the range `low`…`high`: if it's below `low` return `low`, if it's above `high` return `high`.

**Constraints**
- `-10^16 <= value, low, high <= 10^16`
- `low <= high`
""",
                  "def clamp(value: int, low: int, high: int) -> int:\n    return max(low, min(value, high))\n",
                  [([5, 0, 10], 5), ([-3, 0, 10], 0), ([42, 0, 10], 10)], [[0, 0, 10], [10, 0, 10], [-50, -10, -5], [7, 7, 7]],
                  require=["min", "max"], difficulty="Medium",
                  hints=["`min(value, high)` stops `value` going above `high`.", "Then wrap that in `max(low, …)`."],
                  grammar="""
## Building blocks
- **Cap from above:** `min(value, high)`
- **Cap from below:** `max(low, something)`
- **Nest calls:** `max(low, min(value, high))`. The inner call runs first.
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
                  """Print `Hello, NAME!` using the given `name`.

_This task checks what you **print**, not what you return._

**Constraints**
- `0 <= len(name) <= 10^4`
""",
                  'def greet(name: str) -> None:\n    print("Hello, " + name + "!")\n',
                  [(["Ada"], "Hello, Ada!\n"), (["Bob"], "Hello, Bob!\n")], [["Z"], ["Grace Hopper"]],
                  out="stdout", require=["print"],
                  grammar="""
## Building blocks
- **Show text:** `print(...)`
- **Join text pieces:** `"Hello, " + name + "!"` (`+` on strings glues them).
- **Why not `print("Hello,", name, "!")`?** Commas add spaces, giving `Hello, Ada !`.
"""),
                P("py-two-lines", "Two Lines", "def two_lines(first_line: str, second_line: str) -> None:",
                  """Print `first_line` on one line and `second_line` on the next line.

_This task checks what you print._

**Constraints**
- `0 <= len(first_line), len(second_line) <= 10^4`
""",
                  "def two_lines(first_line: str, second_line: str) -> None:\n    print(first_line)\n    print(second_line)\n",
                  [(["top", "bottom"], "top\nbottom\n")], [["1", "2"], ["x", ""]],
                  out="stdout",
                  grammar="""
## Building blocks
- **One `print` per line:** each `print` ends with a new line.
"""),
                P("py-dashed", "Dashed Numbers", "def dashed(first: int, second: int, third: int) -> None:",
                  """Print the three numbers on one line with dashes between them.

_This task checks what you print._

**Constraints**
- `-10^16 <= first, second, third <= 10^16`
""",
                  'def dashed(first: int, second: int, third: int) -> None:\n    print(first, second, third, sep="-")\n',
                  [([1, 2, 3], "1-2-3\n"), ([10, 0, -5], "10-0--5\n")], [[7, 7, 7], [100, 200, 300]],
                  out="stdout",
                  grammar="""
## Building blocks
- **Several values:** `print(first, second, third)` puts spaces between them.
- **Change the separator:** `between="-"`
"""),
                P("py-same-line", "Same Line", "def same_line(first: str, second: str) -> None:",
                  """Print `first` and then `second` using **two** `print` calls, so they appear together on one line with nothing between them, followed by a single new line.

**Constraints**
- `0 <= len(first), len(second) <= 10^4`
""",
                  'def same_line(first: str, second: str) -> None:\n    print(first, end="")\n    print(second)\n',
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
                  """Read one line (a name) with `input()`, then print `Hello NAME`.

**Constraints**
- The input is one line of 1 to 100 characters
""",
                  'def main() -> None:\n    name = input()\n    print("Hello", name)\n',
                  [([["Ada"]], "Hello Ada\n"), ([["Bob"]], "Hello Bob\n")], [[["Grace"]], [["x"]]],
                  out="stdout", stdin=True, require=["input"],
                  grammar="""
## Building blocks
- **Read a line:** `person_name = input()`
- **Print two values with a space:** `print("Hello", person)`
"""),
                P("py-add-inputs", "Add Two Inputs", "def main() -> None:",
                  """Read two whole numbers, one per line, and print their sum.

**Constraints**
- The input is two lines, each a whole number from `-10^7` to `10^7`
""",
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
