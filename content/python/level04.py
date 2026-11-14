# Learn Python, level 4: dicts, sets and tuples.
from _helpers import P, Q

LEVEL = dict(
    n=4,
    title="Dicts, sets & tuples",
    summary="Looking things up by key, keeping unique values, and grouping values that belong together. These three are behind most fast solutions.",
    concepts=[
        # ------------------------------------------------------------------ dict basics
        dict(
            id="dict-basics",
            title="Dictionaries: keys and values",
            builtins=[],
            intro="""
A **dict** maps keys to values: `ages = {"ada": 36, "bo": 4}`.

- Read: `ages["ada"]` → `36`. A missing key raises `KeyError`.
- Safe read: `ages.get("zed", 0)` → `0` when the key is missing.
- Write: `ages["cy"] = 7` adds or replaces.
- Membership: `"ada" in ages` checks the **keys**.
- Lookups are O(1) on average, which is why dicts make slow loops fast.

The **counting pattern**: `counts[x] = counts.get(x, 0) + 1`.
""",
            problems=[
                P("py-price-lookup", "Price Lookup", "def price(prices: Dict[str, int], item: str) -> int:",
                  "Return the price of `item`, or `0` if it isn't in `prices`.",
                  "def price(prices: Dict[str, int], item: str) -> int:\n    return prices.get(item, 0)\n",
                  [([{"tea": 3, "jam": 5}, "jam"], 5), ([{"tea": 3}, "cake"], 0)], [[{}, "x"], [{"a": 0}, "a"]],
                  require=[".get"],
                  grammar="""
## Building blocks
- **Read with a default:** `prices.get(item, 0)`
- **Compare:** `prices[item]` raises `KeyError` if it's missing.
"""),
                P("py-word-frequencies", "Word Frequencies", "def frequencies(words: List[str]) -> Dict[str, int]:",
                  "Return a dict mapping each word to how many times it appears.",
                  "def frequencies(words: List[str]) -> Dict[str, int]:\n    counts = {}\n    for w in words:\n        counts[w] = counts.get(w, 0) + 1\n    return counts\n",
                  [([["a", "b", "a"]], {"a": 2, "b": 1}), ([[]], {})], [[["x"] * 5], [["to", "be", "or", "not", "to", "be"]]],
                  forbid=["Counter"],
                  grammar="""
## Building blocks
- **Empty dict:** `counts = {}`
- **Count one:** `counts[w] = counts.get(w, 0) + 1`
"""),
                P("py-invert-dict", "Swap Keys and Values", "def invert(d: Dict[str, str]) -> Dict[str, str]:",
                  'Return a new dict where each value becomes a key and each key becomes its value. `{"a": "x"}` → `{"x": "a"}`. The values are all different.',
                  "def invert(d: Dict[str, str]) -> Dict[str, str]:\n    out = {}\n    for k, v in d.items():\n        out[v] = k\n    return out\n",
                  [([{"a": "x", "b": "y"}], {"x": "a", "y": "b"}), ([{}], {})], [[{"one": "1"}]],
                  grammar="""
## Building blocks
- **Key and value together:** `for k, v in d.items():`
- **Store the other way round:** `out[v] = k`
"""),
                P("py-first-repeat", "First Repeated Word", "def first_repeat(words: List[str]) -> str:",
                  'Return the first word that appears for the second time as you read left to right, or `""` if none repeats.',
                  'def first_repeat(words: List[str]) -> str:\n    seen = {}\n    for w in words:\n        if w in seen:\n            return w\n        seen[w] = True\n    return ""\n',
                  [([["a", "b", "c", "b", "a"]], "b"), ([["x", "y"]], "")], [[[]], [["z", "z"]]],
                  grammar="""
## Building blocks
- **Remember what you've seen:** a dict (or a set, coming up next).
- **Check before storing:** `if w in seen: return w`, then `seen[w] = True`.
"""),
            ],
            quiz=[
                Q("What does this print?", "0 KeyError", "0 0", "None KeyError", "KeyError KeyError",
                  code="d = {'a': 1}\nprint(d.get('z', 0), end=' ')\ntry:\n    d['z']\nexcept KeyError:\n    print('KeyError')", predict=True,
                  why="`get` returns the default; square brackets raise `KeyError`."),
                Q("What does `'a' in {'x': 'a'}` give?", "False", "True", "error", "'a'", why="`in` checks a dict's keys, not its values."),
            ],
        ),
        # ------------------------------------------------------------------ dict methods
        dict(
            id="dict-methods",
            title="Dict methods and dict()",
            builtins=["dict"],
            intro="""
| | |
|---|---|
| `d.keys()`, `d.values()`, `d.items()` | views of keys, values, and `(key, value)` pairs |
| `d.pop(k)` / `d.pop(k, default)` | remove a key and return its value |
| `d.update(other)` | copy every key from `other` into `d` |
| `d.setdefault(k, [])` | get `d[k]`, creating it with a default first if missing |
| `dict(pairs)` | build a dict from `(key, value)` pairs |
| `dict(zip(keys, values))` | pair up two lists |

Dicts remember the order keys were added. Looping over a dict gives its keys.
""",
            problems=[
                P("py-total-stock", "Total Stock", "def total_stock(stock: Dict[str, int]) -> int:",
                  "Return the sum of all the quantities in `stock`.",
                  "def total_stock(stock: Dict[str, int]) -> int:\n    return sum(stock.values())\n",
                  [([{"apples": 3, "pears": 4}], 7), ([{}], 0)], [[{"x": -1, "y": 1}]],
                  require=[".values"],
                  grammar="""
## Building blocks
- **Just the values:** `stock.values()`
- **Add them:** `sum(...)`
"""),
                P("py-sorted-keys", "Sorted Keys", "def sorted_keys(d: Dict[str, int]) -> List[str]:",
                  "Return the keys of `d` in alphabetical order.",
                  "def sorted_keys(d: Dict[str, int]) -> List[str]:\n    return sorted(d)\n",
                  [([{"b": 1, "a": 2}], ["a", "b"]), ([{}], [])], [[{"z": 0, "m": 0, "a": 0}]],
                  grammar="""
## Building blocks
- **Looping over a dict gives keys:** so `sorted(d)` sorts the keys.
"""),
                P("py-merge-settings", "Merge Settings", "def merge(defaults: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:",
                  "Return a new dict with every key from `defaults`, replaced by the value in `overrides` where one exists. Don't change either input.",
                  "def merge(defaults: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:\n    out = dict(defaults)\n    out.update(overrides)\n    return out\n",
                  [([{"size": 10, "bold": 0}, {"bold": 1}], {"size": 10, "bold": 1}), ([{}, {"a": 1}], {"a": 1})], [[{"a": 1}, {}]],
                  require=["dict", ".update"],
                  grammar="""
## Building blocks
- **Copy a dict:** `dict(defaults)`
- **Copy keys across:** `out.update(overrides)`
- **Shortcut you'll see:** `{**defaults, **overrides}`
"""),
                P("py-pop-key", "Take a Key Out", "def take(d: Dict[str, int], key: str) -> List:",
                  "Remove `key` from `d` and return `[its value, the dict afterwards]`. If the key isn't there, return `[None, d]` unchanged.",
                  "def take(d: Dict[str, int], key: str) -> List:\n    value = d.pop(key, None)\n    return [value, d]\n",
                  [([{"a": 1, "b": 2}, "a"], [1, {"b": 2}]), ([{"a": 1}, "z"], [None, {"a": 1}])], [[{}, "x"]],
                  require=[".pop"],
                  grammar="""
## Building blocks
- **Remove and return, with a default:** `d.pop(key, None)`. Without the default, a missing key raises `KeyError`.
"""),
                P("py-group-by-initial", "Group by First Letter", "def by_initial(words: List[str]) -> Dict[str, List[str]]:",
                  'Group the words by their first letter, keeping their order. `["apple", "bean", "avocado"]` → `{"a": ["apple", "avocado"], "b": ["bean"]}`. No word is empty.',
                  "def by_initial(words: List[str]) -> Dict[str, List[str]]:\n    groups = {}\n    for w in words:\n        groups.setdefault(w[0], []).append(w)\n    return groups\n",
                  [([["apple", "bean", "avocado"]], {"a": ["apple", "avocado"], "b": ["bean"]}), ([[]], {})], [[["x", "y", "x"]]],
                  require=[".setdefault"],
                  grammar="""
## Building blocks
- **Get the list, creating it if missing:** `groups.setdefault(key, [])`
- **Then add to it:** `.append(w)` on what `setdefault` returns.
"""),
                P("py-zip-to-dict", "Two Lists to a Dict", "def to_dict(keys: List[str], values: List[int]) -> Dict[str, int]:",
                  "Pair up `keys[i]` with `values[i]` in a dict. The lists are the same length.",
                  "def to_dict(keys: List[str], values: List[int]) -> Dict[str, int]:\n    return dict(zip(keys, values))\n",
                  [([["a", "b"], [1, 2]], {"a": 1, "b": 2}), ([[], []], {})], [[["x", "x"], [1, 2]]],
                  require=["dict", "zip"],
                  grammar="""
## Building blocks
- **Pairs:** `zip(keys, values)`
- **Pairs to dict:** `dict(zip(keys, values))`. A repeated key keeps its last value.
"""),
            ],
            quiz=[
                Q("What does this print?", "['a', 'b']", "[1, 2]", "[('a', 1), ('b', 2)]", "{'a': 1, 'b': 2}", code="print(list({'a': 1, 'b': 2}))", predict=True,
                  why="Iterating a dict gives its keys."),
                Q("What does this print?", "{'x': [1, 2]}", "{'x': [2]}", "{'x': 1}", "error", code="d = {}\nd.setdefault('x', []).append(1)\nd.setdefault('x', []).append(2)\nprint(d)", predict=True,
                  why="The second `setdefault` finds the existing list and returns it."),
            ],
        ),
        # ------------------------------------------------------------------ sets
        dict(
            id="sets",
            title="Sets: unique values",
            builtins=["set"],
            intro="""
A **set** holds unique values with no order: `{1, 2, 3}`.

- `set(items)` removes duplicates. An empty set is `set()`, because `{}` is an empty **dict**.
- `s.add(x)`, `s.remove(x)` (error if missing), `s.discard(x)` (no error).
- `x in s` is O(1), much faster than `x in some_list`, which checks every item.
""",
            problems=[
                P("py-unique-count", "How Many Different", "def distinct(items: List[int]) -> int:",
                  "Return how many different values are in `items`.",
                  "def distinct(items: List[int]) -> int:\n    return len(set(items))\n",
                  [([[1, 2, 2, 3, 3, 3]], 3), ([[]], 0)], [[[7] * 10], [list(range(50))]],
                  require=["set"],
                  grammar="""
## Building blocks
- **Drop duplicates:** `set(items)`
- **Count:** `len(...)`
"""),
                P("py-dedupe-keep-order", "Remove Duplicates, Keep Order", "def dedupe(items: List[int]) -> List[int]:",
                  "Return the items with duplicates removed, keeping the first occurrence of each and the original order.",
                  "def dedupe(items: List[int]) -> List[int]:\n    seen = set()\n    out = []\n    for x in items:\n        if x not in seen:\n            seen.add(x)\n            out.append(x)\n    return out\n",
                  [([[3, 1, 3, 2, 1]], [3, 1, 2]), ([[]], [])], [[[5, 5, 5]], [[1, 2, 3]]],
                  require=["set"],
                  hints=["`set(items)` loses the order. Keep a set of what you've seen and build a list as you go."],
                  grammar="""
## Building blocks
- **Empty set:** `seen = set()`
- **Not seen yet:** `if x not in seen:`
- **Remember it:** `seen.add(x)`
"""),
                P("py-unique-letters-set", "Set of Letters", "def letters(word: str) -> Set[str]:",
                  "Return the **set** of letters in `word`.",
                  "def letters(word: str) -> Set[str]:\n    return set(word)\n",
                  [(["hello"], {"h", "e", "l", "o"}), ([""], set())], [["aaa"], ["abc"]],
                  compare="strict", require=["set"],
                  grammar="""
## Building blocks
- **A string's characters as a set:** `set(word)`
- **This task checks the type:** a list or string won't pass.
"""),
            ],
            quiz=[
                Q("What does `type({})` give?", "dict", "set", "list", "tuple", why="Empty braces make a dict. Use `set()` for an empty set."),
                Q("What does this print?", "3", "5", "error", "4", code="print(len({1, 1, 2, 2, 3}))", predict=True, why="Duplicates are dropped."),
            ],
        ),
        # ------------------------------------------------------------------ set operations
        dict(
            id="set-operations",
            title="Set operations",
            builtins=[],
            intro="""
| | Operator | Method | Gives |
|---|---|---|---|
| Union | `a \\| b` | `a.union(b)` | in either |
| Intersection | `a & b` | `a.intersection(b)` | in both |
| Difference | `a - b` | `a.difference(b)` | in `a` but not `b` |
| Symmetric difference | `a ^ b` | `a.symmetric_difference(b)` | in exactly one |

`a <= b` asks "is every item of `a` also in `b`?" (subset).
""",
            problems=[
                P("py-in-both", "In Both", "def both(a: List[int], b: List[int]) -> Set[int]:",
                  "Return the set of values that appear in both lists.",
                  "def both(a: List[int], b: List[int]) -> Set[int]:\n    return set(a) & set(b)\n",
                  [([[1, 2, 3], [2, 3, 4]], {2, 3}), ([[1], [2]], set())], [[[], []], [[5, 5], [5]]],
                  compare="strict", require=["op:&"],
                  grammar="""
## Building blocks
- **Make sets:** `set(a)`, `set(b)`
- **Intersection:** `&`
"""),
                P("py-in-either", "In Either", "def either(a: List[int], b: List[int]) -> Set[int]:",
                  "Return the set of values that appear in at least one of the lists.",
                  "def either(a: List[int], b: List[int]) -> Set[int]:\n    return set(a) | set(b)\n",
                  [([[1, 2], [2, 3]], {1, 2, 3}), ([[], []], set())], [[[1], []]],
                  compare="strict", require=["op:|"],
                  grammar="""
## Building blocks
- **Union:** `set(a) | set(b)`
"""),
                P("py-only-in-first", "Missing Guests", "def missing(invited: List[str], arrived: List[str]) -> List[str]:",
                  "Return the invited guests who haven't arrived, in alphabetical order.",
                  "def missing(invited: List[str], arrived: List[str]) -> List[str]:\n    return sorted(set(invited) - set(arrived))\n",
                  [([["ada", "bo", "cy"], ["bo"]], ["ada", "cy"]), ([["a"], ["a"]], [])], [[[], ["x"]], [["z", "y"], []]],
                  require=["op:-"],
                  grammar="""
## Building blocks
- **Difference:** `set(invited) - set(arrived)`
- **Sorted list from a set:** `sorted(...)`
"""),
                P("py-in-exactly-one", "In Exactly One", "def exactly_one(a: List[int], b: List[int]) -> List[int]:",
                  "Return, in increasing order, the values that are in one list but not the other.",
                  "def exactly_one(a: List[int], b: List[int]) -> List[int]:\n    return sorted(set(a) ^ set(b))\n",
                  [([[1, 2, 3], [3, 4]], [1, 2, 4]), ([[1], [1]], [])], [[[], [1, 1]], [[5, 6], [7, 8]]],
                  require=["op:^"],
                  grammar="""
## Building blocks
- **Symmetric difference:** `set(a) ^ set(b)`
"""),
                P("py-is-subset", "Have Everything?", "def can_make(needed: List[str], have: List[str]) -> bool:",
                  "Return `True` if every ingredient in `needed` is somewhere in `have` (quantities don't matter).",
                  "def can_make(needed: List[str], have: List[str]) -> bool:\n    return set(needed) <= set(have)\n",
                  [([["egg", "milk"], ["milk", "egg", "flour"]], True), ([["egg"], []], False), ([[], []], True)], [[["a", "a"], ["a"]]],
                  grammar="""
## Building blocks
- **Subset:** `set(needed) <= set(have)`, or `set(needed).issubset(have)`.
"""),
            ],
            quiz=[
                Q("What does this print?", "[1] [1, 2, 3, 4] [4]", "[2, 3] [1, 2, 3, 4] [1, 4]", "[1] [2, 3] [4]", "[1] [1, 2, 3, 4] [3, 4]",
                  code="a, b = {1, 2, 3}, {2, 3, 4}\nprint(sorted(a - b), sorted(a | b), sorted(b - a))", predict=True,
                  why="`-` keeps what's only in the left set; `|` combines both."),
                Q("Which is fastest for checking membership many times?", "x in a_set", "x in a_list", "a_list.count(x) > 0", "a_list.index(x)",
                  why="Sets use hashing, O(1) on average. The list versions scan every item."),
            ],
        ),
        # ------------------------------------------------------------------ tuples
        dict(
            id="tuples",
            title="Tuples and unpacking",
            builtins=["tuple"],
            intro="""
A **tuple** is like a list that can't change: `point = (3, 4)`.

- Unpacking: `x, y = point`. Swapping: `a, b = b, a`.
- A one-item tuple needs a comma: `(5,)`. Without it, `(5)` is just 5.
- Star unpacking collects the rest: `first, *rest = [1, 2, 3]` → `first = 1`, `rest = [2, 3]`.
- `tuple(items)` converts. Functions often return several values as a tuple: `return low, high`.
""",
            problems=[
                P("py-swap-pair", "Swap a Pair", "def swap(a: int, b: int) -> Tuple[int, int]:",
                  "Return the tuple `(b, a)`.",
                  "def swap(a: int, b: int) -> Tuple[int, int]:\n    return b, a\n",
                  [([1, 2], (2, 1)), ([0, 0], (0, 0))], [[-1, 5]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Return a tuple:** `return b, a`. The comma makes the tuple; brackets are optional.
- **This task checks the type:** `[b, a]` is a list, so it won't pass.
"""),
                P("py-min-max-tuple", "Low and High", "def low_high(nums: List[int]) -> Tuple[int, int]:",
                  "Return `(smallest, largest)` as a tuple. `nums` isn't empty.",
                  "def low_high(nums: List[int]) -> Tuple[int, int]:\n    return min(nums), max(nums)\n",
                  [([[3, 1, 2]], (1, 3)), ([[5]], (5, 5))], [[[-1, -9, 4]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Two results at once:** `return min(nums), max(nums)`
"""),
                P("py-head-tail", "Head and Tail", "def head_tail(items: List[int]) -> Tuple:",
                  "Return a tuple `(first item, list of the rest)` using star unpacking. `items` isn't empty.",
                  "def head_tail(items: List[int]) -> Tuple:\n    first, *rest = items\n    return first, rest\n",
                  [([[1, 2, 3]], (1, [2, 3])), ([[9]], (9, []))], [[[0, 0]]],
                  compare="strict", require=["unpack"],
                  grammar="""
## Building blocks
- **Star unpacking:** `first, *rest = items`. `rest` is always a list.
- **Return both:** `return first, rest`
"""),
                P("py-distance-tuples", "Distance Between Points", "def distance(p: Tuple[int, int], q: Tuple[int, int]) -> float:",
                  "`p` and `q` are `(x, y)` tuples. Return the straight-line distance between them: √((x₁−x₂)² + (y₁−y₂)²).",
                  "def distance(p: Tuple[int, int], q: Tuple[int, int]) -> float:\n    (x1, y1), (x2, y2) = p, q\n    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5\n",
                  [([(0, 0), (3, 4)], 5.0), ([(1, 1), (1, 1)], 0.0)], [[(-1, -1), (2, 3)], [(0, 0), (1, 1)]],
                  **{"in": ["tuple", "tuple"]},
                  grammar="""
## Building blocks
- **Unpack a tuple:** `x1, y1 = p`
- **Square root:** `** 0.5` (or `math.sqrt`).
"""),
                P("py-tuple-from-list", "Freeze a List", "def freeze(items: List[int]) -> Tuple[int, ...]:",
                  "Return the items as a tuple.",
                  "def freeze(items: List[int]) -> Tuple[int, ...]:\n    return tuple(items)\n",
                  [([[1, 2]], (1, 2)), ([[]], ()), ([[7]], (7,))], [[[3, 3, 3]]],
                  compare="strict", require=["tuple"],
                  grammar="""
## Building blocks
- **Convert:** `tuple(items)`
"""),
            ],
            quiz=[
                Q("What does this print?", "<class 'int'> <class 'tuple'>", "<class 'tuple'> <class 'tuple'>", "<class 'int'> <class 'int'>", "error",
                  code="print(type((5)), type((5,)))", predict=True, why="The comma makes a tuple, not the brackets."),
                Q("What does this print?", "2 1", "1 2", "error", "(2, 1)", code="a, b = 1, 2\na, b = b, a\nprint(a, b)", predict=True,
                  why="The right side is built first, then unpacked into a and b."),
                Q("What happens?", "TypeError", "t becomes (9, 2)", "t becomes [9, 2]", "Nothing", code="t = (1, 2)\nt[0] = 9", why="Tuples are immutable."),
            ],
        ),
        # ------------------------------------------------------------------ hashing, frozenset
        dict(
            id="hashing",
            title="Hashing, frozenset and tuple keys",
            builtins=["hash", "frozenset"],
            intro="""
Dict keys and set items must be **hashable**: Python computes `hash(x)` to find them fast. Immutable values (numbers, strings, tuples of hashable things, `frozenset`) are hashable; lists, dicts and sets are not.

- `{[1, 2]: "x"}` → `TypeError: unhashable type: 'list'`. Use `tuple([1, 2])` as the key instead.
- `frozenset(items)` is an unchangeable set, so it *can* be a key or live inside another set.
- Equal values always have equal hashes: `hash("abc") == hash("abc")`.
""",
            problems=[
                P("py-distinct-points", "Distinct Points", "def distinct_points(points: List[List[int]]) -> int:",
                  "`points` is a list of `[x, y]` pairs. Return how many different points there are.",
                  "def distinct_points(points: List[List[int]]) -> int:\n    return len({tuple(p) for p in points})\n",
                  [([[[1, 2], [3, 4], [1, 2]]], 2), ([[]], 0)], [[[[0, 0]] * 5], [[[1, 2], [2, 1]]]],
                  require=["tuple"],
                  hints=["Lists can't go in a set. Convert each one to a tuple first."],
                  grammar="""
## Building blocks
- **Hashable version of a list:** `tuple(p)`
- **Collect into a set:** `seen.add(tuple(p))`, then `len(seen)`.
"""),
                P("py-point-counts", "Count Each Point", "def point_counts(points: List[List[int]]) -> Dict:",
                  "Return a dict mapping each point, as an `(x, y)` tuple, to how many times it appears.",
                  "def point_counts(points: List[List[int]]) -> Dict:\n    counts = {}\n    for p in points:\n        key = tuple(p)\n        counts[key] = counts.get(key, 0) + 1\n    return counts\n",
                  [([[[1, 2], [1, 2], [0, 0]]], {(1, 2): 2, (0, 0): 1}), ([[]], {})], [[[[5, 5]]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Tuple keys:** `counts[tuple(p)]`
- **Counting pattern:** `counts.get(key, 0) + 1`
"""),
                P("py-same-letter-set", "Same Letters", "def same_letters(a: str, b: str) -> bool:",
                  "Return `True` if the two words use exactly the same set of letters (ignoring how many times). Use `frozenset`.",
                  "def same_letters(a: str, b: str) -> bool:\n    return frozenset(a) == frozenset(b)\n",
                  [(["listen", "silent"], True), (["aab", "ab"], True), (["abc", "abd"], False)], [["", ""], ["a", ""]],
                  require=["frozenset"],
                  grammar="""
## Building blocks
- **An unchangeable set:** `frozenset(a)`
- **Sets compare by contents:** `frozenset(a) == frozenset(b)`
"""),
                P("py-group-by-letter-set", "Group by Letter Set", "def group_letter_sets(words: List[str]) -> List[List[str]]:",
                  "Group words that use the same set of letters. Return the groups in the order their first word appears, each group in its original order. `[\"ab\", \"ba\", \"aab\", \"c\"]` → `[[\"ab\", \"ba\", \"aab\"], [\"c\"]]`.",
                  "def group_letter_sets(words: List[str]) -> List[List[str]]:\n    groups = {}\n    for w in words:\n        groups.setdefault(frozenset(w), []).append(w)\n    return list(groups.values())\n",
                  [([["ab", "ba", "aab", "c"]], [["ab", "ba", "aab"], ["c"]]), ([[]], [])], [[["x", "y", "xy", "yx", "x"]]],
                  difficulty="Medium", require=["frozenset"],
                  grammar="""
## Building blocks
- **A key for "same letters":** `frozenset(w)`. A plain `set` can't be a dict key.
- **Group:** `groups.setdefault(key, []).append(w)`
- **Groups in first-seen order:** `list(groups.values())`
"""),
                P("py-hash-equal", "Equal Hashes", "def same_hash(a: str, b: str) -> bool:",
                  "Return whether `hash(a) == hash(b)`. (Equal strings always hash the same.)",
                  "def same_hash(a: str, b: str) -> bool:\n    return hash(a) == hash(b)\n",
                  [(["abc", "abc"], True), (["abc", "abd"], False)], [["", ""], ["a", "A"]],
                  require=["hash"],
                  grammar="""
## Building blocks
- **A value's hash:** `hash(a)`. Equal values → equal hashes; different values almost always differ.
"""),
            ],
            quiz=[
                Q("Which of these can be a dict key?", "(1, 2)", "[1, 2]", "{1, 2}", "{'a': 1}", why="Only immutable (hashable) values can be keys."),
                Q("What does this print?", "TypeError", "{[1]: 'x'}", "{'[1]': 'x'}", "None",
                  code="try:\n    d = {[1]: 'x'}\nexcept TypeError:\n    print('TypeError')", predict=True,
                  why="Lists are unhashable."),
                Q("What does this print?", "True", "False", code="print(frozenset('ab') == frozenset('ba'))", predict=True, why="Sets ignore order."),
            ],
        ),
    ],
)
