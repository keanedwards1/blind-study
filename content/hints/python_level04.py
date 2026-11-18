# Hints for Learn Python level 4 (Dicts, sets & tuples), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ dict basics
    "py-price-lookup": [
        "A dict maps keys (here, item names) to values (their prices).",
        "`d[key]` crashes with a `KeyError` when the key is missing. `.get(key, default)` returns the default instead.",
        "Use `.get` with 0 as the default.",
    ],
    "py-word-frequencies": [
        "Build a dict where each word is a key and its value is how many times you've seen it so far.",
        "Start with an empty dict `{}` and loop over the words.",
        "For each word, look up its current count, using 0 when it isn't there yet (`.get` with a default), add one, and store the new count back under the word.",
    ],
    "py-invert-dict": [
        "Each key/value pair needs to go into a new dict the other way round.",
        "`.items()` gives you each key and value together: `for k, v in d.items():`.",
        "Store each pair the other way round in a new, empty dict, using the value as the new key.",
    ],
    "py-first-repeat": [
        "As you read the words, remember which ones you've already met.",
        "Checking `word in seen` is instant for a dict or a set, however many words there are.",
        "For each word: if you've seen it, return it straight away; otherwise remember it. If the loop finishes, nothing repeated, so return `\"\"`.",
    ],
    # ------------------------------------------------------------------ dict methods
    "py-total-stock": [
        "You only need the quantities, not the item names.",
        "`.values()` gives all the values of a dict.",
        "Add them up with `sum(...)`. An empty dict gives 0.",
    ],
    "py-sorted-keys": [
        "You want the keys, in alphabetical order, as a list.",
        "Looping over a dict (or passing it to a function that loops) goes over its keys.",
        "`sorted(...)` returns a new sorted list, so passing the dict to it gives its keys in order.",
    ],
    "py-merge-settings": [
        "Start with a copy of the defaults, then let the overrides replace matching keys.",
        "`dict(d)` makes a new copy of a dict, so changes don't affect the original.",
        "`.update(other)` copies every key and value from `other` into a dict, replacing any that are already there.",
    ],
    "py-pop-key": [
        "You need to remove a key and keep its value, without crashing if the key isn't there.",
        "`.pop(key, default)` removes the key and returns its value, or returns the default if the key is missing.",
        "Use `None` as the default, then return the value together with the dict, as a list.",
    ],
    "py-group-by-initial": [
        "Build a dict from first letter to a list of words.",
        "`.setdefault(key, [])` returns the list stored under that key, creating an empty one first if there isn't one yet.",
        "For each word, get its first letter's list with `setdefault` and append the word to it. Dicts remember insertion order, so the order is kept.",
    ],
    "py-zip-to-dict": [
        "Pair each key with the value at the same position.",
        "`zip(keys, values)` produces exactly those pairs.",
        "`dict(...)` can build a dict straight from a sequence of `(key, value)` pairs.",
    ],
    # ------------------------------------------------------------------ sets
    "py-unique-count": [
        "A set keeps only one copy of each value.",
        "Turning the list into a set with `set(...)` throws away the duplicates.",
        "Then count what's left with `len`.",
    ],
    "py-dedupe-keep-order": [
        "A set forgets the original order, so you can't simply convert the list to a set.",
        "Use a set only to *remember* what you've already kept, and build a new list for the result.",
        "Loop in order: if the item isn't in the set yet, add it to the set *and* append it to the result list.",
    ],
    "py-unique-letters-set": [
        "A string is a sequence of characters.",
        "`set(...)` takes any sequence and keeps one copy of each item.",
        "Return the set made from `word`.",
    ],
    # ------------------------------------------------------------------ set operations
    "py-in-both": [
        "You want the values the two lists have in common (the intersection).",
        "Convert both lists to sets first.",
        "The `&` operator gives the values that are in both sets.",
    ],
    "py-in-either": [
        "You want every value that's in one list, the other, or both (the union).",
        "Convert both lists to sets first.",
        "The `|` operator combines two sets.",
    ],
    "py-only-in-first": [
        "You want the invited guests minus the ones who arrived.",
        "With sets, `-` gives the items in the first set that aren't in the second (the difference).",
        "A set has no order, so pass the result to `sorted(...)` to get an alphabetical list.",
    ],
    "py-in-exactly-one": [
        "You want values in one list or the other, but not in both.",
        "With sets, the `^` operator (symmetric difference) gives exactly that.",
        "Sort the result to get the increasing order the task asks for.",
    ],
    "py-is-subset": [
        "The question is whether everything in `needed` also appears in `have`. Quantities don't matter, which is a clue to use sets.",
        "With sets, `a <= b` is `True` when every item of `a` is also in `b` (a subset).",
        "Convert both lists to sets and compare them. An empty `needed` is always `True`.",
    ],
    # ------------------------------------------------------------------ tuples
    "py-swap-pair": [
        "A tuple is a fixed group of values written with commas, like `(1, 2)`.",
        "You can return several values separated by commas, and Python packs them into a tuple.",
        "Return the two values in swapped order.",
    ],
    "py-min-max-tuple": [
        "Two answers: the smallest and the largest.",
        "`min(...)` and `max(...)` both work on a whole list.",
        "Return both, separated by a comma, smallest first; that makes a tuple.",
    ],
    "py-head-tail": [
        "Unpacking assigns the items of a sequence to several names at once: `a, b = [1, 2]`.",
        "A star in front of a name collects \"everything else\" into a list: `first, *others = ...`.",
        "Unpack `items` that way, then return the first item and the list of the rest.",
    ],
    "py-distance-tuples": [
        "Unpack each point into its x and y: `x1, y1 = p`.",
        "The distance formula: find the difference in x and in y, square both, add them, then take the square root.",
        "Raising to the power `0.5` is a square root (or use `math.sqrt`). Squaring makes negative differences positive.",
    ],
    "py-tuple-from-list": [
        "A tuple is like a list that can't be changed.",
        "`tuple(...)` builds a tuple from any sequence.",
        "Return the tuple made from `items`.",
    ],
    # ------------------------------------------------------------------ hashing
    "py-distinct-points": [
        "Lists can't go into a set, because they can change (they're not hashable). Tuples can.",
        "Turn each `[x, y]` into an `(x, y)` tuple with `tuple(...)`.",
        "Put the tuples in a set and count it with `len`.",
    ],
    "py-point-counts": [
        "This is word counting, but with points as the keys.",
        "Dict keys must be hashable, so turn each point into a tuple first.",
        "Use the counting pattern: get the current count with a default of 0, add one, and store it back.",
    ],
    "py-same-letter-set": [
        "Only which letters appear matters, not how many times or in what order.",
        "A `frozenset` is a set that can't be changed. Two of them are equal when they hold the same items.",
        "Make a frozenset from each word and compare them with `==`.",
    ],
    "py-group-by-letter-set": [
        "Words belong together when they use the same letters, so the set of letters can be the dict key.",
        "A normal set can't be a dict key (it can change), but a `frozenset` can.",
        "For each word, append it to the list stored under its frozenset (`setdefault` makes the list the first time). Return the dict's values as a list.",
    ],
    "py-hash-equal": [
        "`hash(...)` turns a value into a number that dicts and sets use to find it quickly.",
        "Equal values always have equal hashes.",
        "Compare `hash` of each input with `==`.",
    ],
}
