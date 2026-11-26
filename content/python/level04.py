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

**Constraints**
- `0 <= len(prices) <= 10^4`
- `-10^16 <= prices[name] <= 10^16`
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

**Constraints**
- `0 <= len(words) <= 10^4`
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
                P("py-invert-dict", 'Invert a Lookup Table', "def invert(mapping: Dict[str, str]) -> Dict[str, str]:",
                  """
A config maps internal codes to display names, and you need the reverse mapping too. Write `invert(mapping)` to return a new dict where each value becomes a key and each key becomes its value.

**Constraints**
- `0 <= len(mapping) <= 10^4`
- All the values in `mapping` are different
""",
                  "def invert(mapping: Dict[str, str]) -> Dict[str, str]:\n    out = {}\n    for k, v in mapping.items():\n        out[v] = k\n    return out\n",
                  [([{"a": "x", "b": "y"}], {"x": "a", "y": "b"}), ([{}], {})], [[{"one": "1"}]],
                  grammar="""
## Building blocks
- **Key and value together:** `for cap, value in mapping.items():`
- **Store the other way round:** `acc[x] = kk`
"""),
                P("py-first-repeat", 'Find the First Repeated Word', "def first_repeat(words: List[str]) -> str:",
                  """
A spell checker flags the first word that appears twice in a sentence. Write `first_repeat(words)` to return the first word that you see for a second time, reading left to right, or `""` if no word repeats.

**Constraints**
- `0 <= len(words) <= 10^4`
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

**Constraints**
- `0 <= len(stock) <= 10^4`
- `-10^16 <= stock[name] <= 10^16`
""",
                  "def total_stock(stock: Dict[str, int]) -> int:\n    return sum(stock.values())\n",
                  [([{"apples": 3, "pears": 4}], 7), ([{}], 0)], [[{"x": -1, "y": 1}]],
                  require=[".values"],
                  grammar="""
## Building blocks
- **Just the values:** `stock.values()`
- **Add them:** `sum(...)`
"""),
                P("py-sorted-keys", 'Sort the Keys', "def sorted_keys(settings: Dict[str, int]) -> List[str]:",
                  """
A settings page lists its options alphabetically. Write `sorted_keys(settings)` to return the dict's keys as a list in alphabetical order.

**Constraints**
- `0 <= len(settings) <= 10^4`
""",
                  "def sorted_keys(settings: Dict[str, int]) -> List[str]:\n    return sorted(settings)\n",
                  [([{"b": 1, "a": 2}], ["a", "b"]), ([{}], [])], [[{"z": 0, "m": 0, "a": 0}]],
                  grammar="""
## Building blocks
- **Looping over a dict gives keys:** so `sorted(settings)` sorts the keys.
"""),
                P("py-merge-settings", 'Merge Settings', "def merge(defaults: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:",
                  """
An app starts from default settings and lets each user override some of them. Write `merge(defaults, overrides)` to return a new dict with every default, replaced by the user's value wherever they set one. Keys that appear only in `overrides` are included too. Don't change either input dict.

**Constraints**
- `0 <= len(defaults), len(overrides) <= 10^4`
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
                P("py-pop-key", 'Remove a Key and Keep Its Value', "def take(cart: Dict[str, int], key: str) -> List:",
                  """
When a cart item is removed, the cart code needs the item's price for a refund. Write `take(cart, key)` to remove `key` from `cart` and return `[its value, the dict afterwards]`. If the key isn't there, return `[None, cart]` with the dict unchanged.

**Constraints**
- `0 <= len(cart) <= 10^4`
""",
                  "def take(cart: Dict[str, int], key: str) -> List:\n    value = cart.pop(key, None)\n    return [value, cart]\n",
                  [([{"a": 1, "b": 2}, "a"], [1, {"b": 2}]), ([{"a": 1}, "z"], [None, {"a": 1}])], [[{}, "x"]],
                  require=[".pop"],
                  grammar="""
## Building blocks
- **Remove and return, with a default:** `cart.pop(key, None)`. Without the default, a missing key raises `KeyError`.
"""),
                P("py-group-by-initial", 'Group Names by First Letter', "def by_initial(words: List[str]) -> Dict[str, List[str]]:",
                  """
A contacts screen shows names under a heading for each first letter. Write `by_initial(words)` to return a dict from each first letter to the list of words that start with it, keeping the words in their original order.

**Constraints**
- `0 <= len(words) <= 10^4`
- `1 <= len(words[i]) <= 100`
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
A CSV import gives you the column names in one list and a row's values in another, in the same order. Write `to_dict(keys, values)` to pair them up in a dict.

**Constraints**
- `0 <= len(keys) <= 10^4`
- `len(values) == len(keys)`
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

**Constraints**
- `0 <= len(items) <= 10^4`
- Items are numbers or strings
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

A plain set would lose the order.

**Constraints**
- `0 <= len(items) <= 10^4`
- Items are numbers or strings
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

**Constraints**
- `0 <= len(word) <= 10^4`
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
                P("py-in-both", 'Values in Both Lists', "def both(first_tags: List[int], second_tags: List[int]) -> Set[int]:",
                  """
Two teams each have a list of tags they use. Write `both(first_tags, second_tags)` to return the set of tags that appear in both lists.

**Constraints**
- `0 <= len(first_tags), len(second_tags) <= 10^4`
- Items are numbers or strings
""",
                  "def both(first_tags: List[int], second_tags: List[int]) -> Set[int]:\n    return set(first_tags) & set(second_tags)\n",
                  [([[1, 2, 3], [2, 3, 4]], {2, 3}), ([[1], [2]], set())], [[[], []], [[5, 5], [5]]],
                  compare="strict", require=["op:&"],
                  grammar="""
## Building blocks
- **Make sets:** `set(first_tags)`, `set(second_tags)`
- **Intersection:** `&`
"""),
                P("py-in-either", 'Values in Either List', "def either(first_source: List[int], second_source: List[int]) -> Set[int]:",
                  """
Two data sources each list some product IDs, and the merged catalogue needs every ID once. Write `either(first_source, second_source)` to return the set of values that appear in at least one list.

**Constraints**
- `0 <= len(first_source), len(second_source) <= 10^4`
- Items are numbers or strings
""",
                  "def either(first_source: List[int], second_source: List[int]) -> Set[int]:\n    return set(first_source) | set(second_source)\n",
                  [([[1, 2], [2, 3]], {1, 2, 3}), ([[], []], set())], [[[1], []]],
                  compare="strict", require=["op:|"],
                  grammar="""
## Building blocks
- **Union:** `{1, 2} | {2, 3}` gives `{1, 2, 3}`.
"""),
                P("py-only-in-first", "Who Hasn't Checked In", "def missing(invited: List[str], arrived: List[str]) -> List[str]:",
                  """
An event app compares the guest list with the people who have checked in. Write `missing(invited, arrived)` to return the invited guests who haven't arrived, in alphabetical order.

**Constraints**
- `0 <= len(invited), len(arrived) <= 10^4`
""",
                  "def missing(invited: List[str], arrived: List[str]) -> List[str]:\n    return sorted(set(invited) - set(arrived))\n",
                  [([["ada", "bo", "cy"], ["bo"]], ["ada", "cy"]), ([["a"], ["a"]], [])], [[[], ["x"]], [["z", "y"], []]],
                  require=["op:-"],
                  grammar="""
## Building blocks
- **Difference:** `{1, 2, 3} - {2}` gives `{1, 3}`.
- **Sorted list from a set:** `sorted(...)`
"""),
                P("py-in-exactly-one", 'Values in Exactly One List', "def exactly_one(first_machine: List[int], second_machine: List[int]) -> List[int]:",
                  """
A sync tool compares the file IDs on two machines and needs the ones that exist on only one of them. Write `exactly_one(first_machine, second_machine)` to return those values in increasing order.

**Constraints**
- `0 <= len(first_machine), len(second_machine) <= 10^4`
- `-10^16 <= first_machine[i], second_machine[i] <= 10^16`
""",
                  "def exactly_one(first_machine: List[int], second_machine: List[int]) -> List[int]:\n    return sorted(set(first_machine) ^ set(second_machine))\n",
                  [([[1, 2, 3], [3, 4]], [1, 2, 4]), ([[1], [1]], [])], [[[], [1, 1]], [[5, 6], [7, 8]]],
                  require=["op:^"],
                  grammar="""
## Building blocks
- **Symmetric difference:** `{1, 2} ^ {2, 3}` gives `{1, 3}`.
"""),
                P("py-is-subset", 'Check the Ingredients', "def can_make(needed: List[str], have: List[str]) -> bool:",
                  """
A recipe app checks whether you can cook a dish with what's in your pantry. Write `can_make(needed, have)` to return `True` if every ingredient in `needed` appears somewhere in `have`. Quantities don't matter.

**Constraints**
- `0 <= len(needed), len(have) <= 10^4`
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
                P("py-swap-pair", 'Swap Two Values', "def swap(first: int, second: int) -> Tuple[int, int]:",
                  """
A sorting routine needs a helper that swaps a pair. Write `swap(first, second)` to return the tuple `(second, first)`.

**Constraints**
- `first` and `second` can be values of any type
""",
                  "def swap(first: int, second: int) -> Tuple[int, int]:\n    return second, first\n",
                  [([1, 2], (2, 1)), ([0, 0], (0, 0))], [[-1, 5]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Return a tuple:** `return q, p`. The comma makes the tuple; brackets are optional.
- **This task checks the type:** `[second, first]` is a list, so it won't pass.
"""),
                P("py-min-max-tuple", 'Smallest and Largest', "def low_high(nums: List[int]) -> Tuple[int, int]:",
                  """
A chart needs the lowest and highest values to set its axis. Write `low_high(nums)` to return `(smallest, largest)` as a tuple.

**Constraints**
- `1 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
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
A job queue processes the first job and keeps the rest waiting. Write `head_tail(items)` to return a tuple `(first item, list of the rest)`, using star unpacking.

**Constraints**
- `1 <= len(items) <= 10^4`
- Items can be values of any type
""",
                  "def head_tail(items: List[int]) -> Tuple:\n    first, *rest = items\n    return first, rest\n",
                  [([[1, 2, 3]], (1, [2, 3])), ([[9]], (9, []))], [[[0, 0]]],
                  compare="strict", require=["unpack"],
                  grammar="""
## Building blocks
- **Star unpacking:** `leader, *remainder = things`. `remainder` is always a list.
- **Return both:** `return one, tail_items`
"""),
                P("py-distance-tuples", 'Distance Between Two Points', "def distance(start: Tuple[int, int], end: Tuple[int, int]) -> float:",
                  """
A map feature stores locations as `(x, y)` tuples. Write `distance(start, end)` to return the straight-line distance between two of them: √((x₁−x₂)² + (y₁−y₂)²).

**Constraints**
- `len(start) == len(end) == 2`
- `-10^16 <= start[i], end[i] <= 10^16`
""",
                  "def distance(start: Tuple[int, int], end: Tuple[int, int]) -> float:\n    (x1, y1), (x2, y2) = start, end\n    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5\n",
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

**Constraints**
- `0 <= len(items) <= 10^4`
- Items can be values of any type
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

Lists can't go in a set, but tuples can.

**Constraints**
- `0 <= len(points) <= 10^4`
- `-10^16 <= points[i][j] <= 10^16`
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

**Constraints**
- `0 <= len(points) <= 10^4`
- `-10^16 <= points[i][j] <= 10^16`
""",
                  "def point_counts(points: List[List[int]]) -> Dict:\n    counts = {}\n    for p in points:\n        key = tuple(p)\n        counts[key] = counts.get(key, 0) + 1\n    return counts\n",
                  [([[[1, 2], [1, 2], [0, 0]]], {(1, 2): 2, (0, 0): 1}), ([[]], {})], [[[[5, 5]]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Tuple keys:** `counts[tuple(p)]`
- **Counting pattern:** `counts.get(key, 0) + 1`
"""),
                P("py-same-letter-set", 'Same Set of Letters', "def same_letters(first_word: str, second_word: str) -> bool:",
                  """
A word puzzle checks whether two words use exactly the same letters, ignoring how many times each appears. Write `same_letters(first_word, second_word)` using `frozenset`.

**Constraints**
- `0 <= len(first_word), len(second_word) <= 10^4`
""",
                  "def same_letters(first_word: str, second_word: str) -> bool:\n    return frozenset(first_word) == frozenset(second_word)\n",
                  [(["listen", "silent"], True), (["aab", "ab"], True), (["abc", "abd"], False)], [["", ""], ["a", ""]],
                  require=["frozenset"],
                  grammar="""
## Building blocks
- **An unchangeable set:** `frozenset(first_word)`
- **Sets compare by contents:** `frozenset("ab") == frozenset("ba")` is `True`.
"""),
                P("py-group-by-letter-set", 'Group Words by Their Letters', "def group_letter_sets(words: List[str]) -> List[List[str]]:",
                  """
A word puzzle groups words that use the same set of letters. Write `group_letter_sets(words)` to return the groups as a list of lists, in the order each group's first word appears, with each group's words in their original order.

**Constraints**
- `0 <= len(words) <= 10^4`
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
                P("py-hash-equal", 'Compare Hashes', "def same_hash(first: str, second: str) -> bool:",
                  """
Dicts and sets look values up by their hash. Write `same_hash(first, second)` to return whether `hash(first) == hash(second)`. Equal strings always hash the same.

**Constraints**
- `first` and `second` are each a string, an int or a bool
""",
                  "def same_hash(first: str, second: str) -> bool:\n    return hash(first) == hash(second)\n",
                  [(["abc", "abc"], True), (["abc", "abd"], False)], [["", ""], ["a", "A"]],
                  require=["hash"],
                  grammar="""
## Building blocks
- **A value's hash:** `hash(first)`. Equal values → equal hashes; different values almost always differ.
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
