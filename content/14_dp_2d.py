CATEGORY = "2-D Dynamic Programming"

PROBLEMS = [
    dict(
        slug="unique-paths",
        title="Unique Paths",
        difficulty="Medium",
        sig="def unique_paths(m: int, n: int) -> int:",
        desc="""
A robot starts in the top-left cell of an `m x n` grid and wants to reach the bottom-right cell. It can only move **right** or **down**. How many distinct paths are there?

**Constraints**
- `1 <= m, n <= 100`
""",
        hints=["Use the recurrence paths(r, c) = paths(r-1, c) + paths(r, c-1).", "You only need one row of the table at a time."],
        solution="""
def unique_paths(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
""",
        explanation="""
Each cell is reached either from above or from the left, so its count is the sum of those two. Rolling a single row array works: before the update, `row[c]` holds the value from above.

- **Time:** O(m · n)
- **Space:** O(n)

Combinatorics gives it directly as `C(m + n − 2, m − 1)`.
""",
        examples=[([3, 7], 28), ([3, 2], 3)],
        tests=[[1, 1], [1, 10], [10, 10], [23, 12], [100, 1]],
    ),
    dict(
        slug="longest-common-subsequence",
        title="Longest Common Subsequence",
        difficulty="Medium",
        sig="def longest_common_subsequence(text1: str, text2: str) -> int:",
        desc="""
Return the length of the longest **subsequence** shared by `text1` and `text2`, or `0` if they share none. A subsequence keeps the original order but may skip characters.

**Constraints**
- `1 <= len(text1), len(text2) <= 1000`, lowercase letters
""",
        hints=["Let dp[i][j] be the length of the LCS of text1[i:] and text2[j:].", "If the characters match, dp[i][j] = 1 + dp[i+1][j+1]; otherwise, dp[i][j] = max(dp[i+1][j], dp[i][j+1])."],
        solution="""
def longest_common_subsequence(text1: str, text2: str) -> int:
    n = len(text2)
    prev = [0] * (n + 1)
    for a in text1:
        cur = [0] * (n + 1)
        for j, b in enumerate(text2):
            cur[j + 1] = prev[j] + 1 if a == b else max(prev[j + 1], cur[j])
        prev = cur
    return prev[n]
""",
        explanation="""
This is classic 2-D DP over prefixes. When the current characters match, extend the diagonal; otherwise take the better of dropping a character from either string. Two rows are enough.

- **Time:** O(n · m)
- **Space:** O(m)
""",
        examples=[(["abcde", "ace"], 3), (["abc", "abc"], 3), (["abc", "def"], 0)],
        tests=[["a", "a"], ["bsbininm", "jmjkbkjkv"], ["oxcpqrsvwf", "shmtulqrypy"], ["abcba", "abcbcba"], ["ezupkr", "ubmrapg"]],
    ),
]
