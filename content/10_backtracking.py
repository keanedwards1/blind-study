CATEGORY = "Backtracking"

GRID = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]

PROBLEMS = [
    dict(
        slug="combination-sum",
        title="Combination Sum",
        difficulty="Medium",
        sig="def combination_sum(candidates: List[int], target: int) -> List[List[int]]:",
        compare="unordered_nested",
        desc="""
Given a list of **distinct** positive integers `candidates` and a `target`, return every unique combination of candidates that sums to `target`. Each candidate may be used **any number of times**.

Two combinations are the same if they use the same numbers the same number of times. Return combinations in any order.

**Constraints**
- `1 <= len(candidates) <= 30`, `2 <= candidates[i] <= 40`
- `1 <= target <= 40`
""",
        hints=["Backtrack with a start index: at each step, either reuse the current candidate or move on to the next one. This prevents permutations of the same combination."],
        solution="""
def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    result, path = [], []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] <= remaining:
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i])
                path.pop()

    backtrack(0, target)
    return result
""",
        explanation="""
Run a DFS over the choices, passing index `i` (not `i + 1`) so that a candidate can repeat, but never going back to earlier candidates. This produces each multiset exactly once. Prune when the candidate exceeds the remaining sum.

- **Time:** exponential, roughly O(n^(T/m)) where m is the smallest candidate
- **Space:** O(T/m) recursion depth
""",
        examples=[([[2, 3, 6, 7], 7], [[2, 2, 3], [7]]), ([[2, 3, 5], 8], [[2, 2, 2, 2], [2, 3, 3], [3, 5]]), ([[2], 1], [])],
        tests=[[[3, 4, 5], 12], [[7, 3, 2], 18], [[8, 7, 4, 3], 11], [[2, 5], 3]],
    ),
    dict(
        slug="word-search",
        title="Word Search",
        difficulty="Medium",
        sig="def exist(board: List[List[str]], word: str) -> bool:",
        desc="""
Given an `m x n` grid of characters `board` and a string `word`, return `True` if `word` can be traced through **horizontally or vertically adjacent** cells without reusing any cell.

**Constraints**
- `1 <= m, n <= 6`
- `1 <= len(word) <= 15`
- Upper- and lowercase English letters.
""",
        hints=["Try every cell as a starting point, and run a DFS from it.", "Mark a cell as used while it's on the current path, and restore it when you backtrack."],
        solution="""
def exist(board: List[List[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], "#"
        found = dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
        board[r][c] = saved
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
""",
        explanation="""
Backtrack from every cell. Temporarily overwrite the current cell with `#` so the path can't reuse it, then restore it. Return as soon as all characters are matched.

- **Time:** O(m · n · 4^L)
- **Space:** O(L) recursion depth
""",
        examples=[([GRID, "ABCCED"], True), ([GRID, "SEE"], True), ([GRID, "ABCB"], False)],
        tests=[[[["a"]], "a"], [[["a", "b"], ["c", "d"]], "abdc"], [[["a", "a"]], "aaa"], [[["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]], "AAB"], [GRID, "ESCFDA"]],
    ),
]
