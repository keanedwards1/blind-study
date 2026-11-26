# Learn Python, level 6: numbers, types and control flow.
# raises=True tasks: an exception raised by your function counts as its answer, written {"raises": "ValueError"}.
from _helpers import P, Q

LEVEL = dict(
    n=6,
    title="Numbers, types & control",
    summary="The rest of Python's number tools (bases, bits, complex numbers, bytes), checking types, handling errors, and the less common control flow.",
    concepts=[
        # ------------------------------------------------------------------ divmod / pow / float details
        dict(
            id="number-tools",
            title="divmod, pow and float details",
            builtins=["divmod", "pow"],
            intro="""
- `divmod(a, b)` returns `(a // b, a % b)` in one go: `divmod(125, 60)` → `(2, 5)`.
- `pow(b, e)` is `b ** e`. With a third argument, `pow(b, e, m)` computes `(b ** e) % m` **fast**, even for huge `e`.
- `//` rounds **down** (toward minus infinity): `-7 // 2` is `-4`. `int(-7 / 2)` rounds toward zero: `-3`.
- Floats are approximate: `0.1 + 0.2 == 0.3` is `False`. Compare with `math.isclose(a, b)`.
- `float("inf")` is bigger than every number, which makes it a handy starting value for a minimum.
""",
            problems=[
                P("py-minutes-seconds", 'Format a Duration', "def mm_ss(total: int) -> str:",
                  """
A video player shows a track's length as minutes and seconds. Write `mm_ss(total)` to turn a number of seconds into `"M:SS"`, with the seconds always two digits. Use `divmod`.

**Constraints**
- `0 <= total <= 10^16`
""",
                  'def mm_ss(total: int) -> str:\n    m, s = divmod(total, 60)\n    return f"{m}:{s:02d}"\n',
                  [([125], "2:05"), ([59], "0:59"), ([3600], "60:00")], [[0], [61], [599]],
                  require=["divmod"],
                  grammar="""
## Building blocks
- **Quotient and remainder at once:** `mins, phrase = divmod(sum_so_far, 60)`
- **Two-digit seconds:** `f"{s:02d}"`
"""),
                P("py-mod-pow", 'Huge Power, Small Remainder', "def power_mod(base: int, exponent: int, modulus: int) -> int:",
                  """
A hashing routine needs `(base ** exponent) % modulus`, where `exponent` can be as large as 10¹⁵. Write `power_mod(base, exponent, modulus)`. Working out `base ** exponent` first is far too slow.

**Constraints**
- `0 <= base, exponent <= 10^16`
- `1 <= modulus <= 10^16`
""",
                  "def power_mod(base: int, exponent: int, modulus: int) -> int:\n    return pow(base, exponent, modulus)\n",
                  [([2, 10, 1000], 24), ([3, 0, 7], 1)], [[7, 10 ** 15, 1_000_000_007], [10, 10 ** 12, 9], [5, 3, 1]],
                  require=["pow"],
                  grammar="""
## Building blocks
- **Three-argument pow:** `pow(base, exponent, modulus)` never builds the giant number.
"""),
                P("py-toward-zero", 'Divide Toward Zero', "def divide(dividend: int, divisor: int) -> int:",
                  """
You're porting code from a language whose integer division rounds toward zero. Python's `//` rounds down instead, which gives different answers for negative numbers. Write `divide(dividend, divisor)` to divide and drop the fraction, rounding toward zero.

**Constraints**
- `-10^16 <= dividend, divisor <= 10^16`
- `divisor != 0`
""",
                  "def divide(dividend: int, divisor: int) -> int:\n    q = abs(dividend) // abs(divisor)\n    return q if (dividend < 0) == (divisor < 0) else -q\n",
                  [([7, 2], 3), ([-7, 2], -3), ([7, -2], -3)], [[-7, -2], [0, 5], [6, 3], [-1, 1000]],
                  difficulty="Medium",
                  hints=["`-7 // 2` is `-4` in Python, so `//` alone isn't enough for negatives.", "Divide the absolute values, then fix the sign."],
                  grammar="""
## Building blocks
- **Floor division rounds down:** `-7 // 2` is `-4`.
- **Size without the sign:** `abs(-7)` is `7`.
- **Is it negative?** `x < 0` gives `True` or `False`.
- **Booleans can be compared:** `True == True` is `True`.
- **Shortcut for small numbers:** `int(dividend / divisor)`, but float division loses precision on very large values.
"""),
                P("py-close-enough", 'Compare Floats', "def close(first: float, second: float) -> bool:",
                  """
Floats carry tiny rounding errors, so `0.1 + 0.2` is `0.30000000000000004`. Write `close(first, second)` to return `True` when two floats are equal apart from those errors. Use `math.isclose`.

**Constraints**
- `-10^16 <= first, second <= 10^16`
""",
                  "def close(first: float, second: float) -> bool:\n    return math.isclose(first, second)\n",
                  [([0.30000000000000004, 0.3], True), ([0.3, 0.31], False)], [[1e10, 1e10 + 1], [0.0, 0.0], [1.0, 1.0001]],
                  require=[".isclose"],
                  grammar="""
## Building blocks
- **Tolerant comparison:** `math.isclose(first, second)` (`math` is already imported here).
- **Why:** `0.1 + 0.2 == 0.3` is `False`.
"""),
            ],
            quiz=[
                Q("What does this print?", "-4 -3", "-3 -4", "-4 -4", "-3 -3", code="print(-7 // 2, int(-7 / 2))", predict=True,
                  why="`//` rounds down; `int()` rounds toward zero."),
                Q("What does this print?", "False", "True", code="print(0.1 + 0.2 == 0.3)", predict=True, why="Floats are binary approximations."),
                Q("What does this print?", "(3, 2)", "3 2", "[3, 2]", "3.2", code="print(divmod(17, 5))", predict=True, why="`divmod` returns a tuple."),
            ],
        ),
        # ------------------------------------------------------------------ bases
        dict(
            id="bases",
            title="bin, hex, oct and int(text, base)",
            builtins=["bin", "hex", "oct"],
            intro="""
| | 10 becomes |
|---|---|
| `bin(10)` | `'0b1010'` |
| `oct(10)` | `'0o12'` |
| `hex(255)` | `'0xff'` |

Strip the two-character prefix with `[2:]`. Going the other way, `int("1010", 2)` → `10` and `int("ff", 16)` → `255`.

`format(10, "b")` / `"o"` / `"x"` give the digits without a prefix.
""",
            problems=[
                P("py-to-hex", 'Convert to Hexadecimal', "def to_hex(number: int) -> str:",
                  """
A colour picker shows values in hexadecimal. Write `to_hex(number)` to return `number` in lower-case hex without the `0x` prefix.

**Constraints**
- `0 <= number <= 10^16`
""",
                  "def to_hex(number: int) -> str:\n    return hex(number)[2:]\n",
                  [([255], "ff"), ([0], "0"), ([16], "10")], [[4096], [3735928559]],
                  require=["hex"],
                  grammar="""
## Building blocks
- **Hex text:** `hex(number)` gives `'0xff'`.
- **Drop the prefix:** `[2:]`
"""),
                P("py-to-octal", 'Convert to Octal', "def to_octal(number: int) -> str:",
                  """
Unix file permissions are written in octal. Write `to_octal(number)` to return `number` in octal without the `0o` prefix.

**Constraints**
- `0 <= number <= 10^16`
""",
                  "def to_octal(number: int) -> str:\n    return oct(number)[2:]\n",
                  [([8], "10"), ([0], "0"), ([64], "100")], [[7], [511]],
                  require=["oct"],
                  grammar="""
## Building blocks
- **Octal text:** `oct(number)` gives `'0o10'`; drop `[2:]`.
"""),
                P("py-count-one-bits", 'Count the 1 Bits', "def ones(number: int) -> int:",
                  """
Write `ones(number)` to return how many 1s there are in the binary form of `number`. Use `bin`.

**Constraints**
- `0 <= number <= 10^16`
""",
                  'def ones(number: int) -> int:\n    return bin(number).count("1")\n',
                  [([11], 3), ([0], 0), ([255], 8)], [[1024], [2 ** 40 - 1]],
                  require=["bin"],
                  grammar="""
## Building blocks
- **Binary text:** `bin(number)`
- **Count the ones:** `.count("1")`
"""),
                P("py-from-base", 'Parse a Number in Any Base', "def from_base(digits: str, base: int) -> int:",
                  """
A data import receives numbers written in bases from 2 to 36. Write `from_base(digits, base)` to return the number as a normal int.

**Constraints**
- `2 <= base <= 36`
- `1 <= len(digits) <= 100`
- `digits` is a valid number in `base`, possibly with a `-` in front
""",
                  "def from_base(digits: str, base: int) -> int:\n    return int(digits, base)\n",
                  [(["ff", 16], 255), (["1010", 2], 10), (["z", 36], 35)], [["0", 8], ["777", 8], ["11111111", 2]],
                  require=["int"],
                  grammar="""
## Building blocks
- **Parse in a base:** `int(digits, base)`
"""),
            ],
            quiz=[
                Q("What does this print?", "0b101 5", "101 5", "0b101 0b101", "5 101", code="print(bin(5), int('101', 2))", predict=True,
                  why="`bin` adds a `0b` prefix; `int(text, 2)` parses binary."),
                Q("What does `hex(10)` return?", "'0xa'", "'a'", "10", "'0x10'", why="Hex digits go 0–9 then a–f."),
            ],
        ),
        # ------------------------------------------------------------------ bit operators
        dict(
            id="bit-ops",
            title="Bit operators",
            builtins=[],
            intro="""
| | | `12` is `1100` |
|---|---|---|
| `a & b` | AND | `12 & 10` → `8` (`1000`) |
| `a \\| b` | OR | `12 \\| 3` → `15` |
| `a ^ b` | XOR | `12 ^ 10` → `6` |
| `~a` | NOT | `~12` → `-13` |
| `a << n` | shift left (× 2ⁿ) | `1 << 3` → `8` |
| `a >> n` | shift right (÷ 2ⁿ) | `12 >> 2` → `3` |

Useful tricks: `(n >> k) & 1` reads bit `k`; `n & (n - 1)` clears the lowest 1 bit.
""",
            problems=[
                P("py-get-bit", 'Read One Bit', "def bit(status: int, position: int) -> int:",
                  """
A device reports its status as a number where each bit is a flag. Write `bit(status, position)` to return bit `position` of `status` (0 or 1), where bit 0 is the rightmost.

**Constraints**
- `0 <= status, position <= 10^16`
""",
                  "def bit(status: int, position: int) -> int:\n    return (status >> position) & 1\n",
                  [([5, 0], 1), ([5, 1], 0), ([5, 2], 1)], [[0, 10], [1024, 10], [255, 7]],
                  require=["op:>>", "op:&"],
                  grammar="""
## Building blocks
- **Move that bit to the end:** `status >> position`
- **Keep only the last bit:** `& 1`
"""),
                P("py-toggle-bit", 'Flip One Bit', "def flip(number: int, position: int) -> int:",
                  """
Write `flip(number, position)` to return `number` with bit `position` flipped, so a 0 becomes 1 and a 1 becomes 0.

**Constraints**
- `0 <= number <= 10^4`
- `0 <= position <= 30`
""",
                  "def flip(number: int, position: int) -> int:\n    return number ^ (1 << position)\n",
                  [([5, 1], 7), ([5, 0], 4), ([0, 3], 8)], [[255, 7], [1, 0]],
                  require=["op:^", "op:<<"],
                  grammar="""
## Building blocks
- **A number with only that bit set:** `1 << position`
- **Flip it:** XOR, `number ^ (1 << position)`
"""),
                P("py-power-of-two", 'Power of Two', "def is_power_of_two(number: int) -> bool:",
                  """
A memory allocator only accepts sizes that are powers of two (1, 2, 4, 8, …). Write `is_power_of_two(number)` using a bit trick.

Zero and negative numbers are never powers of two.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def is_power_of_two(number: int) -> bool:\n    return number > 0 and number & (number - 1) == 0\n",
                  [([8], True), ([6], False), ([1], True)], [[0], [-8], [1024], [1023]],
                  require=["op:&"], forbid=["bin", "while", "for"],
                  hints=["A power of two has exactly one 1 bit. What does `number & (number - 1)` do to the lowest 1 bit?"],
                  grammar="""
## Building blocks
- **Clear the lowest 1 bit:** `number & (number - 1)`. For a power of two, that leaves 0.
- **Exclude 0 and negatives:** `number > 0 and …`
"""),
            ],
            quiz=[
                Q("What does this print?", "8 14 6", "8 14 14", "14 8 6", "6 14 8", code="print(12 & 10, 12 | 10, 12 ^ 10)", predict=True,
                  why="1100 & 1010 = 1000; | = 1110; ^ = 0110."),
                Q("What does this print?", "-6", "4", "6", "-5", code="print(~5)", predict=True, why="`~x` equals `-x - 1`."),
            ],
        ),
        # ------------------------------------------------------------------ complex
        dict(
            id="complex-numbers",
            title="Complex numbers",
            builtins=["complex"],
            intro="""
Python has complex numbers built in: `z = 3 + 4j` or `complex(3, 4)`.

- `z.real` → `3.0`, `z.imag` → `4.0`
- `abs(z)` → `5.0` (the distance from 0)
- They add and multiply like normal numbers.

They're handy for 2-D geometry: a point `(x, y)` is `complex(x, y)`, and multiplying by `1j` rotates it 90°.
""",
            problems=[
                P("py-complex-length", 'Distance from the Origin', "def length(x: int, y: int) -> float:",
                  """
Write `length(x, y)` to return the distance from `(0, 0)` to `(x, y)`, using a complex number.

**Constraints**
- `-10^16 <= x, y <= 10^16`
""",
                  "def length(x: int, y: int) -> float:\n    return abs(complex(x, y))\n",
                  [([3, 4], 5.0), ([0, 0], 0.0)], [[-5, 12], [1, 1]],
                  require=["complex"],
                  grammar="""
## Building blocks
- **Make a complex number:** `complex(x, y)`
- **Its size:** `abs(z)`
"""),
                P("py-rotate-point", 'Rotate a Point 90°', "def rotate(x: int, y: int) -> List[int]:",
                  """
A game rotates sprites a quarter turn anticlockwise around the origin. Write `rotate(x, y)` to return the rotated point as `[new_x, new_y]` ints. Multiplying a complex number by `1j` does exactly this rotation.

**Constraints**
- `-10^16 <= x, y <= 10^16`
""",
                  "def rotate(x: int, y: int) -> List[int]:\n    z = complex(x, y) * 1j\n    return [int(z.real), int(z.imag)]\n",
                  [([1, 0], [0, 1]), ([0, 1], [-1, 0]), ([2, 3], [-3, 2])], [[0, 0], [-4, -5]],
                  require=["complex"],
                  grammar="""
## Building blocks
- **Rotate:** `complex(x, y) * 1j`
- **Back to ints:** `int(z.real)`, `int(z.imag)`
"""),
            ],
            quiz=[
                Q("What does this print?", "(-1+0j)", "1", "-1", "error", code="print(1j * 1j)", predict=True, why="j² = −1."),
            ],
        ),
        # ------------------------------------------------------------------ bytes
        dict(
            id="bytes",
            title="bytes, bytearray and memoryview",
            builtins=["bytes", "bytearray", "memoryview"],
            intro="""
Text is made of characters; **bytes** are raw numbers from 0 to 255 (what files and networks really carry).

- `"hi".encode()` → `b'hi'`; `b'hi'.decode()` → `'hi'`
- `bytes([104, 105])` → `b'hi'`; `list(b'hi')` → `[104, 105]`
- `bytes` can't change; `bytearray` can: `b = bytearray(b"hi"); b[0] = 72`.
- `memoryview(data)` looks at bytes **without copying** them. Slicing a memoryview is free, which matters for big binary data.
""",
            problems=[
                P("py-utf8-bytes", 'Encode Text as Bytes', "def to_bytes(text: str) -> List[int]:",
                  """
A network client sends text as UTF-8 bytes. Write `to_bytes(text)` to return the UTF-8 bytes of `text` as a list of numbers.

**Constraints**
- `0 <= len(text) <= 10^4`
- `text` can contain any characters, including emoji
""",
                  'def to_bytes(text: str) -> List[int]:\n    return list(text.encode("utf-8"))\n',
                  [(["hi"], [104, 105]), (["é"], [195, 169]), ([""], [])], [["A1 "], ["€"]],
                  require=[".encode"],
                  grammar="""
## Building blocks
- **Text to bytes:** `text.encode("utf-8")` (UTF-8 is the default).
- **Bytes to numbers:** `list(...)`
"""),
                P("py-bytes-to-text", 'Decode Bytes as Text', "def to_text(nums: List[int]) -> str:",
                  """
A network client receives raw byte values. Write `to_text(nums)` to turn them back into text using UTF-8.

**Constraints**
- `0 <= len(nums) <= 10^4`
- `0 <= nums[i] <= 255`
- `nums` is valid UTF-8
""",
                  "def to_text(nums: List[int]) -> str:\n    return bytes(nums).decode()\n",
                  [([[104, 105]], "hi"), ([[195, 169]], "é"), ([[]], "")], [[[80, 121, 116, 104, 111, 110]]],
                  require=["bytes", ".decode"],
                  grammar="""
## Building blocks
- **Numbers to bytes:** `bytes(nums)`
- **Bytes to text:** `.decode()`
"""),
                P("py-patch-byte", 'Patch One Byte', "def patch(nums: List[int], index: int, value: int) -> List[int]:",
                  """
A file repair tool fixes a single corrupted byte. Write `patch(nums, index, value)` to build a `bytearray` from `nums`, set position `index` to `value`, and return the result as a list.

**Constraints**
- `1 <= len(nums) <= 10^4`
- `0 <= nums[index] <= 255`
- `0 <= index < len(nums)`
- `0 <= value <= 255`
""",
                  "def patch(nums: List[int], index: int, value: int) -> List[int]:\n    data = bytearray(nums)\n    data[index] = value\n    return list(data)\n",
                  [([[1, 2, 3], 0, 9], [9, 2, 3]), ([[0], 0, 255], [255])], [[[5, 5], 1, 0]],
                  require=["bytearray"],
                  grammar="""
## Building blocks
- **Changeable bytes:** `bytearray(nums)`
- **Edit in place:** `buf[k] = amount` (0–255 only).
"""),
                P("py-view-slice", 'Read Part of a Buffer Without Copying', "def window(nums: List[int], start: int, stop: int) -> List[int]:",
                  """
Large binary buffers are expensive to copy. Write `window(nums, start, stop)` to make `bytes` from `nums`, read positions `start` to `stop` through a `memoryview`, and return them as a list.

**Constraints**
- `1 <= len(nums) <= 10^4`
- `0 <= nums[i] <= 255`
- `0 <= start, stop <= 10^4`
""",
                  "def window(nums: List[int], start: int, stop: int) -> List[int]:\n    view = memoryview(bytes(nums))\n    return view[start:stop].tolist()\n",
                  [([[10, 20, 30, 40], 1, 3], [20, 30]), ([[1], 0, 0], [])], [[list(range(100)), 50, 55]],
                  require=["memoryview"],
                  grammar="""
## Building blocks
- **A view of the bytes:** `memoryview(bytes(nums))`
- **Slice it (no copy):** `view[start:stop]`
- **As a list:** `.tolist()`
"""),
            ],
            quiz=[
                Q("What does this print?", "2 1", "1 1", "1 2", "2 2", code="print(len('é'.encode()), len('é'))", predict=True,
                  why="One character, but two bytes in UTF-8."),
                Q("What happens?", "TypeError: bytes can't be changed", "b becomes b'Hi'", "Nothing", "IndexError", code="b = b'hi'\nb[0] = 72",
                  why="Use `bytearray` when you need to change bytes."),
            ],
        ),
        # ------------------------------------------------------------------ types
        dict(
            id="types",
            title="type, isinstance and issubclass",
            builtins=["type", "isinstance", "issubclass"],
            intro="""
- `type(x)` gives the exact type: `type(3)` is `int`; `type(3).__name__` is `'int'`.
- `isinstance(x, int)` is the usual check. It also accepts subclasses, and a tuple of types: `isinstance(x, (int, float))`.
- Watch out: `bool` is a subclass of `int`, so `isinstance(True, int)` is `True`.
- `issubclass(ValueError, Exception)` asks about classes rather than values.
""",
            problems=[
                P("py-type-name", "Name a Value's Type", "def type_name(value) -> str:",
                  """
A logging helper records the type of each value it sees. Write `type_name(value)` to return the name of `value`'s type, as Python spells it (`None` has the type `NoneType`).

**Constraints**
- `value` can be a value of any type
""",
                  "def type_name(value) -> str:\n    return type(value).__name__\n",
                  [([3], "int"), (["a"], "str"), ([None], "NoneType")], [[1.5], [[1, 2]], [{"a": 1}], [True]],
                  require=["type"],
                  grammar="""
## Building blocks
- **The type:** `type(value)`
- **Its name:** `.__name__`
"""),
                P("py-count-real-ints", 'Count the Integers', "def count_ints(items: list) -> int:",
                  """
A data validator counts the whole numbers in a mixed list. In Python, `True` and `False` are technically ints, but they shouldn't count. Write `count_ints(items)`.

**Constraints**
- `0 <= len(items) <= 10^4`
- Items can be values of any type
""",
                  "def count_ints(items: list) -> int:\n    return sum(1 for x in items if isinstance(x, int) and not isinstance(x, bool))\n",
                  [([[1, "2", 3.0, True, 4]], 2), ([[]], 0)], [[[False, 0]], [[None, [], {}]]],
                  require=["isinstance"],
                  grammar="""
## Building blocks
- **Type check:** `isinstance(x, int)`
- **Exclude bools:** `and not isinstance(x, bool)`
"""),
                P("py-exception-family", "Check an Exception's Family", "def is_kind_of(child, parent) -> bool:",
                  """
An error handler decides how to react based on the kind of exception. Write `is_kind_of(child, parent)` to return `True` if the class `child` is `parent` or a subclass of it.

The tests show each class by its name, but your function receives the class itself.

**Constraints**
- `child` and `parent` are built-in exception classes
""",
                  "def is_kind_of(child, parent) -> bool:\n    return issubclass(child, parent)\n",
                  [(["KeyError", "LookupError"], True), (["ValueError", "TypeError"], False)], [["ZeroDivisionError", "ArithmeticError"], ["Exception", "Exception"], ["Exception", "ValueError"]],
                  require=["issubclass"],
                  driver='import builtins\n\ndef driver(ns, child, parent):\n    return resolve(ns, "is_kind_of")(getattr(builtins, child), getattr(builtins, parent))\n',
                  grammar="""
## Building blocks
- **Class relationships:** `issubclass(child, parent)`. Every class counts as a subclass of itself.
"""),
            ],
            quiz=[
                Q("What does this print?", "True False", "False False", "True True", "False True", code="print(isinstance(True, int), type(True) is int)", predict=True,
                  why="`bool` subclasses `int`; `isinstance` accepts subclasses but `type(...) is` doesn't."),
                Q("What does this print?", "True", "False", code="print(isinstance(2.5, (int, float)))", predict=True, why="A tuple of types means \"any of these\"."),
            ],
        ),
        # ------------------------------------------------------------------ exceptions
        dict(
            id="exceptions",
            title="Errors: try, except, raise",
            builtins=[],
            intro="""
```python
try:
    n = int(text)
except ValueError:
    n = 0            # runs only if int() failed
else:
    ...              # runs only if nothing failed
finally:
    ...              # always runs
```

- Catch the **specific** error you expect (`ValueError`, `KeyError`, `ZeroDivisionError`…), not everything.
- `raise ValueError("age can't be negative")` signals a problem to the caller.
- Your own error type: `class OutOfStock(Exception): pass`.

In tasks marked **raises**, the tests check that you raise the right error for bad input.
""",
            problems=[
                P("py-safe-int", 'Parse an Int Safely', "def parse(text: str) -> Optional[int]:",
                  """
A form field should hold a whole number, but users type anything. Write `parse(text)` to return the text as an int, or `None` if it isn't a valid whole number.

**Constraints**
- `0 <= len(text) <= 100`
- `text` can contain any characters
""",
                  "def parse(text: str) -> Optional[int]:\n    try:\n        return int(text)\n    except ValueError:\n        return None\n",
                  [(["42"], 42), (["4.2"], None), (["abc"], None)], [[" 7 "], ["-0"], [""]],
                  require=["try"],
                  grammar="""
## Building blocks
- **Try the risky part:** `try: return int(text)`
- **Catch the specific failure:** `except ValueError: return None`
"""),
                P("py-safe-divide", 'Divide Safely', "def safe_divide(total: int, count: int) -> Optional[float]:",
                  """
A stats page divides totals by counts, and some counts are zero. Write `safe_divide(total, count)` to return `total / count`, or `None` when `count` is 0. Use `try`/`except`, not an `if`.

**Constraints**
- `-10^16 <= total, count <= 10^16`
""",
                  "def safe_divide(total: int, count: int) -> Optional[float]:\n    try:\n        return total / count\n    except ZeroDivisionError:\n        return None\n",
                  [([6, 3], 2.0), ([1, 0], None)], [[0, 0], [-9, 2]],
                  require=["try"], forbid=["if", "ternary"],
                  grammar="""
## Building blocks
- **The error for dividing by zero:** `ZeroDivisionError`
"""),
                P("py-check-age", 'Validate an Age', "def check_age(age: int) -> int:",
                  """
A sign-up form rejects impossible ages. Write `check_age(age)` to return `age` unchanged if it's from 0 to 150, and to raise a `ValueError` otherwise.

**Constraints**
- `-10^16 <= age <= 10^16`
""",
                  'def check_age(age: int) -> int:\n    if not 0 <= age <= 150:\n        raise ValueError(f"invalid age: {age}")\n    return age\n',
                  [([30], 30), ([-1], {"raises": "ValueError"}), ([200], {"raises": "ValueError"})], [[0], [150], [151], [-100]],
                  raises=True, require=["raise"],
                  grammar="""
## Building blocks
- **Signal bad input:** `raise ValueError("message")`
- **Otherwise return normally.**
"""),
                P("py-custom-exception", 'A Custom Exception', "def withdraw(balance: int, amount: int) -> int:",
                  """
A banking module needs its own error for overdrafts. Define an exception class `InsufficientFunds` that subclasses `Exception`, then write `withdraw(balance, amount)` to return the new balance, or raise `InsufficientFunds` when `amount` is more than `balance`.

**Constraints**
- `0 <= balance, amount <= 10^16`
""",
                  "class InsufficientFunds(Exception):\n    pass\n\n\ndef withdraw(balance: int, amount: int) -> int:\n    if amount > balance:\n        raise InsufficientFunds(f\"need {amount - balance} more\")\n    return balance - amount\n",
                  [([100, 30], 70), ([10, 50], {"raises": "InsufficientFunds"})], [[5, 5], [0, 1]],
                  raises=True, require=["class", "raise"],
                  grammar="""
## Building blocks
- **A new exception type:** `class InsufficientFunds(Exception): pass`
- **Raise it:** `raise InsufficientFunds("message")`
"""),
                P("py-finally-log", 'Always Write the Last Log Line', "def run_steps(steps: List[str]) -> List[str]:",
                  """
A batch job runs numbered steps written as text. Write `run_steps(steps)` to return a log with `"ok N"` for each valid step, stopping at the first invalid one with `"bad X"`. Whatever happens, the log must end with `"done"`, so use `finally` for that line.

**Constraints**
- `0 <= len(steps) <= 10^4`
""",
                  'def run_steps(steps: List[str]) -> List[str]:\n    log = []\n    try:\n        for s in steps:\n            try:\n                log.append(f"ok {int(s)}")\n            except ValueError:\n                log.append(f"bad {s}")\n                break\n    finally:\n        log.append("done")\n    return log\n',
                  [([["1", "x", "3"]], ["ok 1", "bad x", "done"]), ([[]], ["done"])], [[["5", "6"]], [["?"]]],
                  difficulty="Medium", require=["try"],
                  grammar="""
## Building blocks
- **Always runs:** `finally:` after a `try`, even after `break` or `return`.
- **Nested try:** an inner `try`/`except ValueError` handles each step.
"""),
            ],
            quiz=[
                Q("What does this print?", "a c d", "a b d", "a b c d", "a d", code="try:\n    print('a', end=' ')\nexcept ValueError:\n    print('b', end=' ')\nelse:\n    print('c', end=' ')\nfinally:\n    print('d')", predict=True,
                  why="No error, so `except` is skipped and `else` runs; `finally` always runs."),
                Q("Why is `except:` (catching everything) usually a bad idea?", "It hides bugs you didn't expect, even typos", "It's slower", "It's a SyntaxError", "It only catches ValueError",
                  why="Catch the specific errors you can handle."),
            ],
        ),
        # ------------------------------------------------------------------ control flow extras
        dict(
            id="control-extras",
            title="for…else, one-line if, walrus and match",
            builtins=[],
            intro="""
- **for…else**: the `else` block runs only if the loop finished **without** `break`.
- **Conditional expression**: `x if condition else y`.
- **Walrus** `:=` assigns inside an expression: `if (n := len(items)) > 10: …`
- **match** (Python 3.10+) compares a value against patterns:

```python
match status:
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case n if 500 <= n < 600:
        return "Server Error"
    case _:
        return "Unknown"
```
""",
            problems=[
                P("py-for-else-prime", 'Prime Check with for…else', "def is_prime(number: int) -> bool:",
                  """
Write `is_prime(number)` to return `True` if `number` is prime. Use a `for` loop that `break`s when it finds a divisor, with an `else` block for the case where it finds none.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def is_prime(number: int) -> bool:\n    if number < 2:\n        return False\n    for d in range(2, int(number ** 0.5) + 1):\n        if number % d == 0:\n            break\n    else:\n        return True\n    return False\n",
                  [([7], True), ([9], False), ([1], False)], [[2], [97], [100], [7919]],
                  grammar="""
## Building blocks
- **Try divisors up to the square root:** `for lookup in range(2, int(num ** 0.5) + 1):`
- **Found one:** `break`
- **Loop finished without break:** an `else:` lined up with the `for`.
"""),
                P("py-ternary-abs", 'Absolute Value in One Line', "def absolute(number: int) -> int:",
                  """
Write `absolute(number)` to return the absolute value of `number` with a single conditional expression. Don't use `abs` or an `if` statement.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
                  "def absolute(number: int) -> int:\n    return -number if number < 0 else number\n",
                  [([-5], 5), ([3], 3), ([0], 0)], [[-1000]],
                  require=["ternary"], forbid=["abs", "if"],
                  grammar="""
## Building blocks
- **Conditional expression:** `"neg" if x < 0 else "pos"`
"""),
                P("py-walrus-positive", 'Keep the Positive Results', "def positive_results(nums: List[int]) -> List[int]:",
                  """
A data pipeline computes `n * n - 10` for each input and keeps only the positive results. Write `positive_results(nums)` so each result is computed only once, using the walrus operator inside a comprehension.

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
""",
                  "def positive_results(nums: List[int]) -> List[int]:\n    return [r for n in nums if (r := n * n - 10) > 0]\n",
                  [([[1, 4, -5]], [6, 15]), ([[3]], [])], [[[]], [[10, 0]]],
                  require=["walrus"], difficulty="Medium",
                  grammar="""
## Building blocks
- **Assign inside a condition:** `(y := x + 1) > 5` stores `x + 1` in `y` and compares it.
- **Then use it:** the stored name can be the comprehension's output expression.
"""),
                P("py-http-status", 'Describe an HTTP Status', "def status_text(code: int) -> str:",
                  """
A monitoring dashboard shows a short label for each HTTP status code. Write `status_text(code)` to return `"OK"` for 200, `"Not Found"` for 404, `"Server Error"` for anything from 500 to 599, and `"Unknown"` otherwise. Use `match`.

**Constraints**
- `-10^16 <= code <= 10^16`
""",
                  'def status_text(code: int) -> str:\n    match code:\n        case 200:\n            return "OK"\n        case 404:\n            return "Not Found"\n        case n if 500 <= n < 600:\n            return "Server Error"\n        case _:\n            return "Unknown"\n',
                  [([200], "OK"), ([404], "Not Found"), ([503], "Server Error"), ([418], "Unknown")], [[500], [599], [600], [0]],
                  require=["match"],
                  grammar="""
## Building blocks
- **Match a value:** `match src:` then `case 200:` …
- **A guard:** `case n if 500 <= n < 600:`
- **Everything else:** `case _:`
"""),
            ],
            quiz=[
                Q("What does this print?", "no", "found", "found\nno", "nothing", code="for x in [1, 3, 5]:\n    if x % 2 == 0:\n        print('found')\n        break\nelse:\n    print('no')", predict=True,
                  why="No `break` happened, so the loop's `else` ran."),
                Q("What does this print?", "small", "big", "error", "None", code="n = 3\nprint('big' if n > 5 else 'small')", predict=True, why="A conditional expression picks one of two values."),
            ],
        ),
        # ------------------------------------------------------------------ eval / exec / compile
        dict(
            id="dynamic-code",
            title="eval, exec and compile",
            builtins=["eval", "exec", "compile"],
            intro="""
Python can run code that's stored as text:

- `eval("2 + 3")` → `5` (one **expression**, returns its value).
- `exec("x = 5", env)` runs **statements**; any variables land in the dict `env`.
- `compile(text, "<name>", "eval")` turns text into a code object once, so you can run it many times quickly.

⚠️ Never `eval` or `exec` text from someone you don't trust: it can do anything your program can. In real code, prefer `int()`, `json.loads()` or `ast.literal_eval()`.
""",
            problems=[
                P("py-calculator", 'Evaluate a Sum Written as Text', "def calculate(expression: str) -> float:",
                  """
A calculator widget receives arithmetic as text. Write `calculate(expression)` to return its value, using `eval`.

**Constraints**
- `1 <= len(expression) <= 10^4`
- `expression` is valid arithmetic using whole numbers, `+`, `-`, `*`, `/`, `%`, `**` and brackets
""",
                  "def calculate(expression: str) -> float:\n    return eval(expression)\n",
                  [(["2 + 3 * 4"], 14), (["(1 + 1) ** 10"], 1024), (["7 / 2"], 3.5)], [["0"], ["-3 * -3"], ["10 // 3 + 10 % 3"]],
                  require=["eval"],
                  grammar="""
## Building blocks
- **Evaluate an expression:** `eval(expression)`
"""),
                P("py-run-snippet", 'Run a Snippet', "def run(code: str) -> int:",
                  """
A teaching tool runs small Python snippets that set a variable called `result`. Write `run(code)` to run the snippet with `exec` in a fresh dict and return `result`.

**Constraints**
- `1 <= len(code) <= 1000`
- `code` is valid Python that sets `result`
""",
                  "def run(code: str) -> int:\n    env = {}\n    exec(code, env)\n    return env[\"result\"]\n",
                  [(["result = 6 * 7"], 42), (["a = 2\nb = 3\nresult = a ** b"], 8)], [["result = sum(range(5))"], ["result = 0\nfor i in range(4):\n    result += i"]],
                  require=["exec"],
                  grammar="""
## Building blocks
- **A dict to hold the variables:** `namespace = {}`
- **Run statements into it:** `exec(text, space)`
- **Read the result:** `env["result"]`
"""),
                P("py-evaluate-many", 'Evaluate a Formula for Many Values', "def table(formula: str, values: List[int]) -> List[int]:",
                  """
A plotting tool evaluates a formula in `x` for a whole column of values. Write `table(formula, values)` to compile the formula once with `compile`, then `eval` the compiled code with `{"x": value}` for each value.

**Constraints**
- `formula` is a valid arithmetic formula in `x`
- `0 <= len(values) <= 10^4`
- `-10^16 <= values[i] <= 10^16`
""",
                  'def table(formula: str, values: List[int]) -> List[int]:\n    code = compile(formula, "<expr>", "eval")\n    return [eval(code, {"x": x}) for x in values]\n',
                  [(["x * x + 1", [0, 1, 2]], [1, 2, 5]), (["2 ** x", []], [])], [["x % 3", list(range(7))], ["-x", [5, -5]]],
                  require=["compile", "eval"], difficulty="Medium",
                  grammar="""
## Building blocks
- **Compile once:** `compile(formula, "<expr>", "eval")`
- **Run with a variable:** `eval(code, {"x": value})`
"""),
            ],
            quiz=[
                Q("What does this print?", "5 None", "5 5", "None 5", "error", code="print(eval('2 + 3'), exec('2 + 3'))", predict=True,
                  why="`eval` returns the expression's value; `exec` runs statements and always returns `None`."),
                Q("Why is `eval(input())` dangerous?", "The user can type any Python code, which then runs", "It's slow", "It only works with numbers", "It isn't; it's the recommended way to read numbers",
                  why="Use `int(input())` or `ast.literal_eval` for data."),
            ],
        ),
        # ------------------------------------------------------------------ interpreter helpers (quiz only)
        dict(
            id="interpreter-helpers",
            title="Interpreter helpers: id, globals, help, …",
            builtins=[],
            quiz_only=["id", "globals", "locals", "help", "breakpoint", "exit", "quit", "copyright", "credits", "license"],
            intro="""
These built-ins are for exploring and debugging, not for computing answers, so there are no coding tasks for them:

- `id(x)`: a number identifying the object. `a is b` is the same as `id(a) == id(b)`.
- `globals()` / `locals()`: dicts of the variables visible at module level / inside the current function.
- `help(x)`: shows documentation in an interactive session.
- `breakpoint()`: pauses the program in the debugger (`pdb`), where you can inspect variables.
- `exit()` / `quit()`: leave the interactive interpreter.
- `copyright`, `credits`, `license`: show Python's legal and credit text.
""",
            quiz=[
                Q("What does this print?", "True True False", "True False False", "False True False", "True True True",
                  code="a = [1]\nb = a\nc = [1]\nprint(a is b, id(a) == id(b), a is c)", predict=True,
                  why="`b` is the same object as `a`; `c` is a different list with equal contents."),
                Q("What does this print?", "True", "False", code="x = 5\nprint('x' in globals())", predict=True, why="Module-level variables live in `globals()`."),
                Q("What does this print?", "['a', 'b']", "{'a': 1, 'b': 2}", "[]", "error", code="def f(a):\n    b = 2\n    return list(locals())\nprint(f(1))", predict=True,
                  why="Inside a function, `locals()` holds its parameters and local variables."),
                Q("What does `breakpoint()` do?", "Pauses the program in the debugger", "Stops the program for good", "Prints the stack", "Nothing outside an IDE",
                  why="It drops you into `pdb`, where you can inspect and step through code."),
                Q("Where is `help(str.split)` useful?", "In an interactive Python session, to read documentation", "Inside a function, to speed it up", "To fix errors automatically", "Only in Jupyter",
                  why="It prints the docstring and signature."),
                Q("What do `exit()` and `quit()` do?", "Leave the interactive interpreter (they raise SystemExit)", "Return from the current function", "Clear the screen", "Restart Python",
                  why="In scripts, prefer `sys.exit()`."),
                Q("What do `copyright`, `credits` and `license` show?", "Python's legal and credit information", "Your program's licence", "Installed packages", "Nothing; they're keywords",
                  why="They're site helpers you can type in an interactive session."),
            ],
        ),
    ],
)
