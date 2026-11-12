# Python building blocks used across the problem set.
# `snippet` is run at build time; its output is shown on the card.
# Quiz questions with predict=True are checked by running `code` and comparing stdout to the marked answer.

CONCEPTS = [
    # ------------------------------------------------------------------ core data structures
    dict(
        id="dict",
        title="dict (hash map)",
        group="Core data structures",
        summary="""
A `dict` (dictionary) stores a value under a key, like a labeled lookup table. You can usually look up, add, or remove an item in about the same amount of time, even as the dictionary grows (average O(1), or constant-time, operations). This makes it useful for questions like "Have I seen this before?", "Where did I see it?", and "How many times have I seen it?".

Keys must be **hashable** (Python can turn them into a stable lookup value), such as integers, strings, or tuples of those. A list cannot be a key because it can change; convert it with `tuple(lst)` first.
""",
        snippet="""seen = {}
for i, word in enumerate(["a", "b", "a"]):
    if word in seen:
        print(word, "first seen at", seen[word])
    seen[word] = i

print(seen.get("z", -1))          # default instead of KeyError
counts = {}
counts["x"] = counts.get("x", 0) + 1
print(counts)
groups = {}
groups.setdefault("k", []).append(1)
print(groups)
for key, value in seen.items():
    print(key, value)
""",
        notes="""
- `d[k]` raises **KeyError** if `k` is missing; `d.get(k, default)` doesn't.
- Iteration order is insertion order (guaranteed since Python 3.7).
- Tuples are hashable: `d[(r, c)] = ...` is the standard way to key by coordinates.
- In the worst case (many hash collisions), each operation is O(n), but in interviews you quote the **O(1) average**.
""",
        quiz=[
            dict(q="What does this print?", code="d = {}\nd['a'] = 1\nd['a'] = 2\nprint(len(d), d['a'])", options=["1 2", "2 2", "2 1", "1 1"], answer=0, predict=True,
                 why="Assigning to an existing key overwrites it; there's still only one key."),
            dict(q="Which of these can **not** be a dict key?", options=["(1, 2)", '"abc"', "[1, 2]", "frozenset({1})"], answer=2,
                 why="Lists are mutable, so they aren't hashable. Use `tuple(lst)` instead."),
        ],
    ),
    dict(
        id="set",
        title="set",
        group="Core data structures",
        summary="""
A `set` stores each hashable value only once. Adding, removing, or checking for a value usually takes about the same time regardless of set size (average O(1), or constant time). Use a set to remember which items you have visited, remove duplicates, or look things up when you do not need to store a value with each item.
""",
        snippet="""visited = set()
visited.add((0, 0))
visited.add((0, 0))      # duplicates are ignored
print(len(visited), (0, 0) in visited)

a, b = {1, 2, 3}, {2, 3, 4}
print(a & b, a | b, a - b)   # intersection, union, difference
print(len(set([3, 1, 3, 2])))
empty = set()                 # NOT {} (that's an empty dict)
print(type(empty).__name__, type({}).__name__)
""",
        notes="""
- `{}` is an empty **dict**; an empty set is `set()`.
- Sets are unordered: never rely on the order you iterate them in.
- `len(set(nums)) != len(nums)` is the one-line duplicate check.
- Sets support `&` (intersection), `|` (union), `-` (difference), and `^` (symmetric difference).
""",
        quiz=[
            dict(q="What does this print?", code="s = {1, 2}\ns.add(2)\ns.add(3)\nprint(len(s))", options=["3", "4", "2", "Error"], answer=0, predict=True,
                 why="Adding 2 again does nothing; only 3 is new."),
            dict(q="What does this print?", code="print(type({}).__name__)", options=["dict", "set", "tuple", "NoneType"], answer=0, predict=True,
                 why="Empty braces make an empty dict. Use `set()` for an empty set."),
        ],
    ),
    dict(
        id="membership",
        title="The `in` operator (membership)",
        group="Core data structures",
        summary="""
`x in container` asks "is x here?" (a membership test). How long that check takes depends on the container, and using the wrong container is a common hidden performance problem:

| container | cost of `x in c` |
|---|---|
| `set`, `dict` (keys) | O(1) average |
| `list`, `tuple`, `str` | O(n), a linear scan |

Turning a list into a set first is often what makes a solution O(n) instead of O(n²).
""",
        snippet="""nums = list(range(100_000))
lookup = set(nums)
print(99_999 in nums)    # scans the whole list
print(99_999 in lookup)  # one hash lookup
print("b" in {"a": 1, "b": 2})   # checks dict KEYS, not values
print("ell" in "hello")          # substring test on strings
""",
        notes="""
- `in` on a dict checks **keys**. Use `v in d.values()` for values (O(n)).
- `in` on a string is a substring search, not a character-set test.
- `not in` is the negation: `if x not in seen:`.
""",
        quiz=[
            dict(q="Inside a loop over `n` items you check `if x in my_list` where `my_list` has n items. What is the total time?",
                 options=["O(n²)", "O(n)", "O(n log n)", "O(1)"], answer=0, why="Each `in` check on a list takes O(n) time, and it runs n times. Using a set instead makes the total O(n)."),
            dict(q="What does this print?", code="d = {'a': 1}\nprint(1 in d, 'a' in d)", options=["False True", "True True", "True False", "False False"], answer=0, predict=True,
                 why="`in` on a dict checks keys only."),
        ],
    ),
    dict(
        id="list-stack",
        title="list as a stack",
        group="Core data structures",
        summary="""
A Python `list` is a resizable array. Adding an item to the end with `append(x)` and removing the last item with `pop()` take O(1) time. This makes a list a good **stack**: the last item added is the first one removed (last in, first out, or LIFO). Use it to match brackets, search depth-first, store undo steps, or build results.

Popping from the **front** (`pop(0)`) is O(n) because every element shifts. Use `collections.deque` for queues.
""",
        snippet="""stack = []
stack.append(1)
stack.append(2)
stack.append(3)
print(stack[-1])     # peek at the top
print(stack.pop())   # remove the top
print(stack)
print(bool([]))      # empty list is falsy, so 'while stack:' works
""",
        notes="""
- `lst[-1]` peeks at the last element; it raises IndexError on an empty list.
- `while stack:` loops until the stack is empty.
- `pop(0)` and `insert(0, x)` are O(n). Avoid them in loops.
- `path.append(x)` … `path.pop()` is the backtracking idiom: choose, recurse, un-choose.
""",
        quiz=[
            dict(q="What does this print?", code="s = [1, 2, 3]\ns.append(4)\ns.pop()\ns.pop()\nprint(s)", options=["[1, 2]", "[3, 4]", "[1, 2, 3]", "[2, 3]"], answer=0, predict=True,
                 why="`pop()` removes items from the end of the list, so it removes 4 and then 3."),
            dict(q="Which operation is **O(n)** on a list?", options=["lst.pop(0)", "lst.pop()", "lst.append(x)", "lst[-1]"], answer=0,
                 why="Removing the first element shifts every other element left."),
        ],
    ),
    dict(
        id="counter",
        title="Counter & defaultdict",
        group="Core data structures",
        summary="""
The `collections` module has two dictionary types that save you from writing repeated setup code:

- `Counter(iterable)` counts how often each item occurs, and a missing key reads as 0.
- `defaultdict(factory)` creates a default value (like `[]` or `0`) the first time you touch a missing key.
""",
        snippet="""from collections import Counter, defaultdict

c = Counter("banana")
print(c["a"], c["z"])            # missing -> 0, no KeyError
print(c.most_common(2))
print(Counter("abc") == Counter("cab"))   # anagram check

groups = defaultdict(list)
for word in ["eat", "tea", "tan"]:
    groups["".join(sorted(word))].append(word)
print(dict(groups))
""",
        notes="""
- `Counter(a) == Counter(b)` is an O(n) anagram test.
- `defaultdict(int)` behaves like a counter; `defaultdict(list)` groups items; `defaultdict(set)` can store each node's neighbours (an adjacency set).
- Reading a missing key on a defaultdict **inserts** it. Use `k in d` if you only want to check.
""",
        quiz=[
            dict(q="What does this print?", code="from collections import Counter\nc = Counter([1, 1, 2])\nprint(c[1], c[3])", options=["2 0", "2 None", "Error", "1 0"], answer=0, predict=True,
                 why="A Counter returns 0 for missing keys instead of raising KeyError."),
            dict(q="What does this print?", code="from collections import defaultdict\nd = defaultdict(list)\nd['x']\nprint(len(d))", options=["1", "0", "Error", "None"], answer=0, predict=True,
                 why="Simply reading a missing key on a defaultdict creates that key."),
        ],
    ),
    dict(
        id="deque",
        title="deque (double-ended queue)",
        group="Core data structures",
        summary="""
`collections.deque` lets you add or remove an item at either end in O(1) time. It is useful as a **queue**: the first item added is the first one removed (first in, first out, or FIFO). Queues are used in breadth-first search, level-by-level tree walks, and sliding-window maximum problems.
""",
        snippet="""from collections import deque

q = deque([1, 2])
q.append(3)          # enqueue at the right
print(q.popleft())   # dequeue from the left: O(1)
q.appendleft(0)
print(list(q))

# BFS skeleton: process one level at a time
q = deque(["root"])
level = 0
while q:
    for _ in range(len(q)):
        node = q.popleft()
    level += 1
print("levels:", level)
""",
        notes="""
- `popleft()` is O(1), while `list.pop(0)` is O(n).
- `for _ in range(len(q))` saves the number of items at the start of the loop, so you can process exactly one level of the tree before moving to the next (level-by-level BFS).
- Indexing into the middle (`q[i]`) is O(n). It's a linked structure.
""",
        quiz=[
            dict(q="What does this print?", code="from collections import deque\nq = deque([1, 2, 3])\nq.append(4)\nq.popleft()\nprint(q[0])", options=["2", "1", "4", "3"], answer=0, predict=True,
                 why="`popleft()` removes 1, so 2 is now at the front."),
        ],
    ),
    dict(
        id="heapq",
        title="heapq (priority queue)",
        group="Core data structures",
        summary="""
`heapq` keeps a list arranged so its smallest item is always first (`heap[0]`). This arrangement is a **min-heap**. Adding or removing an item takes O(log n) time; arranging an existing list as a heap takes O(n) time with `heapify`.

Python only has a min-heap. For a **max-heap**, push negated values.
""",
        snippet="""import heapq

h = []
for x in [5, 1, 8, 3]:
    heapq.heappush(h, x)
print(h[0])                 # smallest, O(1) peek
print(heapq.heappop(h), heapq.heappop(h))

maxh = []
for x in [5, 1, 8]:
    heapq.heappush(maxh, -x)   # negate for a max-heap
print(-maxh[0])

# tuples compare element by element: (priority, tiebreak, payload)
tasks = [(2, 0, "write"), (1, 1, "read")]
heapq.heapify(tasks)
print(heapq.heappop(tasks)[2])
print(heapq.nlargest(2, [4, 9, 1, 7]))
""",
        notes="""
- The list is **not** fully sorted. Only `h[0]` is guaranteed to be the minimum.
- Pushing objects that can't be compared (like ListNodes) crashes on ties. Use `(value, unique_index, obj)` tuples.
- Finding the top k items with a heap of size k takes O(n log k) time.
""",
        quiz=[
            dict(q="What does this print?", code="import heapq\nh = [5, 2, 9]\nheapq.heapify(h)\nheapq.heappush(h, 1)\nprint(heapq.heappop(h), h[0])", options=["1 2", "1 5", "9 5", "2 1"], answer=0, predict=True,
                 why="In a min-heap, pop returns the smallest value (1), and the new minimum is 2."),
            dict(q="How do you get a **max**-heap with heapq?", options=["Push negated values", "heapq.maxheap()", "Pass reverse=True", "Sort the list descending first"], answer=0,
                 why="`heapq` only provides a min-heap, so you negate values when you push them and negate them again when you pop."),
        ],
    ),
    dict(
        id="bisect",
        title="bisect (binary search helpers)",
        group="Core data structures",
        summary="""
`bisect_left(a, x)` finds the first position where `x` could go in the already-sorted list `a` without changing its order. It takes O(log n) time and is Python's built-in binary-search helper.
""",
        snippet="""from bisect import bisect_left, bisect_right, insort

a = [1, 3, 3, 7]
print(bisect_left(a, 3), bisect_right(a, 3))   # first / one-past-last position of 3
print(bisect_left(a, 4))                        # where 4 would go
i = bisect_left(a, 7)
print(i < len(a) and a[i] == 7)                 # membership test in O(log n)
insort(a, 5)
print(a)
""",
        notes="""
- It only works on lists that are already **sorted**.
- `bisect_left` gives the first position ≥ x; `bisect_right` gives the first position > x.
- `insort` finds the spot in O(log n) but inserts in O(n).
""",
        quiz=[
            dict(q="What does this print?", code="from bisect import bisect_left\nprint(bisect_left([2, 4, 6], 5))", options=["2", "1", "3", "-1"], answer=0, predict=True,
                 why="5 belongs between 4 (index 1) and 6 (index 2), so it would be inserted at index 2."),
        ],
    ),
    # ------------------------------------------------------------------ sequences & iteration
    dict(
        id="slicing",
        title="Slicing",
        group="Sequences & iteration",
        summary="""
`seq[start:stop:step]` makes a **new copy** of part of a list or string. The slice includes `start` but stops before `stop`. Negative positions count from the end, and `[::-1]` makes a reversed copy.
""",
        snippet="""s = "abcdef"
print(s[1:4], s[:2], s[-2:], s[::-1], s[::2])
nums = [1, 2, 3, 4]
copy = nums[:]           # shallow copy
copy.append(5)
print(nums, copy)
print(nums[10:])         # out-of-range slices don't raise errors
""",
        notes="""
- A slice costs **O(k)** time and memory for k elements. Slicing inside a loop or recursion can quietly make a solution O(n²).
- `s == s[::-1]` is a quick palindrome check, at O(n) extra space.
- Slices never raise IndexError, unlike plain indexing.
""",
        quiz=[
            dict(q="What does this print?", code="a = [10, 20, 30, 40, 50]\nprint(a[1:-1])", options=["[20, 30, 40]", "[20, 30, 40, 50]", "[10, 20, 30, 40]", "[20, 30]"], answer=0, predict=True,
                 why="The slice starts at index 1 and stops just before the last element."),
            dict(q="What does this print?", code="print('python'[::-2])", options=["nhy", "nohtyp", "pto", "ntp"], answer=0, predict=True,
                 why="A step of -2 starts at the last character and takes every second one going backwards: n, h, y."),
        ],
    ),
    dict(
        id="loops-range",
        title="range & for loops",
        group="Sequences & iteration",
        summary="""
`range(start, stop, step)` provides a sequence of integers without storing them all at once. It includes `start` and stops before `stop`. To count down, give it a negative step; the stop is still excluded: `range(n - 1, -1, -1)` visits `n-1 … 0`.
""",
        snippet="""print(list(range(3)))
print(list(range(2, 8, 2)))
print(list(range(4, -1, -1)))     # count down to 0 inclusive
n = 4
for i in range(n):
    for j in range(i + 1, n):     # every pair i < j
        pass
print(i, j)
""",
        notes="""
- `range` doesn't build a list, so it uses O(1) memory.
- Nested `for i … for j in range(i+1, n)` visits every unordered pair, which is O(n²).
- Prefer `for x in nums` when you don't need the index, and `enumerate` when you need both.
""",
        quiz=[
            dict(q="What does this print?", code="print(list(range(5, 0, -2)))", options=["[5, 3, 1]", "[5, 3]", "[5, 3, 1, -1]", "[]"], answer=0, predict=True,
                 why="It starts at 5 and steps by -2, stopping before 0."),
        ],
    ),
    dict(
        id="enumerate-zip",
        title="enumerate & zip",
        group="Sequences & iteration",
        summary="""
`enumerate(seq)` gives each item together with its position `(index, value)`, so there is no need to write `range(len(seq))`. `zip(a, b)` takes one item from each sequence at a time and stops when the **shorter** sequence ends.
""",
        snippet="""for i, ch in enumerate("abc"):
    print(i, ch)
for a, b in zip([1, 2, 3], "xy"):
    print(a, b)                  # stops after 2 pairs
words = ["ab", "abc", "b"]
for prev, cur in zip(words, words[1:]):   # adjacent pairs
    print(prev, "->", cur)
print(list(enumerate("hi", start=1)))
""",
        notes="""
- `zip(xs, xs[1:])` is a common way to compare neighbouring items.
- `zip` stops when the shorter input ends. This is useful when comparing matching positions at the start of two sequences (their common prefix).
- Both return iterators that produce values as you use them instead of saving all the values. Wrap one in `list()` if you want to print or reuse all its results.
""",
        quiz=[
            dict(q="What does this print?", code="print(list(zip('abc', [1, 2])))", options=["[('a', 1), ('b', 2)]", "[('a', 1), ('b', 2), ('c', None)]", "Error", "[('a', 'b'), (1, 2)]"], answer=0, predict=True,
                 why="`zip` stops as soon as the shorter input runs out."),
        ],
    ),
    dict(
        id="comprehensions",
        title="Comprehensions & generator expressions",
        group="Sequences & iteration",
        summary="""
`[expr for x in it if cond]` builds a list in one readable line. The same form with `{}` builds a set or dictionary; with `()` it makes a **generator**, which produces each value only when needed instead of saving them all at once. Generators are useful inside `sum`, `any`, and `max`.
""",
        snippet="""nums = [3, 1, 4, 1, 5]
print([x * x for x in nums if x > 1])
print({x % 3 for x in nums})                 # set comprehension
print({v: i for i, v in enumerate("abc")})   # dict comprehension
print(sum(x for x in nums if x % 2))         # generator: no list built
grid = [[0] * 3 for _ in range(2)]           # correct 2-D init
grid[0][0] = 1
print(grid)
""",
        notes="""
- **Gotcha:** `[[0] * 3] * 2` repeats the *same* inner list twice, so changing one row changes both. Use a comprehension.
- Generators can only be consumed once.
""",
        quiz=[
            dict(q="What does this print?", code="g = [[0] * 2] * 2\ng[0][0] = 9\nprint(g)", options=["[[9, 0], [9, 0]]", "[[9, 0], [0, 0]]", "[[9, 9], [0, 0]]", "Error"], answer=0, predict=True,
                 why="Both rows are the same list object. That's why `[[0] * c for _ in range(r)]` is the right way."),
            dict(q="What does this print?", code="print({x % 2 for x in range(10)})", options=["{0, 1}", "[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]", "{0: 1}", "{1}"], answer=0, predict=True,
                 why="A set comprehension keeps only the unique remainders."),
        ],
    ),
    dict(
        id="unpacking",
        title="Tuple unpacking & simultaneous assignment",
        group="Sequences & iteration",
        summary="""
`a, b = b, a` works because Python reads the **whole** right side before assigning either value. You can swap values or update two pointers without temporary variables. This feature is called tuple unpacking (assigning several values at once). It also works in loops: `for i, (x, y) in enumerate(pairs)`.
""",
        snippet="""a, b = 1, 2
a, b = b, a
print(a, b)
prev, cur = 0, 1
for _ in range(5):
    prev, cur = cur, prev + cur      # Fibonacci step, no temp needed
print(cur)
for start, end in [[1, 3], [2, 6]]:
    print(start, end)
first, *rest = [1, 2, 3]
print(first, rest)
""",
        notes="""
- You can reverse one linked-list pointer in a single line: `cur.next, prev, cur = prev, cur, cur.next`. The right side is computed first, but the targets are assigned **left to right**, so order matters when targets depend on each other.
- `x, y = point` raises ValueError if the lengths don't match.
""",
        quiz=[
            dict(q="What does this print?", code="a, b = 3, 5\na, b = b, a + b\nprint(a, b)", options=["5 8", "5 10", "8 5", "3 8"], answer=0, predict=True,
                 why="The right side uses the old values: (5, 3 + 5)."),
        ],
    ),
    dict(
        id="any-all",
        title="any & all",
        group="Sequences & iteration",
        summary="""
`any(iterable)` is True if at least one item is truthy; `all(iterable)` is True if every item is. Both **short-circuit**, stopping as soon as the answer is known, and they read nicely with a generator.
""",
        snippet="""nums = [2, 4, 7]
print(any(x % 2 for x in nums), all(x % 2 == 0 for x in nums))
print(any([]), all([]))       # empty: any -> False, all -> True
intervals = [[1, 2], [2, 3], [5, 9]]
print(all(intervals[i][0] >= intervals[i - 1][1] for i in range(1, len(intervals))))
""",
        notes="""
- `all([])` is **True**: there is no item that makes the statement false. This is called vacuous truth; watch for this edge case.
- Passing a generator instead of a list lets `any` and `all` stop as soon as they know the answer, without building a full list (short-circuiting).
""",
        quiz=[
            dict(q="What does this print?", code="print(all([]), any([]))", options=["True False", "False False", "True True", "False True"], answer=0, predict=True,
                 why="`all()` of an empty list is vacuously True, and `any()` of an empty list is False."),
        ],
    ),
    dict(
        id="min-max",
        title="min, max & running best",
        group="Sequences & iteration",
        summary="""
`best = max(best, candidate)` is a common way for greedy and dynamic-programming solutions to remember the best answer so far. `min` and `max` also take a `key` function and a `default` for empty input.
""",
        snippet="""best = 0
for x in [3, -1, 7, 2]:
    best = max(best, x)
print(best)
print(max(["pear", "fig", "banana"], key=len))
print(min([], default=None))
print(max(3, 9, 4))
""",
        notes="""
- `max([])` raises ValueError. Pass `default=` or check for an empty list first.
- Start a running minimum at `float('inf')` and a running maximum at `float('-inf')` (or the first element).
""",
        quiz=[
            dict(q="What does this print?", code="print(min(['bb', 'a', 'ccc'], key=len))", options=["a", "bb", "ccc", "1"], answer=0, predict=True,
                 why="The key function compares by length, and min returns the element itself."),
        ],
    ),
    dict(
        id="iterators",
        title="iter & next",
        group="Sequences & iteration",
        summary="""
`it = iter(seq)` makes an iterator that remembers its position, and `next(it)` pulls the next item. That's useful when recursive calls need to **share** progress through a sequence, as when rebuilding a tree from preorder or deserializing tokens.
""",
        snippet="""tokens = iter("1,2,N".split(","))
print(next(tokens), next(tokens))
print(next(tokens))
print(next(tokens, "done"))     # default instead of StopIteration
""",
        notes="""
- Calling `next` on an exhausted iterator raises **StopIteration** unless you give a default.
- Sharing one iterator across recursive calls avoids passing an index around.
""",
        quiz=[
            dict(q="What does this print?", code="it = iter([1, 2, 3])\nnext(it)\nprint(list(it))", options=["[2, 3]", "[1, 2, 3]", "[3]", "[]"], answer=0, predict=True,
                 why="The iterator already consumed 1, so list() gets the rest."),
        ],
    ),
    dict(
        id="loop-else",
        title="for … else",
        group="Sequences & iteration",
        summary="""
A loop's `else` block runs only if the loop finished **without `break`**. It's ideal for "searched everything and found nothing" logic.
""",
        snippet="""for x in [1, 3, 5]:
    if x % 2 == 0:
        print("found even", x)
        break
else:
    print("no even numbers")
""",
        notes="""
- Think of it as "no break" rather than "else". Many readers find it surprising, so mention it when you explain your code.
""",
        quiz=[
            dict(q="What does this print?", code="for i in range(3):\n    if i == 1:\n        break\nelse:\n    print('A')\nprint('B')", options=["B", "A\nB", "A", "Nothing"], answer=0, predict=True,
                 why="The loop breaks, so the else block is skipped."),
        ],
    ),
    dict(
        id="sorting",
        title="Sorting & key functions",
        group="Sequences & iteration",
        summary="""
`sorted(it)` returns a new list; `lst.sort()` reorders the existing list and returns **None**. Both are O(n log n) and **stable** (items with equal sort keys keep their original order). `key=` tells Python what part of each item to compare, often with a `lambda` function.
""",
        snippet="""intervals = [[5, 6], [1, 4], [2, 3]]
print(sorted(intervals))                        # by first item, then second
print(sorted(intervals, key=lambda iv: iv[1]))  # by end time
words = ["bb", "a", "ccc"]
print(sorted(words, key=len, reverse=True))
print("".join(sorted("listen")) == "".join(sorted("silent")))
x = [3, 1, 2]
print(x.sort())   # None! It sorts in place
print(x)
""",
        notes="""
- `x = x.sort()` sets x to **None**, which is a classic bug.
- Lists and tuples sort one item at a time from left to right (lexicographic order), so pairs like `[start, end]` sort by start time first.
- Sorting first often unlocks two-pointer or greedy solutions (3Sum, Merge Intervals).
""",
        quiz=[
            dict(q="What does this print?", code="a = [3, 1, 2]\nb = a.sort()\nprint(b)", options=["None", "[1, 2, 3]", "[3, 1, 2]", "Error"], answer=0, predict=True,
                 why="list.sort() works in place and returns None."),
            dict(q="What does this print?", code="print(sorted([[2, 1], [1, 9], [1, 3]]))", options=["[[1, 3], [1, 9], [2, 1]]", "[[2, 1], [1, 3], [1, 9]]", "[[1, 9], [1, 3], [2, 1]]", "Error"], answer=0, predict=True,
                 why="Lists are compared by their first elements, and ties are broken by their second elements."),
        ],
    ),
    # ------------------------------------------------------------------ functions & objects
    dict(
        id="recursion",
        title="Recursion",
        group="Functions & objects",
        summary="""
A recursive function solves a problem by calling itself on a smaller input. Every recursive function needs (1) a **base case** that stops, and (2) a step that makes the next input smaller or closer to that stopping case. Trees, backtracking, and divide-and-conquer problems often fit this pattern.
""",
        snippet="""def depth(tree):
    if tree is None:                 # base case
        return 0
    left, right = tree
    return 1 + max(depth(left), depth(right))

t = ((None, None), ((None, None), None))
print(depth(t))

import sys
print(sys.getrecursionlimit())       # default ~1000 frames
""",
        notes="""
- The recursion depth counts toward **space** complexity: O(h) for a tree of height h.
- Python's default limit is about 1000 frames. Deep linked lists or skewed trees can hit RecursionError, so use an explicit stack for those.
- `@functools.cache` saves each result so the function can reuse it instead of calculating it again (memoization). This is called top-down dynamic programming (DP).
""",
        quiz=[
            dict(q="What does this print?", code="def f(n):\n    if n <= 1:\n        return 1\n    return n * f(n - 1)\nprint(f(4))", options=["24", "10", "4", "RecursionError"], answer=0, predict=True,
                 why="f(4) computes 4 × 3 × 2 × 1, which is 24."),
            dict(q="What's the **space** complexity of a recursive DFS on a balanced binary tree with n nodes?", options=["O(log n)", "O(1)", "O(n)", "O(n log n)"], answer=0,
                 why="The call stack holds one frame per level, and a balanced tree has height log n."),
        ],
    ),
    dict(
        id="closures",
        title="Nested functions, closures & nonlocal",
        group="Functions & objects",
        summary="""
Defining a helper **inside** your function lets it use the outer function's variables (such as the grid, word, or result list) without passing them in. This is a closure. To **assign a new value** to an outer variable (rather than changing the list or dictionary it refers to), declare it `nonlocal`.
""",
        snippet="""def max_path(values):
    best = float("-inf")

    def visit(i):
        nonlocal best             # needed because we reassign best
        best = max(best, values[i])

    found = []
    def collect(x):
        found.append(x)           # mutation: no nonlocal needed

    for i in range(len(values)):
        visit(i)
        collect(values[i])
    return best, found

print(max_path([3, 8, 2]))
""",
        notes="""
- Without `nonlocal`, `best = ...` inside the helper creates a **new local** variable, and reading it first raises UnboundLocalError.
- Mutating a list or dict (`res.append`, `memo[k] = v`) doesn't need `nonlocal`.
""",
        quiz=[
            dict(q="What does this print?", code="def outer():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n    inc(); inc()\n    return count\nprint(outer())", options=["2", "0", "1", "UnboundLocalError"], answer=0, predict=True,
                 why="`nonlocal` lets `inc()` rebind the outer `count`, so after two calls it is 2."),
            dict(q="Without `nonlocal`, what happens when a nested function runs `total += 1` on an outer `total`?", options=["UnboundLocalError", "It updates the outer total", "It creates a global", "SyntaxError"], answer=0,
                 why="`+=` assigns, which makes `total` local to the nested function, and it's read before it's assigned."),
        ],
    ),
    dict(
        id="classes",
        title="Classes (design problems)",
        group="Functions & objects",
        summary="""
Design problems (Trie, MedianFinder, Codec) ask you to implement a class. State lives on `self` and is set up in `__init__`. Every method takes `self` first.
""",
        snippet="""class Counter:
    def __init__(self):
        self.total = 0            # instance state

    def add(self, n: int) -> None:
        self.total += n

    def value(self) -> int:
        return self.total

c = Counter()
c.add(3)
c.add(4)
print(c.value())
""",
        notes="""
- Forgetting `self.` makes a local variable that vanishes after the method returns.
- Never use a mutable default argument (`def __init__(self, items=[])`). It's shared between instances.
- Helper methods conventionally start with `_`.
""",
        quiz=[
            dict(q="What does this print?", code="class A:\n    def __init__(self):\n        x = 5\na = A()\nprint(hasattr(a, 'x'))", options=["False", "True", "5", "Error"], answer=0, predict=True,
                 why="`x = 5` without `self.` is just a local variable inside `__init__`."),
        ],
    ),
    dict(
        id="node-refs",
        title="Node objects & references",
        group="Functions & objects",
        summary="""
Linked lists, trees, and graphs contain objects that refer to other objects (`node.next`, `node.left`, `node.neighbors`). A variable holds a reference (a link to an object), so changing that link changes the structure. A temporary first node (dummy head) avoids many special cases when building or joining linked lists.
""",
        snippet="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

head = ListNode(1, ListNode(2, ListNode(3)))
dummy = tail = ListNode()
cur = head
while cur:
    if cur.val != 2:
        tail.next = cur
        tail = cur
    cur = cur.next
tail.next = None
out, cur = [], dummy.next
while cur:
    out.append(cur.val)
    cur = cur.next
print(out)
""",
        notes="""
- Save `nxt = cur.next` **before** overwriting `cur.next`, or you lose the rest of the list.
- Use `is` to compare node identity (`slow is fast`), and `==`/`.val` to compare values.
- Always check `node` (and `node.next`) for `None` before following a pointer.
""",
        quiz=[
            dict(q="What does this print?", code="class N:\n    def __init__(self, v, nxt=None):\n        self.v, self.next = v, nxt\na = N(1, N(2))\nb = a\nb.next = None\nprint(a.next)", options=["None", "<N object>", "2", "Error"], answer=0, predict=True,
                 why="`a` and `b` refer to the same node, so changing b.next changes a.next."),
        ],
    ),
    # ------------------------------------------------------------------ numbers & strings
    dict(
        id="infinity",
        title="float('inf') sentinels",
        group="Numbers & strings",
        summary="""
`float("inf")` is larger than every number, and `float("-inf")` is smaller. They are useful starting values when finding a minimum or maximum, and can mark a value as unreachable in a dynamic-programming table. Such a marker is called a sentinel.
""",
        snippet="""lo = float("inf")
for x in [7, 3, 9]:
    lo = min(lo, x)
print(lo)
print(float("inf") > 10**100, float("-inf") < -10**100)
import math
print(math.inf == float("inf"))
""",
        notes="""
- `inf + 1 == inf`, which is handy because sentinels survive arithmetic.
- If the answer can legitimately be "impossible", convert the sentinel back at the end (e.g. `-1`).
""",
        quiz=[
            dict(q="What does this print?", code="print(min(float('inf'), 5, 2))", options=["2", "inf", "5", "Error"], answer=0, predict=True,
                 why="Every real number is smaller than infinity, so the minimum is 2."),
        ],
    ),
    dict(
        id="int-division",
        title="// and % (floor division & modulo)",
        group="Numbers & strings",
        summary="""
`a // b` is floor division, which rounds toward **negative infinity**. `a % b` is the remainder, with the **sign of b**. Binary search midpoints use `(lo + hi) // 2`.
""",
        snippet="""print(7 // 2, 7 % 2)
print(-7 // 2, -7 % 2)     # floors toward -inf; remainder takes the sign of the divisor
print(divmod(17, 5))
lo, hi = 0, 9
print((lo + hi) // 2)
""",
        notes="""
- `-7 // 2 == -4` in Python (it's -3 in C/Java). Use `int(a / b)` to truncate toward zero.
- Python ints never overflow, so `(lo + hi) // 2` is safe.
""",
        quiz=[
            dict(q="What does this print?", code="print(-7 // 2, -7 % 2)", options=["-4 1", "-3 -1", "-3 1", "-4 -1"], answer=0, predict=True,
                 why="Floor division rounds down to -4; then -7 = 2 × (-4) + 1."),
        ],
    ),
    dict(
        id="bits",
        title="Bitwise operators",
        group="Numbers & strings",
        summary="""
Python's bitwise operators are `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), and the shifts `<<` and `>>`. A few facts come up again and again:

- `x & 1` gives the lowest bit, which tells you whether x is odd.
- `x & (x - 1)` clears the lowest set bit.
- `x ^ x == 0` and `x ^ 0 == x`, so XOR cancels out pairs of equal values.
""",
        snippet="""x = 0b1011
print(x & 1, x >> 1, x << 1)
print(bin(x & (x - 1)))     # lowest set bit cleared
print(5 ^ 5, 5 ^ 0)
missing = 0
for i, v in enumerate([0, 1, 3]):
    missing ^= i ^ v
print(missing ^ 3)
print(bin(10), int("1010", 2))
""",
        notes="""
- Python ints have unlimited size, so `~x == -x - 1` and there's no 32-bit wraparound. Mask with `& 0xFFFFFFFF` when a problem assumes 32-bit integers.
- For non-negative x, `x >> 1` is the same as `x // 2`.
""",
        quiz=[
            dict(q="What does this print?", code="print(6 & 3, 6 | 3, 6 ^ 3)", options=["2 7 5", "2 7 1", "3 6 5", "0 7 5"], answer=0, predict=True,
                 why="In binary, 6 is 110 and 3 is 011. So 110 & 011 = 010 (2), 110 | 011 = 111 (7), and 110 ^ 011 = 101 (5)."),
            dict(q="What does `n & (n - 1)` do?", options=["Clears the lowest set bit", "Sets the lowest bit", "Doubles n", "Counts the 1-bits"], answer=0,
                 why="Subtracting 1 flips the lowest 1-bit and every bit below it, so the AND clears that bit."),
        ],
    ),
    dict(
        id="strings",
        title="String essentials",
        group="Numbers & strings",
        summary="""
Strings are **immutable** sequences. Build output with a list and `"".join(parts)` at the end, never `+=` in a loop. `ord`/`chr` convert between characters and code points, which is handy for 26-slot count arrays.
""",
        snippet="""s = "A man, a plan!"
clean = "".join(c.lower() for c in s if c.isalnum())
print(clean)
print(ord("c") - ord("a"), chr(ord("a") + 2))
print("a,b,,c".split(","), " x  y ".split())
counts = [0] * 26
for c in "banana":
    counts[ord(c) - ord("a")] += 1
print(counts[:3])
""",
        notes="""
- `s += c` in a loop can be O(n²). Collect pieces in a list and join once.
- `str.split()` with no argument splits on any whitespace and drops empty pieces.
- `c.isalnum()`, `c.isdigit()`, `c.isalpha()` and `c.lower()` cover most filtering problems.
""",
        quiz=[
            dict(q="What does this print?", code="print(ord('d') - ord('a'))", options=["3", "4", "100", "Error"], answer=0, predict=True,
                 why="The code point of 'a' is 97 and that of 'd' is 100, so the difference is 3."),
            dict(q="What does this print?", code="print('a  b'.split(' '))", options=["['a', '', 'b']", "['a', 'b']", "['a  b']", "['a', ' ', 'b']"], answer=0, predict=True,
                 why="Splitting on an explicit single space keeps empty strings between consecutive spaces."),
        ],
    ),
]
