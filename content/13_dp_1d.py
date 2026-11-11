CATEGORY = "1-D Dynamic Programming"

PROBLEMS = [
    dict(
        slug="climbing-stairs",
        title="Climbing Stairs",
        difficulty="Easy",
        sig="def climb_stairs(n: int) -> int:",
        desc="""
A staircase has `n` steps. Each move climbs either 1 or 2 steps. In how many distinct ways can you reach the top?

**Constraints**
- `1 <= n <= 45`
""",
        hints=["To reach step i, you must have come from step i-1 or step i-2.", "The recurrence ways(i) = ways(i-1) + ways(i-2) is the Fibonacci recurrence."],
        solution="""
def climb_stairs(n: int) -> int:
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""",
        explanation="""
The last move was either 1 step or 2 steps, so `ways(n) = ways(n-1) + ways(n-2)`. Keep only the last two values.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([2], 2), ([3], 3)],
        tests=[[1], [5], [10], [45]],
    ),
    dict(
        slug="house-robber",
        title="House Robber",
        difficulty="Medium",
        sig="def rob(nums: List[int]) -> int:",
        desc="""
Houses along a street hold `nums[i]` dollars each. You can't take money from **two adjacent houses**. Return the largest total you can collect.

**Constraints**
- `1 <= len(nums) <= 100`
- `0 <= nums[i] <= 400`
""",
        hints=["At each house you either skip it (keep the best so far) or take it (adding its value to the best total from two houses back)."],
        solution="""
def rob(nums: List[int]) -> int:
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
""",
        explanation="""
The recurrence is `best(i) = max(best(i-1), best(i-2) + nums[i])`. Only the last two states matter, so two variables are enough.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[1, 2, 3, 1]], 4), ([[2, 7, 9, 3, 1]], 12)],
        tests=[[[5]], [[2, 1]], [[2, 1, 1, 2]], [[0, 0, 0]], [[1, 3, 1, 3, 100]]],
    ),
    dict(
        slug="house-robber-ii",
        title="House Robber II",
        difficulty="Medium",
        sig="def rob_circle(nums: List[int]) -> int:",
        desc="""
Same as House Robber, but the houses sit in a **circle**: the first and last houses are neighbours. You still can't take from two adjacent houses. Return the maximum total.

**Constraints**
- `1 <= len(nums) <= 100`
- `0 <= nums[i] <= 1000`
""",
        hints=["You can't take both the first and the last house.", "Solve the straight-line version twice: once without the last house, once without the first."],
        solution="""
def rob_circle(nums: List[int]) -> int:
    def line(houses):
        prev2 = prev1 = 0
        for x in houses:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1

    if len(nums) == 1:
        return nums[0]
    return max(line(nums[:-1]), line(nums[1:]))
""",
        explanation="""
The circle only forbids taking both ends. Either the first house is excluded or the last one is, so the answer is the better of two linear House Robber runs.

- **Time:** O(n)
- **Space:** O(1) beyond the slices
""",
        examples=[([[2, 3, 2]], 3), ([[1, 2, 3, 1]], 4), ([[1, 2, 3]], 3)],
        tests=[[[1]], [[1, 2]], [[200, 3, 140, 20, 10]], [[4, 1, 2, 7, 5, 3, 1]], [[0, 0]]],
    ),
    dict(
        slug="longest-palindromic-substring",
        title="Longest Palindromic Substring",
        difficulty="Medium",
        sig="def longest_palindrome(s: str) -> str:",
        checker="""
def check(args, result, expected):
    s = args[0]
    return isinstance(result, str) and len(result) == len(expected) and result in s and result == result[::-1]
""",
        desc="""
Given a string `s`, return its longest contiguous substring that reads the same forwards and backwards. If there's a tie, any of the longest is accepted.

**Constraints**
- `1 <= len(s) <= 1000`
- Digits and English letters.
""",
        hints=["Every palindrome has a centre: either one character or the gap between two.", "Expand outward from each of the 2n − 1 centres."],
        solution="""
def longest_palindrome(s: str) -> str:
    start, end = 0, 0
    for center in range(len(s)):
        for lo, hi in ((center, center), (center, center + 1)):
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            if hi - lo - 1 > end - start:
                start, end = lo + 1, hi
    return s[start:end]
""",
        explanation="""
Expand around centres. For each index, try an odd-length centre `(i, i)` and an even-length centre `(i, i+1)`, and widen while the ends match. Keep the longest span.

- **Time:** O(n²)
- **Space:** O(1)

(Manacher's algorithm does it in O(n), but that's rarely expected.)
""",
        examples=[(["babad"], "bab"), (["cbbd"], "bb")],
        tests=[["a"], ["ac"], ["racecar"], ["forgeeksskeegfor"], ["aaaa"], ["abacdfgdcaba"]],
    ),
    dict(
        slug="palindromic-substrings",
        title="Palindromic Substrings",
        difficulty="Medium",
        sig="def count_substrings(s: str) -> int:",
        desc="""
Return how many substrings of `s` are palindromes. Substrings at different positions count separately, even if they contain the same characters.

**Constraints**
- `1 <= len(s) <= 1000`, lowercase letters
""",
        hints=["Use the same idea as in Longest Palindromic Substring: expand from every centre, counting each successful expansion."],
        solution="""
def count_substrings(s: str) -> int:
    count = 0
    for center in range(len(s)):
        for lo, hi in ((center, center), (center, center + 1)):
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                count += 1
                lo -= 1
                hi += 1
    return count
""",
        explanation="""
Each step of a successful expansion from a centre is one more palindromic substring. Sum the steps over all 2n − 1 centres.

- **Time:** O(n²)
- **Space:** O(1)
""",
        examples=[(["abc"], 3), (["aaa"], 6)],
        tests=[["a"], ["abba"], ["aabaa"], ["abcdcbe"]],
    ),
    dict(
        slug="decode-ways",
        title="Decode Ways",
        difficulty="Medium",
        sig="def num_decodings(s: str) -> int:",
        desc="""
Letters are encoded as numbers: `A → "1"`, `B → "2"`, …, `Z → "26"`. Given a string of digits `s`, return how many ways it can be decoded back into letters.

Groupings with leading zeros are invalid: `"06"` cannot become `F`. The answer fits in a 32-bit integer.

**Constraints**
- `1 <= len(s) <= 100`
""",
        hints=["ways(i) equals ways(i-1) if s[i-1] is between 1 and 9, plus ways(i-2) if s[i-2:i] is between 10 and 26."],
        solution="""
def num_decodings(s: str) -> int:
    prev2, prev1 = 1, 1 if s[0] != "0" else 0
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":
            cur += prev1
        if 10 <= int(s[i - 2 : i]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
""",
        explanation="""
Let `dp[i]` be the number of ways to decode the first `i` digits. The last letter used either one digit (valid if it's not `0`) or two digits (valid if they form 10–26). Rolling variables keep the space constant.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[(["12"], 2), (["226"], 3), (["06"], 0)],
        tests=[["0"], ["10"], ["11106"], ["2101"], ["27"], ["1111111111"], ["100"]],
    ),
    dict(
        slug="coin-change",
        title="Coin Change",
        difficulty="Medium",
        sig="def coin_change(coins: List[int], amount: int) -> int:",
        desc="""
Given coin denominations `coins` (with unlimited coins of each) and a target `amount`, return the **fewest coins** that add up to `amount`, or `-1` if it can't be made.

**Constraints**
- `1 <= len(coins) <= 12`, `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`
""",
        hints=["A greedy approach (always taking the largest coin) fails: with coins [1, 3, 4] and amount 6, it uses three coins (4 + 1 + 1) instead of two (3 + 3).", "Use the recurrence dp[a] = 1 + min(dp[a - c]) over all coins c <= a."],
        solution="""
def coin_change(coins: List[int], amount: int) -> int:
    dp = [0] + [amount + 1] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] <= amount else -1
""",
        explanation="""
Use bottom-up DP over the amounts. `dp[a]` is the fewest coins needed to make `a`; it builds on `dp[a - c]` for every coin. The `amount + 1` initial value means "impossible".

- **Time:** O(amount · len(coins))
- **Space:** O(amount)
""",
        examples=[([[1, 2, 5], 11], 3), ([[2], 3], -1), ([[1], 0], 0)],
        tests=[[[186, 419, 83, 408], 6249], [[2, 5, 10, 1], 27], [[3, 7], 5], [[1, 3, 4], 6]],
    ),
    dict(
        slug="maximum-product-subarray",
        title="Maximum Product Subarray",
        difficulty="Medium",
        sig="def max_product(nums: List[int]) -> int:",
        desc="""
Given an integer list `nums`, return the largest product of any non-empty **contiguous** subarray.

**Constraints**
- `1 <= len(nums) <= 2 * 10^4`
- `-10 <= nums[i] <= 10`
""",
        hints=["A negative number turns the smallest product into the largest one.", "Track both the max and the min product of subarrays ending at each index."],
        solution="""
def max_product(nums: List[int]) -> int:
    best = hi = lo = nums[0]
    for x in nums[1:]:
        candidates = (x, hi * x, lo * x)
        hi, lo = max(candidates), min(candidates)
        best = max(best, hi)
    return best
""",
        explanation="""
Like Kadane's algorithm, but keep both the largest and smallest product of a subarray ending here, since multiplying by a negative swaps them. Zeros reset both through the `x` candidate.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[2, 3, -2, 4]], 6), ([[-2, 0, -1]], 0)],
        tests=[[[-2]], [[-2, 3, -4]], [[0, 2]], [[-1, -2, -3, 0]], [[2, -5, -2, -4, 3]]],
    ),
    dict(
        slug="word-break",
        title="Word Break",
        difficulty="Medium",
        sig="def word_break(s: str, word_dict: List[str]) -> bool:",
        desc="""
Return `True` if the string `s` can be split into a sequence of one or more words from `word_dict`. Words may be reused.

**Constraints**
- `1 <= len(s) <= 300`
- `1 <= len(word_dict) <= 1000`; all words unique
""",
        hints=["dp[i] is True if s[:i] can be segmented.", "Compute dp[i] = any(dp[i - len(w)] and s[i-len(w):i] == w for w in word_dict)."],
        solution="""
def word_break(s: str, word_dict: List[str]) -> bool:
    words = set(word_dict)
    lengths = {len(w) for w in words}
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(L <= i and dp[i - L] and s[i - L : i] in words for L in lengths)
    return dp[-1]
""",
        explanation="""
Use DP over prefixes: `dp[i]` is true if some word ends exactly at `i` and the prefix before that word is breakable. Checking only the word lengths that actually exist keeps it fast.

- **Time:** O(n · distinct word lengths · max word length)
- **Space:** O(n)
""",
        examples=[(["helloworld", ["hello", "world"]], True), (["applepenapple", ["apple", "pen"]], True), (["catsandog", ["cats", "dog", "sand", "and", "cat"]], False)],
        tests=[["a", ["b"]], ["aaaaaaa", ["aaaa", "aaa"]], ["cars", ["car", "ca", "rs"]], ["a" * 40 + "b", ["a", "aa", "aaa"]], ["goalspecial", ["go", "goal", "goals", "special"]]],
    ),
    dict(
        slug="longest-increasing-subsequence",
        title="Longest Increasing Subsequence",
        difficulty="Medium",
        sig="def length_of_lis(nums: List[int]) -> int:",
        desc="""
Return the length of the longest **strictly increasing subsequence** of `nums`. A subsequence keeps the original order but may skip elements.

**Constraints**
- `1 <= len(nums) <= 2500`

**Follow-up:** O(n log n)?
""",
        hints=["For an O(n²) solution, set dp[i] = 1 + max(dp[j]) over all j < i with nums[j] < nums[i].", "For an O(n log n) solution, keep a list `tails`, where tails[k] is the smallest possible tail of an increasing subsequence of length k + 1. Binary-search each number into it."],
        solution="""
def length_of_lis(nums: List[int]) -> int:
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
""",
        explanation="""
This is the patience-sorting technique. `tails[k]` holds the smallest tail value of any increasing subsequence of length `k + 1`, and the list stays sorted. For each number, binary-search the first tail that is `>= x` and replace it, or append if `x` is larger than every tail. The length of `tails` is the answer.

- **Time:** O(n log n)
- **Space:** O(n)
""",
        examples=[([[10, 9, 2, 5, 3, 7, 101, 18]], 4), ([[0, 1, 0, 3, 2, 3]], 4), ([[7, 7, 7, 7]], 1)],
        tests=[[[1]], [[4, 10, 4, 3, 8, 9]], [[3, 5, 6, 2, 5, 4, 19, 5, 6, 7, 12]], [list(range(1000, 0, -1))]],
    ),
]
