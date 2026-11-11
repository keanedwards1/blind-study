CATEGORY = "Tries"

CLASS_NOTE = "\n\n_Tests call the methods in the order listed in `operations`, with the matching entry in `arguments`. The first operation is the constructor. The output lists each call's return value (`None` for constructors and methods that return nothing)._"

BOARD = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]

PROBLEMS = [
    dict(
        slug="implement-trie-prefix-tree",
        title="Implement Trie (Prefix Tree)",
        difficulty="Medium",
        kind="class",
        cls="Trie",
        starter="""class Trie:
    def __init__(self):
        pass

    def insert(self, word: str) -> None:
        pass

    def search(self, word: str) -> bool:
        pass

    def starts_with(self, prefix: str) -> bool:
        pass
""",
        desc="""
Implement a `Trie` class:

- `Trie()` creates an empty trie.
- `insert(word)` adds `word`.
- `search(word)` returns `True` if `word` was inserted.
- `starts_with(prefix)` returns `True` if any inserted word begins with `prefix`.

**Constraints**
- `1 <= len(word), len(prefix) <= 2000`, lowercase letters
- At most `3 * 10^4` calls in total.
""" + CLASS_NOTE,
        hints=["Each node holds a dict of children and an `end` flag.", "`search` and `starts_with` walk the trie the same way; only `search` also requires the end-of-word flag at the last node."],
        solution="""
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True

    def _walk(self, s):
        node = self.root
        for c in s:
            if c not in node:
                return None
            node = node[c]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
""",
        explanation="""
Nested dicts form the tree: each key is a letter leading to a child node, and a `$` key marks the end of a word. `insert`, `search` and `starts_with` each walk at most one node per character.

- **Time:** O(L) per call
- **Space:** O(total inserted characters)
""",
        examples=[(
            [["Trie", "insert", "search", "search", "starts_with", "insert", "search"], [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]],
            [None, None, True, False, True, None, True],
        )],
        tests=[
            [["Trie", "search", "starts_with", "insert", "search", "starts_with", "starts_with"], [[], ["a"], ["a"], ["a"], ["a"], ["a"], ["ab"]]],
            [["Trie", "insert", "insert", "search", "search", "starts_with", "search"], [[], ["car"], ["card"], ["car"], ["ca"], ["card"], ["cards"]]],
        ],
    ),
    dict(
        slug="design-add-and-search-words-data-structure",
        title="Design Add and Search Words Data Structure",
        difficulty="Medium",
        kind="class",
        cls="WordDictionary",
        starter="""class WordDictionary:
    def __init__(self):
        pass

    def add_word(self, word: str) -> None:
        pass

    def search(self, word: str) -> bool:
        pass
""",
        desc="""
Design a `WordDictionary` class:

- `WordDictionary()` creates an empty dictionary.
- `add_word(word)` stores `word`.
- `search(word)` returns `True` if a stored word matches `word`. In a search pattern, `.` matches **any single letter**.

**Constraints**
- `1 <= len(word) <= 25`
- Search patterns contain at most 2 dots.
- At most `10^4` calls.
""" + CLASS_NOTE,
        hints=["Store words in a trie.", "When you see a `.`, try every child (DFS); when you see a letter, follow only that child."],
        solution="""
class WordDictionary:
    def __init__(self):
        self.root = {}

    def add_word(self, word: str) -> None:
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            c = word[i]
            if c == ".":
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return c in node and dfs(node[c], i + 1)

        return dfs(self.root, 0)
""",
        explanation="""
Store the words in a trie, and use a DFS to handle wildcards. Regular letters follow a single edge; a `.` branches into every child at that depth.

- **Time:** add O(L); search O(L) without dots, up to O(26^d · L) with d dots
- **Space:** O(total characters)
""",
        examples=[(
            [["WordDictionary", "add_word", "add_word", "add_word", "search", "search", "search", "search"], [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]]],
            [None, None, None, None, False, True, True, True],
        )],
        tests=[
            [["WordDictionary", "add_word", "search", "search", "search", "search"], [[], ["a"], ["."], ["a"], [".."], ["aa"]]],
            [["WordDictionary", "add_word", "add_word", "search", "search", "search"], [[], ["at"], ["and"], ["a.d"], ["a."], [".t"]]],
        ],
    ),
    dict(
        slug="word-search-ii",
        title="Word Search II",
        difficulty="Hard",
        sig="def find_words(board: List[List[str]], words: List[str]) -> List[str]:",
        compare="unordered",
        desc="""
Given an `m x n` grid of letters `board` and a list of distinct `words`, return every word that can be traced on the board.

A word is traced by moving between **horizontally or vertically adjacent** cells, and a single cell can't be used twice within the same word. Return the words in any order.

**Constraints**
- `1 <= m, n <= 12`
- `1 <= len(words) <= 3 * 10^4`, `1 <= len(words[i]) <= 10`
""",
        hints=["Searching for each word separately is too slow. Build a trie of all the words.", "Run a DFS from each cell while walking the trie alongside it, and stop as soon as the current prefix is not in the trie."],
        solution="""
def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    root = {}
    for w in words:
        node = root
        for c in w:
            node = node.setdefault(c, {})
        node["$"] = w

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent[ch]
        if "$" in node:
            found.append(node.pop("$"))
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch
        if not node:
            parent.pop(ch)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root:
                dfs(r, c, root)
    return found
""",
        explanation="""
Put all the words in a trie, then backtrack from every cell while walking the trie. When a node holds a complete word, record it and remove the marker so the word isn't reported twice. Pruning empty trie nodes on the way back keeps later searches fast.

- **Time:** O(m · n · 4 · 3^(L−1)) worst case
- **Space:** O(total characters in words)
""",
        examples=[([BOARD, ["oath", "pea", "eat", "rain"]], ["eat", "oath"]), ([[["a", "b"], ["c", "d"]], ["abcb"]], [])],
        tests=[[[["a"]], ["a"]], [[["a", "a"]], ["aaa"]], [[["o", "a", "b", "n"], ["o", "t", "a", "e"], ["a", "h", "k", "r"], ["a", "f", "l", "v"]], ["oa", "oaa"]], [BOARD, ["oath", "oat", "eta", "hike", "taa", "naan"]]],
    ),
]
