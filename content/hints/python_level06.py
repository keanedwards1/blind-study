# Hints for Learn Python level 6 (Numbers, types & control), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ number tools
    "py-minutes-seconds": [
        "Minutes = how many whole 60s fit into the seconds; seconds = what's left over.",
        "`divmod(a, b)` returns both at once, as `(a // b, a % b)`, and you can unpack them into two names.",
        "The seconds always need two digits (`5` → `05`): in an f-string, the format `02d` pads a whole number to width 2 with zeros.",
    ],
    "py-mod-pow": [
        "Calculating the giant power first would take far too long, because the number has billions of digits.",
        "The built-in `pow` accepts a third argument, a modulus, and then it keeps the number small at every step.",
        "Pass base, exponent and modulus to `pow` and return the result.",
    ],
    "py-toward-zero": [
        "Python's `//` rounds *down*, so `-7 // 2` is `-4`. You need `-3`: rounding towards zero.",
        "Divide the sizes instead: the absolute values (`abs`) with `//` always give the right number of whole parts.",
        "Then fix the sign: the answer is negative only when exactly one of `dividend` and `divisor` is negative.",
    ],
    "py-close-enough": [
        "Floats can be slightly off: `0.1 + 0.2 == 0.3` is `False`, because of tiny rounding errors.",
        "`math.isclose(first, second)` treats two floats as equal when they're within a tiny tolerance.",
        "Return its result. The `math` module is already available.",
    ],
    # ------------------------------------------------------------------ bases
    "py-to-hex": [
        "Hexadecimal is base 16, using digits 0-9 and letters a-f.",
        "`hex(number)` returns text like `\"0xff\"`, with a two-character `0x` prefix.",
        "Slice off the first two characters.",
    ],
    "py-to-octal": [
        "Octal is base 8.",
        "`oct(number)` returns text like `\"0o10\"`, with a two-character `0o` prefix.",
        "Slice off the first two characters.",
    ],
    "py-count-one-bits": [
        "`bin(number)` gives the binary form as text, like `\"0b101\"`.",
        "The prefix `0b` contains no `1`, so it doesn't affect counting 1s.",
        "Count the `\"1\"` characters in that text with `.count`.",
    ],
    "py-from-base": [
        "`int(...)` can read text in any base from 2 to 36, not just base 10.",
        "Pass the base as a second argument: `int(text, base)`.",
        "Letters stand for digits above 9 (`a` = 10, `f` = 15), and `int` handles that for you.",
    ],
    # ------------------------------------------------------------------ bit operators
    "py-get-bit": [
        "Shifting right (`>>`) moves bits towards position 0: shift by `position` and the bit you want ends up rightmost.",
        "`& 1` keeps only the rightmost bit and clears everything else.",
        "Shift first, then mask, so the answer is 0 or 1.",
    ],
    "py-toggle-bit": [
        "`1 << position` is a number whose only 1 bit is at position `position` (a mask).",
        "XOR (`^`) flips the bits where the mask has a 1 and leaves the rest alone.",
        "XOR `number` with the mask for position `position`.",
    ],
    "py-power-of-two": [
        "A power of two has exactly one 1 bit in binary (1, 10, 100, …).",
        "Subtracting 1 flips that bit and turns every bit below it on, so `number & (number - 1)` is 0 exactly when `number` has a single 1 bit.",
        "Zero and negative numbers aren't powers of two, so check that `number` is positive too. (`&` happens before `==`, so `x & y == 0` already means `(x & y) == 0`.)",
    ],
    # ------------------------------------------------------------------ complex numbers
    "py-complex-length": [
        "A complex number `x + yj` can stand for the point (x, y).",
        "`complex(x, y)` builds it, and `abs(...)` of a complex number is its distance from 0.",
        "Build the number and return its `abs`.",
    ],
    "py-rotate-point": [
        "Multiplying a complex number by `1j` rotates its point 90° anticlockwise.",
        "Build the point with `complex(x, y)` and multiply it by `1j`.",
        "Read the result's `.real` and `.imag` parts. They're floats, so convert each with `int` before returning them in a list.",
    ],
    # ------------------------------------------------------------------ bytes
    "py-utf8-bytes": [
        "Text has to be encoded into bytes before it can be stored or sent.",
        "`.encode(\"utf-8\")` turns a string into a `bytes` object.",
        "`list(...)` of a bytes object gives a list of the byte numbers (0-255).",
    ],
    "py-bytes-to-text": [
        "Go the other way: numbers → bytes → text.",
        "`bytes(list_of_numbers)` builds a bytes object.",
        "`.decode()` turns bytes back into a string (UTF-8 is the default).",
    ],
    "py-patch-byte": [
        "`bytes` can't be changed after it's made, but a `bytearray` can.",
        "Build a `bytearray` from the numbers, then set one position with square brackets, as you would with a list.",
        "Convert the result back to a list with `list(...)`.",
    ],
    "py-view-slice": [
        "A `memoryview` looks at existing bytes without copying them.",
        "Build `bytes` from the numbers, wrap them in `memoryview(...)`, then slice the view as normal.",
        "A memoryview slice has a `.tolist()` method that gives the numbers back as a list.",
    ],
    # ------------------------------------------------------------------ types
    "py-type-name": [
        "`type(value)` gives the class (the type) of a value.",
        "Every class has a `__name__` attribute with its name as text.",
        "Read `__name__` from the type. For `None`, the type's name is `NoneType`.",
    ],
    "py-count-real-ints": [
        "`isinstance(x, int)` checks whether `x` is an int, but `True` and `False` pass that check too, because `bool` is a kind of `int`.",
        "So you need two checks: it is an `int`, and it is not a `bool`.",
        "Count the items that pass both, with a loop and a counter or with `sum` over a generator of 1s.",
    ],
    "py-exception-family": [
        "Exception types form a family tree: `KeyError` is a more specific kind of `LookupError`.",
        "`issubclass(child, parent)` checks whether one class is the same as, or a descendant of, another.",
        "Return its result directly. It works on classes, not on instances.",
    ],
    # ------------------------------------------------------------------ exceptions
    "py-safe-int": [
        "`int(\"4.2\")` and `int(\"abc\")` don't return anything; they raise a `ValueError`.",
        "`try:` runs code that might fail; `except ValueError:` runs instead if that error happens.",
        "Try the conversion and return the number; in the `except` branch, return `None`.",
    ],
    "py-safe-divide": [
        "Dividing by zero raises a `ZeroDivisionError`.",
        "Put the division in a `try` block and catch that specific error.",
        "Return the division's result normally, and `None` from the `except` branch. Catch only `ZeroDivisionError`, not every error.",
    ],
    "py-check-age": [
        "Valid ages are 0 to 150, including both ends.",
        "`raise ValueError(\"message\")` stops the function and signals a problem to whoever called it.",
        "If the age is outside the range, raise; otherwise return it unchanged. A chained comparison with `not` in front checks \"outside the range\" neatly.",
    ],
    "py-custom-exception": [
        "You can make your own error type by writing a class that inherits from `Exception`.",
        "The class can be empty: a single `pass` in its body is enough.",
        "In `withdraw`, raise your new error when the amount is more than the balance; otherwise return the new balance.",
    ],
    "py-finally-log": [
        "Two layers: an inner `try` that converts one step and catches a `ValueError`, and an outer `try` around the whole loop.",
        "For a bad step, log it and `break` out of the loop.",
        "A `finally:` block always runs, whether the `try` finished normally or stopped early. Add `\"done\"` there so it's always last.",
    ],
    # ------------------------------------------------------------------ control extras
    "py-for-else-prime": [
        "A number is prime when nothing from 2 up to its square root divides it evenly.",
        "A `for` loop can have an `else:` block, which runs only if the loop finished *without* hitting `break`.",
        "Break when you find a divisor. In the `else`, return `True`. After the loop, return `False`. Handle numbers below 2 first: they aren't prime.",
    ],
    "py-ternary-abs": [
        "A conditional expression chooses between two values in one line: `value_if_true if condition else value_if_false`.",
        "When `number` is negative, its absolute value is `-number`; otherwise it's `number` itself.",
        "Return that one-line expression.",
    ],
    "py-walrus-positive": [
        "The walrus operator `:=` assigns a value *and* gives it back, inside a bigger expression.",
        "In a comprehension's `if` part, compute the result, store it with `:=`, and compare it with 0, all at once.",
        "The comprehension's output expression can then use the stored name, so each result is only computed once.",
    ],
    "py-http-status": [
        "`match code:` compares the value against each `case` in order, and runs the first one that fits.",
        "`case 200:` matches an exact value. A guard (`case n if ...:`) captures the value and checks a condition.",
        "End with `case _:`, which matches anything left over.",
    ],
    # ------------------------------------------------------------------ dynamic code
    "py-calculator": [
        "`eval(text)` runs text as a Python expression and returns its value.",
        "Arithmetic follows the normal rules, so multiplication happens before addition.",
        "Return what `eval` gives you. (Never `eval` text from people you don't trust: it can run any code.)",
    ],
    "py-run-snippet": [
        "`exec(text, namespace)` runs statements, storing any variables they create in the dict you pass as `namespace`.",
        "Start with an empty dict so the snippet runs in a clean space.",
        "After it runs, read `result` out of the dict.",
    ],
    "py-evaluate-many": [
        "Compiling turns text into a code object once, so it doesn't have to be re-read for every value.",
        "`compile(text, \"<expr>\", \"eval\")` makes a code object for a single expression.",
        "Then `eval` that code object once per value, passing a dict that sets `x`. Collect the results in a list.",
    ],
}
