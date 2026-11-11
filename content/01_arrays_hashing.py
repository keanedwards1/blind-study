CATEGORY = "Arrays & Hashing"

PROBLEMS = [
    dict(
        slug="contains-duplicate",
        title="Contains Duplicate",
        difficulty="Easy",
        sig="def contains_duplicate(nums: List[int]) -> bool:",
        desc="""
Given an integer list `nums`, return `True` if some value occurs **two or more times**, and `False` if every value is unique.

**Constraints**
- `0 <= len(nums) <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
""",
        hints=["A set lets you check whether you've seen a value before in O(1)."],
        solution="""
def contains_duplicate(nums: List[int]) -> bool:
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False
""",
        explanation="""
Walk the list once while keeping a set of values already seen. The first time a value is already in the set, a duplicate exists.

- **Time:** O(n)
- **Space:** O(n)

(Sorting and comparing neighbours also works in O(n log n) time and O(1) extra space.)
""",
        examples=[([[1, 2, 3, 1]], True), ([[1, 2, 3, 4]], False), ([[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], True)],
        tests=[[[]], [[5]], [[-1, -1]], [list(range(2000))], [list(range(2000)) + [1999]]],
    ),
    dict(
        slug="valid-anagram",
        title="Valid Anagram",
        difficulty="Easy",
        sig="def is_anagram(s: str, t: str) -> bool:",
        desc="""
Given two strings `s` and `t`, return `True` if `t` is a rearrangement of the letters of `s` (each letter used exactly as many times), otherwise `False`.

**Constraints**
- `0 <= len(s), len(t) <= 5 * 10^4`
- Both strings contain lowercase English letters.
""",
        hints=["Two strings are anagrams exactly when every character appears the same number of times in both."],
        solution="""
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    counts = {}
    for a, b in zip(s, t):
        counts[a] = counts.get(a, 0) + 1
        counts[b] = counts.get(b, 0) - 1
    return all(v == 0 for v in counts.values())
""",
        explanation="""
Count characters: add one for each char in `s`, subtract one for each char in `t`. If every count ends at zero, the strings are anagrams. (`Counter(s) == Counter(t)` is the one-liner.)

- **Time:** O(n)
- **Space:** O(1) — at most 26 keys.
""",
        examples=[(["anagram", "nagaram"], True), (["rat", "car"], False)],
        tests=[["a", "a"], ["ab", "a"], ["", ""], ["aacc", "ccac"], ["listen", "silent"], ["aabbcc", "abcabc"]],
    ),
    dict(
        slug="two-sum",
        title="Two Sum",
        difficulty="Easy",
        sig="def two_sum(nums: List[int], target: int) -> List[int]:",
        compare="unordered",
        desc="""
Given a list of integers `nums` and an integer `target`, return the **indices** of the two different elements that add up to `target`.

Each input has exactly one valid answer. The two indices may be returned in either order.

**Constraints**
- `2 <= len(nums) <= 10^4`
- `-10^9 <= nums[i], target <= 10^9`
""",
        hints=[
            "For each number x, the partner you need is target - x.",
            "Store each value's index in a dict as you go so you can look up the partner in O(1).",
        ],
        solution="""
def two_sum(nums: List[int], target: int) -> List[int]:
    index_of = {}
    for i, n in enumerate(nums):
        if target - n in index_of:
            return [index_of[target - n], i]
        index_of[n] = i
    return []
""",
        explanation="""
Make one pass over the list with a hash map from each value to its index. For each element, check whether its complement `target - n` has already been seen; if so, we have the pair. Inserting *after* the check prevents using the same element twice.

- **Time:** O(n)
- **Space:** O(n)
""",
        examples=[([[2, 7, 11, 15], 9], [0, 1]), ([[3, 2, 4], 6], [1, 2]), ([[3, 3], 6], [0, 1])],
        tests=[[[-1, -2, -3, -4, -5], -8], [[0, 4, 3, 0], 0], [[1, 5, 9, 13, 2], 15], [[5, 75, 25], 100], [[-10, 7, 19, 15], 9]],
    ),
    dict(
        slug="group-anagrams",
        title="Group Anagrams",
        difficulty="Medium",
        sig="def group_anagrams(strs: List[str]) -> List[List[str]]:",
        compare="unordered_nested",
        desc="""
Given a list of strings `strs`, group together the strings that are anagrams of one another. Return the groups in any order; strings within a group may also be in any order.

**Constraints**
- `1 <= len(strs) <= 10^4`
- `0 <= len(strs[i]) <= 100`, lowercase English letters
""",
        hints=["Anagrams share the same sorted string (or the same 26-letter count tuple). Use that as a dict key."],
        solution="""
def group_anagrams(strs: List[str]) -> List[List[str]]:
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
""",
        explanation="""
Every anagram group shares a canonical key. Using a tuple of 26 letter counts as the key avoids sorting each word.

- **Time:** O(n · k) where k is the max word length (O(n · k log k) if you sort each word for the key)
- **Space:** O(n · k)
""",
        examples=[
            ([["eat", "tea", "tan", "ate", "nat", "bat"]], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
            ([[""]], [[""]]),
            ([["a"]], [["a"]]),
        ],
        tests=[[["abc", "bca", "cab", "xyz", "zyx", "yxz", "foo"]], [["", ""]], [["ab", "ba", "abc"]], [["ddddddddddg", "dgggggggggg"]]],
    ),
    dict(
        slug="top-k-frequent-elements",
        title="Top K Frequent Elements",
        difficulty="Medium",
        sig="def top_k_frequent(nums: List[int], k: int) -> List[int]:",
        compare="unordered",
        desc="""
Given an integer list `nums` and an integer `k`, return the `k` values that occur most often. The answer is guaranteed to be unique; return it in any order.

**Constraints**
- `1 <= len(nums) <= 10^5`
- `1 <= k <=` number of distinct values

**Follow-up:** can you beat O(n log n)?
""",
        hints=[
            "First count frequencies with a dict.",
            "A frequency can be at most n, so you can bucket values by frequency and read buckets from high to low.",
        ],
        solution="""
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in count.items():
        buckets[freq].append(value)
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            result.append(value)
            if len(result) == k:
                return result
    return result
""",
        explanation="""
Count each value, then place values into buckets indexed by frequency (frequencies range 1..n). Scanning buckets from the highest frequency down collects the top `k` without sorting.

- **Time:** O(n)
- **Space:** O(n)

A heap of size k (`heapq.nlargest(k, count, key=count.get)`) is O(n log k) and also a fine answer.
""",
        examples=[([[1, 1, 1, 2, 2, 3], 2], [1, 2]), ([[1], 1], [1])],
        tests=[[[4, 4, 4, 5, 5, 6, 6, 6, 6], 2], [[-1, -1, 2, 2, 2, 3], 2], [[7, 7, 8, 8, 8, 9, 9, 9, 9, 10], 3], [[1, 2], 2]],
    ),
    dict(
        slug="encode-and-decode-strings",
        title="Encode and Decode Strings",
        difficulty="Medium",
        params=["strs"],
        starter="""def encode(strs: List[str]) -> str:
    pass


def decode(s: str) -> List[str]:
    pass
""",
        driver="""
def driver(ns, strs):
    encoded = resolve(ns, "encode")(list(strs))
    if not isinstance(encoded, str):
        raise TypeError(f"encode must return a str, got {type(encoded).__name__}")
    return resolve(ns, "decode")(encoded)
""",
        desc="""
Write `encode`, which turns a list of strings into a **single string**, and `decode`, which turns that string back into the original list.

The tests check that `decode(encode(strs)) == strs`. The strings can contain **any** characters, including `#`, digits, spaces, and empty strings, so a simple delimiter won't work on its own.

**Constraints**
- `0 <= len(strs) <= 200`
- `0 <= len(strs[i]) <= 200`
""",
        hints=["Prefix each string with its length and a separator, e.g. `5#hello`. When decoding, read the length first, then exactly that many characters."],
        solution="""
def encode(strs: List[str]) -> str:
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s: str) -> List[str]:
    result, i = [], 0
    while i < len(s):
        j = s.index("#", i)
        length = int(s[i:j])
        result.append(s[j + 1 : j + 1 + length])
        i = j + 1 + length
    return result
""",
        explanation="""
Use length-prefix encoding: write `len(s)`, a `#`, then `s` itself. When decoding, read digits up to the first `#`, which gives the length, then slice exactly that many characters. Since we never search *inside* a string's contents, any characters are safe.

- **Time:** O(total characters)
- **Space:** O(total characters)
""",
        examples=[([["neet", "code", "love", "you"]], ["neet", "code", "love", "you"]), ([[""]], [""])],
        tests=[[[]], [["a#b", "3#", "", ":;"]], [["with space", "x" * 50]], [["4#abcd", "12", "#"]]],
    ),
    dict(
        slug="product-of-array-except-self",
        title="Product of Array Except Self",
        difficulty="Medium",
        sig="def product_except_self(nums: List[int]) -> List[int]:",
        desc="""
Given an integer list `nums`, return a list `answer` where `answer[i]` is the product of every element of `nums` **except** `nums[i]`.

Solve it in O(n) time **without using division**.

**Constraints**
- `2 <= len(nums) <= 10^5`
- `-30 <= nums[i] <= 30`
""",
        hints=["answer[i] is the product of everything to the left of i multiplied by the product of everything to the right of i.", "Compute prefix products in one pass and suffix products in a second pass."],
        solution="""
def product_except_self(nums: List[int]) -> List[int]:
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer
""",
        explanation="""
Fill `answer[i]` with the product of everything left of `i` (running prefix), then sweep from the right multiplying in the running suffix product.

- **Time:** O(n)
- **Space:** O(1) extra (the output doesn't count)
""",
        examples=[([[1, 2, 3, 4]], [24, 12, 8, 6]), ([[-1, 1, 0, -3, 3]], [0, 0, 9, 0, 0])],
        tests=[[[2, 3]], [[0, 0]], [[5, 1, 1, 1]], [[-2, -3, 4, 1]], [[0, 4, 0]], [[1, 0, 2, 3]]],
    ),
    dict(
        slug="longest-consecutive-sequence",
        title="Longest Consecutive Sequence",
        difficulty="Medium",
        sig="def longest_consecutive(nums: List[int]) -> int:",
        desc="""
Given an unsorted integer list `nums`, return the length of the longest run of **consecutive integers** (like 4, 5, 6, 7) whose values all appear in `nums`. The values can appear anywhere in the list.

Aim for O(n) time.

**Constraints**
- `0 <= len(nums) <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
""",
        hints=["Put everything in a set.", "Only start counting from x if x - 1 is NOT in the set. That way each run is counted once."],
        solution="""
def longest_consecutive(nums: List[int]) -> int:
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
    return best
""",
        explanation="""
With all values in a set, a number starts a sequence only if `x - 1` is absent. From each start, extend upward while `x + length` exists. Each number is visited at most twice overall, so the work stays linear.

- **Time:** O(n)
- **Space:** O(n)
""",
        examples=[([[100, 4, 200, 1, 3, 2]], 4), ([[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], 9)],
        tests=[[[]], [[1]], [[1, 2, 0, 1]], [[9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]], [list(range(0, 4000, 2))], [list(range(3000, 0, -1))]],
    ),
]
