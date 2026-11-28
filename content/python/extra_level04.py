# Extra practice for Learn Python level 4 (Dicts, sets & tuples). See extra_level03.py for the format.
from _helpers import P, Q

EXTRA = {
    "dict-basics": dict(
        warmup=[
            P("py-service-owner", "Who Owns This Service?", "def owner(teams: Dict[str, str], service: str) -> str:",
              """
An on-call tool keeps a dict from each service name to the team that owns it. Write `owner(teams, service)` to return the team for `service`.

**Constraints**
- `1 <= len(teams) <= 1000`
- `service` is a key in `teams`
""",
              "def owner(teams: Dict[str, str], service: str) -> str:\n    return teams[service]\n",
              [([{"billing": "Ada", "search": "Bo"}, "search"], "Bo")], [[{"x": "y"}, "x"]],
              hints=["A dict looks things up by key: put the key in square brackets after the dict.",
                     "Here the key is the service name, and the value you get back is the team.",
                     "The service is always there, so plain square brackets are safe."],
              grammar="""
## Building blocks
- **Look up a key:** `ages["ada"]`
"""),
        ],
        practice=[
            P("py-restock-list", 'Items to Reorder', "def restock(stock: Dict[str, int], order: List[str]) -> List[str]:",
              """
A warehouse runs a script every time it receives an order. The script checks each item in the order against the warehouse's inventory. Any item with zero units in stock, or missing from the stock dictionary entirely, needs to be reordered. Write `restock()` to return the items that need reordering, in the same order they appear in `order`. An item that gets ordered twice appears twice in the list that's returned.

**Constraints**
- `0 <= len(stock), len(order) <= 10^4`
- `0 <= stock[name] <= 10^16`
""",
              "def restock(stock: Dict[str, int], order: List[str]) -> List[str]:\n    out = []\n    for item in order:\n        if stock.get(item, 0) == 0:\n            out.append(item)\n    return out\n",
              [([{"wireless earbuds": 120, "yoga mat": 0}, ["wireless earbuds", "yoga mat", "phone case"]], ["yoga mat", "phone case"]), ([{}, []], [])],
              [[{"desk lamp": 14}, ["desk lamp"]], [{}, ["board game", "water bottle"]]],
              hints=["Go through the items in `order` one by one.",
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
            P("py-registry-names", "List the Registered Names", "def names(registry: Dict[str, int]) -> List[str]:",
              """
A plugin registry maps each plugin's name to its load order. Write `names(registry)` to return the plugin names as a list, in the order they were registered.

**Constraints**
- `0 <= len(registry) <= 10^4`
- `0 <= registry[name] <= 10^16`
""",
              "def names(registry: Dict[str, int]) -> List[str]:\n    return list(registry.keys())\n",
              [([{"auth": 3, "cache": 1}], ["auth", "cache"]), ([{}], [])], [[{"a": 1}]],
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
            P("py-cheapest-supplier", 'Cheapest Supplier', "def cheapest(prices: Dict[str, float]) -> str:",
              """
A purchasing tool compares quotes from several suppliers for a given order. Write `cheapest()` so that it returns the name of the cheapest supplier given the input. If several tie, return the one that comes first alphabetically.

**Constraints**
- `1 <= len(prices) <= 10^4`
- `0 <= prices[name] <= 10^6`, with at most two decimal places
""",
              "def cheapest(prices: Dict[str, float]) -> str:\n    best = None\n    for name, cost in sorted(prices.items()):\n        if best is None or cost < prices[best]:\n            best = name\n    return best\n",
              [([{"Northgate Supply": 412.50, "Harbor Line Packaging": 398.75, "Brightwell Industrial": 398.75}], "Brightwell Industrial"),
               ([{"Cedar Ridge Lumber": 1249.99}], "Cedar Ridge Lumber")],
              [[{"Pinecrest Office Supply": 24.99, "Lakeshore Stationers": 24.98}], [{"Willowbrook Farms": 3.15, "Amberfield Dairy": 3.89}]],
              hints=["`.items()` gives each supplier together with its price.",
                     "Sorting the items puts the names in alphabetical order, so on a tie the first one you see is the right one.",
                     "Keep the best supplier so far, and replace it only when a price is strictly lower."],
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
            P("py-has-repeat-visitor", 'Any Repeat Visitors?', "def any_repeat(visitors: List[str]) -> bool:",
              """
An analytics report flags whether anyone visited the site more than once today. Write `any_repeat(visitors)`, where `visitors` lists user names in the order they arrived, to return `True` if any name appears more than once.

**Constraints**
- `0 <= len(visitors) <= 10^4`
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
            P("py-new-faces", 'Count New Users', "def new_today(regulars: List[str], today: List[str]) -> int:",
              """
A growth report counts how many different people used the app today who aren't regular users. Write `new_today(regulars, today)`, where `today` can contain the same person more than once, to return that count.

**Constraints**
- `0 <= len(regulars), len(today) <= 10^4`
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
            P("py-shared-deps", 'Shared Dependencies', "def shared(first_service: Set[str], second_service: Set[str]) -> Set[str]:",
              """
Two services each have a set of the libraries they depend on. Write `shared(first_service, second_service)` to return the libraries both services use, with the `&` operator.

**Constraints**
- `0 <= len(first_service), len(second_service) <= 1000`
""",
              "def shared(first_service: Set[str], second_service: Set[str]) -> Set[str]:\n    return first_service & second_service\n",
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
            P("py-unvisited-pages", "Pages Nobody Visited", "def unvisited(pages: List[str], visited: List[str]) -> int:",
              """
A site audit compares every page with the pages that got traffic. Both lists can contain repeats. Write `unvisited(pages, visited)` to return how many different pages got no visits at all.

**Constraints**
- `0 <= len(pages), len(visited) <= 10^4`
""",
              "def unvisited(pages: List[str], visited: List[str]) -> int:\n    return len(set(pages) - set(visited))\n",
              [([["home", "about", "blog", "about"], ["about"]], 2), ([[], []], 0)], [[["a"], ["a"]], [["a", "b"], []]],
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
            P("py-make-pair", 'Return a Pair', "def bundle(item: str, price: int) -> Tuple[str, int]:",
              """
An order system records each sale as an `(item, price)` tuple. Write `bundle(item, price)` to return that tuple.

**Constraints**
- `0 <= len(item) <= 10^4`
- `price` is a number or `None`
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
            P("py-best-sale", 'Biggest Single Sale', "def best_sale(sales: List[Tuple[str, int]]) -> str:",
              """
A sales report highlights the item behind the largest single sale. Each sale is an `(item, price)` tuple. Write `best_sale(sales)` to return the item from the sale with the highest price, or the first one if several tie.

**Constraints**
- `1 <= len(sales) <= 10^4`
- `-10^16 <= sales[i][1] <= 10^16`
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
            P("py-tuple-key", 'Look Up a Grid Cell', "def at(spots: List[List], x: int, y: int) -> str:",
              """
A floor-plan tool receives what's placed where as `[x, y, thing]` entries. Write `at(spots, x, y)` to turn the entries into a dict keyed by `(x, y)` tuples and return what's at the requested position, or `"empty"` if nothing is recorded there.

**Constraints**
- `0 <= len(spots) <= 10^4`
- `-10^16 <= x, y <= 10^16`
""",
              "def at(spots: List[List], x: int, y: int) -> str:\n    where = {}\n    for a, b, thing in spots:\n        where[(a, b)] = thing\n    return where.get((x, y), \"empty\")\n",
              [([[[0, 0, "desk"]], 0, 0], "desk"), ([[[0, 0, "desk"]], 1, 0], "empty")], [[[], 3, 4], [[[1, 2, "lamp"], [3, 4, "chair"]], 3, 4]],
              hints=["Tuples can be dict keys because they can't change; lists can't.",
                     "Loop over the entries, unpacking each into its two coordinates and the thing, and store the thing under the `(x, y)` tuple.",
                     "Look up the asked-for position with `.get`, using `\"empty\"` as the default."],
              grammar="""
## Building blocks
- **A tuple as a key:** `table[(2, 3)] = "chair"`
- **Unpack three values:** `for a, b, c in rows:`
- **Read with a default:** `d.get(key, "none")`
"""),
        ],
        practice=[
            P("py-visited-squares", 'Cells a Robot Visited', "def squares_walked(steps: str) -> int:",
              """
A warehouse robot starts at `(0, 0)` and moves one cell per command: `N`, `S`, `E` or `W`. Write `squares_walked(steps)` to return how many different cells it stood on, counting the start.

**Constraints**
- `0 <= len(steps) <= 10^4`
- `steps` is made of the letters `N`, `S`, `E` and `W`
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
            P("py-ds-guest-check", 'Fast Membership Checks', "def arrived(guest_list: List[str], arrivals: List[str]) -> List[bool]:",
              """
A door scanner checks every arriving badge against a very long guest list. Checking a list one item at a time is slow, so pick a better structure. Write `arrived(guest_list, arrivals)` to return, for each arrival in order, `True` if they're on the guest list.

**Constraints**
- `0 <= len(guest_list), len(arrivals) <= 10^4`
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
            P("py-ds-tally-and-order", 'Count Orders in Arrival Order', "def tally(orders: List[str]) -> List[Tuple[str, int]]:",
              """
A kitchen display counts how many times each dish has been ordered and lists the dishes in the order they were first ordered. Write `tally(orders)` to return a list of `(dish, count)` tuples in that order.

**Constraints**
- `0 <= len(orders) <= 10^4`
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
            P("py-ds-pick-structure", 'Pick the Right Structure', "def pick(task: str) -> str:",
              """
Write `pick(task)` to name the best structure for each job: `"list"`, `"tuple"`, `"set"` or `"dict"`. The `task` is one of `"queue"` (customers in arrival order), `"point"` (a fixed `(x, y)` position), `"dedupe"` (remove repeated names) or `"phonebook"` (look up a number by name).

**Constraints**
- `task` is `"queue"`, `"point"`, `"dedupe"` or `"phonebook"`
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
    id="review-4", title="Review: dicts, sets and tuples",
    intro="""
A mix of everything from this world: dicts for looking up and counting, sets for uniqueness, tuples for fixed bundles, and choosing between them.
""",
    problems=[
        P("py-review-loyal-customers", 'Users Active Every Day', "def loyal(days: List[List[str]]) -> List[str]:",
          """
A retention report wants the users who were active on **every** day in the period. Write `loyal(days)`, where each inner list holds one day's active users, to return those users in alphabetical order.

**Constraints**
- `1 <= len(days) <= 10^4`
- `0 <= len(days[i]) <= 10^4`
""",
          "def loyal(days: List[List[str]]) -> List[str]:\n    common = set(days[0])\n    for day in days[1:]:\n        common &= set(day)\n    return sorted(common)\n",
          [([[["ada", "bo"], ["bo", "ada", "cy"], ["bo", "ada"]]], ["ada", "bo"]), ([[["x"]]], ["x"])],
          [[[["a"], ["b"]]], [[["a", "b"], ["b", "a"]]]],
          hints=["Start with everyone from the first day as possible answers.",
                 "Each following day, keep only the people who also came that day: that's the intersection, `&`.",
                 "Sort what's left at the end."],
          grammar="""
## Building blocks
- **Intersect in place:** `group &= other_set`
- **All but the first:** `xs[1:]`
- **Sorted list from a set:** `sorted(s)`
"""),
        P("py-review-price-changes", 'Price Changes', "def changes(old: Dict[str, int], new: Dict[str, int]) -> List[Tuple[str, int]]:",
          """
A pricing job compares yesterday's and today's price lists. For every product on **both** lists whose price changed, report `(product, change)`, where change is new minus old. Write `changes(old, new)` to return those pairs sorted by product name.

**Constraints**
- `0 <= len(old), len(new) <= 10^4`
- `0 <= old[name], new[name] <= 10^16`
""",
          "def changes(old: Dict[str, int], new: Dict[str, int]) -> List[Tuple[str, int]]:\n    out = []\n    for item in sorted(old.keys() & new.keys()):\n        if old[item] != new[item]:\n            out.append((item, new[item] - old[item]))\n    return out\n",
          [([{"jam": 3, "tea": 2}, {"jam": 4, "tea": 2, "bun": 1}], [["jam", 1]]), ([{}, {}], [])],
          [[{"a": 5}, {"a": 2}], [{"a": 1, "b": 2}, {"b": 5, "a": 1}]],
          hints=["Only products on both lists matter. Dict key views support set operations, so `&` finds the shared keys.",
                 "Go through the shared products in alphabetical order.",
                 "Skip products whose price didn't change; for the rest, record the product with the new price minus the old one."],
          grammar="""
## Building blocks
- **The keys of a dict:** `d.keys()` (they work like a set).
- **In both:** `&`
- **Not equal:** `!=`
- **A pair in a list:** `out.append((name, diff))`
"""),
        P("py-review-busiest-page", "Most Popular Page", "def busiest(visits: List[Tuple[str, str]]) -> str:",
              """
An analytics job finds the page with the most **different** visitors. Each visit is a `(user, page)` tuple, and a user who visits a page twice only counts once. Write `busiest(visits)` to return that page; if pages tie, return the one that comes first alphabetically.

**Constraints**
- `1 <= len(visits) <= 10^4`
""",
              "def busiest(visits: List[Tuple[str, str]]) -> str:\n    people = {}\n    for who, page in visits:\n        people.setdefault(page, set()).add(who)\n    return min(people, key=lambda p: (-len(people[p]), p))\n",
              [([[("ada", "home"), ("ada", "home"), ("bo", "blog"), ("cy", "blog")]], "blog"), ([[("x", "a")]], "a")],
              [[[("a", "z"), ("b", "y")]], [[("a", "s"), ("b", "s"), ("a", "t")]]],
              hints=["For each page, keep a **set** of its visitors so repeat visits only count once.",
                     "A dict from page to set works well; `setdefault(page, set())` creates each set the first time.",
                     "Pick the page with the biggest set. To break ties alphabetically, compare `(-size, name)` with `min`."],
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
