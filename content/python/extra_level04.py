# Extra practice for Learn Python level 4 (Dicts, sets & tuples): the forest market. See extra_level03.py for the format.
from _helpers import P, Q

EXTRA = {
    "dict-basics": dict(
        warmup=[
            P("py-stall-owner", "Who Runs This Stall?", "def owner(stalls: Dict[str, str], stall: str) -> str:",
              """
The market office has a dict from stall name to the person who runs it. Every stall you ask about is in it.

- **You get:** `stalls` and a `stall` name.
- **Return:** the name of the person who runs that stall.
- **Example:** `{"jam": "Ada", "tea": "Bo"}` and `"tea"` → `"Bo"`.
""",
              "def owner(stalls: Dict[str, str], stall: str) -> str:\n    return stalls[stall]\n",
              [([{"jam": "Ada", "tea": "Bo"}, "tea"], "Bo")], [[{"x": "y"}, "x"]],
              hints=["A dict looks things up by key: put the key in square brackets after the dict.",
                     "Here the key is the stall name, and the value you get back is the owner.",
                     "The stall is always there, so plain square brackets are safe."],
              grammar="""
## Building blocks
- **Look up a key:** `ages["ada"]`
"""),
        ],
        practice=[
            P("py-restock-list", "Restock List", "def restock(stock: Dict[str, int], wanted: List[str]) -> List[str]:",
              """
Before market day, check each wanted item against the stock. Anything with 0 crates, or missing from the stock entirely, goes on the restock list.

- **You get:** `stock` (item → crates) and `wanted` (items, in order).
- **Return:** the wanted items that need restocking, in the same order.
- **Example:** `{"jam": 2, "tea": 0}` and `["jam", "tea", "honey"]` → `["tea", "honey"]`.
- **Watch out:** a missing item must not crash; treat it as 0.
""",
              "def restock(stock: Dict[str, int], wanted: List[str]) -> List[str]:\n    out = []\n    for item in wanted:\n        if stock.get(item, 0) == 0:\n            out.append(item)\n    return out\n",
              [([{"jam": 2, "tea": 0}, ["jam", "tea", "honey"]], ["tea", "honey"]), ([{}, []], [])], [[{"a": 1}, ["a"]], [{}, ["x", "y"]]],
              hints=["Go through the wanted items one by one.",
                     "`.get(key, default)` reads a count without crashing, using the default when the item isn't in the dict.",
                     "If the count is 0 (including missing items), add the item to your result list."],
              grammar="""
## Building blocks
- **Read with a default:** `d.get(name, 0)`
- **Loop over a list:** `for thing in things:`
- **Add to a list:** `out.append(x)`
"""),
        ],
        reps=[
            Q("What does this print?", "5 0", "5 None", "5 KeyError", "None 0", code="p = {'jam': 5}\nprint(p.get('jam', 0), p.get('tea', 0))", predict=True,
              why="`get` returns the stored value when the key exists, and the default when it doesn't."),
            Q("What does this print?", "None", "0", "KeyError", "''", code="p = {'jam': 5}\nprint(p.get('tea'))", predict=True,
              why="Without a default, `get` returns `None` for a missing key."),
            Q("What does this print?", "KeyError", "None", "0", "jam", code="p = {'jam': 5}\ntry:\n    print(p['tea'])\nexcept KeyError:\n    print('KeyError')", predict=True,
              why="Square brackets raise `KeyError` for a missing key; `get` never does."),
            Q("What does this print?", "{'jam': 6}", "{'jam': 5}", "{'jam': 1}", "6", code="p = {'jam': 5}\np['jam'] = p.get('jam', 0) + 1\nprint(p)", predict=True,
              why="Read the old count with `get`, add one, and store it back under the same key."),
        ],
    ),
    "dict-methods": dict(
        warmup=[
            P("py-stall-names", "List the Stalls", "def stall_names(stalls: Dict[str, int]) -> List[str]:",
              """
The market crier needs every stall name in the order the stalls were registered.

- **You get:** `stalls` (name → pitch number).
- **Return:** a list of the names, in the dict's order.
- **Example:** `{"jam": 3, "tea": 1}` → `["jam", "tea"]`.
""",
              "def stall_names(stalls: Dict[str, int]) -> List[str]:\n    return list(stalls.keys())\n",
              [([{"jam": 3, "tea": 1}], ["jam", "tea"]), ([{}], [])], [[{"a": 1}]],
              hints=["Dicts remember the order keys were added.",
                     "`.keys()` gives the keys, but as a view rather than a list.",
                     "Wrap it in `list(...)` to get a real list."],
              grammar="""
## Building blocks
- **All the keys:** `d.keys()`
- **Turn it into a list:** `list(...)`
"""),
        ],
        practice=[
            P("py-cheapest-stall", "The Cheapest Stall", "def cheapest(prices: Dict[str, int]) -> str:",
              """
Which stall sells for the least? Several stalls may tie; pick the one that comes first alphabetically.

- **You get:** `prices` (stall → price), with at least one stall.
- **Return:** the name of the cheapest stall.
- **Example:** `{"tea": 3, "jam": 2, "bun": 2}` → `"bun"`.
""",
              "def cheapest(prices: Dict[str, int]) -> str:\n    best = None\n    for name, cost in sorted(prices.items()):\n        if best is None or cost < prices[best]:\n            best = name\n    return best\n",
              [([{"tea": 3, "jam": 2, "bun": 2}], "bun"), ([{"x": 1}], "x")], [[{"b": 1, "a": 1}], [{"z": 5, "y": 9}]],
              hints=["`.items()` gives each stall together with its price.",
                     "Sorting the items puts the stall names in alphabetical order, so on a tie the first one you see is the right one.",
                     "Keep the best stall so far, and replace it only when a price is strictly lower."],
              grammar="""
## Building blocks
- **Key and value together:** `for k, v in d.items():`
- **Alphabetical order:** `sorted(pairs)` sorts pairs by their first part.
- **Nothing yet:** `None`, checked with `x is None`.
"""),
        ],
        reps=[
            Q("What does this print?", "['a', 'b'] [1, 2]", "[('a', 1), ('b', 2)] [1, 2]", "['a', 'b'] ['a', 'b']", "error",
              code="d = {'a': 1, 'b': 2}\nprint(list(d), list(d.values()))", predict=True,
              why="Looping over a dict (or `list(d)`) gives its keys; `.values()` gives the values."),
            Q("What does this print?", "{'a': 1, 'b': 9}", "{'a': 1, 'b': 2}", "{'b': 9}", "error",
              code="d = {'a': 1, 'b': 2}\nd.update({'b': 9})\nprint(d)", predict=True, why="`update` replaces values for keys that already exist."),
            Q("What does this print?", "[] {'x': ['hi']}", "None {'x': ['hi']}", "[] {}", "error",
              code="d = {}\nlst = d.setdefault('x', [])\nprint(lst, end=' ')\nlst.append('hi')\nprint(d)", predict=True,
              why="`setdefault` stores the empty list and returns that same list, so appending to it changes the dict."),
        ],
    ),
    "sets": dict(
        warmup=[
            P("py-has-repeat-visitor", "A Returning Visitor?", "def any_repeat(visitors: List[str]) -> bool:",
              """
Did anyone visit the market more than once today?

- **You get:** `visitors`, names in the order they arrived.
- **Return:** `True` if any name appears more than once.
- **Example:** `["ada", "bo", "ada"]` → `True`; `["ada", "bo"]` → `False`.
""",
              "def any_repeat(visitors: List[str]) -> bool:\n    return len(set(visitors)) < len(visitors)\n",
              [([["ada", "bo", "ada"]], True), ([["ada", "bo"]], False)], [[[]], [["x", "x"]]],
              hints=["A set keeps only one copy of each name.",
                     "If there was a repeat, the set ends up smaller than the list.",
                     "Compare the two lengths."],
              grammar="""
## Building blocks
- **Unique values:** `set(names)`
- **How many:** `len(xs)`
"""),
        ],
        practice=[
            P("py-new-faces", "New Faces Today", "def new_today(regulars: List[str], today: List[str]) -> int:",
              """
How many **different** people came today who aren't regulars?

- **You get:** `regulars` and `today` (today's visitors, with repeats).
- **Return:** how many different non-regulars visited.
- **Example:** `["ada"]` and `["ada", "cy", "cy", "di"]` → `2`.
""",
              "def new_today(regulars: List[str], today: List[str]) -> int:\n    known = set(regulars)\n    fresh = set()\n    for name in today:\n        if name not in known:\n            fresh.add(name)\n    return len(fresh)\n",
              [([["ada"], ["ada", "cy", "cy", "di"]], 2), ([[], []], 0)], [[["a"], ["a"]], [[], ["x", "y", "x"]]],
              hints=["Put the regulars in a set so checking `name in ...` is instant.",
                     "Collect today's newcomers in another set, so repeats only count once.",
                     "Add a visitor only if they're not a regular, then count the set."],
              grammar="""
## Building blocks
- **Empty set:** `set()`
- **Add to a set:** `found.add(x)`
- **Not in it:** `x not in group`
"""),
        ],
        reps=[
            Q("What does this print?", "3", "5", "2", "{1, 2, 3}", code="print(len(set([1, 1, 2, 3, 3])))", predict=True, why="A set keeps one copy of each value."),
            Q("What does this print?", "<class 'dict'>", "<class 'set'>", "{}", "error", code="print(type({}))", predict=True,
              why="Empty braces make an empty **dict**. Use `set()` for an empty set."),
            Q("What does this print?", "True", "False", "1", "error", code="s = {3, 5}\nprint(5 in s)", predict=True, why="`in` checks membership instantly."),
        ],
    ),
    "set-operations": dict(
        warmup=[
            P("py-common-stalls", "Shared Suppliers", "def shared(a: Set[str], b: Set[str]) -> Set[str]:",
              """
Two markets each have a set of suppliers. Which suppliers work with both?

- **You get:** two sets, `a` and `b`.
- **Return:** the suppliers in both, using `&`.
- **Example:** `{"x", "y"}` and `{"y", "z"}` → `{"y"}`.
""",
              "def shared(a: Set[str], b: Set[str]) -> Set[str]:\n    return a & b\n",
              [([["x", "y"], ["y", "z"]], ["y"]), ([[], ["a"]], [])], [[["a"], ["a"]]],
              **{"in": ["set", "set"]},
              hints=["The values that are in both sets are called the intersection.",
                     "Python's `&` operator between two sets gives exactly that.",
                     "Return the result directly."],
              grammar="""
## Building blocks
- **In both sets:** `{1, 2} & {2, 3}` gives `{2}`.
"""),
        ],
        practice=[
            P("py-unvisited-stalls", "Stalls You Missed", "def missed(stalls: List[str], visited: List[str]) -> int:",
              """
At the end of the day, how many stalls did you never get to?

- **You get:** `stalls` (every stall, possibly listed twice) and `visited` (where you went, with repeats).
- **Return:** how many different stalls you didn't visit.
- **Example:** `["jam", "tea", "bun", "tea"]` and `["tea"]` → `2`.
""",
              "def missed(stalls: List[str], visited: List[str]) -> int:\n    return len(set(stalls) - set(visited))\n",
              [([["jam", "tea", "bun", "tea"], ["tea"]], 2), ([[], []], 0)], [[["a"], ["a"]], [["a", "b"], []]],
              hints=["Repeats don't matter, so sets fit.",
                     "With sets, `-` gives the items in the first set that aren't in the second.",
                     "Count what's left with `len`."],
              grammar="""
## Building blocks
- **Difference:** `{1, 2, 3} - {2}` gives `{1, 3}`.
- **How many:** `len(xs)`
"""),
        ],
        reps=[
            Q("What does this print?", "{1, 2, 3}", "{2}", "{1, 3}", "[1, 2, 2, 3]", code="print({1, 2} | {2, 3})", predict=True, why="`|` combines both sets."),
            Q("What does this print?", "{1}", "{3}", "{1, 3}", "{2}", code="print({1, 2} - {2, 3})", predict=True, why="`-` keeps what's in the first set only."),
            Q("What does this print?", "True", "False", "{1, 2}", "error", code="print({1, 2} <= {1, 2, 3})", predict=True, why="`<=` asks whether the first set is a subset of the second."),
        ],
    ),
    "tuples": dict(
        warmup=[
            P("py-make-pair", "Bundle a Pair", "def bundle(item: str, price: int) -> Tuple[str, int]:",
              """
Every sale is recorded as an `(item, price)` tuple.

- **You get:** `item` and `price`.
- **Return:** the tuple `(item, price)`.
- **Example:** `"jam", 3` → `("jam", 3)`.
""",
              "def bundle(item: str, price: int) -> Tuple[str, int]:\n    return (item, price)\n",
              [(["jam", 3], ["jam", 3])], [["tea", 0]],
              hints=["A tuple is a fixed group of values written with round brackets and commas.",
                     "Put the item first and the price second.",
                     "Return the tuple."],
              grammar="""
## Building blocks
- **A tuple:** `("a", 1)`
"""),
        ],
        practice=[
            P("py-best-sale", "Best Sale of the Day", "def best_sale(sales: List[Tuple[str, int]]) -> str:",
              """
Each sale is an `(item, price)` tuple. Which item made the single biggest sale?

- **You get:** `sales` (at least one).
- **Return:** the item from the sale with the highest price (the first one if tied).
- **Example:** `[("jam", 3), ("tea", 7), ("bun", 7)]` → `"tea"`.
""",
              "def best_sale(sales: List[Tuple[str, int]]) -> str:\n    best_item, best_price = sales[0]\n    for item, price in sales:\n        if price > best_price:\n            best_item, best_price = item, price\n    return best_item\n",
              [([[("jam", 3), ("tea", 7), ("bun", 7)]], "tea"), ([[("x", 1)]], "x")], [[[("a", 2), ("b", 1)]]],
              hints=["Unpack each tuple straight into two names in the `for` line.",
                     "Start with the first sale as the best, unpacked the same way.",
                     "Replace the best only when a price is strictly higher, so ties keep the first."],
              grammar="""
## Building blocks
- **Unpack a pair:** `name, cost = pair`
- **Unpack in a loop:** `for name, cost in pairs:`
"""),
        ],
        reps=[
            Q("What does this print?", "2 1", "1 2", "(1, 2)", "error", code="a, b = 1, 2\na, b = b, a\nprint(a, b)", predict=True,
              why="The right side is built first, so the values swap in one step."),
            Q("What does this print?", "TypeError", "(9, 2)", "(1, 2)", "None", code="t = (1, 2)\ntry:\n    t[0] = 9\nexcept TypeError:\n    print('TypeError')", predict=True,
              why="Tuples can't be changed after they're made."),
            Q("What does this print?", "1 [2, 3]", "1 (2, 3)", "[1] [2, 3]", "error", code="first, *rest = [1, 2, 3]\nprint(first, rest)", predict=True,
              why="The starred name collects everything left over into a list."),
        ],
    ),
    "hashing": dict(
        warmup=[
            P("py-tuple-key", "Map Grid Lookup", "def at(spots: List[List], x: int, y: int) -> str:",
              """
The market surveyor wrote down what stands where as `[x, y, thing]` entries. Turn them into a dict keyed by `(x, y)` tuples, then look up one spot.

- **You get:** `spots` (a list of `[x, y, thing]`) and a position `x`, `y`.
- **Return:** what's at that spot, or `"grass"` if nothing is recorded there.
- **Example:** `[[0, 0, "well"]]` with `0, 0` → `"well"`; with `1, 0` → `"grass"`.
""",
              "def at(spots: List[List], x: int, y: int) -> str:\n    where = {}\n    for a, b, thing in spots:\n        where[(a, b)] = thing\n    return where.get((x, y), \"grass\")\n",
              [([[[0, 0, "well"]], 0, 0], "well"), ([[[0, 0, "well"]], 1, 0], "grass")], [[[], 3, 4], [[[1, 2, "tree"], [3, 4, "cart"]], 3, 4]],
              hints=["Tuples can be dict keys because they can't change; lists can't.",
                     "Loop over the entries, unpacking each into its two coordinates and the thing, and store the thing under the `(x, y)` tuple.",
                     "Look up the asked-for position with `.get`, using `\"grass\"` as the default."],
              grammar="""
## Building blocks
- **A tuple as a key:** `table[(2, 3)] = "cart"`
- **Unpack three values:** `for a, b, c in rows:`
- **Read with a default:** `d.get(key, "none")`
"""),
        ],
        practice=[
            P("py-visited-squares", "Squares You've Walked", "def squares_walked(steps: str) -> int:",
              """
You start at `(0, 0)` on the market grid. Each letter in `steps` moves you one square: `N`, `S`, `E` or `W`. How many **different** squares did you stand on, counting the start?

- **You get:** `steps`, a string of moves.
- **Return:** the number of different squares visited.
- **Example:** `"NESW"` → `4` (you walk a little square and end where you started).
""",
              "def squares_walked(steps: str) -> int:\n    x = y = 0\n    seen = {(x, y)}\n    moves = {\"N\": (0, 1), \"S\": (0, -1), \"E\": (1, 0), \"W\": (-1, 0)}\n    for s in steps:\n        dx, dy = moves[s]\n        x, y = x + dx, y + dy\n        seen.add((x, y))\n    return len(seen)\n",
              [(["NESW"], 4), ([""], 1)], [["NNNN"], ["NSNS"], ["EEWW"]],
              hints=["Keep your position as two numbers and a set of every square you've stood on.",
                     "Squares go in the set as `(x, y)` tuples (lists can't go in a set).",
                     "A small dict from letter to `(dx, dy)` keeps the moves tidy. Start the set with `(0, 0)`, and add each new square after you move."],
              grammar="""
## Building blocks
- **A set holding one tuple:** `{(0, 0)}`
- **Add a tuple to a set:** `spots.add((a, b))`
- **Unpack a pair:** `dx, dy = (1, 0)`
"""),
        ],
        reps=[
            Q("What does this print?", "TypeError", "{[1, 2]}", "{1, 2}", "None",
              code="try:\n    s = {[1, 2]}\nexcept TypeError:\n    print('TypeError')", predict=True,
              why="Lists can change, so they can't be hashed and can't go in a set."),
            Q("What does this print?", "{(1, 2)}", "{[1, 2]}", "{1, 2}", "error", code="print({tuple([1, 2])})", predict=True,
              why="Turning the list into a tuple makes it hashable."),
            Q("What does this print?", "True", "False", "error", "None", code="print(frozenset('ab') == frozenset('ba'))", predict=True,
              why="Frozensets compare by their contents, ignoring order."),
        ],
    ),
}

NEW_CONCEPTS = [
    dict(
        id="choosing-structures", after="hashing", title="Choosing a data structure",
        builtins=[],
        intro="""
You now know four ways to keep a group of values together. Each one is good at different jobs, and picking the right one makes your code shorter and faster.

**A list** keeps items **in order** and allows **repeats**. Use it when order matters, like a queue of customers or a row of numbers. You read items by their position: `queue[0]` is the first. Checking whether something is in a list (`x in queue`) means looking at every item one by one, which gets slow for long lists.

**A tuple** is a list that **can't be changed** after it's made. Use it for a small, fixed group of values that belong together, like a point `(3, 4)` or a sale `("jam", 3)`. Because it can't change, a tuple can be a dict key or go in a set (it's *hashable*).

**A set** keeps **one copy of each value** and has **no order**. Use it to remove duplicates, or to ask "have I seen this?" over and over: `x in seen` is instant however big the set gets. Sets also do maths between groups: `&` (in both), `|` (in either), `-` (in the first only).

**A dict** maps **keys to values**. Use it to look things up by name (`prices["jam"]`), to count things (`counts[word] += 1`), or to group things (`groups[letter].append(word)`). Looking up a key is instant, just like a set.

| You need to… | Use |
|---|---|
| keep things in order, repeats allowed | list |
| a small fixed bundle, or a key made of several parts | tuple |
| remove duplicates, or check "seen it?" quickly | set |
| look up, count, or group by a key | dict |

**Common mistakes:** checking `x in some_list` inside a loop over a long list (use a set instead); trying to put a list in a set or use it as a dict key (use a tuple); and expecting a set to remember order (it doesn't, so sort it or use a list).
""",
        problems=[
            P("py-ds-guest-check", "The Fast Guest Check", "def arrived(guest_list: List[str], arrivals: List[str]) -> List[bool]:",
              """
The guest list is huge, and the door staff check every arrival against it. A list makes each check slow; pick a better structure.

- **You get:** `guest_list` and `arrivals`.
- **Return:** for each arrival, in order, `True` if they're on the guest list.
- **Example:** `["ada", "bo"]` and `["bo", "cy"]` → `[True, False]`.
""",
              "def arrived(guest_list: List[str], arrivals: List[str]) -> List[bool]:\n    guests = set(guest_list)\n    return [name in guests for name in arrivals]\n",
              [([["ada", "bo"], ["bo", "cy"]], [True, False]), ([[], []], [])],
              [[["a"], ["a", "a"]], [[f"g{i}" for i in range(3000)], [f"g{i}" for i in range(0, 6000, 2)]]],
              hints=["You check membership many times, which is exactly what a set is fast at.",
                     "Turn the guest list into a set once, before you start checking.",
                     "Then check each arrival with `in` and collect the answers in order."],
              grammar="""
## Building blocks
- **Make a set once:** `set(names)`
- **Is it in the set?** `name in group`
- **A list built from a loop:** `[f(x) for x in xs]`
"""),
            P("py-ds-tally-and-order", "Tally in Arrival Order", "def tally(orders: List[str]) -> List[Tuple[str, int]]:",
              """
Count how many times each item was ordered, and report the items in the order they were **first** ordered.

- **You get:** `orders`, item names in order.
- **Return:** a list of `(item, count)` tuples, in first-order order.
- **Example:** `["tea", "jam", "tea"]` → `[("tea", 2), ("jam", 1)]`.
""",
              "def tally(orders: List[str]) -> List[Tuple[str, int]]:\n    counts = {}\n    for item in orders:\n        counts[item] = counts.get(item, 0) + 1\n    return list(counts.items())\n",
              [([["tea", "jam", "tea"]], [["tea", 2], ["jam", 1]]), ([[]], [])], [[["x"]], [["a", "b", "a", "c", "b", "a"]]],
              hints=["Counting by name is a dict's job.",
                     "Dicts remember the order keys were first added, so the first-order order comes for free.",
                     "Count with the read-with-a-default pattern, then turn `.items()` into a list of tuples."],
              grammar="""
## Building blocks
- **Read with a default:** `d.get(k, 0)`
- **Store under a key:** `d[k] = v`
- **Key and value pairs as a list:** `list(d.items())`
"""),
            P("py-ds-pick-structure", "Pick the Right Tool", "def pick(task: str) -> str:",
              """
A quick quiz from the market manager. For each job, name the best structure: `"list"`, `"tuple"`, `"set"` or `"dict"`.

- **You get:** `task`, one of: `"queue"` (customers in arrival order), `"point"` (a fixed `(x, y)` position), `"dedupe"` (remove repeated names), `"phonebook"` (look up a number by name).
- **Return:** the best structure's name.
- **Example:** `"queue"` → `"list"`.
""",
              "def pick(task: str) -> str:\n    best = {\"queue\": \"list\", \"point\": \"tuple\", \"dedupe\": \"set\", \"phonebook\": \"dict\"}\n    return best[task]\n",
              [(["queue"], "list"), (["phonebook"], "dict")], [["point"], ["dedupe"]],
              hints=["Order and repeats → list. Fixed little bundle → tuple. One of each / fast \"seen it?\" → set. Look up by a key → dict.",
                     "A dict from task name to answer is a tidy way to write the answer table.",
                     "Then look the task up in your dict."],
              grammar="""
## Building blocks
- **A dict written out:** `{"a": 1, "b": 2}`
- **Look up a key:** `d[k]`
"""),
        ],
        quiz=[
            Q("You need to check \"have I seen this name?\" thousands of times. Which is fastest?", "a set", "a list", "a tuple", "a string",
              why="Sets check membership instantly; lists check every item."),
            Q("Which can be used as a dict key?", "`(1, 2)`", "`[1, 2]`", "`{1, 2}`", "`{'a': 1}`",
              why="Only values that can't change (hashable ones) can be keys, and a tuple of numbers can't change."),
            Q("You must keep customers in the order they arrived, and the same name can appear twice. Which fits?", "a list", "a set", "a dict", "a frozenset",
              why="Lists keep order and allow repeats; sets do neither."),
        ],
        reps=[
            Q("What does this print?", "[1, 2, 3]", "{1, 2, 3}", "[3, 2, 1]", "[1, 1, 2, 3]", code="print(sorted(set([3, 1, 2, 1])))", predict=True,
              why="The set removes the repeat; `sorted` gives back an ordered list."),
            Q("What does this print?", "{'a': 2, 'b': 1}", "{'a': 1, 'b': 1}", "['a', 'b', 'a']", "{'a', 'b'}",
              code="c = {}\nfor w in ['a', 'b', 'a']:\n    c[w] = c.get(w, 0) + 1\nprint(c)", predict=True, why="A dict counts by key."),
        ],
    ),
]

REVIEW = dict(
    id="review-4", title="Review: the market accounts",
    intro="""
A mix of everything from the market: dicts for looking up and counting, sets for uniqueness, tuples for fixed bundles, and choosing between them.
""",
    problems=[
        P("py-review-loyal-customers", "Loyal Customers", "def loyal(days: List[List[str]]) -> List[str]:",
          """
Each inner list is one market day's customers. A loyal customer came on **every** day.

- **You get:** `days`, at least one day.
- **Return:** the loyal customers in alphabetical order.
- **Example:** `[["ada", "bo"], ["bo", "ada", "cy"], ["bo", "ada"]]` → `["ada", "bo"]`.
""",
          "def loyal(days: List[List[str]]) -> List[str]:\n    common = set(days[0])\n    for day in days[1:]:\n        common &= set(day)\n    return sorted(common)\n",
          [([[["ada", "bo"], ["bo", "ada", "cy"], ["bo", "ada"]]], ["ada", "bo"]), ([[["x"]]], ["x"])],
          [[[["a"], ["b"]]], [[["a", "b"], ["b", "a"]]]],
          hints=["Start with everyone from the first day as possible loyal customers.",
                 "Each following day, keep only the people who also came that day: that's the intersection, `&`.",
                 "Sort what's left at the end."],
          grammar="""
## Building blocks
- **Intersect in place:** `group &= other_set`
- **All but the first:** `xs[1:]`
- **Sorted list from a set:** `sorted(s)`
"""),
        P("py-review-price-changes", "Price Changes", "def changes(old: Dict[str, int], new: Dict[str, int]) -> List[Tuple[str, int]]:",
          """
Compare yesterday's and today's price boards. For every item on **both** boards whose price changed, report `(item, change)` where change = new − old.

- **You get:** `old` and `new`, item → price.
- **Return:** the changes sorted by item name.
- **Example:** `{"jam": 3, "tea": 2}` and `{"jam": 4, "tea": 2, "bun": 1}` → `[("jam", 1)]`.
""",
          "def changes(old: Dict[str, int], new: Dict[str, int]) -> List[Tuple[str, int]]:\n    out = []\n    for item in sorted(old.keys() & new.keys()):\n        if old[item] != new[item]:\n            out.append((item, new[item] - old[item]))\n    return out\n",
          [([{"jam": 3, "tea": 2}, {"jam": 4, "tea": 2, "bun": 1}], [["jam", 1]]), ([{}, {}], [])],
          [[{"a": 5}, {"a": 2}], [{"a": 1, "b": 2}, {"b": 5, "a": 1}]],
          hints=["Only items on both boards matter. Dict key views support set operations, so `&` finds the shared keys.",
                 "Go through the shared items in alphabetical order.",
                 "Skip items whose price didn't change; for the rest, record the item with the new price minus the old one."],
          grammar="""
## Building blocks
- **The keys of a dict:** `d.keys()` (they work like a set).
- **In both:** `&`
- **Not equal:** `!=`
- **A pair in a list:** `out.append((name, diff))`
"""),
        P("py-review-busiest-stall", "Busiest Stall", "def busiest(visits: List[Tuple[str, str]]) -> str:",
          """
Each visit is a `(customer, stall)` tuple. The busiest stall had the most **different** customers (a customer who visits twice only counts once).

- **You get:** `visits` (at least one).
- **Return:** the busiest stall; if tied, the one that comes first alphabetically.
- **Example:** `[("ada", "jam"), ("ada", "jam"), ("bo", "tea"), ("cy", "tea")]` → `"tea"`.
""",
          "def busiest(visits: List[Tuple[str, str]]) -> str:\n    people = {}\n    for who, stall in visits:\n        people.setdefault(stall, set()).add(who)\n    return min(people, key=lambda s: (-len(people[s]), s))\n",
          [([[("ada", "jam"), ("ada", "jam"), ("bo", "tea"), ("cy", "tea")]], "tea"), ([[("x", "a")]], "a")],
          [[[("a", "z"), ("b", "y")]], [[("a", "s"), ("b", "s"), ("a", "t")]]],
          hints=["For each stall, keep a **set** of its customers so repeat visits only count once.",
                 "A dict from stall to set works well; `setdefault(stall, set())` creates each set the first time.",
                 "Pick the stall with the biggest set. To break ties alphabetically, compare `(-size, name)` with `min`."],
          grammar="""
## Building blocks
- **Get or create a value:** `d.setdefault(k, set())` returns the stored set, creating it the first time.
- **Add to a set:** `s.add(x)`
- **Smallest by a key:** `min(items, key=...)`
- **Size of a set:** `len(s)`
"""),
    ],
    quiz=[
        Q("What does this print?", "{'a': [1, 2]}", "{'a': 2}", "{'a': [2]}", "error", code="d = {}\nfor x in [1, 2]:\n    d.setdefault('a', []).append(x)\nprint(d)", predict=True,
          why="`setdefault` returns the same list each time, so both numbers go into it."),
        Q("Which removes duplicates but forgets the original order?", "`set(items)`", "`list(items)`", "`tuple(items)`", "`sorted(items)`",
          why="A set has no order."),
    ],
)
