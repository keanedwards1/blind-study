# Hints for Learn Python level 2 (Strings), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ len and indexing
    "py-string-length": [
        "You want the number of characters in the text, counting spaces and punctuation too.",
        "The built-in `len(...)` gives the length of a string (and of lists, and more).",
        "Return what `len` gives you for `s`. An empty string has length 0.",
    ],
    "py-first-and-last": [
        "Every character in a string has a position number (an index), starting from 0 for the first character.",
        "Square brackets read one character: `word[0]` is the first. Negative positions count from the end, so `word[-1]` is the last.",
        "Read both characters and join them with `+`. With a one-letter string, the first and last characters are the same letter, so you get it twice.",
    ],
    "py-middle-char": [
        "For an odd length like 5, the middle position is 2 (positions 0, 1, **2**, 3, 4).",
        "That middle position is the length divided by 2, using whole-number division `//` so you get an int (indexes must be whole numbers).",
        "Work out the middle index from `len(s)`, then use it inside square brackets.",
    ],
    "py-repeat-text": [
        "Repeating text `n` times is like multiplying it.",
        "In Python, a string times a number repeats it: `\"ha\" * 2` gives `\"haha\"`.",
        "Return `s` multiplied by `n`. If `n` is 0 you get an empty string automatically.",
    ],
    # ------------------------------------------------------------------ slicing
    "py-first-three": [
        "A slice takes a stretch of a string: `text[start:stop]` goes from `start` up to, but not including, `stop`.",
        "Leave out `start` and the slice begins at the very beginning.",
        "Slices never crash when they go past the end; they just stop at the end. So a short string comes back whole.",
    ],
    "py-reverse-text": [
        "A slice can have a third number, the step: `text[start:stop:step]`.",
        "A step of `-1` walks backwards through the string.",
        "Leave start and stop empty so the slice covers the whole string, and use a step of -1.",
    ],
    "py-every-other": [
        "You want positions 0, 2, 4, …: start at the beginning and jump 2 each time.",
        "The third slice number is the step size.",
        "Leave start and stop empty (the whole string) and use a step of 2.",
    ],
    "py-drop-ends": [
        "You want everything from position 1 up to, but not including, the last character.",
        "`-1` as a slice end means \"stop just before the last character\".",
        "Slice from 1 to -1. For strings shorter than 2, that slice is already empty, so no `if` is needed.",
    ],
    "py-capitalise-first": [
        "Split the job in two: the first character (made upper case) and everything after it (unchanged).",
        "`.upper()` makes text upper case. A slice like `text[:1]` gives the first character, or an empty string if `text` is empty, so it never crashes.",
        "Join the upper-cased first part and the rest with `+`. Using `s[0]` instead would crash on an empty string.",
    ],
    # ------------------------------------------------------------------ case and clean-up
    "py-shout": [
        "Two steps: make every letter a capital, then add an exclamation mark.",
        "`.upper()` returns an upper-case copy of the string.",
        "Join the result and `\"!\"` with `+`.",
    ],
    "py-clean-username": [
        "Two clean-ups: remove the spaces around the outside, and make everything lower case.",
        "`.strip()` removes whitespace from both ends; `.lower()` makes letters lower case.",
        "You can chain methods: each one returns a new string you can call the next method on.",
    ],
    "py-spaces-to-underscores": [
        "You want every space swapped for an underscore.",
        "`.replace(old, new)` swaps every occurrence of `old` for `new`.",
        "Call it with a space as `old` and an underscore as `new`, and return the result.",
    ],
    "py-title-case": [
        "Each word should start with a capital, and every other letter should be lower case.",
        "Strings have a built-in method that does exactly this to every word.",
        "Look for the method named after book and film titles. It also fixes words that were ALL CAPS.",
    ],
    # ------------------------------------------------------------------ searching
    "py-mentions-cat": [
        "\"cat\" might be written `CAT`, `Cat` or `cat`, so first make the case the same everywhere.",
        "`\"x\" in text` is `True` if the text contains `x` anywhere.",
        "Lower-case the text, then check whether `\"cat\"` is in it.",
    ],
    "py-count-vowels": [
        "Upper and lower case both count, so lower-case the text first.",
        "`.count(\"a\")` tells you how many times `a` appears in a string.",
        "Count each of the five vowels and add the counts together. (A loop over `\"aeiou\"` works too.)",
    ],
    "py-is-link": [
        "There are two valid beginnings: `http://` and `https://`.",
        "`.startswith(...)` checks the beginning of a string. It also accepts a tuple of several options, and is `True` if any of them match.",
        "Either pass both beginnings in a tuple, or check each one separately and join the checks with `or`.",
    ],
    "py-find-position": [
        "You need the index where the smaller text first appears.",
        "`.find(sub)` returns that index, or `-1` when it isn't there, which is exactly the required answer.",
        "Return what `.find` gives you. (`.index` would crash when it's missing, so it's the wrong choice here.)",
    ],
    "py-file-extension": [
        "The extension is whatever comes after the **last** dot; a name like `a.tar.gz` has more than one dot.",
        "`.rfind(\".\")` finds the last dot (searching from the right). It returns `-1` if there's no dot at all.",
        "If you found a dot, slice from just after it to the end. Otherwise return an empty string.",
    ],
    # ------------------------------------------------------------------ split and join
    "py-word-count": [
        "First break the text into words, then count them.",
        "`.split()` with nothing in the brackets splits on any run of spaces and ignores extra spaces at the ends.",
        "Count the pieces with `len`. An empty string gives an empty list, so 0 words.",
    ],
    "py-join-commas": [
        "You're gluing a list of words together with `\", \"` between them.",
        "`separator.join(list)` does exactly that. Note that the separator string comes first, before the dot.",
        "Call `join` on the text `\", \"`, passing in the list. An empty list gives an empty string.",
    ],
    "py-csv-fields": [
        "Each comma separates two fields, so the line should be cut at every comma.",
        "`.split(\",\")` cuts at every comma. Unlike `.split()`, it keeps empty fields (that's how `,,` gives `\"\"`).",
        "Return the list `split` gives you. Don't strip the spaces: the task says to keep them.",
    ],
    "py-swap-name": [
        "Break the name into its two words, then put them back in the other order.",
        "`.split()` gives you a list of two words, and you can unpack it straight into two variables: `a, b = ...`.",
        "Build the result as the last name, then `\", \"`, then the first name.",
    ],
    "py-snake-to-camel": [
        "Split the text at the underscores. The first word stays as it is; every word after it gets a capital first letter.",
        "`.split(\"_\")` gives the words. `.capitalize()` makes the first letter upper case and the rest lower.",
        "Keep the first word, capitalise the rest, and glue everything together with `\"\".join(...)` (join with nothing between).",
        "A single word with no underscores should come back unchanged.",
    ],
    # ------------------------------------------------------------------ formatting
    "py-introduce": [
        "You're building a sentence with two values slotted in.",
        "An f-string (a string with `f` before the opening quote) lets you put values inside curly braces: `f\"I am {name}\"`.",
        "Write the sentence as an f-string with both values in braces. Numbers are converted to text for you.",
    ],
    "py-two-decimals": [
        "You need text with exactly two digits after the point, even for whole numbers (`2` → `\"2.00\"`).",
        "Inside an f-string's braces you can add a format after a colon. `.2f` means \"a float with 2 decimal places\".",
        "Put `x` in the braces followed by that format. It rounds for you.",
    ],
    "py-zero-pad": [
        "The number must always be 4 characters wide, with zeros filling the front.",
        "`format(value, spec)` formats a value using a format spec (the same mini-language as f-strings).",
        "In the spec, `0` means \"pad with zeros\", `4` is the width and `d` means a whole number. Put those together.",
    ],
    "py-percent": [
        "First divide `part` by `whole` to get a fraction like 0.333…",
        "The `%` format type multiplies by 100 and adds a percent sign for you. `.1%` also rounds to one decimal place.",
        "Put the division inside an f-string's braces, followed by the format. Don't multiply by 100 yourself as well.",
    ],
    "py-receipt-line": [
        "Two fixed-width columns: the name padded to 12 characters on the left, the price padded to 8 on the right.",
        "In an f-string format, `<` means align left and `>` means align right, followed by the width.",
        "For the price, combine right-alignment, width 8 and two decimal places in one format. Put both formatted values next to each other with nothing between them.",
    ],
    # ------------------------------------------------------------------ ord and chr
    "py-char-code": [
        "Every character has a number code (its Unicode code point). For example `A` is 65.",
        "`ord(...)` gives the code of a single character.",
        "Return `ord` of `c`.",
    ],
    "py-next-letter": [
        "Turn the letter into a number, add one, and turn it back into a letter. `ord` gives the number and `chr` turns a number back into a character.",
        "To wrap `z` round to `a`, first work out the letter's position from 0 to 25 (its code minus the code of `\"a\"`).",
        "Add one to that position, use `% 26` so 26 wraps back to 0, then add the code of `\"a\"` back on and convert with `chr`.",
    ],
    "py-alphabet-position": [
        "Lower-case the letter first, so `A` and `a` give the same answer.",
        "Letters have consecutive codes, so the code of a letter minus the code of `\"a\"` is its position counting from 0.",
        "Add one, because the alphabet positions here start at 1.",
    ],
    # ------------------------------------------------------------------ character tests
    "py-valid-pin": [
        "Two rules must both hold: the length is 4 or 6, and every character is a digit.",
        "`.isdigit()` is `True` only when the string is non-empty and made only of digits.",
        "Combine the length check (4 *or* 6) and the digit check with `and`. Put brackets round the length check so the `or` is grouped first.",
    ],
    "py-is-word": [
        "You need to know whether every character is a letter.",
        "`.isalpha()` checks exactly that, and it's `False` for an empty string.",
        "Return the result of calling it on `s`.",
    ],
    "py-is-shouting": [
        "\"Shouting\" means there's at least one letter, and none of the letters are lower case. Digits and punctuation don't matter.",
        "`.isupper()` follows exactly those rules: it ignores non-letters but needs at least one capital letter.",
        "Return what `isupper` says. That's why `\"123\"` is `False`: it has no letters at all.",
    ],
    # ------------------------------------------------------------------ repr and ascii
    "py-show-repr": [
        "The \"repr\" of a value is how you'd write it in code: for text, that includes the quotes.",
        "The built-in `repr(...)` produces it.",
        "Return `repr` of `s`. Notice Python picks the kind of quotes for you.",
    ],
    "py-ascii-safe": [
        "ASCII is the basic set of English characters. Anything else (like `é` or an emoji) needs to be written as an escape code.",
        "The built-in `ascii(...)` works like `repr`, but escapes every non-ASCII character.",
        "Return `ascii` of `s`.",
    ],
    "py-has-hidden-whitespace": [
        "If there's whitespace at either end, removing it changes the text.",
        "`.strip()` returns a copy without whitespace at either end.",
        "Compare the original text with its stripped version: if they're different, there was hidden whitespace.",
    ],
}
