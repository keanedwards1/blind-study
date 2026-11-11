CATEGORY = "Advanced Graphs"

PROBLEMS = [
    dict(
        slug="alien-dictionary",
        title="Alien Dictionary",
        difficulty="Hard",
        sig="def alien_order(words: List[str]) -> str:",
        checker="""
def check(args, result, expected):
    words = args[0]
    if expected == "":
        return result == ""
    if not isinstance(result, str):
        return False
    letters = set("".join(words))
    if len(result) != len(letters) or set(result) != letters:
        return False
    pos = {c: i for i, c in enumerate(result)}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if pos[x] > pos[y]:
                    return False
                break
    return True
""",
        desc="""
An alien language uses lowercase English letters in an unknown order. You're given `words`, a list of words from its dictionary **already sorted** by the alien ordering.

Return a string containing every distinct letter that appears in `words`, arranged in an order consistent with the dictionary. If several orders work, return any of them. If no valid order exists, return `""`.

Ordering is lexicographic: the first position where two words differ decides which comes first. If one word is a prefix of the other, the shorter word comes first.

**Constraints**
- `1 <= len(words) <= 100`, `1 <= len(words[i]) <= 100`
""",
        hints=[
            "Compare each pair of adjacent words. The first differing letters give one edge: a comes before b.",
            "Watch for the invalid case where a longer word comes before its own prefix (e.g. 'abc' before 'ab').",
            "Topologically sort the letters; a cycle means there's no valid order.",
        ],
        solution="""
def alien_order(words: List[str]) -> str:
    graph = {c: set() for w in words for c in w}
    indegree = {c: 0 for c in graph}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in graph[x]:
                    graph[x].add(y)
                    indegree[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    queue = deque(sorted(c for c in indegree if indegree[c] == 0))
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in sorted(graph[c]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(graph) else ""
""",
        explanation="""
Build a graph over letters: for each adjacent pair of words, the first mismatch gives the edge `x → y`. If the pairs never differ and the first word is longer, the input is invalid. Then use Kahn's topological sort; if not every letter gets output, there's a cycle.

- **Time:** O(C), where C is the total number of characters across all words
- **Space:** O(U + edges), where U is the number of unique letters (≤ 26)
""",
        examples=[([["wrt", "wrf", "er", "ett", "rftt"]], "wertf"), ([["z", "x"]], "zx"), ([["z", "x", "z"]], "")],
        tests=[[["abc", "ab"]], [["z", "z"]], [["ab", "adc"]], [["ac", "ab", "zc", "zb"]], [["baa", "abcd", "abca", "cab", "cad"]]],
    ),
]
