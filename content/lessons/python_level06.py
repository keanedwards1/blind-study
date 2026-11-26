# Beginner lessons for Learn Python level 6 (Numbers, types & control). See python_level01.py for the style.

LESSONS = {
    "number-tools": r"""
**Overview:** a few number tools save you work and avoid surprises with division and decimals.

### divmod: whole part and remainder together
```python
divmod(125, 60)    # (2, 5)   125 seconds is 2 minutes and 5 seconds
```
It gives the same two answers as `125 // 60` and `125 % 60`, in one go.

### pow: powers, and powers with a remainder
`pow(2, 10)` is `2 ** 10`, which is `1024`. With a third number, `pow(base, exp, m)` gives the remainder after dividing by `m`, and it stays fast even when the power is enormous (*modular exponentiation*).

### Division rounds down
`//` always rounds **down**, towards minus infinity: `-7 // 2` is `-4`. To round towards zero instead, as many other languages do, use `int(-7 / 2)`, which is `-3`.

### Decimals are approximate
Computers store decimal numbers (*floats*) with tiny rounding errors:

```python
0.1 + 0.2              # 0.30000000000000004
0.1 + 0.2 == 0.3       # False
math.isclose(0.1 + 0.2, 0.3)   # True: "equal apart from tiny errors"
```

`float("inf")` is a number bigger than every other number: a handy starting value when you're searching for a minimum.

### Common mistakes
- Comparing floats with `==`. Use `math.isclose`.
""",
    "bases": r"""
**Overview:** the same number can be written in binary, octal or hexadecimal, and Python converts between them.

### The idea
We normally count in tens (*base 10*). Computers also use base 2 (*binary*: digits 0-1), base 8 (*octal*: 0-7) and base 16 (*hexadecimal*: 0-9 then a-f).

```python
bin(10)          # '0b1010'   binary
oct(10)          # '0o12'     octal
hex(255)         # '0xff'     hexadecimal
bin(10)[2:]      # '1010'     slice off the 2-character prefix
format(255, "x") # 'ff'       or ask format() for no prefix ("b", "o", "x")
```

Going the other way, give `int` the base as a second input:

```python
int("1010", 2)   # 10
int("ff", 16)    # 255
```

### When you'd use it
Colour codes (`#ff8000`), counting the 1s in a number's binary form, and reading data written in other bases.

### Common mistakes
- Forgetting the prefix. `bin`, `oct` and `hex` always add `0b`, `0o` or `0x`.
""",
    "bit-ops": r"""
**Overview:** bit operators work on the individual 1s and 0s of a number.

### The idea
Every whole number is stored as a row of binary digits (*bits*). 12 is `1100`; 10 is `1010`. These operators combine numbers bit by bit:

| Write | Name | Keeps a 1 where… | `12 ? 10` |
|---|---|---|---|
| `a & b` | AND | **both** have a 1 | `8` (`1000`) |
| `a \| b` | OR | **either** has a 1 | `14` (`1110`) |
| `a ^ b` | XOR | **exactly one** has a 1 | `6` (`0110`) |

Shifting slides the bits along:

```python
1 << 3      # 8    1 becomes 1000: multiply by 2 three times
12 >> 2     # 3    1100 becomes 11: divide by 2 twice
```

### Handy tricks
- `(n >> k) & 1` reads bit number `k` (bit 0 is the rightmost).
- `n & 1` is 1 for odd numbers and 0 for even ones.
- `n & (n - 1)` removes the lowest 1 bit; it's 0 only for powers of two.

### Common mistakes
- Brackets with `+`: maths happens **before** `&`, so `a + b & 1` means `(a + b) & 1`. Wrap the `&` part in brackets when you add to it: `a + (b & 1)`. (Comparisons like `==` happen *after* `&`, so `n & 1 == 1` already works.)
- `~12` is `-13`, not `3`: Python's NOT flips the sign as well.
""",
    "complex-numbers": r"""
**Overview:** complex numbers store two numbers in one, which makes them handy for points on a map.

### The idea
A complex number has a normal part and a second part marked with `j` (the *real* and *imaginary* parts):

```python
z = 3 + 4j          # or complex(3, 4)
z.real              # 3.0
z.imag              # 4.0
abs(z)              # 5.0   its distance from 0
```

They add and multiply like normal numbers.

### Points and turns
Treat the point `(x, y)` as `complex(x, y)`:

- Adding two of them moves a point: `(1 + 2j) + (3 + 0j)` is `(4 + 2j)`.
- `abs(...)` gives the straight-line distance from the origin.
- Multiplying by `1j` turns the point 90° anticlockwise around the origin.

### Common mistakes
- Writing `i` like in maths class. Python uses `j`, and needs a number in front: `1j`, not `j`.
""",
    "bytes": r"""
**Overview:** bytes are the raw numbers (0 to 255) that files and networks actually carry, and text has to be converted into them.

### The idea
```python
"hi".encode()            # b'hi'          text → bytes (encoding)
b"hi".decode()           # 'hi'           bytes → text (decoding)
list(b"hi")              # [104, 105]     the numbers inside
bytes([104, 105])        # b'hi'
len("é".encode())        # 2              some characters take more than one byte
```

The usual way to turn text into bytes is called *UTF-8*. Plain English letters take one byte each; accented letters and emoji take more.

### Changing bytes
`bytes` can't be changed. `bytearray` is the changeable version:

```python
data = bytearray(b"hi")
data[0] = 72             # 72 is 'H'
bytes(data)              # b'Hi'
```

`memoryview(data)` lets you look at part of some bytes **without copying them**, which matters when the data is huge.

### Common mistakes
- Counting characters when you need bytes: `len("é")` is 1, but it takes 2 bytes.
""",
    "types": r"""
**Overview:** you can ask Python what kind of value something is.

### The idea
Every value has a kind (its *type*): `3` is an `int`, `"hi"` is a `str`, `[1]` is a `list`.

```python
type(3)                    # <class 'int'>
type(3).__name__           # 'int'
isinstance(3, int)         # True
isinstance(3.5, (int, float))   # True   either type is fine
```

`isinstance` is the usual check. It also says yes for related, more specific kinds (*subclasses*).

### A surprise: True is a number
In Python, `True` and `False` are a special kind of whole number (`bool` is a subclass of `int`), so `isinstance(True, int)` is `True`. If you only want real numbers, exclude bools: `isinstance(x, int) and not isinstance(x, bool)`.

### Asking about kinds themselves
`issubclass(KeyError, LookupError)` asks whether one kind is a more specific version of another. Errors form a family tree like this.
""",
    "exceptions": r"""
**Overview:** when something goes wrong, Python raises an error, and `try`/`except` lets you catch it and carry on.

### The idea
```python
try:
    n = int(text)          # this might fail
except ValueError:
    n = 0                  # runs only if int() failed
finally:
    print("done")          # always runs, either way
```

Errors have names that say what went wrong (each is an *exception*): `ValueError` (bad value), `KeyError` (missing dict key), `IndexError` (position past the end), `ZeroDivisionError`.

### Raising your own
`raise` signals a problem to whoever called your function:

```python
if age < 0:
    raise ValueError("age can't be negative")
```

You can even invent your own error type: `class OutOfStock(Exception): pass`.

Tasks marked **raises** check that you raise the right error for bad input.

### Common mistakes
- Catching everything with a bare `except:`. It hides real bugs. Catch the specific error you expect.
""",
    "control-extras": r"""
**Overview:** four extra shapes for decisions and loops that make some code shorter.

### One-line if/else
```python
label = "even" if n % 2 == 0 else "odd"
```
Reads as "this **if** the condition is true, **else** that" (a *conditional expression*).

### for … else
A loop can have an `else` block that runs only when the loop finished **without** hitting `break`. It's perfect for "searched everything, found nothing":

```python
for d in range(2, n):
    if n % d == 0:
        break          # found a divisor
else:
    print("prime")     # no break happened
```

### The walrus :=
`:=` stores a value **and** uses it in the same breath (the *walrus operator*, because `:=` looks like a walrus):

```python
[y for x in nums if (y := x * x) > 10]
```

### match
`match` compares a value against several shapes, top to bottom (*pattern matching*):

```python
match code:
    case 200:
        return "OK"
    case n if 500 <= n < 600:
        return "Server Error"
    case _:
        return "Unknown"     # _ matches anything
```
""",
    "dynamic-code": r"""
**Overview:** Python can run code that's stored as text.

### The idea
```python
eval("2 + 3 * 4")          # 14    works out one expression and gives its value
env = {}
exec("x = 5", env)         # runs statements; new variables land in env
env["x"]                   # 5
code = compile("x * 2", "<expr>", "eval")   # prepare once…
eval(code, {"x": 21})      # 42    …run many times
```

- `eval` handles a single *expression* (something with a value).
- `exec` handles *statements* (whole lines, like assignments and loops).
- `compile` turns text into ready-to-run code, so repeating it is faster.

### Common mistakes
- **Running text you don't trust.** `eval` and `exec` can do anything your program can, including deleting files. In real programs, use safer tools: `int()` for numbers, `json.loads()` for data, or `ast.literal_eval()` for simple Python values.
""",
    "interpreter-helpers": r"""
**Overview:** these built-ins help you explore and debug Python, rather than compute answers, so they appear only in quiz questions.

### The idea
- `id(x)`: a number identifying one particular object. `a is b` means the two names point at the very same object, the same as `id(a) == id(b)`.
- `globals()` and `locals()`: dicts of the variable names you can see, at the top of the file and inside the current function.
- `help(x)`: shows the documentation for something, in an interactive session.
- `breakpoint()`: pauses your program in the debugger (a tool for stepping through code line by line, called `pdb`) so you can inspect variables.
- `exit()` and `quit()`: leave the interactive Python prompt.
- `copyright`, `credits` and `license`: show Python's legal and thank-you text.

### When you'd use it
While you're working something out: checking whether two names share an object, peeking at variables, or reading documentation.
""",
}
