# Learn Python, level 2: strings.
from _helpers import P, Q

LEVEL = dict(
    n=2,
    title="Strings",
    summary="Text in Python: indexing, slicing, the string methods you'll use constantly, f-strings, and character codes.",
    concepts=[
        # ------------------------------------------------------------------ len + indexing
        dict(
            id="indexing",
            title="len and indexing",
            builtins=["len"],
            intro="""
A string is a sequence of characters. Each one has a position (an **index**), starting at **0**.

```python
s = "python"
s[0]        # 'p'
s[5]        # 'n'
s[-1]       # 'n'   (negative indices count from the end)
len(s)      # 6
```

- The last index is `len(s) - 1`. `s[len(s)]` is an `IndexError`.
- Strings can't be changed in place: `s[0] = "P"` is an error. Build a new string instead.
""",
            problems=[
                P("py-string-length", "String Length", "def length(s: str) -> int:",
                  "Return how many characters `s` has.",
                  "def length(s: str) -> int:\n    return len(s)\n",
                  [(["hello"], 5), ([""], 0), (["a b"], 3)], [["x"], ["spaces   "], ["🙂"]],
                  require=["len"],
                  grammar="""
## Building blocks
- **Length:** `len(s)`. Spaces count as characters.
"""),
                P("py-first-and-last", "First and Last", "def ends(s: str) -> str:",
                  'Return the first character of `s` followed by its last character. `"python"` → `"pn"`. `s` has at least one character.',
                  "def ends(s: str) -> str:\n    return s[0] + s[-1]\n",
                  [(["python"], "pn"), (["a"], "aa"), (["ok"], "ok")], [["hello world"], ["xyz"]],
                  grammar="""
## Building blocks
- **First character:** `s[0]`
- **Last character:** `s[-1]` (or `s[len(s) - 1]`).
- **Join two strings:** `+`
"""),
                P("py-middle-char", "Middle Character", "def middle(s: str) -> str:",
                  'Return the middle character of `s`, which has an odd length. `"abcde"` → `"c"`.',
                  "def middle(s: str) -> str:\n    return s[len(s) // 2]\n",
                  [(["abcde"], "c"), (["x"], "x"), (["cat"], "a")], [["1234567"], ["racecar"]],
                  hints=["For length 5 the middle index is 2. How do you get 2 from 5?"],
                  grammar="""
## Building blocks
- **Middle index:** `len(s) // 2`. Floor division keeps it a whole number.
- **Index with an expression:** `word[2 + 1]` works; anything that gives a whole number can go in the brackets.
"""),
                P("py-repeat-text", "Repeat It", "def repeat(s: str, n: int) -> str:",
                  'Return `s` repeated `n` times. `"ab"`, `3` → `"ababab"`.',
                  "def repeat(s: str, n: int) -> str:\n    return s * n\n",
                  [(["ab", 3], "ababab"), (["x", 0], ""), (["-", 5], "-----")], [["hi ", 2], ["", 4]],
                  require=["op:*"],
                  grammar="""
## Building blocks
- **Repeat a string:** `s * n`. `"-" * 3` is `"---"`.
"""),
            ],
            quiz=[
                Q("What does this print?", "n o", "o n", "n h", "error", code="s = 'python'\nprint(s[-1], s[4])", predict=True,
                  why="`s[-1]` is the last character; index 4 is the fifth one."),
                Q("What happens?", "TypeError: strings can't be changed in place", "s becomes 'Hat'", "s stays 'hat' silently", "IndexError",
                  code="s = 'hat'\ns[0] = 'H'", why="Strings are **immutable**. Build a new one: `'H' + s[1:]`."),
                Q("For `s = 'abc'`, which index is out of range?", "s[3]", "s[-3]", "s[2]", "s[-1]", why="Valid indices are 0–2 and -1 to -3."),
            ],
        ),
        # ------------------------------------------------------------------ slicing
        dict(
            id="slicing",
            title="Slicing",
            builtins=[],
            intro="""
A **slice** takes a piece of a string: `s[start:stop:step]`.

```python
s = "abcdef"
s[1:4]    # 'bcd'   from 1 up to (not including) 4
s[:3]     # 'abc'   start defaults to the beginning
s[3:]     # 'def'   stop defaults to the end
s[::2]    # 'ace'   every second character
s[::-1]   # 'fedcba' reversed
```

- Slices never raise an `IndexError`. `s[2:100]` just stops at the end.
- Slicing always makes a **new** string.
""",
            problems=[
                P("py-first-three", "First Three", "def first_three(s: str) -> str:",
                  "Return the first three characters of `s` (or all of it, if it's shorter).",
                  "def first_three(s: str) -> str:\n    return s[:3]\n",
                  [(["python"], "pyt"), (["hi"], "hi"), ([""], "")], [["abc"], ["abcd"]],
                  require=["slicing"],
                  grammar="""
## Building blocks
- **From the start up to index 3:** `s[:3]`. It's fine if `s` is shorter.
"""),
                P("py-reverse-text", "Reverse the Text", "def reverse(s: str) -> str:",
                  'Return `s` backwards. `"stressed"` → `"desserts"`.',
                  "def reverse(s: str) -> str:\n    return s[::-1]\n",
                  [(["stressed"], "desserts"), ([""], ""), (["a"], "a")], [["racecar"], ["Hello, World"]],
                  require=["slicing"],
                  grammar="""
## Building blocks
- **Step of -1:** `s[::-1]` walks the string from the end to the start.
"""),
                P("py-every-other", "Every Other Character", "def every_other(s: str) -> str:",
                  'Return the characters at positions 0, 2, 4, …. `"abcdefg"` → `"aceg"`.',
                  "def every_other(s: str) -> str:\n    return s[::2]\n",
                  [(["abcdefg"], "aceg"), (["ab"], "a"), ([""], "")], [["0123456789"], ["x"]],
                  require=["slicing"],
                  grammar="""
## Building blocks
- **A step:** the third number in a slice, `s[::2]`.
"""),
                P("py-drop-ends", "Drop the Ends", "def inner(s: str) -> str:",
                  'Return `s` without its first and last characters. `"[hello]"` → `"hello"`. If `s` has fewer than 2 characters, return `""`.',
                  "def inner(s: str) -> str:\n    return s[1:-1]\n",
                  [(["[hello]"], "hello"), (["ab"], ""), (["a"], "")], [["(x)"], ["''"], ["abcdef"]],
                  grammar="""
## Building blocks
- **Skip the first:** start at `1`.
- **Stop before the last:** a stop of `-1`.
- **Together:** `s[1:-1]`. Slices never raise errors, so short strings just give `""`.
"""),
                P("py-capitalise-first", "Capitalise the First Letter", "def cap_first(s: str) -> str:",
                  'Return `s` with only its first character changed to upper case. `"hello world"` → `"Hello world"`. `s` may be empty.',
                  "def cap_first(s: str) -> str:\n    return s[:1].upper() + s[1:]\n",
                  [(["hello world"], "Hello world"), ([""], ""), (["Already"], "Already")], [["x"], ["iPhone"], ["1st"]],
                  difficulty="Medium",
                  hints=["`s[0]` fails on an empty string, but `s[:1]` doesn't."],
                  grammar="""
## Building blocks
- **First character safely:** `s[:1]` is `""` for an empty string, where `s[0]` would crash.
- **Upper case:** `.upper()`
- **The rest:** `s[1:]`
- **Rebuild:** strings can't be edited, so build a new one by joining pieces with `+`.
"""),
            ],
            quiz=[
                Q("What does this print?", "bcd", "bcde", "abcd", "cde", code="print('abcdef'[1:4])", predict=True,
                  why="The stop index is not included: positions 1, 2, 3."),
                Q("What does this print?", "abc", "error", "abcdef", "''", code="print('abc'[0:100])", predict=True,
                  why="Slices clamp to the string's length instead of raising an error."),
                Q("What does this print?", "fdb", "bdf", "fedcba", "ace", code="print('abcdef'[::-2])", predict=True,
                  why="Start from the end and take every second character going backwards."),
            ],
        ),
        # ------------------------------------------------------------------ case and cleanup methods
        dict(
            id="string-methods",
            title="Case and clean-up methods",
            builtins=[],
            intro="""
Strings come with **methods**: functions you call with a dot. They always return a **new** string.

| Method | `"  Hello World  "` becomes |
|---|---|
| `.upper()` / `.lower()` | `"  HELLO WORLD  "` / `"  hello world  "` |
| `.strip()` | `"Hello World"` (removes spaces at both ends) |
| `.replace("o", "0")` | `"  Hell0 W0rld  "` |
| `.title()` | `"  Hello World  "` (each word capitalised) |
| `.capitalize()` | `"  hello world  "` (first character only) |

Methods can be chained: `s.strip().lower()`.
""",
            problems=[
                P("py-shout", "Shout", "def shout(s: str) -> str:",
                  'Return `s` in capitals with `"!"` added. `"hey"` → `"HEY!"`.',
                  'def shout(s: str) -> str:\n    return s.upper() + "!"\n',
                  [(["hey"], "HEY!"), (["Go team"], "GO TEAM!")], [[""], ["already LOUD"]],
                  require=[".upper"],
                  grammar="""
## Building blocks
- **Capitals:** `s.upper()`
- **Add text:** `+ "!"`
"""),
                P("py-clean-username", "Clean Username", "def clean(s: str) -> str:",
                  'Usernames are stored without surrounding spaces, in lower case. `"  Ada_L "` → `"ada_l"`.',
                  "def clean(s: str) -> str:\n    return s.strip().lower()\n",
                  [(["  Ada_L "], "ada_l"), (["bob"], "bob")], [["   "], ["\tTabbed\n"], ["MiXeD"]],
                  require=[".strip", ".lower"],
                  grammar="""
## Building blocks
- **Trim whitespace at both ends:** `s.strip()` (spaces, tabs and new lines).
- **Lower case:** `.lower()`
- **Chain:** `s.strip().lower()`
"""),
                P("py-spaces-to-underscores", "Spaces to Underscores", "def to_snake(s: str) -> str:",
                  'Replace every space in `s` with an underscore. `"my file name"` → `"my_file_name"`.',
                  'def to_snake(s: str) -> str:\n    return s.replace(" ", "_")\n',
                  [(["my file name"], "my_file_name"), (["none"], "none")], [["  "], ["a b c d"]],
                  require=[".replace"],
                  grammar="""
## Building blocks
- **Replace every match:** `s.replace(old, new)`
"""),
                P("py-title-case", "Title Case", "def headline(s: str) -> str:",
                  'Capitalise the first letter of every word and lower-case the rest. `"the QUICK fox"` → `"The Quick Fox"`.',
                  "def headline(s: str) -> str:\n    return s.title()\n",
                  [(["the QUICK fox"], "The Quick Fox"), (["a"], "A")], [[""], ["hello world"], ["ONE TWO"]],
                  require=[".title"],
                  grammar="""
## Building blocks
- **Every word capitalised:** `s.title()`
- **Compare:** `s.capitalize()` only capitalises the very first character.
"""),
            ],
            quiz=[
                Q("What does this print?", "hello", "HELLO", "Hello", "error", code="s = 'hello'\ns.upper()\nprint(s)", predict=True,
                  why="`.upper()` returns a new string, and nothing stored it. Strings never change in place: write `s = s.upper()`."),
                Q("What does this print?", "'x'", "'  x  '", "'x  '", "x", code="print(repr('  x  '.strip()))", predict=True,
                  why="`strip()` removes whitespace from both ends."),
            ],
        ),
        # ------------------------------------------------------------------ searching
        dict(
            id="searching",
            title="Searching: in, find, count, startswith",
            builtins=[],
            intro="""
- `"cat" in s` is `True` if `"cat"` appears anywhere in `s`.
- `s.find("cat")` gives the index of the first match, or `-1` if there isn't one. (`s.index` is the same but raises an error instead.)
- `s.count("a")` counts non-overlapping matches.
- `s.startswith("http")` and `s.endswith(".py")` check the ends. Both accept a tuple of options: `s.endswith((".jpg", ".png"))`.
""",
            problems=[
                P("py-mentions-cat", "Mentions a Cat", "def mentions_cat(s: str) -> bool:",
                  'Return `True` if the text contains `"cat"` anywhere, in any case. `"My CAT is grey"` → `True`.',
                  'def mentions_cat(s: str) -> bool:\n    return "cat" in s.lower()\n',
                  [(["My CAT is grey"], True), (["dog"], False), (["concatenate"], True)], [[""], ["c a t"], ["Cat"]],
                  require=["op:in"],
                  grammar="""
## Building blocks
- **Substring test:** `"cat" in text`
- **Ignore case:** lower-case first: `"cat" in s.lower()`
"""),
                P("py-count-vowels", "Count the Vowels", "def vowels(s: str) -> int:",
                  "Count the vowels (a, e, i, o, u) in `s`, upper or lower case.",
                  'def vowels(s: str) -> int:\n    t = s.lower()\n    return t.count("a") + t.count("e") + t.count("i") + t.count("o") + t.count("u")\n',
                  [(["Hello World"], 3), (["rhythm"], 0), (["AEIOU"], 5)], [[""], ["banana"], ["Queueing"]],
                  require=[".count"],
                  hints=["`.count` counts one thing at a time. Add up five counts."],
                  grammar="""
## Building blocks
- **Count occurrences:** `t.count("a")`
- **A variable for the lower-case copy:** `partner = text.lower()`, so you only convert once.
- **Add the counts:** `t.count("a") + t.count("e") + …`
- **Later:** a loop or `sum(c in "aeiou" for c in t)` does this in one line (levels 3 and 5).
"""),
                P("py-is-link", "Is It a Link?", "def is_link(s: str) -> bool:",
                  'Return `True` if `s` starts with `"http://"` or `"https://"`.',
                  'def is_link(s: str) -> bool:\n    return s.startswith(("http://", "https://"))\n',
                  [(["https://python.org"], True), (["ftp://x"], False), (["http://a"], True)], [[""], ["www.example.com"], ["https:/broken"]],
                  require=[".startswith"],
                  grammar="""
## Building blocks
- **Check the start:** `s.startswith("http://")`
- **Several options at once:** pass a tuple: `s.startswith(("http://", "https://"))`
"""),
                P("py-find-position", "Where Is It?", "def position(s: str, sub: str) -> int:",
                  "Return the index where `sub` first appears in `s`, or `-1` if it doesn't.",
                  "def position(s: str, sub: str) -> int:\n    return s.find(sub)\n",
                  [(["banana", "na"], 2), (["banana", "x"], -1), (["abc", "a"], 0)], [["", "a"], ["aaaa", "aa"], ["hello", "o"]],
                  require=[".find"],
                  grammar="""
## Building blocks
- **First position, or -1:** `s.find(sub)`
- **Compare:** `s.index(sub)` raises `ValueError` when it's missing.
"""),
                P("py-file-extension", "File Extension", "def extension(filename: str) -> str:",
                  'Return the extension of `filename`: everything after the **last** dot, without the dot. If there is no dot, return `""`. `"archive.tar.gz"` → `"gz"`.',
                  'def extension(filename: str) -> str:\n    dot = filename.rfind(".")\n    return filename[dot + 1:] if dot != -1 else ""\n',
                  [(["archive.tar.gz"], "gz"), (["notes.txt"], "txt"), (["README"], "")], [[".bashrc"], ["a.b.c.d"], ["trailing."]],
                  difficulty="Medium",
                  hints=["`rfind` searches from the right.", "Slice from just after that position."],
                  grammar="""
## Building blocks
- **Last match:** `s.rfind(".")` gives the index of the last dot, or `-1`.
- **Everything after it:** `s[dot + 1:]`
- **One-line if/else:** `a if condition else b`
"""),
            ],
            quiz=[
                Q("What does this print?", "2 -1", "2 0", "3 -1", "2 error", code="s = 'banana'\nprint(s.find('n'), s.find('z'))", predict=True,
                  why="`find` returns the first index, or -1 when there's no match."),
                Q("What does this print?", "2", "3", "1", "4", code="print('aaaa'.count('aa'))", predict=True,
                  why="`count` counts non-overlapping matches: 'aa' + 'aa'."),
                Q("What does this print?", "True", "False", code="print('' in 'abc')", predict=True,
                  why="The empty string is a substring of every string."),
            ],
        ),
        # ------------------------------------------------------------------ split and join
        dict(
            id="split-join",
            title="split and join",
            builtins=[],
            intro="""
- `s.split()` breaks text into a **list** of words, splitting on any run of whitespace.
- `s.split(",")` splits on a specific separator (and keeps empty pieces: `"a,,b".split(",")` is `['a', '', 'b']`).
- `", ".join(words)` glues a list of strings together with `", "` between each one. The separator comes first: `sep.join(list)`.
""",
            problems=[
                P("py-word-count", "Word Count", "def word_count(s: str) -> int:",
                  "Return how many words `s` has. Words are separated by one or more spaces.",
                  "def word_count(s: str) -> int:\n    return len(s.split())\n",
                  [(["the quick brown fox"], 4), (["  spaced   out  "], 2), ([""], 0)], [["one"], ["a b c d e f"]],
                  require=[".split"],
                  grammar="""
## Building blocks
- **Split on whitespace:** `s.split()` with no argument ignores extra spaces.
- **How many items:** `len(list)`
"""),
                P("py-join-commas", "Comma List", "def comma_list(words: List[str]) -> str:",
                  'Join the words into one string separated by a comma and a space. `["a", "b", "c"]` → `"a, b, c"`.',
                  'def comma_list(words: List[str]) -> str:\n    return ", ".join(words)\n',
                  [([["a", "b", "c"]], "a, b, c"), ([["solo"]], "solo"), ([[]], "")], [[["x", "y"]], [["", ""]]],
                  require=[".join"],
                  grammar="""
## Building blocks
- **Glue with a separator:** `", ".join(words)`. The separator goes before `.join`.
"""),
                P("py-csv-fields", "Read a CSV Line", "def fields(line: str) -> List[str]:",
                  'Split a comma-separated line into a list of its fields, leaving any spaces as they are. `"a,b,,c"` → `["a", "b", "", "c"]`.',
                  'def fields(line: str) -> List[str]:\n    return line.split(",")\n',
                  [(["a,b,,c"], ["a", "b", "", "c"]), (["one"], ["one"])], [[""], [",,"], ["x, y"]],
                  grammar="""
## Building blocks
- **Split on a separator:** `line.split(",")`. Empty fields are kept.
- **Note:** `"".split(",")` is `['']`, a list with one empty string.
"""),
                P("py-swap-name", "Last Name First", "def last_first(name: str) -> str:",
                  'Turn `"First Last"` into `"Last, First"`. The name is always exactly two words.',
                  'def last_first(name: str) -> str:\n    first, last = name.split()\n    return last + ", " + first\n',
                  [(["Ada Lovelace"], "Lovelace, Ada"), (["Alan Turing"], "Turing, Alan")], [["A B"], ["Grace Hopper"]],
                  grammar="""
## Building blocks
- **Split into words:** `name.split()`
- **Unpack two items into two names:** `leader, ultimate = who.split()`
- **Rebuild:** `last + ", " + first`
"""),
                P("py-snake-to-camel", "snake_case to camelCase", "def camel(s: str) -> str:",
                  'Convert `snake_case` to `camelCase`: remove the underscores and capitalise each word after the first. `"user_first_name"` → `"userFirstName"`. Every word is lower case.',
                  'def camel(s: str) -> str:\n    first, *rest = s.split("_")\n    return first + "".join(w.capitalize() for w in rest)\n',
                  [(["user_first_name"], "userFirstName"), (["id"], "id")], [["a_b_c"], ["already"], ["x_y"]],
                  difficulty="Medium",
                  hints=["Split on `_`, keep the first word, capitalise the others, and join them with `\"\"`.",
                         "`s.title()` capitalises every word: you could title-case, remove underscores, and lower-case just the first letter."],
                  grammar="""
## Building blocks
- **Pieces:** `s.split("_")`
- **Option A:** `pattern = word.title().replace("_", "")`, then `pattern[:1].lower() + pattern[1:]`.
- **Option B (preview of level 5):** star unpacking, `head, *remainder = [1, 2, 3]`, puts the leftovers in a list.
"""),
            ],
            quiz=[
                Q("What does this print?", "['a', 'b']", "['a', '', 'b']", "['', 'a', 'b', '']", "a b", code="print('  a   b '.split())", predict=True,
                  why="With no argument, `split()` splits on runs of whitespace and drops empty pieces."),
                Q("What does this print?", "a-b-c", "-a-b-c-", "abc", "['a', 'b', 'c']", code="print('-'.join(['a', 'b', 'c']))", predict=True,
                  why="The separator goes between items, not at the ends."),
                Q("Why is `', '.join([1, 2, 3])` an error?", "join only accepts strings", "join needs a tuple", "the separator must be one character", "it isn't an error",
                  why="Convert first: `', '.join(str(n) for n in nums)`."),
            ],
        ),
        # ------------------------------------------------------------------ f-strings and format
        dict(
            id="formatting",
            title="f-strings and format()",
            builtins=["format"],
            intro="""
An **f-string** puts values straight into text: `f"{name} is {age}"`.

After a colon you can add a **format spec**:

| Spec | Example | Result |
|---|---|---|
| `.2f` | `f"{3.14159:.2f}"` | `3.14` |
| `03d` | `f"{7:03d}"` | `007` |
| `>5` | `f"{'x':>5}"` | `    x` (right-aligned in 5) |
| `,` | `f"{1234567:,}"` | `1,234,567` |
| `.0%` | `f"{0.25:.0%}"` | `25%` |

The built-in `format(value, spec)` does the same thing without the f-string: `format(7, "03d")` is `"007"`.
""",
            problems=[
                P("py-introduce", "Introduce Someone", "def introduce(name: str, age: int) -> str:",
                  'Return `"NAME is AGE years old"`. `"Ada", 36` → `"Ada is 36 years old"`.',
                  'def introduce(name: str, age: int) -> str:\n    return f"{name} is {age} years old"\n',
                  [(["Ada", 36], "Ada is 36 years old"), (["Bo", 1], "Bo is 1 years old")], [["", 0], ["Methuselah", 969]],
                  require=["fstring"],
                  grammar="""
## Building blocks
- **f-string:** put `f` before the quotes and the values in braces: `f"{name} is {age} years old"`.
- **No `str()` needed:** f-strings convert numbers for you.
"""),
                P("py-two-decimals", "Two Decimal Places", "def money(x: float) -> str:",
                  'Return `x` as text with exactly two decimal places. `3.14159` → `"3.14"`, `2` → `"2.00"`.',
                  'def money(x: float) -> str:\n    return f"{x:.2f}"\n',
                  [([3.14159], "3.14"), ([2], "2.00"), ([0.005], "0.01")], [[100.0], [-1.234], [9.999]],
                  grammar="""
## Building blocks
- **Fixed decimals:** `f"{x:.2f}"`. `.2f` means "a float with 2 decimal places".
- **Not the same as `round`:** `round(2, 2)` is `2`, but the format always shows `2.00`.
"""),
                P("py-zero-pad", "Zero-Padded Number", "def ticket(n: int) -> str:",
                  'Ticket numbers are always 4 digits, padded with zeros. `42` → `"0042"`. Use the built-in `format` function.',
                  'def ticket(n: int) -> str:\n    return format(n, "04d")\n',
                  [([42], "0042"), ([7], "0007"), ([1234], "1234")], [[0], [99999]],
                  require=["format"],
                  grammar="""
## Building blocks
- **Built-in format:** `format(value, spec)`
- **Zero-pad to 4 digits:** the spec `"04d"`. Longer numbers aren't cut off.
"""),
                P("py-percent", "As a Percentage", "def percent(part: int, whole: int) -> str:",
                  'Return `part / whole` as a percentage with one decimal place. `1, 3` → `"33.3%"`.',
                  'def percent(part: int, whole: int) -> str:\n    return f"{part / whole:.1%}"\n',
                  [([1, 3], "33.3%"), ([1, 2], "50.0%"), ([3, 3], "100.0%")], [[0, 5], [2, 3], [7, 8]],
                  grammar="""
## Building blocks
- **Percent format:** `.1%` multiplies by 100, shows 1 decimal place and adds `%`.
- **Expressions inside braces:** `f"{part / whole:.1%}"`
"""),
                P("py-receipt-line", "Receipt Line", "def receipt_line(item: str, price: float) -> str:",
                  'Return a 20-character receipt line: the item name left-aligned in 12 characters, then the price right-aligned in 8 characters with 2 decimals.\n\n`"Tea", 2.5` → `"Tea             2.50"`.',
                  'def receipt_line(item: str, price: float) -> str:\n    return f"{item:<12}{price:>8.2f}"\n',
                  [(["Tea", 2.5], "Tea             2.50"), (["Sandwich", 12], "Sandwich       12.00")], [["", 0], ["Cake", 3.456]],
                  difficulty="Medium",
                  grammar="""
## Building blocks
- **Left-align in a width:** `{item:<12}`
- **Right-align a float with 2 decimals:** `{price:>8.2f}`
- **Two fields side by side:** `f"{item:<12}{price:>8.2f}"`
"""),
            ],
            quiz=[
                Q("What does this print?", "005|  5|5.00", "5|5|5.00", "005|5  |5.0", "error", code="n = 5\nprint(f'{n:03d}|{n:>3}|{n:.2f}')", predict=True,
                  why="`03d` pads with zeros, `>3` right-aligns, `.2f` shows two decimals."),
                Q("What does this print?", "1,000,000", "1000000", "1.000.000", "1e6", code="print(format(1000000, ','))", predict=True,
                  why="The `,` spec adds thousands separators."),
            ],
        ),
        # ------------------------------------------------------------------ ord / chr
        dict(
            id="char-codes",
            title="Character codes: ord and chr",
            builtins=["ord", "chr"],
            intro="""
Every character has a number (its Unicode **code point**).

- `ord("a")` → `97`, `ord("A")` → `65`, `ord("0")` → `48`
- `chr(97)` → `"a"`

The letters are consecutive, so `ord(c) - ord("a")` turns `'a'…'z'` into `0…25`. That trick shows up all over the Blind 75.
""",
            problems=[
                P("py-char-code", "Character Code", "def code(c: str) -> int:",
                  "Return the Unicode code point of the single character `c`.",
                  "def code(c: str) -> int:\n    return ord(c)\n",
                  [(["a"], 97), (["A"], 65), (["0"], 48)], [[" "], ["z"], ["€"]],
                  require=["ord"],
                  grammar="""
## Building blocks
- **Character to number:** `ord(c)`
"""),
                P("py-next-letter", "Next Letter", "def next_letter(c: str) -> str:",
                  'Return the letter after `c` in the alphabet, wrapping `"z"` around to `"a"`. `c` is a lower-case letter.',
                  'def next_letter(c: str) -> str:\n    return chr((ord(c) - ord("a") + 1) % 26 + ord("a"))\n',
                  [(["a"], "b"), (["m"], "n"), (["z"], "a")], [["y"], ["q"]],
                  require=["ord", "chr"],
                  hints=["Turn the letter into 0–25, add 1, wrap with `% 26`, then turn it back."],
                  grammar="""
## Building blocks
- **Letter to 0-25:** a letter's code minus the code of `"a"`.
- **Wrap around:** `% 26`
- **Back to a letter:** `chr(n + ord("a"))`
"""),
                P("py-alphabet-position", "Alphabet Position", "def position_in_alphabet(c: str) -> int:",
                  'Return the position of letter `c` in the alphabet, starting at 1 and ignoring case. `"a"` and `"A"` → `1`, `"z"` → `26`.',
                  'def position_in_alphabet(c: str) -> int:\n    return ord(c.lower()) - ord("a") + 1\n',
                  [(["a"], 1), (["Z"], 26), (["m"], 13)], [["B"], ["y"]],
                  grammar="""
## Building blocks
- **Ignore case:** `c.lower()` first.
- **Distance from 'a':** `ord(c) - ord("a")`, then `+ 1` to start counting at 1.
"""),
            ],
            quiz=[
                Q("What does this print?", "c", "99", "b", "error", code="print(chr(ord('a') + 2))", predict=True,
                  why="`ord('a')` is 97; 99 is 'c'."),
                Q("What does `ord('b') - ord('a')` give?", "1", "2", "'1'", "98", why="Consecutive letters differ by one."),
            ],
        ),
        # ------------------------------------------------------------------ character tests
        dict(
            id="char-tests",
            title="Character tests: isdigit, isalpha, …",
            builtins=[],
            intro="""
These methods return `True`/`False` about **every** character in the string (and `False` for an empty string):

- `.isdigit()`: only digits 0–9
- `.isalpha()`: only letters
- `.isalnum()`: only letters and digits
- `.isspace()`: only whitespace
- `.isupper()` / `.islower()`: all the letters are upper / lower case
""",
            problems=[
                P("py-valid-pin", "Valid PIN", "def valid_pin(pin: str) -> bool:",
                  "A PIN is valid if it is exactly 4 or 6 characters long and contains only digits.",
                  "def valid_pin(pin: str) -> bool:\n    return (len(pin) == 4 or len(pin) == 6) and pin.isdigit()\n",
                  [(["1234"], True), (["12345"], False), (["12a4"], False)], [["123456"], [""], ["0000"], ["1234567"], ["-123"]],
                  require=[".isdigit"],
                  grammar="""
## Building blocks
- **Only digits:** `pin.isdigit()`
- **Is it one of several values?** `x in (1, 2)`
- **Brackets around the `or`:** `(a or b) and c`
"""),
                P("py-is-word", "Just Letters", "def is_word(s: str) -> bool:",
                  "Return `True` if `s` is non-empty and made only of letters.",
                  "def is_word(s: str) -> bool:\n    return s.isalpha()\n",
                  [(["hello"], True), (["hello!"], False), ([""], False)], [["two words"], ["Ünïcödé"], ["abc1"]],
                  require=[".isalpha"],
                  grammar="""
## Building blocks
- **Only letters:** `s.isalpha()`, which is already `False` for `""`.
"""),
                P("py-is-shouting", "Is It Shouting?", "def is_shouting(s: str) -> bool:",
                  'Return `True` if `s` has at least one letter and all its letters are capitals. `"STOP!"` → `True`, `"123"` → `False`.',
                  "def is_shouting(s: str) -> bool:\n    return s.isupper()\n",
                  [(["STOP!"], True), (["Stop"], False), (["123"], False)], [["HI THERE"], [""], ["A1"]],
                  require=[".isupper"],
                  grammar="""
## Building blocks
- **All letters upper case (and at least one letter):** `s.isupper()`. Digits and punctuation are ignored.
"""),
            ],
            quiz=[
                Q("What does this print?", "False True False", "True True False", "False True True", "False False False",
                  code="print(''.isdigit(), '42'.isdigit(), '4.2'.isdigit())", predict=True,
                  why="Empty strings are never digits, and '.' isn't a digit."),
                Q("What does this print?", "True", "False", code="print('ab12'.isalnum())", predict=True, why="Letters and digits only."),
            ],
        ),
        # ------------------------------------------------------------------ repr / ascii
        dict(
            id="repr-ascii",
            title="repr and ascii: text for programmers",
            builtins=["repr", "ascii"],
            intro="""
`str(x)` is text for people. `repr(x)` is text for programmers: it shows exactly what the value is.

```python
print(str("hi"))    # hi
print(repr("hi"))   # 'hi'      (quotes show it's a string)
print(repr("a\\tb")) # 'a\\tb'   (invisible characters made visible)
```

`ascii(x)` is like `repr`, but replaces any non-ASCII character with an escape: `ascii("café")` is `'caf\\xe9'`.

Tip: when debugging, `print(repr(s))` reveals stray spaces and new lines.
""",
            problems=[
                P("py-show-repr", "Show the repr", "def show(s: str) -> str:",
                  "Return the `repr` of `s`: the text you'd type to create it, including quotes. `hi` → `'hi'`.",
                  "def show(s: str) -> str:\n    return repr(s)\n",
                  [(["hi"], "'hi'"), ([""], "''"), (["it's"], "\"it's\"")], [["tab\there"], ["new\nline"]],
                  require=["repr"],
                  grammar="""
## Building blocks
- **Programmer's view of a value:** `repr(s)`. Note Python picks double quotes when the text contains a `'`.
"""),
                P("py-ascii-safe", "ASCII-Safe Text", "def ascii_safe(s: str) -> str:",
                  "Return the `ascii` representation of `s`, which escapes every non-ASCII character.",
                  "def ascii_safe(s: str) -> str:\n    return ascii(s)\n",
                  [(["café"], "'caf\\xe9'"), (["plain"], "'plain'")], [["naïve"], ["日本"], [""]],
                  require=["ascii"],
                  grammar="""
## Building blocks
- **repr with escapes:** `ascii(s)` turns `é` into `\\xe9` (and wider characters into `\\u…`).
"""),
                P("py-has-hidden-whitespace", "Hidden Whitespace", "def has_hidden(s: str) -> bool:",
                  "Return `True` if `s` has whitespace at the start or end (a common bug in user input).",
                  "def has_hidden(s: str) -> bool:\n    return s != s.strip()\n",
                  [(["ok"], False), (["ok "], True), (["\tok"], True)], [[""], ["in side"], ["\n"]],
                  grammar="""
## Building blocks
- **Compare with the trimmed version:** `s != s.strip()`
- **Debugging tip:** `print(repr(s))` would show `'ok '` so you can see the space.
"""),
            ],
            quiz=[
                Q("What does this print?", "5 '5'", "5 5", "'5' '5'", "'5' 5", code="print(str('5'), repr('5'))", predict=True,
                  why="`repr` adds the quotes that show it's a string."),
                Q("What does this print?", "'\\xe9'", "'é'", "e", "233", code="print(ascii('é'))", predict=True,
                  why="`ascii` escapes non-ASCII characters."),
            ],
        ),
    ],
)
