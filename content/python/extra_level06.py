# Extra practice for Learn Python level 6 (Numbers, types & control). See extra_level03.py for the format.
from _helpers import P, Q

EXTRA = {
    "number-tools": dict(
        warmup=[
            P("py-split-hours", 'Hours and Minutes', "def hours_minutes(minutes: int) -> List[int]:",
              """
A video player shows a video's length as hours and minutes. Write `hours_minutes(minutes)` to return `[hours, minutes left over]`, using `divmod`. `minutes` is 0 or more.

Example: `hours_minutes(135)` returns `[2, 15]`.
""",
              "def hours_minutes(minutes: int) -> List[int]:\n    h, m = divmod(minutes, 60)\n    return [h, m]\n",
              [([135], [2, 15]), ([59], [0, 59])], [[0], [60], [1000]],
              require=["divmod"],
              hints=["Hours = how many whole 60s fit; minutes = the remainder.",
                     "`divmod(a, b)` gives both at once as a pair.",
                     "Unpack the pair and return it as a list."],
              grammar="""
## Building blocks
- **Whole part and remainder together:** `divmod(17, 5)` gives `(3, 2)`.
- **Unpack a pair:** `q, r = pair`
"""),
        ],
        practice=[
            P("py-average-pace", 'Average Pace', "def pace(seconds: int, km: float) -> str:",
              """
A running app shows the average pace of a run as `"M:SS /km"`. Write `pace(seconds, km)` to work out the seconds per kilometre, rounded to the nearest whole second, and format it that way. `km` is more than 0.

Example: `pace(1500, 5.0)` returns `"5:00 /km"`, and `pace(1000, 3.0)` returns `"5:33 /km"`.
""",
              "def pace(seconds: int, km: float) -> str:\n    per_km = round(seconds / km)\n    m, s = divmod(per_km, 60)\n    return f\"{m}:{s:02d} /km\"\n",
              [([1500, 5.0], "5:00 /km"), ([1000, 3.0], "5:33 /km")], [[59, 1.0], [3600, 10.0], [400, 1.5]],
              hints=["First work out the seconds per kilometre, rounded to a whole number with `round`.",
                     "Then split that into minutes and seconds with `divmod`.",
                     "Pad the seconds to two digits in the f-string with `:02d`."],
              grammar="""
## Building blocks
- **Round to a whole number:** `round(4.6)` gives `5`.
- **Whole part and remainder:** `divmod(a, b)`
- **Two-digit padding:** `f"{n:02d}"`
"""),
        ],
        reps=[
            Q("What does this print?", "(3, 2)", "3.4", "(2, 3)", "3", code="print(divmod(17, 5))", predict=True, why="17 is 3 fives with 2 left over."),
            Q("What does this print?", "-4", "-3", "-3.5", "3", code="print(-7 // 2)", predict=True, why="`//` rounds **down**, and down from -3.5 is -4."),
            Q("What does this print?", "False", "True", "0.3", "error", code="print(0.1 + 0.2 == 0.3)", predict=True,
              why="Floats have tiny rounding errors; use `math.isclose` to compare them."),
        ],
    ),
    "bases": dict(
        warmup=[
            P("py-to-binary", 'Number to Binary', "def to_binary(n: int) -> str:",
              """
A debugging tool prints numbers in binary. Write `to_binary(n)` to return `n` in binary without the `0b` prefix, using `bin`. `n` is 0 or more.

Example: `to_binary(5)` returns `"101"`, and `to_binary(0)` returns `"0"`.
""",
              "def to_binary(n: int) -> str:\n    return bin(n)[2:]\n",
              [([5], "101"), ([0], "0")], [[1], [255]],
              require=["bin"],
              hints=["`bin(n)` returns text starting with `0b`.",
                     "That prefix is always two characters long.",
                     "Slice it off."],
              grammar="""
## Building blocks
- **Binary text:** `bin(6)` gives `"0b110"`.
- **From a position to the end:** `text[2:]`
"""),
        ],
        practice=[
            P("py-colour-code", 'RGB to Hex', "def colour(r: int, g: int, b: int) -> str:",
              """
A design tool stores colours as hex codes like `"#ff8000"`, with two hex digits each for red, green and blue. Write `colour(r, g, b)`, where each value is from 0 to 255, to return `"#"` followed by each value as two lower-case hex digits.

Example: `colour(255, 128, 0)` returns `"#ff8000"`.
""",
              "def colour(r: int, g: int, b: int) -> str:\n    return \"#\" + \"\".join(format(v, \"02x\") for v in (r, g, b))\n",
              [([255, 128, 0], "#ff8000"), ([0, 0, 0], "#000000")], [[1, 2, 3], [16, 255, 10]],
              hints=["Each colour needs exactly two hex digits, so small numbers need a leading zero.",
                     "`format(value, \"02x\")` gives lower-case hex padded to 2 digits.",
                     "Format all three and join them after a `#`."],
              grammar="""
## Building blocks
- **Hex with padding:** `format(10, "02x")` gives `"0a"`.
- **Join pieces:** `"".join(parts)`
"""),
        ],
        reps=[
            Q("What does this print?", "0b1010", "1010", "10", "0x1010", code="print(bin(10))", predict=True, why="`bin` adds the `0b` prefix."),
            Q("What does this print?", "255", "ff", "0xff", "error", code="print(int('ff', 16))", predict=True, why="The second argument says the text is in base 16."),
            Q("What does this print?", "0x1f", "1f", "31", "0o37", code="print(hex(31))", predict=True, why="`hex` adds the `0x` prefix; 31 is 1f in hex."),
        ],
    ),
    "bit-ops": dict(
        warmup=[
            P("py-is-odd-bit", 'Odd Check with a Bit', "def is_odd(n: int) -> bool:",
              """
Odd numbers always have their last binary digit set. Write `is_odd(n)` to return `True` if `n` is odd, checking that bit with `&` instead of using `%`. `n` is 0 or more.

Example: `is_odd(7)` returns `True`, and `is_odd(10)` returns `False`.
""",
              "def is_odd(n: int) -> bool:\n    return n & 1 == 1\n",
              [([7], True), ([10], False)], [[0], [1], [1001]],
              forbid=["op:%"], require=["op:&"],
              hints=["In binary, odd numbers end in 1 and even numbers end in 0.",
                     "`n & 1` keeps only that last bit.",
                     "Compare it with 1."],
              grammar="""
## Building blocks
- **Last bit only:** `x & 1`
- **Equal?** `==`
"""),
        ],
        practice=[
            P("py-permission-flags", 'Permission Flags', "def can(flags: int, action: str) -> bool:",
              """
An app stores each user's permissions as bits in one number: `read` is bit 0, `write` is bit 1 and `admin` is bit 2. Write `can(flags, action)`, where `action` is `"read"`, `"write"` or `"admin"`, to return `True` if that action's bit is set.

Example: `5` is `101` in binary, so `can(5, "read")` and `can(5, "admin")` return `True` and `can(5, "write")` returns `False`.
""",
              "def can(flags: int, action: str) -> bool:\n    bit = {\"read\": 0, \"write\": 1, \"admin\": 2}[action]\n    return flags & (1 << bit) != 0\n",
              [([5, "read"], True), ([5, "write"], False), ([5, "admin"], True)], [[0, "read"], [7, "write"], [2, "admin"]],
              require=["op:<<"],
              hints=["First turn the action into its bit number (a small dict works).",
                     "`1 << k` is a number with only bit `k` set (a mask).",
                     "`flags & mask` is non-zero exactly when that bit is set. (`&` happens before `!=`, so no extra brackets are needed.)"],
              grammar="""
## Building blocks
- **A mask for one bit:** `1 << 3` gives `8`.
- **Keep only masked bits:** `x & mask`
- **Look something up:** `{"a": 0, "b": 1}["b"]`
"""),
        ],
        reps=[
            Q("What does this print?", "1", "7", "6", "0", code="print(5 & 3)", predict=True, why="101 & 011 = 001."),
            Q("What does this print?", "7", "1", "8", "2", code="print(5 | 3)", predict=True, why="101 | 011 = 111."),
            Q("What does this print?", "8", "4", "6", "32", code="print(1 << 3)", predict=True, why="Shifting 1 left three places gives 1000 in binary."),
        ],
    ),
    "complex-numbers": dict(
        warmup=[
            P("py-make-complex", 'Complex Number Parts', "def as_complex(x: int, y: int) -> List[float]:",
              """
A plotting helper stores 2D points as complex numbers. Write `as_complex(x, y)` to build `complex(x, y)` and return `[real part, imaginary part]`.

Example: `as_complex(3, 4)` returns `[3.0, 4.0]`.
""",
              "def as_complex(x: int, y: int) -> List[float]:\n    z = complex(x, y)\n    return [z.real, z.imag]\n",
              [([3, 4], [3.0, 4.0]), ([0, -1], [0.0, -1.0])], [[1, 1]],
              hints=["`complex(x, y)` builds the number `x + yj`.",
                     "Its parts are the attributes `.real` and `.imag`, both floats.",
                     "Return them in a list."],
              grammar="""
## Building blocks
- **Build a complex number:** `complex(2, 5)`
- **Its parts:** `z.real`, `z.imag`
"""),
        ],
        practice=[
            P("py-walk-complex", 'Track a Position with Complex Numbers', "def end_point(steps: str) -> List[int]:",
              """
A grid game stores a character's position as a complex number: east is `1`, west is `-1`, north is `1j` and south is `-1j`. Write `end_point(steps)`, where `steps` is a string of `N`, `S`, `E` and `W`, to return the final `[x, y]` as ints, starting from `(0, 0)`.

Example: `end_point("NNE")` returns `[1, 2]`.
""",
              "def end_point(steps: str) -> List[int]:\n    move = {\"N\": 1j, \"S\": -1j, \"E\": 1, \"W\": -1}\n    pos = 0\n    for s in steps:\n        pos += move[s]\n    return [int(pos.real), int(pos.imag)]\n",
              [(["NNE"], [1, 2]), ([""], [0, 0])], [["WWS"], ["NESW"]],
              hints=["A complex number holds two numbers at once: x as the real part and y as the imaginary part.",
                     "Map each letter to its step and add it to the position.",
                     "At the end, read `.real` and `.imag` and convert each with `int`."],
              grammar="""
## Building blocks
- **An imaginary step:** `1j`
- **Add in place:** `pos += step`
- **Back to whole numbers:** `int(3.0)`
"""),
        ],
        reps=[
            Q("What does this print?", "5.0", "7", "25", "(3+4j)", code="print(abs(3 + 4j))", predict=True, why="`abs` of a complex number is its distance from 0."),
            Q("What does this print?", "-1", "1", "1j", "(1+0j)", code="print(int((1j * 1j).real))", predict=True, why="`j` squared is -1."),
        ],
    ),
    "bytes": dict(
        warmup=[
            P("py-byte-count", 'Message Size in Bytes', "def size(message: str) -> int:",
              """
An SMS gateway charges by the byte, not the character. Write `size(message)` to return how many bytes the message takes in UTF-8.

Example: `size("hi")` returns `2`, and `size("é")` also returns `2`.
""",
              "def size(message: str) -> int:\n    return len(message.encode(\"utf-8\"))\n",
              [(["hi"], 2), (["é"], 2)], [[""], ["naïve"]],
              hints=["Letters outside basic English can take more than one byte.",
                     "`.encode(\"utf-8\")` turns text into bytes.",
                     "Count the bytes with `len`."],
              grammar="""
## Building blocks
- **Text to bytes:** `"ok".encode("utf-8")`
- **How many:** `len(data)`
"""),
        ],
        practice=[
            P("py-checksum", 'Message Checksum', "def checksum(message: str) -> int:",
              """
A serial protocol adds a simple checksum to every message: the sum of its UTF-8 byte values, kept between 0 and 255. Write `checksum(message)` to return the sum of the byte values modulo 256.

Example: `checksum("hi")` returns `209`, which is 104 + 105.
""",
              "def checksum(message: str) -> int:\n    return sum(message.encode(\"utf-8\")) % 256\n",
              [(["hi"], 209), ([""], 0)], [["hello world"], ["é"]],
              hints=["Encode the text to bytes first.",
                     "A bytes object behaves like a list of numbers, so `sum` works on it directly.",
                     "Keep the result between 0 and 255 with `% 256`."],
              grammar="""
## Building blocks
- **Text to bytes:** `text.encode("utf-8")`
- **Add up numbers:** `sum(xs)`
- **Remainder:** `x % 256`
"""),
        ],
        reps=[
            Q("What does this print?", "[104, 105]", "['h', 'i']", "b'hi'", "2", code="print(list('hi'.encode()))", predict=True, why="Each byte is a number from 0 to 255."),
            Q("What does this print?", "hi", "b'hi'", "[104, 105]", "error", code="print(bytes([104, 105]).decode())", predict=True, why="`decode` turns bytes back into text."),
            Q("What does this print?", "TypeError", "b'Xi'", "Xi", "None",
              code="b = b'hi'\ntry:\n    b[0] = 88\nexcept TypeError:\n    print('TypeError')", predict=True, why="`bytes` can't be changed; `bytearray` can."),
        ],
    ),
    "types": dict(
        warmup=[
            P("py-is-text", 'Is It Text?', "def is_text(x) -> bool:",
              """
A form validator only accepts text in its name field. Write `is_text(x)` to return `True` if `x` is a `str`, using `isinstance`.

Example: `is_text("abc")` returns `True`, and `is_text(3)` returns `False`.
""",
              "def is_text(x) -> bool:\n    return isinstance(x, str)\n",
              [(["abc"], True), ([3], False)], [[None], [[1]]],
              require=["isinstance"],
              hints=["`isinstance(value, type)` checks a value's type.",
                     "The type for text is `str`.",
                     "Return the check."],
              grammar="""
## Building blocks
- **Check a type:** `isinstance(v, int)`
"""),
        ],
        practice=[
            P("py-count-by-type", 'Count Values by Type', "def by_type(items: list) -> Dict[str, int]:",
              """
A debugging tool reports what types a list holds. Write `by_type(items)` to return a dict from each type name to how many values have that type, in the order each type first appears.

Example: `by_type([1, "a", 2, None])` returns `{"int": 2, "str": 1, "NoneType": 1}`.
""",
              "def by_type(items: list) -> Dict[str, int]:\n    counts = {}\n    for x in items:\n        name = type(x).__name__\n        counts[name] = counts.get(name, 0) + 1\n    return counts\n",
              [([[1, "a", 2, None]], {"int": 2, "str": 1, "NoneType": 1}), ([[]], {})], [[[True, 1, 1.5]], [[[], {}]]],
              hints=["`type(x).__name__` gives a value's type name as text.",
                     "Count by that name with a dict, reading the current count with a default of 0.",
                     "Dicts keep insertion order, so the first-seen order comes for free."],
              grammar="""
## Building blocks
- **A type's name:** `type(v).__name__`
- **Read with a default:** `d.get(k, 0)`
- **Store under a key:** `d[k] = v`
"""),
        ],
        reps=[
            Q("What does this print?", "True", "False", "int", "error", code="print(isinstance(True, int))", predict=True, why="`bool` is a kind of `int` in Python."),
            Q("What does this print?", "float", "int", "str", "number", code="print(type(3 / 1).__name__)", predict=True, why="`/` always gives a float."),
            Q("What does this print?", "True", "False", "error", "None", code="print(issubclass(KeyError, LookupError))", predict=True,
              why="`KeyError` is a more specific kind of `LookupError`."),
        ],
    ),
    "exceptions": dict(
        warmup=[
            P("py-safe-first", 'First Reading or None', "def first_reading(readings: List[int]) -> Optional[int]:",
              """
A monitoring page shows the first reading from a sensor, and sometimes the sensor hasn't sent any. Write `first_reading(readings)` to return the first reading, or `None` if the list is empty. Reading `readings[0]` on an empty list raises an `IndexError`, so catch it with `try`/`except`.

Example: `first_reading([7, 3])` returns `7`, and `first_reading([])` returns `None`.
""",
              "def first_reading(readings: List[int]) -> Optional[int]:\n    try:\n        return readings[0]\n    except IndexError:\n        return None\n",
              [([[7, 3]], 7), ([[]], None)], [[[0]]],
              require=["try"],
              hints=["Reading position 0 of an empty list raises an `IndexError`.",
                     "Put the risky line inside `try:`.",
                     "Catch `IndexError` specifically and return `None` there."],
              grammar="""
## Building blocks
- **Try something risky:** `try:` … `except IndexError:`
- **First item:** `xs[0]`
"""),
        ],
        practice=[
            P("py-parse-readings", 'Clean Up the Readings', "def clean(raw: List[str]) -> List[int]:",
              """
A CSV export of sensor readings has some bad values in it. Write `clean(raw)` to convert the readings that are valid whole numbers and skip the rest, in order. A blank reading means the export itself is broken, so raise `ValueError("blank reading")` as soon as you see one.

Example: `clean(["12", "x", "7"])` returns `[12, 7]`, and `clean(["5", ""])` raises `ValueError`.
""",
              "def clean(raw: List[str]) -> List[int]:\n    out = []\n    for r in raw:\n        if r == \"\":\n            raise ValueError(\"blank reading\")\n        try:\n            out.append(int(r))\n        except ValueError:\n            pass\n    return out\n",
              [([["12", "x", "7"]], [12, 7]), ([["5", ""]], {"raises": "ValueError"})], [[[]], [["a", "b"]], [["-3", "4.5"]]],
              raises=True,
              hints=["Check for a blank reading first and `raise` before trying to convert it.",
                     "For the others, try `int(...)` inside `try` and add the number on success.",
                     "In `except ValueError:` do nothing (`pass`) so the bad reading is skipped."],
              grammar="""
## Building blocks
- **Raise an error:** `raise ValueError("message")`
- **Ignore an error:** `except ValueError:` then `pass`
- **Text to number:** `int("12")`
"""),
        ],
        reps=[
            Q("What does this print?", "caught", "error", "None", "0", code="try:\n    1 / 0\nexcept ZeroDivisionError:\n    print('caught')", predict=True,
              why="The `except` branch runs when that error happens."),
            Q("What does this print?", "a b", "a", "b", "error", code="try:\n    print('a', end=' ')\nfinally:\n    print('b')", predict=True,
              why="`finally` always runs."),
            Q("What does this print?", "ValueError", "TypeError", "None", "42", code="try:\n    int('4.2')\nexcept ValueError:\n    print('ValueError')", predict=True,
              why="`int` can't read a decimal point from text."),
        ],
    ),
    "control-extras": dict(
        warmup=[
            P("py-ternary-label", 'Day or Night', "def label(hour: int) -> str:",
              """
A weather app labels each hour `"day"` from 6 up to, but not including, 18, and `"night"` otherwise. Write `label(hour)`, where `hour` is from 0 to 23, using one conditional expression.

Example: `label(12)` returns `"day"`, and `label(20)` returns `"night"`.
""",
              "def label(hour: int) -> str:\n    return \"day\" if 6 <= hour < 18 else \"night\"\n",
              [([12], "day"), ([20], "night")], [[6], [18], [0]],
              require=["ternary"],
              hints=["A conditional expression is `value_if_true if condition else value_if_false`.",
                     "A chained comparison checks the range neatly.",
                     "Mind the edges: 6 is day, 18 is night."],
              grammar="""
## Building blocks
- **One-line if/else:** `"yes" if ok else "no"`
- **Chained comparison:** `1 <= x < 5`
"""),
        ],
        practice=[
            P("py-match-command", 'Handle Chat Commands', "def command(cmd: List[str]) -> str:",
              """
A chat bot receives each command as a list of words. Write `command(cmd)` to handle them with `match`:

- `["go", place]` returns `"heading to PLACE"`
- `["stop"]` returns `"stopping"`
- `["report", *items]` returns `"reporting N items"`, for any number of items
- anything else returns `"unknown"`

Example: `command(["go", "lake"])` returns `"heading to lake"`, and `command(["report", "a", "b"])` returns `"reporting 2 items"`.
""",
              "def command(cmd: List[str]) -> str:\n    match cmd:\n        case [\"go\", place]:\n            return f\"heading to {place}\"\n        case [\"stop\"]:\n            return \"stopping\"\n        case [\"report\", *items]:\n            return f\"reporting {len(items)} items\"\n        case _:\n            return \"unknown\"\n",
              [([["go", "lake"]], "heading to lake"), ([["report", "a", "b"]], "reporting 2 items")], [[["stop"]], [["report"]], [["fly"]], [[]]],
              require=["match"],
              hints=["`match` can compare against list shapes: `case [\"halt\"]:` would match exactly the one-word list `[\"halt\"]`.",
                     "A name inside a pattern captures that position: `case [\"fly\", where]:` would store the second word in `where`.",
                     "`*items` in a pattern collects the rest, and `case _:` catches everything else."],
              grammar="""
## Building blocks
- **Match a list shape:** `case ["jump", height]:`
- **Collect the rest:** `case ["say", *words]:`
- **Anything else:** `case _:`
"""),
        ],
        reps=[
            Q("What does this print?", "found", "none", "found\nnone", "error",
              code="for x in [1, 2, 3]:\n    if x == 2:\n        print('found')\n        break\nelse:\n    print('none')", predict=True,
              why="The `else` of a loop only runs when the loop ends without `break`."),
            Q("What does this print?", "[4, 9]", "[2, 3]", "[1, 4, 9]", "error", code="print([y for x in [1, 2, 3] if (y := x * x) > 1])", predict=True,
              why="The walrus operator stores each square in `y` and the comprehension keeps the ones above 1."),
            Q("What does this print?", "small", "big", "error", "None", code="n = 3\nprint('big' if n > 5 else 'small')", predict=True, why="3 isn't greater than 5."),
        ],
    ),
    "dynamic-code": dict(
        warmup=[
            P("py-eval-sum", 'Evaluate an Expression', "def calc(expr: str) -> int:",
              """
A calculator widget receives each sum as text, like `"3 + 4"`. Write `calc(expr)` to return its value, using `eval`.

Example: `calc("3 + 4")` returns `7`.
""",
              "def calc(expr: str) -> int:\n    return eval(expr)\n",
              [(["3 + 4"], 7), (["10 - 2 * 3"], 4)], [["0"], ["2 ** 5"]],
              require=["eval"],
              hints=["`eval(text)` runs a Python expression written as text and returns its value.",
                     "Normal maths rules apply, so `*` happens before `+` and `-`.",
                     "Return what `eval` gives you."],
              grammar="""
## Building blocks
- **Evaluate text as an expression:** `eval("1 + 1")`
"""),
        ],
        practice=[
            P("py-safe-formula", 'A Safer Formula', "def apply(formula: str, x: int) -> int:",
              """
A spreadsheet feature lets users write formulas in `x`, like `"x * 2 + 1"`. Write `apply(formula, x)` to evaluate one safely: give `eval` **only** the variable `x` and an empty `__builtins__`, so the formula can't call anything else.

Example: `apply("x * 2 + 1", 5)` returns `11`.
""",
              "def apply(formula: str, x: int) -> int:\n    return eval(formula, {\"__builtins__\": {}}, {\"x\": x})\n",
              [(["x * 2 + 1", 5], 11), (["x", 0], 0)], [["x ** 2", 7], ["(x + 1) * (x - 1)", 3]],
              require=["eval"],
              hints=["`eval` accepts two extra dicts: the global names, then the local names.",
                     "Passing `{\"__builtins__\": {}}` as the globals stops the formula reaching built-ins like `open`.",
                     "Pass `{\"x\": x}` as the locals so the formula can use `x`."],
              grammar="""
## Building blocks
- **Evaluate with chosen names:** `eval(text, globals_dict, locals_dict)`
- **No built-ins:** `{"__builtins__": {}}`
"""),
        ],
        reps=[
            Q("What does this print?", "14", "20", "2 + 3 * 4", "error", code="print(eval('2 + 3 * 4'))", predict=True, why="`eval` follows normal maths rules."),
            Q("What does this print?", "10", "None", "error", "x = 10", code="env = {}\nexec('x = 10', env)\nprint(env['x'])", predict=True,
              why="`exec` stores the variables it creates in the dict you give it."),
        ],
    ),
}

REVIEW = dict(
    id="review-6", title="Review: numbers, types and control",
    intro="""
This review mixes this world's tools: number helpers, bases and bits, types, errors and the extra control-flow forms.
""",
    problems=[
        P("py-review-log-parse", 'Parse Config Values', "def parse(lines: List[str]) -> List:",
          """
A config file has one setting per line, written as `"KIND VALUE"`. Write `parse(lines)` to turn each line into a value based on its kind:

- `"int 42"` becomes the int `42`
- `"hex ff"` becomes the int `255`
- `"bin 101"` becomes the int `5`
- `"flag yes"` and `"flag no"` become `True` and `False`

A line that can't be read, because the kind is unknown or the value is bad, becomes `None`.

Example: `parse(["int 42", "hex ff", "bin 2", "flag yes"])` returns `[42, 255, None, True]`.
""",
          "def parse(lines: List[str]) -> List:\n    out = []\n    for line in lines:\n        kind, _, value = line.partition(\" \")\n        try:\n            match kind:\n                case \"int\":\n                    out.append(int(value))\n                case \"hex\":\n                    out.append(int(value, 16))\n                case \"bin\":\n                    out.append(int(value, 2))\n                case \"flag\" if value in (\"yes\", \"no\"):\n                    out.append(value == \"yes\")\n                case _:\n                    out.append(None)\n        except ValueError:\n            out.append(None)\n    return out\n",
          [([["int 42", "hex ff", "bin 2", "flag yes"]], [42, 255, None, True]), ([[]], [])], [[["flag no", "zip 1", "int x"]], [["hex 10", "bin 0"]]],
          hints=["Split each line into its kind and value (`partition(\" \")` splits at the first space).",
                 "`int(text, base)` reads hex (base 16) and binary (base 2) as well as normal numbers.",
                 "Wrap the conversion in `try`/`except ValueError` so bad values become `None`; `match` on the kind keeps the cases tidy."],
          grammar="""
## Building blocks
- **Split at the first space:** `"a b c".partition(" ")` gives `("a", " ", "b c")`.
- **Read text in a base:** `int("1f", 16)`
- **Match a value:** `case "x":` … `case _:`
"""),
        P("py-review-feature-flags", "Read Feature Flags", "def features(flags: List[int]) -> List[str]:",
          """
An admin page stores each account's enabled features as bits: bit 0 is `beta`, bit 1 is `dark` and bit 2 is `export`. Write `features(flags)`, with one number per account, to return each account's features joined with `"+"`, or `"none"` if it has none.

Example: `features([5, 0, 2])` returns `["beta+export", "none", "dark"]`.
""",
          "def features(flags: List[int]) -> List[str]:\n    names = [\"beta\", \"dark\", \"export\"]\n    out = []\n    for f in flags:\n        on = [name for bit, name in enumerate(names) if f >> bit & 1]\n        out.append(\"+\".join(on) if on else \"none\")\n    return out\n",
          [([[5, 0, 2]], ["beta+export", "none", "dark"]), ([[]], [])], [[[7]], [[1, 4]]],
          hints=["List the feature names in bit order, so a feature's position is its bit number.",
                 "`(f >> bit) & 1` reads one bit; keep the names whose bit is 1.",
                 "Join the enabled features with `\"+\"`, or use `\"none\"` when there are none (a one-line if/else fits)."],
          grammar="""
## Building blocks
- **Read one bit:** `(x >> k) & 1`
- **Position and item:** `enumerate(names)`
- **One-line if/else:** `a if cond else b`
"""),
        P("py-review-safe-average", 'Safe Average', "def safe_average(values: list) -> Optional[float]:",
          """
A metrics export mixes numbers with junk values. Write `safe_average(values)` to average only the real numbers (ints and floats, **not** bools), rounded to 2 decimal places. If there are none, return `None`.

Example: `safe_average([1, "x", 2.5, True])` returns `1.75`.
""",
          "def safe_average(values: list) -> Optional[float]:\n    nums = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]\n    if not nums:\n        return None\n    return round(sum(nums) / len(nums), 2)\n",
          [([[1, "x", 2.5, True]], 1.75), ([["a"]], None)], [[[]], [[3]], [[1, 2, 2]]],
          hints=["`isinstance(v, (int, float))` accepts either type, but bools pass too, so exclude them separately.",
                 "Collect the real numbers in a list first.",
                 "If that list is empty, return `None`; otherwise average and `round(..., 2)`."],
          grammar="""
## Building blocks
- **Either of two types:** `isinstance(v, (int, str))`
- **Round to 2 places:** `round(x, 2)`
- **Empty list is falsy:** `if not xs:`
"""),
    ],
    quiz=[
        Q("What does this print?", "3", "2", "11", "error", code="print(bin(11).count('1'))", predict=True, why="11 is 1011 in binary: three 1s."),
        Q("Which runs whether or not an error happened?", "`finally`", "`except`", "`else`", "`raise`", why="A `finally` block always runs."),
    ],
)
