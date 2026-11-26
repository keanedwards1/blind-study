# Learn Python placement test: 20 coding tasks, 2 per level, easiest first.
# Your level is the lowest level where you didn't pass both tasks (pass all 20 and you start at level 10).
# Tasks for levels 8-10 resemble Blind 75 problems at that difficulty without repeating any of them.


def P(slug, title, sig, desc, solution, examples, tests, *, difficulty="Easy", **spec):
    d = dict(slug=slug, title=title, difficulty=difficulty, desc=desc, hints=[], solution=solution,
             explanation="This is a placement task, so the solution is shown only to explain the result.",
             examples=examples, tests=tests, **spec)
    if sig:  # class tasks give their own `starter` instead
        d["sig"] = sig
    return d


PLACEMENT = [
    # ------------------------------------------------------------------ level 1: arithmetic, if/else
    dict(level=1, problem=P(
        "py-place-temperature", "Temperature Label", "def label(celsius: int) -> str:",
        """Return `"cold"` if `celsius` is below 10, `"mild"` if it is 10 up to (but not including) 25, and `"hot"` otherwise.

**Constraints**
- `-10^16 <= celsius <= 10^16`
""",
        'def label(celsius: int) -> str:\n    if celsius < 10:\n        return "cold"\n    if celsius < 25:\n        return "mild"\n    return "hot"\n',
        [([3], "cold"), ([18], "mild"), ([30], "hot")], [[10], [24], [25], [-5], [9]])),
    dict(level=1, problem=P(
        "py-place-next-step", "Next Step", "def next_step(number: int) -> int:",
        """If `number` is even, return half of it. If `number` is odd, return `3 * number + 1`.

**Constraints**
- `-10^16 <= number <= 10^16`
""",
        "def next_step(number: int) -> int:\n    if number % 2 == 0:\n        return number // 2\n    return 3 * number + 1\n",
        [([6], 3), ([7], 22), ([1], 4)], [[2], [100], [9], [0]])),
    # ------------------------------------------------------------------ level 2: strings
    dict(level=2, problem=P(
        "py-place-initials", "Initials", "def initials(full_name: str) -> str:",
        """Given a name made of words separated by single spaces, return the first letter of each word in capitals, each followed by a dot.

**Constraints**
- `1 <= len(full_name) <= 10^4`
""",
        'def initials(full_name: str) -> str:\n    return "".join(w[0].upper() + "." for w in full_name.split())\n',
        [(["ada lovelace"], "A.L."), (["Grace Brewster Hopper"], "G.B.H.")], [["x"], ["alan turing"], ["a b c d"]])),
    dict(level=2, problem=P(
        "py-place-word-palindrome", "Mirror Word", "def is_mirror(word: str) -> bool:",
        """Return `True` if `word` reads the same backwards, ignoring upper/lower case.

**Constraints**
- `0 <= len(word) <= 10^4`
- `word` is English letters
""",
        "def is_mirror(word: str) -> bool:\n    w = word.lower()\n    return w == w[::-1]\n",
        [(["Level"], True), (["Hello"], False), (["a"], True)], [["Racecar"], ["ab"], ["Noon"], [""], ["abca"]])),
    # ------------------------------------------------------------------ level 3: loops and lists
    dict(level=3, problem=P(
        "py-place-count-evens", "Count the Evens", "def count_evens(nums: List[int]) -> int:",
        """Return how many numbers in `nums` are even.

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
""",
        "def count_evens(nums: List[int]) -> int:\n    count = 0\n    for n in nums:\n        if n % 2 == 0:\n            count += 1\n    return count\n",
        [([[1, 2, 3, 4]], 2), ([[]], 0), ([[7, 9]], 0)], [[[0, -2, 5]], [[2, 2, 2, 2]], [list(range(101))]])),
    dict(level=3, problem=P(
        "py-place-running-total", "Running Total", "def running_total(nums: List[int]) -> List[int]:",
        """Return a list where each position holds the sum of `nums` up to and including that position.

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
""",
        "def running_total(nums: List[int]) -> List[int]:\n    out, total = [], 0\n    for n in nums:\n        total += n\n        out.append(total)\n    return out\n",
        [([[1, 2, 3]], [1, 3, 6]), ([[]], []), ([[5, -5, 5]], [5, 0, 5])], [[[0]], [[10, 20, 30, 40]], [[-1, -1, -1]]])),
    # ------------------------------------------------------------------ level 4: dicts and sets
    dict(level=4, problem=P(
        "py-place-letter-counts", "Letter Counts", "def letter_counts(word: str) -> Dict[str, int]:",
        """Return a dictionary mapping each letter in `word` to how many times it appears.

**Constraints**
- `0 <= len(word) <= 10^4`
""",
        "def letter_counts(word: str) -> Dict[str, int]:\n    counts = {}\n    for c in word:\n        counts[c] = counts.get(c, 0) + 1\n    return counts\n",
        [(["hello"], {"h": 1, "e": 1, "l": 2, "o": 1}), ([""], {})], [["aaa"], ["abcabc"], ["mississippi"]])),
    dict(level=4, problem=P(
        "py-place-common", "In Both Lists", "def common(first: List[int], second: List[int]) -> List[int]:",
        """Return the values that appear in both `first` and `second`, each listed once, in increasing order.

**Constraints**
- `0 <= len(first), len(second) <= 10^4`
- The values are all whole numbers or all strings
""",
        "def common(first: List[int], second: List[int]) -> List[int]:\n    return sorted(set(first) & set(second))\n",
        [([[1, 2, 2, 3], [2, 3, 4]], [2, 3]), ([[1], [2]], [])], [[[5, 1, 5], [5, 5]], [[], [1]], [[3, 2, 1], [1, 2, 3]]])),
    # ------------------------------------------------------------------ level 5: functions, key=, recursion
    dict(level=5, problem=P(
        "py-place-sort-by-length", "Sort by Length", "def sort_words(words: List[str]) -> List[str]:",
        """Return the words sorted from shortest to longest. Words of the same length go in alphabetical order.

**Constraints**
- `0 <= len(words) <= 10^4`
""",
        "def sort_words(words: List[str]) -> List[str]:\n    return sorted(words, key=lambda w: (len(w), w))\n",
        [([["pear", "fig", "apple", "kiwi"]], ["fig", "kiwi", "pear", "apple"]), ([[]], [])], [[["b", "a", "cc", "aa"]], [["same", "size", "word"]]])),
    dict(level=5, problem=P(
        "py-place-flatten", "Flatten", "def flatten(nested: list) -> List[int]:",
        """`nested` is a list whose items are numbers or more lists (which can be nested to any depth). Return all the numbers in one flat list, in order.

**Constraints**
- `0 <= len(nested) <= 10^4`
- Every number is from `-10^16` to `10^16`
""",
        "def flatten(nested: list) -> List[int]:\n    out = []\n    for x in nested:\n        if isinstance(x, list):\n            out.extend(flatten(x))\n        else:\n            out.append(x)\n    return out\n",
        [([[1, [2, [3, 4]], 5]], [1, 2, 3, 4, 5]), ([[]], [])], [[[[[[]]]]], [[[1], [2], [3]]], [[1, [2, [3, [4, [5]]]]]]],
        difficulty="Medium")),
    # ------------------------------------------------------------------ level 6: number tools, errors
    dict(level=6, problem=P(
        "py-place-to-binary", "To Binary", "def to_binary(number: int) -> str:",
        """Return `number` written in binary, without any prefix.

**Constraints**
- `0 <= number <= 10^16`
""",
        'def to_binary(number: int) -> str:\n    return bin(number)[2:]\n',
        [([5], "101"), ([0], "0"), ([8], "1000")], [[1], [255], [1024], [37]])),
    dict(level=6, problem=P(
        "py-place-sum-valid", "Sum the Valid Numbers", "def sum_valid(items: List[str]) -> int:",
        """Each item is text. Add up the ones that are valid whole numbers, with an optional `-` sign, and skip anything else, including decimals.

**Constraints**
- `0 <= len(items) <= 10^4`
""",
        "def sum_valid(items: List[str]) -> int:\n    total = 0\n    for s in items:\n        try:\n            total += int(s)\n        except ValueError:\n            pass\n    return total\n",
        [([["3", "x", "-2", "4.5"]], 1), ([[]], 0)], [[["10", "20"]], [["a", "b"]], [["007", " 5 ", "1e3"]]],
        difficulty="Medium")),
    # ------------------------------------------------------------------ level 7: classes, standard library
    dict(level=7, problem=P(
        "py-place-stack-class", "Stack Class", "",
        """Write a class `Stack` with:

- `push(item)`: add `item` to the top;
- `pop()`: remove and return the top item, or `None` if it's empty;
- `size()`: return how many items it holds.

**Constraints**
- `item` can be a value of any type
- Up to 100 method calls
""",
        "class Stack:\n    def __init__(self):\n        self.items = []\n\n    def push(self, item: int) -> None:\n        self.items.append(item)\n\n    def pop(self):\n        return self.items.pop() if self.items else None\n\n    def size(self) -> int:\n        return len(self.items)\n",
        [([["Stack", "push", "push", "pop", "size", "pop", "pop"], [[], [1], [2], [], [], [], []]], [None, None, None, 2, 1, 1, None])],
        [[["Stack", "size", "pop"], [[], [], []]], [["Stack", "push", "push", "push", "size", "pop"], [[], [5], [6], [7], [], []]]],
        kind="class", cls="Stack",
        starter="class Stack:\n    def __init__(self):\n        pass\n\n    def push(self, item: int) -> None:\n        pass\n\n    def pop(self):\n        pass\n\n    def size(self) -> int:\n        pass\n")),
    dict(level=7, problem=P(
        "py-place-top-words", "Top Words", "def top_words(text: str, count: int) -> List[str]:",
        """Return the `count` most frequent words in `text` (words are separated by spaces). Break ties alphabetically.

**Constraints**
- `1 <= len(text) <= 10^4`
- `text` is lowercase letters and spaces
- `1 <= count <= 10^16`
""",
        "def top_words(text: str, count: int) -> List[str]:\n    counts = Counter(text.split())\n    return sorted(counts, key=lambda w: (-counts[w], w))[:count]\n",
        [(["the cat and the hat", 2], ["the", "and"]), (["a b c", 2], ["a", "b"])], [["x x y y z", 2], ["one", 1], ["b a b a c c c", 3]],
        difficulty="Medium")),
    # ------------------------------------------------------------------ level 8: Blind 75 Easy style
    dict(level=8, problem=P(
        "py-place-first-unique", "First Unique Character", "def first_unique(text: str) -> int:",
        """Return the index of the first character in `text` that appears only once, or `-1` if there isn't one.

**Constraints**
- `0 <= len(text) <= 10^4`
""",
        "def first_unique(text: str) -> int:\n    counts = Counter(text)\n    for i, c in enumerate(text):\n        if counts[c] == 1:\n            return i\n    return -1\n",
        [(["leetcode"], 0), (["loveleetcode"], 2), (["aabb"], -1)], [[""], ["z"], ["abcabcd"], ["aabbccddeef"]])),
    dict(level=8, problem=P(
        "py-place-merge-sorted", "Merge Two Sorted Lists", "def merge(first: List[int], second: List[int]) -> List[int]:",
        """Return one sorted list with all the values from `first` and `second`, in O(len(first) + len(second)) time (don't just sort them together).

**Constraints**
- `0 <= len(first), len(second) <= 10^4`
- `first` and `second` are each sorted from smallest to largest
- `-10^16 <= first[i], second[i] <= 10^16`
""",
        "def merge(first: List[int], second: List[int]) -> List[int]:\n    i = j = 0\n    out = []\n    while i < len(first) and j < len(second):\n        if first[i] <= second[j]:\n            out.append(first[i])\n            i += 1\n        else:\n            out.append(second[j])\n            j += 1\n    return out + first[i:] + second[j:]\n",
        [([[1, 3, 5], [2, 4]], [1, 2, 3, 4, 5]), ([[], [1]], [1])], [[[], []], [[1, 1], [1, 1]], [[-5, 0, 9], [-6, 10]]],
        forbid=["sorted", ".sort"])),
    # ------------------------------------------------------------------ level 9: Blind 75 Medium style
    dict(level=9, problem=P(
        "py-place-subarray-sum", "Subarrays Summing to a Target", "def count_subarrays(nums: List[int], target: int) -> int:",
        """Return how many contiguous, non-empty sublists of `nums` add up to exactly `target`. Aim for O(n).

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
- `-10^16 <= target <= 10^16`
""",
        "def count_subarrays(nums: List[int], target: int) -> int:\n    seen = {0: 1}\n    total = count = 0\n    for n in nums:\n        total += n\n        count += seen.get(total - target, 0)\n        seen[total] = seen.get(total, 0) + 1\n    return count\n",
        [([[1, 1, 1], 2], 2), ([[1, 2, 3], 3], 2), ([[1, -1, 0], 0], 3)], [[[], 0], [[5], 5], [[0, 0, 0], 0], [[3, 4, 7, 2, -3, 1, 4, 2], 7], [list(range(1, 2001)), 4950]],
        difficulty="Medium")),
    dict(level=9, problem=P(
        "py-place-warmer-days", "Days Until Warmer", "def days_until_warmer(temps: List[int]) -> List[int]:",
        """For each day, return how many days you'd wait for a warmer temperature, or `0` if no warmer day comes. Aim for O(n).

**Constraints**
- `0 <= len(temps) <= 10^4`
- `-10^16 <= temps[i] <= 10^16`
""",
        "def days_until_warmer(temps: List[int]) -> List[int]:\n    answer = [0] * len(temps)\n    stack = []\n    for i, t in enumerate(temps):\n        while stack and temps[stack[-1]] < t:\n            j = stack.pop()\n            answer[j] = i - j\n        stack.append(i)\n    return answer\n",
        [([[73, 74, 75, 71, 69, 72, 76, 73]], [1, 1, 4, 2, 1, 1, 0, 0]), ([[30, 30]], [0, 0])], [[[]], [[90, 80, 70]], [[1, 2, 3, 4]], [list(range(3000, 0, -1)) + [5000]]],
        difficulty="Medium")),
    # ------------------------------------------------------------------ level 10: Blind 75 Medium/Hard style
    dict(level=10, problem=P(
        "py-place-grid-paths", "Paths Around Rocks", "def count_paths(grid: List[List[int]]) -> int:",
        """Start at the top-left cell of `grid` and move only right or down to reach the bottom-right. Cells with `1` are rocks you can't enter. Return the number of different paths (0 if the start or end is a rock).

**Constraints**
- `1 <= len(grid) <= 10^4`
- `1 <= len(grid[i]) <= 100`
- All rows have the same length
- `0 <= grid[i][j] <= 1`
""",
        "def count_paths(grid: List[List[int]]) -> int:\n    cols = len(grid[0])\n    row = [0] * cols\n    row[0] = 1\n    for r in grid:\n        for c in range(cols):\n            if r[c] == 1:\n                row[c] = 0\n            elif c > 0:\n                row[c] += row[c - 1]\n    return row[-1]\n",
        [([[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], 2), ([[[0, 1], [0, 0]]], 1), ([[[1]]], 0)], [[[[0]]], [[[0, 0], [0, 1]]], [[[0] * 10 for _ in range(10)]], [[[0, 0, 0, 0], [1, 1, 0, 1], [0, 0, 0, 0]]]],
        difficulty="Medium")),
    dict(level=10, problem=P(
        "py-place-rain-water", "Trapped Rain Water", "def trapped_water(heights: List[int]) -> int:",
        """`heights` describes a row of walls, each 1 unit wide. After it rains, how many units of water are trapped between the walls? Aim for O(n) time.

**Constraints**
- `0 <= len(heights) <= 10^4`
- `0 <= heights[i] <= 10^16`
""",
        "def trapped_water(heights: List[int]) -> int:\n    lo, hi = 0, len(heights) - 1\n    left_max = right_max = water = 0\n    while lo < hi:\n        if heights[lo] < heights[hi]:\n            left_max = max(left_max, heights[lo])\n            water += left_max - heights[lo]\n            lo += 1\n        else:\n            right_max = max(right_max, heights[hi])\n            water += right_max - heights[hi]\n            hi -= 1\n    return water\n",
        [([[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6), ([[4, 2, 0, 3, 2, 5]], 9)], [[[]], [[5]], [[1, 2, 3]], [[3, 0, 3]], [[5, 4, 1, 2]]],
        difficulty="Hard")),
]
