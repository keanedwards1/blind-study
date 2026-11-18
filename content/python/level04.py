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
                P("py-price-lookup", 'The Market Price Board', "def price(prices: Dict[str, int], item: str) -> int:",
                  """
The forest market keeps its prices on a board: a dict from item name to price in acorns. Customers ask about all sorts of things, including items the market doesn't sell.

- **You get:** `prices` (item name → price) and the `item` someone asked about.
- **Return:** that item's price, or `0` if it isn't on the board.
- **Example:** `{"tea": 3, "jam": 5}` and `"jam"` → `5`; asking for `"cake"` → `0`.
- **Watch out:** asking for a missing item must not crash.
""",
                  "def price(prices: Dict[str, int], item: str) -> int:\n    return prices.get(item, 0)\n",
                  [([{"tea": 3, "jam": 5}, "jam"], 5), ([{"tea": 3}, "cake"], 0)], [[{}, "x"], [{"a": 0}, "a"]],
                  require=[".get"],
                  grammar="""
## Building blocks
- **Read with a default:** `prices.get(item, 0)`
- **Compare:** `prices[item]` raises `KeyError` if it's missing.
"""),
                P("py-word-frequencies", 'Tally the Shouts', "def frequencies(words: List[str]) -> Dict[str, int]:",
                  """
Stallholders shout what they're selling all morning, and you've written every shout down. Now count how often each word came up.

- **You get:** `words`, a list of words in the order you heard them.
- **Return:** a dict mapping each word to how many times it appears.
- **Example:** `["a", "b", "a"]` → `{"a": 2, "b": 1}`.
- **Watch out:** an empty list gives an empty dict. Count it yourself (don't use `Counter`).
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
                P("py-invert-dict", 'The Translation Card', "def invert(d: Dict[str, str]) -> Dict[str, str]:",
                  """
The market's translation card turns each forest word into a city word. A visitor from the city needs it the other way round.

- **You get:** `d`, mapping forest words to city words. Every city word is different.
- **Return:** a new dict mapping each city word back to its forest word.
- **Example:** `{"a": "x", "b": "y"}` → `{"x": "a", "y": "b"}`.
""",
                  "def invert(d: Dict[str, str]) -> Dict[str, str]:\n    out = {}\n    for k, v in d.items():\n        out[v] = k\n    return out\n",
                  [([{"a": "x", "b": "y"}], {"x": "a", "y": "b"}), ([{}], {})], [[{"one": "1"}]],
                  grammar="""
## Building blocks
- **Key and value together:** `for cap, value in mapping.items():`
- **Store the other way round:** `acc[x] = kk`
"""),
                P("py-first-repeat", "Haven't I Heard That?", "def first_repeat(words: List[str]) -> str:",
                  """
The market parrot repeats things, but only some things. Reading its chatter from left to right, find the first word it says a **second** time.

- **You get:** `words`, the parrot's chatter in order.
- **Return:** the first word you meet for the second time, or `""` if it never repeats itself.
- **Example:** `["a", "b", "c", "b", "a"]` → `"b"` (you hear `b` again before you hear `a` again).
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
                P("py-total-stock", 'Count the Crates', "def total_stock(stock: Dict[str, int]) -> int:",
                  """
At closing time the storekeeper wants one number: how many crates are left in total, whatever is in them.

- **You get:** `stock`, mapping each item to how many crates of it there are.
- **Return:** the total number of crates.
- **Example:** `{"apples": 3, "pears": 4}` → `7`. An empty store has `0`.
""",
                  "def total_stock(stock: Dict[str, int]) -> int:\n    return sum(stock.values())\n",
                  [([{"apples": 3, "pears": 4}], 7), ([{}], 0)], [[{"x": -1, "y": 1}]],
                  require=[".values"],
                  grammar="""
## Building blocks
- **Just the values:** `stock.values()`
- **Add them:** `sum(...)`
"""),
                P("py-sorted-keys", 'Alphabetise the Stalls', "def sorted_keys(d: Dict[str, int]) -> List[str]:",
                  """
The new market map should list the stalls in alphabetical order.

- **You get:** `d`, mapping stall names to their pitch numbers.
- **Return:** a list of the stall names in alphabetical order.
- **Example:** `{"b": 1, "a": 2}` → `["a", "b"]`.
""",
                  "def sorted_keys(d: Dict[str, int]) -> List[str]:\n    return sorted(d)\n",
                  [([{"b": 1, "a": 2}], ["a", "b"]), ([{}], [])], [[{"z": 0, "m": 0, "a": 0}]],
                  grammar="""
## Building blocks
- **Looping over a dict gives keys:** so `sorted(d)` sorts the keys.
"""),
                P("py-merge-settings", 'House Rules', "def merge(defaults: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:",
                  """
Every stall starts with the market's default settings, and a stall can override some of them with its own rules.

- **You get:** `defaults` and `overrides`, both dicts from setting name to value.
- **Return:** a **new** dict with every default, replaced by the override wherever the stall set one. Any extra keys in `overrides` are included too.
- **Example:** `{"size": 10, "bold": 0}` with `{"bold": 1}` → `{"size": 10, "bold": 1}`.
- **Watch out:** don't change either of the dicts you were given.
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
                P("py-pop-key", 'Sold!', "def take(d: Dict[str, int], key: str) -> List:",
                  """
When an item sells, it comes off the shelf and you note its price.

- **You get:** `d` (the shelf: item → price) and the `key` of the item that sold.
- **Return:** a list `[price, shelf afterwards]`. If the item isn't on the shelf, return `[None, d]` with the shelf unchanged.
- **Example:** `{"a": 1, "b": 2}` and `"a"` → `[1, {"b": 2}]`.
""",
                  "def take(d: Dict[str, int], key: str) -> List:\n    value = d.pop(key, None)\n    return [value, d]\n",
                  [([{"a": 1, "b": 2}, "a"], [1, {"b": 2}]), ([{"a": 1}, "z"], [None, {"a": 1}])], [[{}, "x"]],
                  require=[".pop"],
                  grammar="""
## Building blocks
- **Remove and return, with a default:** `d.pop(key, None)`. Without the default, a missing key raises `KeyError`.
"""),
                P("py-group-by-initial", 'Shelves by Letter', "def by_initial(words: List[str]) -> Dict[str, List[str]]:",
                  """
The market library shelves its recipe cards by first letter, keeping the cards on each shelf in the order they arrived.

- **You get:** `words`, the recipe names in arrival order. None is empty.
- **Return:** a dict mapping each first letter to the list of names that start with it.
- **Example:** `["apple", "bean", "avocado"]` → `{"a": ["apple", "avocado"], "b": ["bean"]}`.
""",
                  "def by_initial(words: List[str]) -> Dict[str, List[str]]:\n    groups = {}\n    for w in words:\n        groups.setdefault(w[0], []).append(w)\n    return groups\n",
                  [([["apple", "bean", "avocado"]], {"a": ["apple", "avocado"], "b": ["bean"]}), ([[]], {})], [[["x", "y", "x"]]],
                  require=[".setdefault"],
                  grammar="""
## Building blocks
- **Get the list, creating it if missing:** `groups.setdefault(key, [])`
- **Then add to it:** `.append(w)` on what `setdefault` returns.
"""),
                P("py-zip-to-dict", 'Pair the Labels', "def to_dict(keys: List[str], values: List[int]) -> Dict[str, int]:",
                  """
Two lists came back from the stocktake: the item labels and, in the same order, the counts.

- **You get:** `keys` and `values`, the same length.
- **Return:** a dict pairing each label with the count at the same position.
- **Example:** `["a", "b"]` and `[1, 2]` → `{"a": 1, "b": 2}`.
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
                P("py-unique-count", 'How Many Kinds?', "def distinct(items: List[int]) -> int:",
                  """
A basket of mushrooms holds lots of repeats. The forager wants to know how many **different** kinds are in it.

- **You get:** `items`, a list of mushroom numbers (repeats allowed).
- **Return:** how many different values there are.
- **Example:** `[1, 2, 2, 3, 3, 3]` → `3`. An empty basket has `0`.
""",
                  "def distinct(items: List[int]) -> int:\n    return len(set(items))\n",
                  [([[1, 2, 2, 3, 3, 3]], 3), ([[]], 0)], [[[7] * 10], [list(range(50))]],
                  require=["set"],
                  grammar="""
## Building blocks
- **Drop duplicates:** `set(items)`
- **Count:** `len(...)`
"""),
                P("py-dedupe-keep-order", 'The Guest Book', "def dedupe(items: List[int]) -> List[int]:",
                  """
Some visitors signed the guest book more than once. Keep each name the first time it appears, in the order people signed.

- **You get:** `items`, the signatures in order (as numbers).
- **Return:** the list without repeats, keeping first appearances in their original order.
- **Example:** `[3, 1, 3, 2, 1]` → `[3, 1, 2]`.
- **Watch out:** a set alone loses the order.
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
                P("py-unique-letters-set", "Sign-Painter's Letters", "def letters(word: str) -> Set[str]:",
                  """
The sign-painter only needs one stencil per letter, however many times it's used.

- **You get:** `word`, the text of the sign.
- **Return:** the **set** of its letters.
- **Example:** `"hello"` → `{"h", "e", "l", "o"}`. An empty sign needs `set()`.
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
                P("py-in-both", 'Stocked at Both Stalls', "def both(a: List[int], b: List[int]) -> Set[int]:",
                  """
Two stalls want to know which products they *both* sell, so they can agree on a price.

- **You get:** `a` and `b`, each stall's product numbers.
- **Return:** the set of products found in both lists.
- **Example:** `[1, 2, 3]` and `[2, 3, 4]` → `{2, 3}`.
""",
                  "def both(a: List[int], b: List[int]) -> Set[int]:\n    return set(a) & set(b)\n",
                  [([[1, 2, 3], [2, 3, 4]], {2, 3}), ([[1], [2]], set())], [[[], []], [[5, 5], [5]]],
                  compare="strict", require=["op:&"],
                  grammar="""
## Building blocks
- **Make sets:** `set(a)`, `set(b)`
- **Intersection:** `&`
"""),
                P("py-in-either", 'The Combined Catalogue', "def either(a: List[int], b: List[int]) -> Set[int]:",
                  """
The two stalls are printing one catalogue together. Every product either of them sells goes in, once.

- **You get:** `a` and `b`, each stall's product numbers.
- **Return:** the set of products in at least one list.
- **Example:** `[1, 2]` and `[2, 3]` → `{1, 2, 3}`.
""",
                  "def either(a: List[int], b: List[int]) -> Set[int]:\n    return set(a) | set(b)\n",
                  [([[1, 2], [2, 3]], {1, 2, 3}), ([[], []], set())], [[[1], []]],
                  compare="strict", require=["op:|"],
                  grammar="""
## Building blocks
- **Union:** `{1, 2} | {2, 3}` gives `{1, 2, 3}`.
"""),
                P("py-only-in-first", "Who's Still Missing?", "def missing(invited: List[str], arrived: List[str]) -> List[str]:",
                  """
The market feast is starting. Check the invitations against the people who've arrived.

- **You get:** `invited` and `arrived`, two lists of names.
- **Return:** the invited guests who haven't arrived, in alphabetical order.
- **Example:** `["ada", "bo", "cy"]` and `["bo"]` → `["ada", "cy"]`.
""",
                  "def missing(invited: List[str], arrived: List[str]) -> List[str]:\n    return sorted(set(invited) - set(arrived))\n",
                  [([["ada", "bo", "cy"], ["bo"]], ["ada", "cy"]), ([["a"], ["a"]], [])], [[[], ["x"]], [["z", "y"], []]],
                  require=["op:-"],
                  grammar="""
## Building blocks
- **Difference:** `{1, 2, 3} - {2}` gives `{1, 3}`.
- **Sorted list from a set:** `sorted(...)`
"""),
                P("py-in-exactly-one", 'Swap Meet', "def exactly_one(a: List[int], b: List[int]) -> List[int]:",
                  """
Two traders compare their collections. Anything only *one* of them owns is up for swapping.

- **You get:** `a` and `b`, each trader's item numbers.
- **Return:** the items in one list but not the other, in increasing order.
- **Example:** `[1, 2, 3]` and `[3, 4]` → `[1, 2, 4]`.
""",
                  "def exactly_one(a: List[int], b: List[int]) -> List[int]:\n    return sorted(set(a) ^ set(b))\n",
                  [([[1, 2, 3], [3, 4]], [1, 2, 4]), ([[1], [1]], [])], [[[], [1, 1]], [[5, 6], [7, 8]]],
                  require=["op:^"],
                  grammar="""
## Building blocks
- **Symmetric difference:** `{1, 2} ^ {2, 3}` gives `{1, 3}`.
"""),
                P("py-is-subset", 'Can We Bake It?', "def can_make(needed: List[str], have: List[str]) -> bool:",
                  """
The baker has a recipe and a pantry. The recipe can be made if every ingredient it needs is somewhere in the pantry. How much of each doesn't matter.

- **You get:** `needed` (the recipe's ingredients) and `have` (what's in the pantry).
- **Return:** `True` if every needed ingredient is in the pantry, otherwise `False`.
- **Example:** `["egg", "milk"]` and `["milk", "egg", "flour"]` → `True`.
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
                P("py-swap-pair", 'Trade Places', "def swap(a: int, b: int) -> Tuple[int, int]:",
                  """
Two stallholders swap pitches for the day.

- **You get:** two numbers, `a` and `b`.
- **Return:** the tuple `(b, a)`.
- **Example:** `1, 2` → `(2, 1)`.
""",
                  "def swap(a: int, b: int) -> Tuple[int, int]:\n    return b, a\n",
                  [([1, 2], (2, 1)), ([0, 0], (0, 0))], [[-1, 5]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Return a tuple:** `return q, p`. The comma makes the tuple; brackets are optional.
- **This task checks the type:** `[b, a]` is a list, so it won't pass.
"""),
                P("py-min-max-tuple", 'Cheapest and Dearest', "def low_high(nums: List[int]) -> Tuple[int, int]:",
                  """
A shopper wants the cheapest and the most expensive price on the board in one go.

- **You get:** `nums`, the prices (at least one).
- **Return:** the tuple `(cheapest, dearest)`.
- **Example:** `[3, 1, 2]` → `(1, 3)`. With a single price, both are that price.
""",
                  "def low_high(nums: List[int]) -> Tuple[int, int]:\n    return min(nums), max(nums)\n",
                  [([[3, 1, 2]], (1, 3)), ([[5]], (5, 5))], [[[-1, -9, 4]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Return two results at once:** `return a, b` returns a tuple.
"""),
                P("py-head-tail", 'First in the Queue', "def head_tail(items: List[int]) -> Tuple:",
                  """
The market queue: serve the person at the front and keep the rest waiting in order.

- **You get:** `items`, the queue (at least one person).
- **Return:** a tuple `(first person, list of everyone else)`. Use star unpacking.
- **Example:** `[1, 2, 3]` → `(1, [2, 3])`; `[9]` → `(9, [])`.
""",
                  "def head_tail(items: List[int]) -> Tuple:\n    first, *rest = items\n    return first, rest\n",
                  [([[1, 2, 3]], (1, [2, 3])), ([[9]], (9, []))], [[[0, 0]]],
                  compare="strict", require=["unpack"],
                  grammar="""
## Building blocks
- **Star unpacking:** `leader, *remainder = things`. `remainder` is always a list.
- **Return both:** `return one, tail_items`
"""),
                P("py-distance-tuples", 'As the Crow Flies', "def distance(p: Tuple[int, int], q: Tuple[int, int]) -> float:",
                  """
The market map gives each stall as `(x, y)` coordinates. How far is it in a straight line from one stall to another?

- **You get:** `p` and `q`, two `(x, y)` tuples.
- **Return:** the straight-line distance: √((x₁−x₂)² + (y₁−y₂)²).
- **Example:** `(0, 0)` and `(3, 4)` → `5.0`.
""",
                  "def distance(p: Tuple[int, int], q: Tuple[int, int]) -> float:\n    (x1, y1), (x2, y2) = p, q\n    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5\n",
                  [([(0, 0), (3, 4)], 5.0), ([(1, 1), (1, 1)], 0.0)], [[(-1, -1), (2, 3)], [(0, 0), (1, 1)]],
                  **{"in": ["tuple", "tuple"]},
                  grammar="""
## Building blocks
- **Unpack a tuple:** `ax, ay = pt`
- **Square root:** `** 0.5` (or `math.sqrt`).
"""),
                P("py-tuple-from-list", 'Seal the Order', "def freeze(items: List[int]) -> Tuple[int, ...]:",
                  """
Once an order is confirmed it mustn't change, so it's stored as a tuple instead of a list.

- **You get:** `items`, the order as a list.
- **Return:** the same items as a tuple.
- **Example:** `[1, 2]` → `(1, 2)`; `[]` → `()`.
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
                P("py-distinct-points", 'Pitch Map', "def distinct_points(points: List[List[int]]) -> int:",
                  """
Stalls report where they set up as `[x, y]` pairs, and some reported the same spot twice.

- **You get:** `points`, a list of `[x, y]` pairs.
- **Return:** how many different spots there are.
- **Example:** `[[1, 2], [3, 4], [1, 2]]` → `2`.
- **Watch out:** lists can't go in a set, but tuples can.
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
                P("py-point-counts", 'Busiest Spots', "def point_counts(points: List[List[int]]) -> Dict:",
                  """
Count how many stalls set up at each spot on the market map.

- **You get:** `points`, a list of `[x, y]` pairs.
- **Return:** a dict mapping each spot, as an `(x, y)` tuple, to how many times it appears.
- **Example:** `[[1, 2], [1, 2], [0, 0]]` → `{(1, 2): 2, (0, 0): 1}`.
""",
                  "def point_counts(points: List[List[int]]) -> Dict:\n    counts = {}\n    for p in points:\n        key = tuple(p)\n        counts[key] = counts.get(key, 0) + 1\n    return counts\n",
                  [([[[1, 2], [1, 2], [0, 0]]], {(1, 2): 2, (0, 0): 1}), ([[]], {})], [[[[5, 5]]]],
                  compare="strict",
                  grammar="""
## Building blocks
- **Tuple keys:** `counts[tuple(p)]`
- **Counting pattern:** `counts.get(key, 0) + 1`
"""),
                P("py-same-letter-set", 'Same Stencils', "def same_letters(a: str, b: str) -> bool:",
                  """
Two signs can share a stencil set if they use exactly the same letters (how many times doesn't matter).

- **You get:** two words, `a` and `b`.
- **Return:** `True` if they use the same set of letters. Use `frozenset`.
- **Example:** `"listen"` and `"silent"` → `True`; `"aab"` and `"ab"` → `True`.
""",
                  "def same_letters(a: str, b: str) -> bool:\n    return frozenset(a) == frozenset(b)\n",
                  [(["listen", "silent"], True), (["aab", "ab"], True), (["abc", "abd"], False)], [["", ""], ["a", ""]],
                  require=["frozenset"],
                  grammar="""
## Building blocks
- **An unchangeable set:** `frozenset(a)`
- **Sets compare by contents:** `frozenset("ab") == frozenset("ba")` is `True`.
"""),
                P("py-group-by-letter-set", 'Stencil Groups', "def group_letter_sets(words: List[str]) -> List[List[str]]:",
                  """
Group the market's sign words so that words using the same set of letters share one stencil kit.

- **You get:** `words`.
- **Return:** a list of groups, in the order each group's first word appears, with each group's words in their original order.
- **Example:** `["ab", "ba", "aab", "c"]` → `[["ab", "ba", "aab"], ["c"]]`.
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
                P("py-hash-equal", 'Matching Fingerprints', "def same_hash(a: str, b: str) -> bool:",
                  """
Dicts and sets find things by their "fingerprint" (their hash). Equal words always get the same fingerprint.

- **You get:** two words, `a` and `b`.
- **Return:** whether their hashes are equal.
- **Example:** `"abc"` and `"abc"` → `True`; `"abc"` and `"abd"` → `False`.
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
