# Hints for Learn Python level 5 (Functions), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ defaults and keyword arguments
    "py-greet-default": [
        "A parameter can have a default value that's used when the caller leaves it out.",
        "You write the default in the function's first line (its signature): `def f(a, b=\"x\"):`. Parameters with defaults go after the ones without.",
        "Give `greeting` the default `\"Hello\"`, then build the result with an f-string: greeting, comma, space, name, exclamation mark.",
    ],
    "py-power-default": [
        "The second parameter should be optional, using 2 when it isn't given.",
        "Write the default straight into the signature with `=`.",
        "Return the base raised to the power with `**`. Check both calls: with one argument it squares, with two it uses the given power.",
    ],
    "py-fix-mutable-default": [
        "A default value is created only **once**, when the function is defined, not each time it's called. A default list is therefore shared by every call.",
        "The standard fix: make the default `None`, which never changes.",
        "At the start of the function, if the list is `None`, make a brand-new empty list. Use `is None` for the check, so that an empty list the caller passed in is still used.",
    ],
    # ------------------------------------------------------------------ *args and **kwargs
    "py-sum-all": [
        "The function must accept any number of values.",
        "A star before a parameter name (`*nums`) collects all the positional arguments into a tuple.",
        "Once you have the tuple, add it up with `sum`. Calling with no arguments gives 0.",
    ],
    "py-build-profile": [
        "`name` is a normal parameter; every other keyword argument should be collected.",
        "Two stars (`**details`) collect the keyword arguments into a dict.",
        "Build a new dict with `\"name\"` first, then unpack the collected dict into it with `**` inside the braces.",
    ],
    "py-count-arguments": [
        "Collect the positional arguments with `*args` and the keyword ones with `**kwargs`.",
        "`args` arrives as a tuple and `kwargs` as a dict, and `len` works on both.",
        "Return the two counts in a list, positional first.",
    ],
    # ------------------------------------------------------------------ lambda and key=
    "py-sort-by-last-letter": [
        "`sorted` can sort by anything you choose, if you give it a `key` function: it sorts by whatever that function returns.",
        "A `lambda` is a tiny one-line function: `lambda w: something about w`.",
        "Make the key \"the last letter of the word\". Python's sort is stable, so ties keep their original order automatically.",
    ],
    "py-longest-word": [
        "`max` can compare things by a key, just like `sorted`.",
        "The key can be any function, including a built-in like `len`, passed without brackets.",
        "`max` returns the first of several equal items, so ties are handled for you.",
    ],
    "py-sort-by-score": [
        "You need two rules: higher score first, then alphabetical by name for equal scores.",
        "A key can return a tuple; Python compares tuples one item at a time. Negating the score makes higher scores sort first.",
        "Sort the pairs with that key, then pull out just the names (a list comprehension that unpacks each pair).",
    ],
    # ------------------------------------------------------------------ map and filter
    "py-strings-to-ints": [
        "You want to apply the same conversion to every item.",
        "`map(function, items)` applies the function to each item. `int` is itself a function, so you can pass it directly (no brackets).",
        "`map` gives items one at a time; wrap it in `list(...)` to get a list.",
    ],
    "py-squares-map": [
        "`map` needs a function that turns one number into its square.",
        "Write that function inline as a `lambda` that takes `x` and returns `x` multiplied by itself.",
        "Pass the lambda and the list to `map`, then wrap the result in `list(...)`.",
    ],
    "py-filter-evens": [
        "`filter(function, items)` keeps the items for which the function returns `True`.",
        "Write a `lambda` that checks whether a number is even (`% 2` gives 0).",
        "Wrap the result in `list(...)`.",
    ],
    "py-non-empty": [
        "Empty strings are falsy; any other string is truthy.",
        "Passing `None` as `filter`'s function means \"keep only truthy items\".",
        "Wrap the result in `list(...)`.",
    ],
    # ------------------------------------------------------------------ comprehensions
    "py-squares-comp": [
        "A list comprehension builds a list in one line: `[expression for item in items]`.",
        "The expression is what each new item should be; here, the number times itself.",
        "Write the comprehension and return it.",
    ],
    "py-positive-doubles": [
        "A comprehension can filter as it goes: `[expression for item in items if condition]`.",
        "The condition keeps only positive numbers; the expression doubles them.",
        "Zero isn't positive, so it's skipped.",
    ],
    "py-word-lengths": [
        "A dict comprehension uses braces and a colon: `{key: value for item in items}`.",
        "Here the key is the word and the value is its length.",
        "Repeated words just overwrite the same key with the same length.",
    ],
    "py-length-set": [
        "A set comprehension uses braces without a colon: `{expression for item in items}`.",
        "The expression is each word's length; the set removes repeats for you.",
        "Return the set.",
    ],
    "py-sum-odd-squares": [
        "A generator expression is like a list comprehension in round brackets. Inside `sum(...)` you don't even need the extra brackets.",
        "Square each number, but only the odd ones: odd means `% 2` leaves 1, which is truthy.",
        "Put the expression and the `if` inside `sum(...)`.",
    ],
    "py-flatten-comp": [
        "A comprehension can have two `for` parts, written in the same order as nested loops.",
        "The first `for` goes over the rows; the second goes over the values in that row.",
        "The expression is just the value itself.",
    ],
    # ------------------------------------------------------------------ recursion
    "py-factorial": [
        "Recursion means a function calling itself on a smaller version of the problem.",
        "Factorial has a natural smaller version: n! = n × (n − 1)!.",
        "Every recursive function needs a base case where it stops calling itself: for 0 and 1 the answer is 1.",
    ],
    "py-recursive-sum": [
        "The sum of a list = its first item + the sum of the rest.",
        "\"The rest\" is a slice from position 1 onward, which is a smaller list.",
        "Base case: an empty list sums to 0. Without it, the function never stops.",
    ],
    "py-recursive-reverse": [
        "Reversing a string = reverse everything after the first character, then put the first character at the end.",
        "Call the function on the string without its first character.",
        "Base case: a string of length 0 or 1 is already reversed.",
    ],
    "py-count-nested": [
        "Each item is either a number (count 1) or a list (count everything inside it).",
        "`isinstance(x, list)` tells you whether something is a list.",
        "Loop over the items: for a number add 1; for a list, add whatever a recursive call on that list returns. An empty list contains 0 numbers.",
    ],
    # ------------------------------------------------------------------ closures
    "py-make-adder": [
        "The outer function doesn't return a number; it returns a *function*.",
        "Define a small function inside `make_adder` that takes `x`. It can use `n` from the outer function: it remembers it (this is called a closure).",
        "Return the inner function itself, without brackets, so you're not calling it.",
    ],
    "py-make-counter": [
        "Each counter needs its own count that survives between calls.",
        "Keep the count as a variable in the outer function and return an inner function that increases it.",
        "To change an outer variable from inside the inner function, declare it with `nonlocal` first. Each call to `make_counter` creates a fresh count.",
    ],
    "py-call-if-callable": [
        "Some inputs are functions (like `len`) and some are plain values (like `5`).",
        "`callable(x)` is `True` when `x` can be called with brackets.",
        "If it's callable, call it with `arg` and return the result; otherwise return `x` unchanged. A conditional expression (`a if test else b`) fits in one line.",
    ],
    # ------------------------------------------------------------------ iterators and generators
    "py-first-or-default": [
        "`iter(items)` makes an iterator: something you can ask for items one at a time.",
        "`next(iterator)` takes the next item. Given a second argument, it returns that instead of crashing when there are no items left.",
        "Make the iterator and ask for its first item, with `default` as the fallback.",
    ],
    "py-first-match": [
        "A generator expression produces matching items lazily: it only does the work when asked.",
        "Write one that yields only the words longer than `n`.",
        "Pass it to `next` with `None` as the fallback. Note the generator needs its own brackets when there's a second argument.",
    ],
    "py-countdown-generator": [
        "A generator is a function that uses `yield` instead of `return`. Each `yield` hands out one value and pauses until the next one is asked for.",
        "Loop from `n` down to 1, yielding each number.",
        "Don't build a list; just yield the numbers one by one. With `n` of 0 it yields nothing.",
    ],
    "py-chunks": [
        "Chunks start at positions 0, size, 2×size, and so on.",
        "`range(0, len(items), size)` gives exactly those starting positions.",
        "For each start, yield the slice from that start to start + size. A slice past the end is just shorter, which handles the last chunk.",
    ],
    # ------------------------------------------------------------------ decorators
    "py-double-result": [
        "A decorator takes a function and returns a new function (a wrapper) to use in its place.",
        "The wrapper should accept any arguments (`*args, **kwargs`) and pass them straight on to the original function.",
        "Inside the wrapper, call the original, double its result and return that. The decorator returns the wrapper.",
    ],
    "py-count-calls": [
        "Functions can carry attributes, just like objects: `greet.uses = 5` stores a number on the function `greet`.",
        "Inside the decorator, after defining the wrapper, set its counting attribute to 0.",
        "Each time the wrapper runs, add one to its attribute, then call and return the original function.",
    ],
}
