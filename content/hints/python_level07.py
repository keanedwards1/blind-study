# Hints for Learn Python level 7 (Classes & the standard library), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ classes
    "py-class-counter": [
        "An object needs to remember two things: where it started (for `reset`) and its current value.",
        "`__init__` runs when the object is created. Store values on `self` there (`self.something = ...`) so the other methods can see them.",
        "`increment` adds one to the current value and returns it. `reset` copies the starting value back into the current value and returns nothing.",
    ],
    "py-class-bank-account": [
        "Each account keeps its own balance, starting at 0, stored on `self` in `__init__`.",
        "`deposit` adds to the balance. `withdraw` must first check whether there's enough money.",
        "If the amount is too big, return `False` without changing anything; otherwise subtract it and return `True`. `balance()` just returns the stored number.",
    ],
    "py-class-stack": [
        "A list stored on `self` makes a good stack: the end of the list is the top.",
        "`append` pushes onto the top and `pop` removes from the top. The last item is `[-1]`.",
        "`pop` and `peek` must return `None` for an empty stack instead of crashing, so check whether the list is empty first.",
    ],
    # ------------------------------------------------------------------ special methods
    "py-point-class": [
        "Special methods (with double underscores) let your class work with built-in operations.",
        "`__repr__` returns the text that `repr(...)` shows. `__eq__(self, other)` decides what `==` means for your objects.",
        "In `__eq__`, compare both coordinates. Also check that the other value is a `Point` at all (`isinstance`), so comparing with something else gives `False` instead of crashing.",
    ],
    "py-sortable-money": [
        "Sorting only needs to know what \"less than\" means for your objects.",
        "Define `__lt__(self, other)` to compare the cents.",
        "For the repr, split the cents into dollars and cents with `//` and `%`, and pad the cents to two digits (`02d`).",
    ],
    "py-vector-add": [
        "`*components` collects any number of numbers into a tuple; store it as a list.",
        "`__add__(self, other)` defines `+`. It should return a *new* `Vector`, not change either existing one.",
        "Pair up the components with `zip`, add each pair, and pass the sums to `Vector(...)` (unpacked with `*`). `__len__` returns how many components there are.",
    ],
    # ------------------------------------------------------------------ property, staticmethod, classmethod
    "py-temperature-property": [
        "A property looks like a plain attribute from outside (`t.fahrenheit`), but it's really a method that calculates the value.",
        "Put `@property` above a method to make it a getter. A second method with the same name, decorated with `@<that name>.setter`, handles assignment.",
        "Only store `celsius`. The getter converts it to Fahrenheit; the setter converts a Fahrenheit value back and stores it as `celsius`.",
    ],
    "py-date-from-string": [
        "A classmethod receives the class itself (`cls`) instead of an object, so it can build new objects: an alternative way to construct one.",
        "In `from_string`, split the text on `-`, convert the three parts to ints, and return `cls(...)` with them.",
        "A staticmethod gets neither `self` nor `cls`; it's a plain function kept inside the class. Leap years: divisible by 4, except centuries, unless divisible by 400.",
    ],
    # ------------------------------------------------------------------ inheritance
    "py-animal-sounds": [
        "A subclass (`class Dog(Animal):`) gets everything from its parent class automatically, including `__init__`.",
        "So `Dog` and `Cat` only need their own version of `speak`, which replaces (overrides) the parent's.",
        "Each `speak` uses `self.name`, which the parent's `__init__` stored.",
    ],
    "py-square-super": [
        "A square is a rectangle whose width and height are equal.",
        "`super().__init__(...)` runs the parent class's `__init__` from inside the child's.",
        "`Square.__init__` takes one side and passes it to the parent twice. `area` is inherited, so you don't write it again.",
    ],
    "py-sentinel-default": [
        "You need a default value that no caller could ever pass by accident, since even `None` is a valid default here.",
        "`object()` creates a brand-new, unique object. Store one in a module-level name and use it as the parameter's default.",
        "Check with `is` whether the default is still your sentinel: if it is, nothing was passed, so raise `KeyError`; otherwise return the default.",
    ],
    # ------------------------------------------------------------------ attribute tools
    "py-read-field": [
        "You have the attribute's name as text, so `obj.name` won't work.",
        "`getattr(obj, \"x\")` reads an attribute by its name.",
        "A third argument to `getattr` is returned when the attribute doesn't exist.",
    ],
    "py-fill-fields": [
        "You need to set attributes whose names you only know as text.",
        "`setattr(obj, name, value)` sets an attribute by name.",
        "Loop over the dict's `.items()` and set each one.",
    ],
    "py-has-all-fields": [
        "`hasattr(obj, name)` checks a single attribute.",
        "You need it to be true for every name in the list.",
        "Combine the checks with `all(...)` over a generator.",
    ],
    "py-strip-private": [
        "`vars(obj)` is a dict of the object's own attributes.",
        "`delattr(thing, \"field\")` deletes an attribute when you only have its name as text.",
        "Changing a dict while looping over it causes an error, so loop over a *copy* of the names (`list(...)`), delete the ones starting with `_`, then return `vars(obj)`.",
    ],
    "py-public-methods": [
        "`dir(obj)` lists every name an object has, including lots of built-in ones starting with `_`.",
        "Keep only the names that don't start with an underscore.",
        "`dir` already returns them in alphabetical order, so a list comprehension with a condition is enough.",
    ],
    # ------------------------------------------------------------------ collections
    "py-most-common-letter": [
        "`Counter(text)` counts every character for you.",
        "`.most_common(1)` returns a list holding the single most common `(item, count)` pair. Ties go to whichever was seen first.",
        "Take the first pair from that list, then its first part (the character).",
    ],
    "py-anagram-groups-dd": [
        "Anagrams have the same letters, so sorting each word's letters gives the same key for every anagram.",
        "`defaultdict(list)` creates an empty list automatically the first time a key is used.",
        "Join the sorted letters into a string to use as the key, and append each word under its key. Return the dict's values as a list.",
    ],
    "py-recent-items": [
        "A `deque` with `maxlen=k` throws away its oldest item whenever it gets too full.",
        "Create it with that limit, then append every item in order.",
        "Whatever is left at the end is the last `k` items; convert it to a list.",
    ],
    "py-namedtuple-points": [
        "`namedtuple(\"Point\", \"x y\")` makes a tiny class whose fields are read by name: `p.x`, `p.y`.",
        "Build a `Point` from each pair (unpacking with `*`).",
        "Find the furthest with `max` and a key of x² + y². You don't need the square root just to compare distances. Return its coordinates as a list.",
    ],
    # ------------------------------------------------------------------ heapq and bisect
    "py-k-smallest": [
        "A heap always keeps its smallest item at the front, ready to take.",
        "Copy the list (so the input isn't changed), turn the copy into a heap with `heapify`, then take items one by one with `heappop`.",
        "Pop `k` times, but never more times than there are items.",
    ],
    "py-insert-sorted": [
        "The list is already sorted, so the new item belongs in one specific place.",
        "`bisect` finds that place quickly; `insort(list, x)` finds it and inserts in one step.",
        "Call it on `items` (it changes the list in place) and return nothing.",
    ],
    "py-grade-bisect": [
        "`bisect_right(cutoffs, score)` returns how many cut-offs are less than or equal to the score.",
        "That count (0 to 4) can be used as an index into the grades written from worst to best.",
        "A score of exactly 70 should be a C, which is why it's `bisect_right` rather than `bisect_left`.",
    ],
    # ------------------------------------------------------------------ itertools
    "py-all-pairs": [
        "`combinations(items, 2)` produces every pair once, in the list's order.",
        "Each pair comes out as a tuple, but the task wants lists.",
        "Convert each pair with `list(...)` inside a list comprehension.",
    ],
    "py-running-max": [
        "`accumulate(items, function)` combines the items left to right and gives every intermediate result.",
        "With `max` as the function, each result is the largest value seen so far.",
        "Wrap the result in `list(...)`.",
    ],
    "py-run-lengths": [
        "`itertools.groupby(text)` splits the text into runs of identical characters, giving `(character, run)` pairs.",
        "Each run is an iterator, not a list, so count it by converting it with `list(...)` and taking its `len`.",
        "Build `\"<char><count>\"` for each run and join them all with an empty string.",
    ],
    "py-every-outfit": [
        "`product(a, b)` gives every pairing of an item from `a` with an item from `b`, looping over `a` on the outside.",
        "Each pairing is a `(top, bottom)` tuple.",
        "Format each one as `\"top + bottom\"` with an f-string inside a list comprehension.",
    ],
    # ------------------------------------------------------------------ functools and math
    "py-memo-fib": [
        "Plain recursive Fibonacci recalculates the same values an enormous number of times.",
        "`@cache` on a function remembers each result, so every value is calculated only once.",
        "Put `@cache` on the line above `def`. The base cases are 0 and 1, which return themselves.",
    ],
    "py-product-reduce": [
        "`reduce(function, items, start)` combines the items one at a time, starting from `start`.",
        "The function takes the running result and the next item, and returns them multiplied.",
        "Start at 1, so an empty list gives 1.",
    ],
    "py-largest-number": [
        "Normal number order doesn't work: 9 should come before 34 here.",
        "Compare pairs as text: put `a` before `b` if `a + b` (joined as strings) is bigger than `b + a`.",
        "Turn that comparison into a sort key with `functools.cmp_to_key`, sort the numbers as strings, and join them. If the result starts with `0`, every number was 0, so return `\"0\"`.",
    ],
    "py-gcd-of-list": [
        "`math.gcd(a, b)` finds the greatest common divisor of two numbers.",
        "The GCD of a whole list can be built up two numbers at a time.",
        "`reduce` does exactly that, using `math.gcd` as the combining function.",
    ],
    "py-perfect-square": [
        "`n ** 0.5` uses floats, which lose precision for huge numbers.",
        "`math.isqrt(n)` gives the exact whole-number square root (rounded down).",
        "Square it back up; if you get `n` again, it's a perfect square.",
    ],
    # ------------------------------------------------------------------ files
    "py-count-lines": [
        "`with open(path) as f:` opens the file and closes it again automatically.",
        "Looping over a file object gives one line at a time.",
        "Count the lines while looping, or use `sum` with a 1 for each line.",
    ],
    "py-word-count-file": [
        "Read the whole file into one string with `.read()`.",
        "`.split()` with no argument splits on any whitespace, including new lines.",
        "Count the pieces with `len`.",
    ],
    "py-write-lines": [
        "Open the file in write mode by passing `\"w\"` as the second argument to `open`.",
        "`f.write(text)` doesn't add a new line for you.",
        "Write each line followed by `\"\\n\"`, inside a `with` block so the file is saved and closed properly.",
    ],
}
