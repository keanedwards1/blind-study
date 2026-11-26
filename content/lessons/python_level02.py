# Beginner lessons for Learn Python level 2 (Strings). See python_level01.py for the style.

LESSONS = {
    "indexing": r"""
**Overview:** text is a row of characters, and you can read any one of them by its position.

### The idea
A piece of text (a *string*) is a row of characters. Each character has a position number (its *index*), and **counting starts at 0**, not 1.

```python
s = "python"
s[0]      # 'p'   the first character
s[1]      # 'y'
s[-1]     # 'n'   negative numbers count from the end
len(s)    # 6     how many characters (its *length*)
```

So for `"python"`: `p` is at 0, `y` at 1, … `n` at 5. The last position is always the length minus one.

### When you'd use it
Reading the first letter of a name, the last character of a word, or the middle of something.

### Common mistakes
- **Off by one.** `s[6]` is an error for `"python"` (an `IndexError`), because the last position is 5.
- **Trying to change one letter.** `s[0] = "P"` is an error: strings can't be changed once made (they're *immutable*). Build a new string instead.
""",
    "slicing": r"""
**Overview:** a slice takes a stretch of characters out of a piece of text.

### The idea
Write `text[start:stop]` to get the characters from position `start` up to, **but not including**, position `stop` (this is called *slicing*).

```python
s = "python"
s[1:4]    # 'yth'     positions 1, 2, 3
s[:3]     # 'pyt'     leave out start → from the beginning
s[3:]     # 'hon'     leave out stop → to the end
s[:]      # 'python'  leave out both → a copy of the whole thing
s[-2:]    # 'on'      the last two characters
```

A third number is the *step*: how far to jump each time.

```python
s[::2]    # 'pto'     every second character
s[::-1]   # 'nohtyp'  a step of -1 walks backwards (reverses it)
```

### When you'd use it
Taking the first few letters, dropping the first and last characters, reversing a word.

### Common mistakes
- Expecting `stop` to be included: `s[1:4]` stops **before** position 4.
- Worrying about going past the end: slices never crash. `"hi"[0:100]` is just `"hi"`.
""",
    "string-methods": r"""
**Overview:** text comes with built-in tools for changing case and tidying up.

### The idea
A *method* is a function that belongs to a value; you call it with a dot after the value. String methods **always give you a new string**; the original never changes.

```python
s = "  Hello World  "
s.upper()            # '  HELLO WORLD  '
s.lower()            # '  hello world  '
s.strip()            # 'Hello World'      spaces removed from both ends
s.replace("o", "0")  # '  Hell0 W0rld  '  every match replaced
"the fox".title()    # 'The Fox'          each word capitalised
"hello".capitalize() # 'Hello'            only the first character
```

You can chain them, one after another: `s.strip().lower()` gives `'hello world'`.

### When you'd use it
Cleaning up what people type (extra spaces, random capitals) before comparing or storing it.

### Common mistakes
- Calling a method and throwing the result away: `s.upper()` on its own line does nothing useful. Keep the result: `s = s.upper()`.
""",
    "searching": r"""
**Overview:** Python can tell you whether some text contains other text, where, and how often.

### The idea
```python
s = "concatenate"
"cat" in s             # True   is it in there anywhere?
s.find("cat")          # 3      the position of the first match
s.find("dog")          # -1     -1 means "not found"
s.count("a")           # 2      how many times it appears
s.startswith("con")    # True   does it begin with this?
s.endswith(".py")      # False  does it end with this?
```

`startswith` and `endswith` also accept several options in brackets (a *tuple*): `name.endswith((".jpg", ".png"))`.

### When you'd use it
Checking a file type, finding where a word appears, or counting letters.

### Common mistakes
- Forgetting that searches care about case: `"Cat" in "my cat"` is `False`. Lower-case both first.
- Using `s.index("x")` when it might be missing: unlike `find`, `index` crashes (raises a `ValueError`) instead of giving `-1`.
""",
    "split-join": r"""
**Overview:** `split` breaks text into a list of pieces, and `join` glues a list of pieces back into text.

### The idea
```python
"red green  blue".split()    # ['red', 'green', 'blue']
"a,b,,c".split(",")          # ['a', 'b', '', 'c']
", ".join(["a", "b", "c"])   # 'a, b, c'
"".join(["h", "i"])          # 'hi'
```

- `split()` with nothing in the brackets splits wherever there are spaces, however many.
- `split(",")` splits at each comma exactly, so two commas in a row give an empty piece.
- For `join`, the **glue comes first**, then `.join(...)` with the list.

### When you'd use it
Turning a sentence into words, reading comma-separated data, building a sentence from a list.

### Common mistakes
- Writing `words.join(", ")`. It's the other way round: `", ".join(words)`.
- Joining numbers: `join` only works on text, so `", ".join([1, 2])` is an error. Convert them with `str` first.
""",
    "formatting": r"""
**Overview:** an f-string lets you drop values straight into a piece of text, and format them neatly.

### The idea
Put an `f` before the opening quote, then write values inside curly braces (this is an *f-string*):

```python
name, age = "Ada", 36
f"{name} is {age}"      # 'Ada is 36'
f"{age + 1} next year"  # '37 next year'  (any expression works)
```

After a colon inside the braces you can describe **how** to show the value (a *format spec*):

| Write | Gives | Means |
|---|---|---|
| `f"{3.14159:.2f}"` | `3.14` | 2 decimal places |
| `f"{7:03d}"` | `007` | whole number, padded with zeros to width 3 |
| `f"{'x':>5}"` | `    x` | right-aligned in 5 spaces (`<` is left) |
| `f"{1234567:,}"` | `1,234,567` | thousands separators |
| `f"{0.25:.0%}"` | `25%` | as a percentage |

`format(7, "03d")` does the same thing as a function, without an f-string.

### Common mistakes
- Forgetting the `f`: `"{name}"` without it shows the braces literally.
""",
    "char-codes": r"""
**Overview:** every character has a number behind it, and you can switch between the two.

### The idea
Computers store each character as a number (its *Unicode code point*).

```python
ord("a")    # 97     character → number
ord("b")    # 98
ord("A")    # 65
chr(97)     # 'a'    number → character
```

Letters have numbers that follow each other, so you can do maths with them:

```python
ord("d") - ord("a")      # 3     'd' is 3 letters after 'a'
chr(ord("a") + 2)        # 'c'   2 letters after 'a'
```

### When you'd use it
Shifting letters (secret codes), turning a letter into its alphabet position (0 for `a` up to 25 for `z`), and counting letters in a list of 26.

### Common mistakes
- Forgetting that capitals have different numbers from lower-case letters. Lower-case first if case shouldn't matter.
""",
    "char-tests": r"""
**Overview:** these methods answer yes/no questions about what kind of characters a piece of text contains.

### The idea
Each one checks **every** character, and gives `False` for empty text:

```python
"2024".isdigit()     # True   only digits 0-9
"abc".isalpha()      # True   only letters
"abc123".isalnum()   # True   only letters and digits
"   ".isspace()      # True   only whitespace
"HELLO!".isupper()   # True   every letter is a capital (other characters are ignored)
"hello".islower()    # True   every letter is lower case
```

### When you'd use it
Checking that a PIN is all digits, that a username has no symbols, or skipping punctuation while you scan a sentence.

### Common mistakes
- `"".isdigit()` is `False`: empty text never passes.
- `"12.5".isdigit()` is `False`: the dot isn't a digit.
""",
    "repr-ascii": r"""
**Overview:** `repr` shows a value exactly as a programmer would type it, which makes hidden characters visible.

### The idea
`str(x)` makes friendly text for people. `repr(x)` makes exact text for programmers (the value's *representation*).

```python
print(str("hi"))       # hi
print(repr("hi"))      # 'hi'       the quotes show it's text
print(repr("a\tb"))    # 'a\tb'     a tab, made visible
print(repr("hi\n"))    # 'hi\n'     a hidden new line, made visible
```

`ascii(x)` is like `repr`, but also writes any non-English character as a code (an *escape*): `ascii("café")` gives `'caf\xe9'`.

### When you'd use it
Debugging. When two strings look the same but aren't equal, `print(repr(s))` usually reveals a stray space or new line.
""",
}
