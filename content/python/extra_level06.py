# Extra practice for Learn Python level 6 (Numbers, types & control): the ranger station. See extra_level03.py for the format.
from _helpers import P, Q

EXTRA = {
    "number-tools": dict(
        warmup=[
            P("py-split-hours", "Hours and Minutes", "def hours_minutes(minutes: int) -> List[int]:",
              """
The trail board shows a hike's length as hours and minutes.

- **You get:** `minutes` (0 or more).
- **Return:** `[hours, minutes left over]`, using `divmod`.
- **Example:** `135` → `[2, 15]`.
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
            P("py-average-pace", "Average Pace", "def pace(seconds: int, km: float) -> str:",
              """
A ranger ran `km` kilometres in `seconds`. Show the average pace per kilometre as `"M:SS /km"`, rounding to the nearest whole second.

- **You get:** `seconds` and `km` (more than 0).
- **Return:** the pace text.
- **Example:** `1500, 5.0` → `"5:00 /km"`; `1000, 3.0` → `"5:33 /km"`.
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
            P("py-to-binary", "Binary Beacon", "def beacon(n: int) -> str:",
              """
The beacon flashes numbers in binary.

- **You get:** `n` (0 or more).
- **Return:** `n` in binary without the `0b` prefix, using `bin`.
- **Example:** `5` → `"101"`; `0` → `"0"`.
""",
              "def beacon(n: int) -> str:\n    return bin(n)[2:]\n",
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
            P("py-colour-code", "Paint Colour Code", "def colour(r: int, g: int, b: int) -> str:",
              """
The station's paint machine wants colours as hex codes like `"#ff8000"`: two hex digits each for red, green and blue.

- **You get:** `r`, `g`, `b`, each from 0 to 255.
- **Return:** `"#"` followed by each value as two lower-case hex digits.
- **Example:** `255, 128, 0` → `"#ff8000"`.
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
            P("py-is-odd-bit", "Odd Patrol Number?", "def is_odd(n: int) -> bool:",
              """
Odd numbers always have their last binary digit set. Use that instead of `%`.

- **You get:** `n` (0 or more).
- **Return:** `True` if `n` is odd, using `&`.
- **Example:** `7` → `True`; `10` → `False`.
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
            P("py-permission-flags", "Station Permissions", "def can(flags: int, action: str) -> bool:",
              """
Each ranger's permissions are stored as bits in one number: `read` is bit 0, `write` is bit 1, `admin` is bit 2.

- **You get:** `flags` and an `action` (`"read"`, `"write"` or `"admin"`).
- **Return:** `True` if that action's bit is set.
- **Example:** `5` (binary `101`) can `"read"` and `"admin"` but not `"write"`.
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
            P("py-make-complex", "Plot a Point", "def as_complex(x: int, y: int) -> List[float]:",
              """
Store the map point `(x, y)` as a complex number, then read its parts back.

- **You get:** `x` and `y`.
- **Return:** `[real part, imaginary part]` of `complex(x, y)`.
- **Example:** `3, 4` → `[3.0, 4.0]`.
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
            P("py-walk-complex", "Walk with Complex Steps", "def end_point(steps: str) -> List[int]:",
              """
Track a walk using a complex number as the position: east is `1`, west is `-1`, north is `1j`, south is `-1j`.

- **You get:** `steps`, letters `N`, `S`, `E`, `W`.
- **Return:** the final `[x, y]` as ints, starting from `(0, 0)`.
- **Example:** `"NNE"` → `[1, 2]`.
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
            P("py-byte-count", "Message Size", "def size(message: str) -> int:",
              """
The radio charges by the byte, not the letter.

- **You get:** `message`.
- **Return:** how many bytes it takes in UTF-8.
- **Example:** `"hi"` → `2`; `"é"` → `2`.
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
            P("py-checksum", "Message Checksum", "def checksum(message: str) -> int:",
              """
The radio adds a simple checksum to every message: the sum of its UTF-8 byte values, kept between 0 and 255.

- **You get:** `message`.
- **Return:** the sum of the byte values, modulo 256.
- **Example:** `"hi"` → `209` (104 + 105).
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
            P("py-is-text", "Is It Text?", "def is_text(x) -> bool:",
              """
The specimen labeller only accepts text.

- **You get:** any value `x`.
- **Return:** `True` if `x` is a `str`, using `isinstance`.
- **Example:** `"oak"` → `True`; `3` → `False`.
""",
              "def is_text(x) -> bool:\n    return isinstance(x, str)\n",
              [(["oak"], True), ([3], False)], [[None], [[1]]],
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
            P("py-sort-specimens", "Sort the Specimens", "def by_type(items: list) -> Dict[str, int]:",
              """
Count the specimens in a mixed box by type name.

- **You get:** `items`, a mixed list.
- **Return:** a dict from type name to count, in the order each type first appears.
- **Example:** `[1, "a", 2, None]` → `{"int": 2, "str": 1, "NoneType": 1}`.
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
            P("py-safe-first", "First Reading or Nothing", "def first_reading(readings: List[int]) -> Optional[int]:",
              """
Grab the first gauge reading. If the list is empty, reading `readings[0]` raises an `IndexError`; catch it.

- **You get:** `readings`.
- **Return:** the first reading, or `None` if there are none. Use `try`/`except`.
- **Example:** `[7, 3]` → `7`; `[]` → `None`.
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
            P("py-parse-readings", "Clean Up the Readings", "def clean(raw: List[str]) -> List[int]:",
              """
Hand-written readings get smudged. Convert the ones that are valid whole numbers and skip the rest, but a blank reading means the logger broke: raise a `ValueError("blank reading")` straight away.

- **You get:** `raw`, reading strings.
- **Return:** the valid readings as ints, in order.
- **Example:** `["12", "x", "7"]` → `[12, 7]`; `["5", ""]` raises `ValueError`.
""",
              "def clean(raw: List[str]) -> List[int]:\n    out = []\n    for r in raw:\n        if r == \"\":\n            raise ValueError(\"blank reading\")\n        try:\n            out.append(int(r))\n        except ValueError:\n            pass\n    return out\n",
              [([["12", "x", "7"]], [12, 7]), ([["5", ""]], {"raises": "ValueError"})], [[[]], [["a", "b"]], [["-3", "4.5"]]],
              raises=True,
              hints=["Check for a blank reading first and `raise` before trying to convert it.",
                     "For the others, try `int(...)` inside `try` and add the number on success.",
                     "In `except ValueError:` do nothing (`pass`) so the smudged reading is skipped."],
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
            P("py-ternary-label", "Day or Night", "def label(hour: int) -> str:",
              """
The station sign shows `"day"` from 6 up to (not including) 18, and `"night"` otherwise.

- **You get:** `hour`, from 0 to 23.
- **Return:** the label, using one conditional expression.
- **Example:** `12` → `"day"`; `20` → `"night"`.
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
            P("py-match-command", "Radio Commands", "def command(cmd: List[str]) -> str:",
              """
Commands arrive as lists of words. Handle them with `match`:

- `["go", place]` → `"heading to PLACE"`
- `["stop"]` → `"stopping"`
- `["report", *items]` → `"reporting N items"` (any number of items)
- anything else → `"unknown"`

**Example:** `["go", "lake"]` → `"heading to lake"`; `["report", "a", "b"]` → `"reporting 2 items"`.
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
            P("py-eval-sum", "Field Sum", "def field_sum(expr: str) -> int:",
              """
The field notebook has sums written as text, like `"3 + 4"`.

- **You get:** `expr`.
- **Return:** its value, using `eval`.
- **Example:** `"3 + 4"` → `7`.
""",
              "def field_sum(expr: str) -> int:\n    return eval(expr)\n",
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
            P("py-safe-formula", "A Safer Formula", "def apply(formula: str, x: int) -> int:",
              """
Rangers write formulas in `x`, like `"x * 2 + 1"`. Evaluate one safely: give `eval` **only** the variable `x`, and an empty `__builtins__`, so the formula can't call anything else.

- **You get:** `formula` and `x`.
- **Return:** the formula's value.
- **Example:** `"x * 2 + 1", 5` → `11`.
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
    id="review-6", title="Review: the ranger's logbook",
    intro="""
The ranger's logbook mixes this world's tools: number helpers, bases and bits, types, errors and the extra control-flow forms.
""",
    problems=[
        P("py-review-log-parse", "Parse the Logbook", "def parse(lines: List[str]) -> List:",
          """
Each logbook line is `"KIND VALUE"`. Turn every line into a value by kind:

- `"int 42"` → the int `42`
- `"hex ff"` → the int `255`
- `"bin 101"` → the int `5`
- `"flag yes"` / `"flag no"` → `True` / `False`

Any line that can't be read (unknown kind, or a bad value) becomes `None`.

**Example:** `["int 42", "hex ff", "bin 2", "flag yes"]` → `[42, 255, None, True]`.
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
        P("py-review-bit-inventory", "Bit Inventory", "def inventory(flags: List[int]) -> List[str]:",
          """
Each ranger's kit is stored as bits: bit 0 rope, bit 1 torch, bit 2 map. For each ranger, list what they carry joined with `"+"`, or `"nothing"`.

- **You get:** `flags`, one number per ranger.
- **Return:** one text per ranger.
- **Example:** `[5, 0, 2]` → `["rope+map", "nothing", "torch"]`.
""",
          "def inventory(flags: List[int]) -> List[str]:\n    names = [\"rope\", \"torch\", \"map\"]\n    out = []\n    for f in flags:\n        kit = [name for bit, name in enumerate(names) if f >> bit & 1]\n        out.append(\"+\".join(kit) if kit else \"nothing\")\n    return out\n",
          [([[5, 0, 2]], ["rope+map", "nothing", "torch"]), ([[]], [])], [[[7]], [[1, 4]]],
          hints=["List the item names in bit order, so an item's position is its bit number.",
                 "`(f >> bit) & 1` reads one bit; keep the names whose bit is 1.",
                 "Join the kit with `\"+\"`, or use `\"nothing\"` when it's empty (a one-line if/else fits)."],
          grammar="""
## Building blocks
- **Read one bit:** `(x >> k) & 1`
- **Position and item:** `enumerate(names)`
- **One-line if/else:** `a if cond else b`
"""),
        P("py-review-safe-average", "Safe Average", "def safe_average(values: list) -> Optional[float]:",
          """
Average the readings, but the box is messy: count only real numbers (ints and floats, **not** bools). If there are none, return `None`. Round to 2 decimal places.

- **You get:** `values`, a mixed list.
- **Return:** the rounded average of the real numbers, or `None`.
- **Example:** `[1, "x", 2.5, True]` → `1.75`.
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
