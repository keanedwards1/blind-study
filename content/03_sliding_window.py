CATEGORY = "Sliding Window"

PROBLEMS = [
    dict(
        slug="best-time-to-buy-and-sell-stock",
        title="Best Time to Buy and Sell Stock",
        difficulty="Easy",
        sig="def max_profit(prices: List[int]) -> int:",
        desc="""
`prices[i]` is a stock's price on day `i`. You may buy once and sell once, on a **later** day. Return the largest profit possible, or `0` if no trade makes money.

**Constraints**
- `1 <= len(prices) <= 10^5`
- `0 <= prices[i] <= 10^4`
""",
        hints=["As you scan left to right, remember the cheapest price seen so far."],
        solution="""
def max_profit(prices: List[int]) -> int:
    cheapest = float("inf")
    best = 0
    for p in prices:
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
    return best
""",
        explanation="""
For each day, the best sale ending today buys at the minimum price before it. Track that running minimum and the best difference.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[7, 1, 5, 3, 6, 4]], 5), ([[7, 6, 4, 3, 1]], 0)],
        tests=[[[1]], [[2, 4, 1]], [[3, 2, 6, 5, 0, 3]], [[1, 2]], [[2, 1, 2, 1, 0, 1, 2]]],
    ),
    dict(
        slug="longest-substring-without-repeating-characters",
        title="Longest Substring Without Repeating Characters",
        difficulty="Medium",
        sig="def length_of_longest_substring(s: str) -> int:",
        desc="""
Given a string `s`, return the length of the longest contiguous substring that contains **no repeated characters**.

**Constraints**
- `0 <= len(s) <= 5 * 10^4`
- `s` may contain letters, digits, symbols and spaces.
""",
        hints=["Keep a window [left, right] with no duplicates.", "Store each character's most recent index; when you see a repeat inside the window, jump `left` past it."],
        solution="""
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last_seen and last_seen[c] >= left:
            left = last_seen[c] + 1
        last_seen[c] = right
        best = max(best, right - left + 1)
    return best
""",
        explanation="""
Use a sliding window: extend `right` one character at a time. If the character was last seen inside the current window, move `left` just past that position. The window always holds unique characters, so its maximum size is the answer.

- **Time:** O(n)
- **Space:** O(min(n, alphabet))
""",
        examples=[(["abcabcbb"], 3), (["bbbbb"], 1), (["pwwkew"], 3)],
        tests=[[""], [" "], ["dvdf"], ["abba"], ["tmmzuxt"], ["au"]],
    ),
    dict(
        slug="longest-repeating-character-replacement",
        title="Longest Repeating Character Replacement",
        difficulty="Medium",
        sig="def character_replacement(s: str, k: int) -> int:",
        desc="""
You are given an uppercase string `s` and an integer `k`. You may change at most `k` characters of `s` to any other uppercase letter.

Return the length of the longest substring that can be made of **one repeated letter** after those changes.

**Constraints**
- `1 <= len(s) <= 10^5`
- `0 <= k <= len(s)`
""",
        hints=["A window is valid if (window length − count of its most common letter) <= k.", "Grow the window to the right; shrink from the left when it becomes invalid."],
        solution="""
def character_replacement(s: str, k: int) -> int:
    count = {}
    left = top = best = 0
    for right, c in enumerate(s):
        count[c] = count.get(c, 0) + 1
        top = max(top, count[c])
        while (right - left + 1) - top > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
""",
        explanation="""
A window needs `len - maxFreq` replacements. Expand right; while that exceeds `k`, shrink from the left. `top` never needs to decrease: the answer only grows when a strictly larger frequency appears, so a stale `top` can't produce a wrong maximum.

- **Time:** O(n)
- **Space:** O(26)
""",
        examples=[(["ABAB", 2], 4), (["AABABBA", 1], 4)],
        tests=[["A", 0], ["AAAA", 0], ["ABCDE", 1], ["ABBB", 2], ["BAAAB", 2], ["ABAA", 0]],
    ),
    dict(
        slug="minimum-window-substring",
        title="Minimum Window Substring",
        difficulty="Hard",
        sig="def min_window(s: str, t: str) -> str:",
        desc="""
Given strings `s` and `t`, return the **shortest substring of `s`** that contains every character of `t`, counting duplicates (if `t` has two `a`s, the window needs at least two `a`s). If no such window exists, return `""`.

The answer is guaranteed to be unique.

**Constraints**
- `1 <= len(s), len(t) <= 10^5`
- Upper- and lowercase English letters.
""",
        hints=["Count what t needs. Expand right until the window satisfies every count.", "Then shrink from the left as much as possible while it still satisfies every count, recording the best window."],
        solution="""
def min_window(s: str, t: str) -> str:
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (float("inf"), 0, 0)
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2]]
""",
        explanation="""
`need` tracks how many of each character the window still lacks (negative means surplus), and `missing` counts how many required characters are still missing. Expand `right`; once `missing == 0` the window is valid, so shrink from the left while recording the smallest window, and stop when removing a char makes it invalid again.

- **Time:** O(|s| + |t|)
- **Space:** O(alphabet)
""",
        examples=[(["ADOBECODEBANC", "ABC"], "BANC"), (["a", "a"], "a"), (["a", "aa"], "")],
        tests=[["ab", "b"], ["aa", "aa"], ["bba", "ab"], ["cabwefgewcwaefgcf", "cae"], ["abc", "d"]],
    ),
]
