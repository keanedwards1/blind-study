# Beginner lessons for Learn Python level 1 (First steps), keyed by concept id. They replace the concept `intro`s.
# Style: plain English first; any technical term or abstract idea goes in brackets after the plain explanation.

LESSONS = {
    "return-arithmetic": """
**In one sentence:** a function is a small machine that takes some inputs and hands back one answer.

### The idea
Every task in Learn Python asks you to finish a **function** (a named, reusable piece of code). Python runs your function with some values, and whatever comes after the word `return` is your answer.

```python
def add_two(n):
    return n + 2
```

- `def add_two(n):` names the machine `add_two` and says it takes one input, called `n` (an input like this is called a *parameter*).
- The indented line underneath is what the machine does. `return` hands the answer back and stops the function straight away.
- If you call `add_two(5)`, the answer is `7`.

### Doing maths
`+` adds, `-` subtracts and `*` multiplies (Python uses a star for "times", not `x`). Brackets decide what happens first, exactly like in maths:

```python
(2 + 3) * 4    # 20
2 + 3 * 4      # 14, because * happens before +
```

### When you'd use it
Every single task. Read the inputs, work something out, `return` it.

### Common mistakes
- **Forgetting `return`.** Without it, the function hands back nothing (Python's special "no value", `None`) and the tests fail.
- **Not indenting.** The lines inside a function must be pushed in by 4 spaces.
""",
    "division": """
**In one sentence:** Python has three kinds of division, and each answers a different question.

### The idea
| Write | Question it answers | `7 ? 2` gives |
|---|---|---|
| `/` | "What's the exact answer?" (always a decimal number, called a *float*) | `3.5` |
| `//` | "How many **whole** times does it fit?" (*floor division*) | `3` |
| `%` | "What's left over?" (the *remainder*, also called *modulo*) | `1` |

And `**` means "to the power of": `2 ** 3` is 2 × 2 × 2 = `8`.

### Try it
```python
10 / 4     # 2.5
10 // 4    # 2   (4 fits into 10 twice)
10 % 4     # 2   (and 2 is left over)
6 / 2      # 3.0 (a float, even though it's a whole number)
```

### When you'd use it
- Sharing things out evenly: `//` for how many each person gets, `%` for how many are left.
- Checking whether a number is even: `n % 2 == 0` (nothing left over after dividing by 2).

### Common mistakes
- Expecting `/` to give a whole number. `6 / 2` is `3.0`. Use `//` when you need a whole number.
- Forgetting that `//` rounds **down**: `-7 // 2` is `-4`, not `-3`.
""",
    "comparisons": """
**In one sentence:** a comparison asks a yes-or-no question, and Python answers `True` or `False`.

### The idea
`True` and `False` are Python's yes and no (values of this kind are called *booleans*, or *bools*). You get them by comparing things:

| Write | Means |
|---|---|
| `==` | equal to |
| `!=` | not equal to |
| `<` `>` | less than, greater than |
| `<=` `>=` | less than or equal, greater than or equal |

```python
5 > 3      # True
5 == 6     # False
```

You can return a comparison directly, with no `if` needed: `return age >= 18`.

### Truthy and falsy
Python can treat *any* value as a yes or no. Zero, empty text `""`, an empty list `[]` and `None` count as **no** (they're *falsy*); almost everything else counts as **yes** (*truthy*). `bool(value)` shows you which: `bool(0)` is `False`, `bool(7)` is `True`.

### Common mistakes
- **One `=` versus two.** One `=` *stores* a value (`x = 5`). Two `==` *asks* whether two values are equal (`x == 5`).
""",
    "if-else": """
**In one sentence:** `if` lets your code make decisions.

### The idea
`if` runs some lines only when a condition is true. `elif` (short for "else if") checks another condition, and `else` catches everything that's left.

```python
def describe(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"
```

`describe(4)` gives `"positive"`; `describe(0)` gives `"zero"`.

- Python checks the conditions from top to bottom and runs only the **first** one that's true.
- Each condition line ends with a colon `:`, and the lines that belong to it are indented by 4 spaces (a group of indented lines is called a *block*).

### When you'd use it
Any time the answer depends on the input: grades, labels, prices with discounts.

### Common mistakes
- **Wrong order.** If you check `score >= 70` before `score >= 90`, a score of 95 stops at the first check. Put the most specific case first.
- **Forgetting the colon** at the end of an `if` line.
""",
    "boolean-logic": """
**In one sentence:** `and`, `or` and `not` combine several yes/no questions into one.

### The idea
- `a and b` is true only when **both** are true.
- `a or b` is true when **at least one** is true.
- `not a` flips true to false and false to true.

```python
age = 20
age >= 18 and age < 65     # True: both are true
age < 13 or age > 60       # False: neither is true
not age > 30               # True
```

### A handy shortcut
Python lets you chain comparisons like you would in maths: `13 <= age <= 19` means "age is at least 13 **and** at most 19".

### Common mistakes
- **Writing `day == 6 or 7`.** Python reads this as `(day == 6) or 7`, and `7` on its own always counts as true. Write the full comparison on each side: `day == 6 or day == 7`.
""",
    "conversions": """
**In one sentence:** numbers and text are different kinds of value, and you sometimes need to turn one into the other.

### The idea
`42` is a number, but `"42"` (in quotes) is text that happens to contain digits (text values are called *strings*). Python won't guess what you mean, so `"5" + 1` is an error.

Three functions convert between them (the kind of a value is called its *type*):

```python
int("42")      # 42      text → whole number (an *int*)
int(3.9)       # 3       chops off the decimals, toward zero
float("2.5")   # 2.5     text → decimal number (a *float*)
float(3)       # 3.0
str(42)        # "42"    number → text
```

### When you'd use it
Whenever text and numbers meet: reading what someone typed (always text), or building a message that includes a number.

### Common mistakes
- `int("2.5")` is an error: `int` can't read a decimal point. Use `float` first if you need to.
- `int(3.9)` is `3`, not `4`. It cuts the decimals off; it doesn't round.
""",
    "number-builtins": """
**In one sentence:** Python comes with ready-made functions for common number jobs.

### The idea
These are *built-in functions*: they're always available, with nothing to import.

```python
abs(-4)            # 4     distance from zero (always positive)
round(2.567, 2)    # 2.57  round to 2 decimal places
round(2.6)         # 3     round to a whole number
min(3, 8)          # 3     the smallest
max(3, 8, 5)       # 8     the largest (any number of values)
```

### When you'd use it
- `abs` for "how far apart": `abs(a - b)`.
- `min` and `max` for limits, like keeping a value between 0 and 100.

### Common mistakes
- `round(2.5)` gives `2`, not `3`! Python rounds exact halves to the nearest **even** number (called *banker's rounding*), so `round(3.5)` is `4`.
""",
    "print": """
**In one sentence:** `print` shows something on the screen.

### The idea
```python
print("hi")             # hi
print("a", 1)           # a 1     (a space between values)
print(1, 2, 3, sep="-") # 1-2-3   (sep= changes what goes between)
print("a", end="")      # stays on the same line (end= changes the ending)
```

Normally `print` finishes with a new line, so each `print` starts on a fresh line.

### print is not return
This is the big one. `print` **shows** something to a person, but the function still hands back nothing (`None`). `return` **hands an answer back** to the code that called the function. Most tasks want `return`; tasks that check your printing say so.

### When you'd use it
Talking to the person running your program, and checking what your code is doing while you work on it (*debugging*).

### Common mistakes
- Using `print` when the task wants `return`, or the other way round.
- Extra or missing spaces: `print("a", "b")` shows `a b` with a space, but `print("a" + "b")` shows `ab`.
""",
    "input": """
**In one sentence:** `input()` waits for someone to type a line, and gives you what they typed.

### The idea
```python
name = input()
age = int(input())
```

- `input()` pauses the program until a line is typed, then hands it back **as text**, even if the person typed a number.
- That's why the second line wraps it in `int(...)`: to turn the typed text into a number you can do maths with.
- `input("Your name? ")` shows a question (a *prompt*) first.

In these tasks, nobody actually types: the tests feed your program the lines for you, one per `input()` call.

### Common mistakes
- Forgetting to convert: `input() + 1` is an error because the input is text.
- Calling `input()` too many or too few times: each call reads exactly one line.
""",
}
