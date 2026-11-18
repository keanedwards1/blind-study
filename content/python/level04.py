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
                P("py-price-lookup", 'Look Up a Price', "def price(prices: Dict[str, int], item: str) -> int:",
                  """
A checkout service keeps its prices in a dict from product name to price. Write `price(prices, item)` to return the price of `item`, or `0` if the store doesn't sell it.

Example: `price({"tea": 3, "jam": 5}, "jam")` returns `5`, and `price({"tea": 3}, "cake")` returns `0`.
""",
                  "def price(prices: Dict[str, int], item: str) -> int:\n    return prices.get(item, 0)\n",
                  [([{"tea": 3, "jam": 5}, "jam"], 5), ([{"tea": 3}, "cake"], 0)], [[{}, "x"], [{"a": 0}, "a"]],
                  require=[".get"],
                  grammar="""
## Building blocks
- **Read with a default:** `prices.get(item, 0)`
- **Compare:** `prices[item]` raises `KeyError` if it's missing.
"""),
                P("py-word-frequencies", 'Count Word Frequencies', "def frequencies(words: List[str]) -> Dict[str, int]:",
                  """
A search feature needs to know how often each word appears in a document. Write `frequencies(words)` to return a dict from each word to the number of times it appears. Count with a plain dict (don't use `Counter`).

Example: `frequencies(["a", "b", "a"])` returns `{"a": 2, "b": 1}`. An empty list gives `{}`.
""",
                  "def frequencies(words: List[str]) -> Dict[str, int]:\n    counts = {}\n    for w in words:\n        counts[w] = counts.get(w, 0) + 1\n    return counts\n",
                  [([["a", "b", "a"]], {"a": 2, "b": 1}), ([[]], {})], [[["x"] * 5], [["to", "be", "or", "not", "to", "be"]]],
                  forbid=["Counter"],
                  grammar="""
## Building blocks
- **Empty dict:** `counter = {}`
- **Read with a default:** `d.get(key, 0)`
- **Store under a key:** `d[key] = value`
"""),
                P("py-invert-dict", 'Invert a Lookup Table', "def invert(d: Dict[str, str]) -> Dict[str, str]:",
                  """
A config maps internal codes to display names, and you need the reverse mapping too. Write `invert(d)` to return a new dict where each value becomes a key and each key becomes its value. The values are all different.

Example: `invert({"a": "x", "b": "y"})` returns `{"x": "a", "y": "b"}`.
""",
                  "def invert(d: Dict[str, str]) -> Dict[str, str]:\n    out = {}\n    for k, v in d.items():\n        out[v] = k\n    return out\n",
                  [([{"a": "x", "b": "y"}], {"x": "a", "y": "b"}), ([{}], {})], [[{"one": "1"}]],
                  grammar="""
## Building blocks
- **Key and value together:** `for cap, value in mapping.items():`
- **Store the other way round:** `acc[x] = kk`
"""),
                P("py-first-repeat", 'Find the First Repeated Word', "def first_repeat(words: List[str]) -> str:",
                  """
A spell checker flags the first word that appears twice in a sentence. Write `first_repeat(words)` to return the first word that you see for a second time, reading left to right, or `""` if no word repeats.

Example: `first_repeat(["a", "b", "c", "b", "a"])` returns `"b"`, because the second `b` comes before the second `a`.
""",
                  'def first_repeat(words: List[str]) -> str:\n    seen = {}\n    for w in words:\n        if w in seen:\n            return w\n        seen[w] = True\n    return ""\n',
                  [([["a", "b", "c", "b", "a"]], "b"), ([["x", "y"]], "")], [[[]], [["z", "z"]]],
                  grammar="""
## Building blocks
- **Remember what you've seen:** a dict (or a set, coming up next).
- **Check before storing:** `if term in met: return term`, then `visited[word] = True`.
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
                P("py-total-stock", 'Total the Inventory', "def total_stock(stock: Dict[str, int]) -> int:",
                  """
An inventory report needs the total number of units in stock across all products. Write `total_stock(stock)`, where `stock` maps product names to quantities, and return the total.

Example: `total_stock({"apples": 3, "pears": 4})` returns `7`. An empty dict returns `0`.
""",
                  "def total_stock(stock: Dict[str, int]) -> int:\n    return sum(stock.values())\n",
                  [([{"apples": 3, "pears": 4}], 7), ([{}], 0)], [[{"x": -1, "y": 1}]],
                  require=[".values"],
                  grammar="""
## Building blocks
- **Just the values:** `stock.values()`
- **Add them:** `sum(...)`
"""),
                P("py-sorted-keys", 'Sort the Keys', "def sorted_keys(d: Dict[str, int]) -> List[str]:",
                  """
A settings page lists its options alphabetically. Write `sorted_keys(d)` to return the dict's keys as a list in alphabetical order.

Example: `sorted_keys({"b": 1, "a": 2})` returns `["a", "b"]`.
""",
                  "def sorted_keys(d: Dict[str, int]) -> List[str]:\n    return sorted(d)\n",
                  [([{"b": 1, "a": 2}], ["a", "b"]), ([{}], [])], [[{"z": 0, "m": 0, "a": 0}]],
                  grammar="""
## Building blocks
- **Looping over a dict gives keys:** so `sorted(d)` sorts the keys.
"""),
                P("py-merge-settings", 'Merge Settings', "def merge(defaults: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:",
                  """
An app starts from default settings and lets each user override some of them. Write `merge(defaults, overrides)` to return a new dict with every default, replaced by the user's value wherever they set one. Keys that appear only in `overrides` are included too. Don't change either input dict.

Example: `merge({"size": 10, "bold": 0}, {"bold": 1})` returns `{"size": 10, "bold": 1}`.
""",
                  "def merge(defaults: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:\n    out = dict(defaults)\n    out.update(overrides)\n    return out\n",
                  [([{"size": 10, "bold": 0}, {"bold": 1}], {"size": 10, "bold": 1}), ([{}, {"a": 1}], {"a": 1})], [[{"a": 1}, {}]],
                  require=["dict", ".update"],
                  grammar="""
## Building blocks
- **Copy a dict:** `dict(defaults)`
- **Copy keys across:** `result.update(changes)`
- **Shortcut you'll see:** `{**defaults, **overrides}`
"""),
                P("py-pop-key", 'Remove a Key and Keep Its Value', "def take(d: Dict[str, int], key: str) -> List:",
                  """
When a cart item is removed, the cart code needs the item's price for a refund. Write `take(d, key)` to remove `key` from `d` and return `[its value, the dict afterwards]`. If the key isn't there, return `[None, d]` with the dict unchanged.

Example: `take({"a": 1, "b": 2}, "a")` returns `[1, {"b": 2}]`.
""",
                  "def take(d: Dict[str, int], key: str) -> List:\n    value = d.pop(key, None)\n    return [value, d]\n",
                  [([{"a": 1, "b": 2}, "a"], [1, {"b": 2}]), ([{"a": 1}, "z"], [None, {"a": 1}])], [[{}, "x"]],
                  require=[".pop"],
                  grammar="""
## Building blocks
- **Remove and return, with a default:** `d.pop(key, None)`. Without the default, a missing key raises `KeyError`.
"""),
                P("py-group-by-initial", 'Group Names by First Letter', "def by_initial(words: List[str]) -> Dict[str, List[str]]:",
                  """
A contacts screen shows names under a heading for each first letter. Write `by_initial(words)` to return a dict from each first letter to the list of words that start with it, keeping the words in their original order. No word is empty.

Example: `by_initial(["apple", "bean", "avocado"])` returns `{"a": ["apple", "avocado"], "b": ["bean"]}`.
""",
                  "def by_initial(words: List[str]) -> Dict[str, List[str]]:\n    groups = {}\n    for w in words:\n        groups.setdefault(w[0], []).append(w)\n    return groups\n",
                  [([["apple", "bean", "avocado"]], {"a": ["apple", "avocado"], "b": ["bean"]}), ([[]], {})], [[["x", "y", "x"]]],
                  require=[".setdefault"],
                  grammar="""
## Building blocks
- **Get the list, creating it if missing:** `groups.setdefault(key, [])`
- **Then add to it:** `.append(w)` on what `setdefault` returns.
"""),
                P("py-zip-to-dict", 'Build a Dict from Two Lists', "def to_dict(keys: List[str], values: List[int]) -> Dict[str, int]:",
                  """
A CSV import gives you the column names in one list and a row's values in another, in the same order. Write `to_dict(keys, values)` to pair them up in a dict. The lists are the same length.

Example: `to_dict(["a", "b"], [1, 2])` returns `{"a": 1, "b": 2}`.
""",
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
                P("py-unique-count", 'Count Distinct Values', "def distinct(items: List[int]) -> int:",
                  """
An analytics dashboard shows how many different user IDs appeared in a log. Write `distinct(items)` to return the number of different values in the list.

Example: `distinct([1, 2, 2, 3, 3, 3])` returns `3`. An empty list returns `0`.
""",
                  "def distinct(items: List[int]) -> int:\n    return len(set(items))\n",
                  [([[1, 2, 2, 3, 3, 3]], 3), ([[]], 0)], [[[7] * 10], [list(range(50))]],
                  require=["set"],
                  grammar="""
## Building blocks
- **Drop duplicates:** `set(items)`
- **Count:** `len(...)`
"""),
                P("py-dedupe-keep-order", 'Remove Duplicates, Keep Order', "def dedupe(items: List[int]) -> List[int]:",
                  """
A mailing list has some addresses more than once. Write `dedupe(items)` to return the list with duplicates removed, keeping the first occurrence of each value in its original order.

Example: `dedupe([3, 1, 3, 2, 1])` returns `[3, 1, 2]`. A plain set would lose the order.
""",
                  "def dedupe(items: List[int]) -> List[int]:\n    seen = set()\n    out = []\n    for x in items:\n        if x not in seen:\n            seen.add(x)\n            out.append(x)\n    return out\n",
                  [([[3, 1, 3, 2, 1]], [3, 1, 2]), ([[]], [])], [[[5, 5, 5]], [[1, 2, 3]]],
                  require=["set"],
                  hints=["`set(items)` loses the order. Keep a set of what you've seen and build a list as you go."],
                  grammar="""
## Building blocks
- **Empty set:** `been = set()`
- **Not seen yet:** `if item not in met:`
- **Remember it:** `visited.add(val)`
"""),
                P("py-unique-letters-set", 'Letters Used in a Word', "def letters(word: str) -> Set[str]:",
                  """
A word game needs the set of letters in the player's word. Write `letters(word)` to return the set of its letters.

Example: `letters("hello")` returns `{"h", "e", "l", "o"}`, and `letters("")` returns `set()`.
""",
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
                P("py-in-both", 'Values in Both Lists', "def both(a: List[int], b: List[int]) -> Set[int]:",
                  """
Two teams each have a list of tags they use. Write `both(a, b)` to return the set of tags that appear in both lists.

Example: `both([1, 2, 3], [2, 3, 4])` returns `{2, 3}`.
""",
                  "def both(a: List[int], b: List[int]) -> Set[int]:\n    return set(a) & set(b)\n",
                  [([[1, 2, 3], [2, 3, 4]], {2, 3}), ([[1], [2]], set())], [[[], []], [[5, 5], [5]]],
                  compare="strict", require=["op:&"],
                  grammar="""
## Building blocks
- **Make sets:** `set(a)`, `set(b)`
- **Intersection:** `&`
"""),
                P("py-in-either", 'Values in Either List', "def either(a: List[int], b: List[int]) -> Set[int]:",
                  """
Two data sources each list some product IDs, and the merged catalogue needs every ID once. Write `either(a, b)` to return the set of values that appear in at least one list.

Example: `either([1, 2], [2, 3])` returns `{1, 2, 3}`.
""",
                  "def either(a: List[int], b: List[int]) -> Set[int]:\n    return set(a) | set(b)\n",
                  [([[1, 2], [2, 3]], {1, 2, 3}), ([[], []], set())], [[[1], []]],
                  compare="strict", require=["op:|"],
                  grammar="""
## Building blocks
- **Union:** `{1, 2} | {2, 3}` gives `{1, 2, 3}`.
"""),
                P("py-only-in-first", "Who Hasn't Checked In", "def missing(invited: List[str], arrived: List[str]) -> List[str]:",
                  """
An event app compares the guest list with the people who have checked in. Write `missing(invited, arrived)` to return the invited guests who haven't arrived, in alphabetical order.

Example: `missing(["ada", "bo", "cy"], ["bo"])` returns `["ada", "cy"]`.
""",
                  "def missing(invited: List[str], arrived: List[str]) -> List[str]:\n    return sorted(set(invited) - set(arrived))\n",
                  [([["ada", "bo", "cy"], ["bo"]], ["ada", "cy"]), ([["a"], ["a"]], [])], [[[], ["x"]], [["z", "y"], []]],
                  require=["op:-"],
                  grammar="""
## Building blocks
- **Difference:** `{1, 2, 3} - {2}` gives `{1, 3}`.
- **Sorted list from a set:** `sorted(...)`
"""),
                P("py-in-exactly-one", 'Values in Exactly One List', "def exactly_one(a: List[int], b: List[int]) -> List[int]:",
                  """
A sync tool compares the file IDs on two machines and needs the ones that exist on only one of them. Write `exactly_one(a, b)` to return those values in increasing order.

Example: `exactly_one([1, 2, 3], [3, 4])` returns `[1, 2, 4]`.
""",
                  "def exactly_one(a: List[int], b: List[int]) -> List[int]:\n    return sorted(set(a) ^ set(b))\n",
                  [([[1, 2, 3], [3, 4]], [1, 2, 4]), ([[1], [1]], [])], [[[], [1, 1]], [[5, 6], [7, 8]]],
                  require=["op:^"],
                  grammar="""
## Building blocks
- **Symmetric difference:** `{1, 2} ^ {2, 3}` gives `{1, 3}`.
"""),
                P("py-is-subset", 'Check the Ingredients', "def can_make(needed: List[str], have: List[str]) -> bool:",
                  """
A recipe app checks whether you can cook a dish with what's in your pantry. Write `can_make(needed, have)` to return `True` if every ingredient in `needed` appears somewhere in `have`. Quantities don't matter.

Example: `can_make(["egg", "milk"], ["milk", "egg", "flour"])` returns `True`, and `can_make(["egg"], [])` returns `False`.
""",
                  "def can_make(needed: List[str], have: List[str]) -> bool:\n    return set(needed) <= set(have)\n",
                  [([["egg", "milk"], ["milk", "egg", "flour"]], True), ([["egg"], []], False), ([[], []], True)], [[["a", "a"], ["a"]]],
                  grammar="""
## Building blocks
- **Subset:** `{1, 2} <= {1, 2, 3}` is `True`; so is `{1, 2}.issubset([1, 2, 3])`.
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
                P("py-swap-pair", 'Swap Two Values', "def swap(a: int, b: int) -> Tuple[int, int]:",
                  """
A sorting routine needs a helper that swaps a pair. Write `swap(a, b)` to return the tuple `(b, a)`.

Example: `swap(1, 2)` returns `(2, 1)`.
""",
                  "def swap(a: int, b: int) -> Tuple[int, int]:\n    return b, a\n",
                  [([1, 2], (2, 1)), ([0, 0], (0, 0))], [[-1, 5]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Return a tuple:** `return q, p`. The comma makes the tuple; brackets are optional.
- **This task checks the type:** `[b, a]` is a list, so it won't pass.
"""),
                P("py-min-max-tuple", 'Smallest and Largest', "def low_high(nums: List[int]) -> Tuple[int, int]:",
                  """
A chart needs the lowest and highest values to set its axis. Write `low_high(nums)` to return `(smallest, largest)` as a tuple. The list has at least one number.

Example: `low_high([3, 1, 2])` returns `(1, 3)`, and `low_high([5])` returns `(5, 5)`.
""",
                  "def low_high(nums: List[int]) -> Tuple[int, int]:\n    return min(nums), max(nums)\n",
                  [([[3, 1, 2]], (1, 3)), ([[5]], (5, 5))], [[[-1, -9, 4]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Return two results at once:** `return a, b` returns a tuple.
"""),
                P("py-head-tail", 'First Item and the Rest', "def head_tail(items: List[int]) -> Tuple:",
                  """
A job queue processes the first job and keeps the rest waiting. Write `head_tail(items)` to return a tuple `(first item, list of the rest)`, using star unpacking. The list has at least one item.

Example: `head_tail([1, 2, 3])` returns `(1, [2, 3])`, and `head_tail([9])` returns `(9, [])`.
""",
                  "def head_tail(items: List[int]) -> Tuple:\n    first, *rest = items\n    return first, rest\n",
                  [([[1, 2, 3]], (1, [2, 3])), ([[9]], (9, []))], [[[0, 0]]],
                  compare="strict", require=["unpack"],
                  grammar="""
## Building blocks
- **Star unpacking:** `leader, *remainder = things`. `remainder` is always a list.
- **Return both:** `return one, tail_items`
"""),
                P("py-distance-tuples", 'Distance Between Two Points', "def distance(p: Tuple[int, int], q: Tuple[int, int]) -> float:",
                  """
A map feature stores locations as `(x, y)` tuples. Write `distance(p, q)` to return the straight-line distance between two of them: √((x₁−x₂)² + (y₁−y₂)²).

Example: `distance((0, 0), (3, 4))` returns `5.0`.
""",
                  "def distance(p: Tuple[int, int], q: Tuple[int, int]) -> float:\n    (x1, y1), (x2, y2) = p, q\n    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5\n",
                  [([(0, 0), (3, 4)], 5.0), ([(1, 1), (1, 1)], 0.0)], [[(-1, -1), (2, 3)], [(0, 0), (1, 1)]],
                  **{"in": ["tuple", "tuple"]},
                  grammar="""
## Building blocks
- **Unpack a tuple:** `ax, ay = pt`
- **Square root:** `** 0.5` (or `math.sqrt`).
"""),
                P("py-tuple-from-list", 'Make a List Read-Only', "def freeze(items: List[int]) -> Tuple[int, ...]:",
                  """
Once an order is confirmed it shouldn't change, so it's stored as a tuple. Write `freeze(items)` to return the items as a tuple.

Example: `freeze([1, 2])` returns `(1, 2)`, and `freeze([])` returns `()`.
""",
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
                P("py-distinct-points", 'Count Distinct Points', "def distinct_points(points: List[List[int]]) -> int:",
                  """
A drawing app records every click as an `[x, y]` pair, and some clicks land on the same spot. Write `distinct_points(points)` to return how many different spots were clicked.

Example: `distinct_points([[1, 2], [3, 4], [1, 2]])` returns `2`. Lists can't go in a set, but tuples can.
""",
                  "def distinct_points(points: List[List[int]]) -> int:\n    return len({tuple(p) for p in points})\n",
                  [([[[1, 2], [3, 4], [1, 2]]], 2), ([[]], 0)], [[[[0, 0]] * 5], [[[1, 2], [2, 1]]]],
                  require=["tuple"],
                  hints=["Lists can't go in a set. Convert each one to a tuple first."],
                  grammar="""
## Building blocks
- **Hashable version of a list:** `tuple(p)`
- **Collect into a set:** `seen.add(tuple(p))`, then `len(seen)`.
"""),
                P("py-point-counts", 'Count Clicks per Point', "def point_counts(points: List[List[int]]) -> Dict:",
                  """
A heatmap needs to know how many clicks landed on each spot. Write `point_counts(points)` to return a dict from each spot, as an `(x, y)` tuple, to how many times it appears.

Example: `point_counts([[1, 2], [1, 2], [0, 0]])` returns `{(1, 2): 2, (0, 0): 1}`.
""",
                  "def point_counts(points: List[List[int]]) -> Dict:\n    counts = {}\n    for p in points:\n        key = tuple(p)\n        counts[key] = counts.get(key, 0) + 1\n    return counts\n",
                  [([[[1, 2], [1, 2], [0, 0]]], {(1, 2): 2, (0, 0): 1}), ([[]], {})], [[[[5, 5]]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Tuple keys:** `counts[tuple(p)]`
- **Counting pattern:** `counts.get(key, 0) + 1`
"""),
                P("py-same-letter-set", 'Same Set of Letters', "def same_letters(a: str, b: str) -> bool:",
                  """
A word puzzle checks whether two words use exactly the same letters, ignoring how many times each appears. Write `same_letters(a, b)` using `frozenset`.

Example: `same_letters("listen", "silent")` returns `True`, and so does `same_letters("aab", "ab")`.
""",
                  "def same_letters(a: str, b: str) -> bool:\n    return frozenset(a) == frozenset(b)\n",
                  [(["listen", "silent"], True), (["aab", "ab"], True), (["abc", "abd"], False)], [["", ""], ["a", ""]],
                  require=["frozenset"],
                  grammar="""
## Building blocks
- **An unchangeable set:** `frozenset(a)`
- **Sets compare by contents:** `frozenset("ab") == frozenset("ba")` is `True`.
"""),
                P("py-group-by-letter-set", 'Group Words by Their Letters', "def group_letter_sets(words: List[str]) -> List[List[str]]:",
                  """
A word puzzle groups words that use the same set of letters. Write `group_letter_sets(words)` to return the groups as a list of lists, in the order each group's first word appears, with each group's words in their original order.

Example: `group_letter_sets(["ab", "ba", "aab", "c"])` returns `[["ab", "ba", "aab"], ["c"]]`.
""",
                  "def group_letter_sets(words: List[str]) -> List[List[str]]:\n    groups = {}\n    for w in words:\n        groups.setdefault(frozenset(w), []).append(w)\n    return list(groups.values())\n",
                  [([["ab", "ba", "aab", "c"]], [["ab", "ba", "aab"], ["c"]]), ([[]], [])], [[["x", "y", "xy", "yx", "x"]]],
                  difficulty="Medium", require=["frozenset"],
                  grammar="""
## Building blocks
- **A key for "same letters":** `frozenset(w)`. A plain `set` can't be a dict key.
- **Group:** `groups.setdefault(key, []).append(w)`
- **Groups in first-seen order:** `list(groups.values())`
"""),
                P("py-hash-equal", 'Compare Hashes', "def same_hash(a: str, b: str) -> bool:",
                  """
Dicts and sets look values up by their hash. Write `same_hash(a, b)` to return whether `hash(a) == hash(b)`. Equal strings always hash the same.

Example: `same_hash("abc", "abc")` returns `True`, and `same_hash("abc", "abd")` returns `False`.
""",
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
