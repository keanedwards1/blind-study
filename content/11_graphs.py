CATEGORY = "Graphs"

ISLANDS_1 = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
ISLANDS_3 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
HEIGHTS = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]

PROBLEMS = [
    dict(
        slug="number-of-islands",
        title="Number of Islands",
        difficulty="Medium",
        sig="def num_islands(grid: List[List[str]]) -> int:",
        desc="""
`grid` is an `m x n` map where `"1"` is land and `"0"` is water. An island is a group of land cells connected **horizontally or vertically**. Return the number of islands.

**Constraints**
- `1 <= m, n <= 300`
""",
        hints=["Scan every cell. Each time you find unvisited land, count an island and flood-fill (DFS/BFS) all land connected to it."],
        solution="""
def num_islands(grid: List[List[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                stack = [(r, c)]
                grid[r][c] = "0"
                while stack:
                    i, j = stack.pop()
                    for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == "1":
                            grid[ni][nj] = "0"
                            stack.append((ni, nj))
    return count
""",
        explanation="""
Each time you hit unvisited land, count one island and flood-fill it, sinking land cells to `"0"` so they're never counted again. An explicit stack avoids recursion limits on big grids.

- **Time:** O(m · n)
- **Space:** O(m · n) worst case for the stack
""",
        examples=[([ISLANDS_1], 1), ([ISLANDS_3], 3)],
        tests=[[[["0"]]], [[["1"]]], [[["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]], [[["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]]],
    ),
    dict(
        slug="clone-graph",
        title="Clone Graph",
        difficulty="Medium",
        sig="def clone_graph(node: Optional['Node']) -> Optional['Node']:",
        uses=["graph"],
        params=["adj_list"],
        driver="""
def driver(ns, adj):
    node = build_graph(adj)
    originals = {id(n) for n in collect_graph(node)}
    result = resolve(ns, "clone_graph")(node)
    if any(id(n) in originals for n in collect_graph(result)):
        raise AssertionError("the returned graph reuses original nodes; it must be a deep copy")
    return graph_to_adj(result)
""",
        desc="""
You are given a reference to one node of a connected, undirected graph. Return a **deep copy** of the whole graph. Every node in the copy must be a new `Node` object with the same `val` and the same connections.

Each `Node` has a `val` (int) and `neighbors` (list of `Node`). Node values run from `1` to `n`, and the node you receive is always the one with `val == 1`.

In the examples the graph is shown as an adjacency list: `adj_list[i]` lists the neighbours of node `i + 1`.

**Constraints**
- `0 <= n <= 100`; no repeated edges or self-loops.
""",
        hints=["Keep a dict from original node to its copy. It doubles as the visited set.", "In a DFS, create the copy, record it, and then clone each neighbour (or reuse its existing copy)."],
        solution="""
def clone_graph(node: Optional['Node']) -> Optional['Node']:
    copies = {}

    def clone(n):
        if n in copies:
            return copies[n]
        copy = Node(n.val)
        copies[n] = copy
        copy.neighbors = [clone(nb) for nb in n.neighbors]
        return copy

    return clone(node) if node else None
""",
        explanation="""
A map from original to clone serves as both the memo and the visited set. Register the copy **before** recursing into neighbours; otherwise cycles cause infinite recursion.

- **Time:** O(V + E)
- **Space:** O(V)
""",
        examples=[([[[2, 4], [1, 3], [2, 4], [1, 3]]], [[2, 4], [1, 3], [2, 4], [1, 3]]), ([[[]]], [[]]), ([[]], [])],
        tests=[[[[2], [1]]], [[[2, 3], [1, 3], [1, 2]]], [[[2, 3, 4], [1], [1], [1]]]],
    ),
    dict(
        slug="pacific-atlantic-water-flow",
        title="Pacific Atlantic Water Flow",
        difficulty="Medium",
        sig="def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:",
        compare="unordered",
        desc="""
An `m x n` island has the **Pacific** ocean along its top and left edges and the **Atlantic** along its bottom and right edges. `heights[r][c]` is the height of each cell.

Rain flows from a cell to a neighbouring cell (up, down, left or right) whose height is **less than or equal to** its own. Edge cells flow directly into the ocean they touch.

Return the coordinates `[r, c]` of every cell from which water can reach **both** oceans, in any order.

**Constraints**
- `1 <= m, n <= 200`
- `0 <= heights[r][c] <= 10^5`
""",
        hints=["Work backwards: start from each ocean's border and climb *uphill* (to neighbours that are >= the current cell).", "The answer is the intersection of the two reachable sets."],
        solution="""
def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    rows, cols = len(heights), len(heights[0])

    def reach(starts):
        seen = set(starts)
        stack = list(starts)
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return seen

    pacific = reach([(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)])
    atlantic = reach([(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)])
    return [[r, c] for r, c in sorted(pacific & atlantic)]
""",
        explanation="""
Reverse the flow. Run a DFS from all Pacific border cells that only climbs to equal-or-higher neighbours; the cells it reaches are exactly those that can drain to the Pacific. Do the same for the Atlantic and intersect.

- **Time:** O(m · n)
- **Space:** O(m · n)
""",
        examples=[([HEIGHTS], [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]), ([[[1]]], [[0, 0]])],
        tests=[[[[1, 2], [4, 3]]], [[[2, 1], [1, 2]]], [[[3, 3, 3], [3, 1, 3], [0, 2, 4]]], [[[1, 1], [1, 1], [1, 1]]]],
    ),
    dict(
        slug="course-schedule",
        title="Course Schedule",
        difficulty="Medium",
        sig="def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:",
        desc="""
There are `num_courses` courses labelled `0` to `num_courses - 1`. Each pair `[a, b]` in `prerequisites` means you must take course `b` before course `a`.

Return `True` if it's possible to finish every course.

**Constraints**
- `1 <= num_courses <= 2000`
- `0 <= len(prerequisites) <= 5000`; all pairs are distinct.
""",
        hints=["This is cycle detection in a directed graph.", "Use Kahn's algorithm: repeatedly take courses with zero remaining prerequisites. If you can take all of them, there's no cycle."],
        solution="""
def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses
""",
        explanation="""
Use a topological sort (Kahn's algorithm). Start with courses that have no prerequisites; taking one lowers the in-degree of the courses that depend on it. If a cycle exists, some courses never reach in-degree 0.

- **Time:** O(V + E)
- **Space:** O(V + E)

DFS with three colours (unvisited / visiting / done) is the other standard approach.
""",
        examples=[([2, [[1, 0]]], True), ([2, [[1, 0], [0, 1]]], False)],
        tests=[[1, []], [3, [[0, 1], [1, 2], [2, 0]]], [4, [[1, 0], [2, 1], [3, 2]]], [5, [[1, 4], [2, 4], [3, 1], [3, 2]]], [3, [[1, 1]]]],
    ),
    dict(
        slug="graph-valid-tree",
        title="Graph Valid Tree",
        difficulty="Medium",
        sig="def valid_tree(n: int, edges: List[List[int]]) -> bool:",
        desc="""
You have `n` nodes labelled `0` to `n - 1` and a list of undirected `edges`. Return `True` if these edges form a valid **tree**: the graph is connected and contains no cycles.

**Constraints**
- `1 <= n <= 2000`
- No duplicate edges or self-loops.
""",
        hints=["A tree with n nodes has exactly n - 1 edges.", "With exactly n - 1 edges, the graph is a tree if and only if it is connected (equivalently, if it has no cycle). Union-find or DFS can check this."],
        solution="""
def valid_tree(n: int, edges: List[List[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True
""",
        explanation="""
Reject immediately unless there are exactly `n - 1` edges. Then run union-find: if any edge joins two nodes that are already connected, it forms a cycle. With `n - 1` edges and no cycle, the graph must be connected.

- **Time:** O(n · α(n))
- **Space:** O(n)
""",
        examples=[([5, [[0, 1], [0, 2], [0, 3], [1, 4]]], True), ([5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]], False)],
        tests=[[1, []], [2, []], [4, [[0, 1], [2, 3]]], [3, [[0, 1], [1, 2], [2, 0]]], [4, [[0, 1], [2, 3], [1, 2]]]],
    ),
    dict(
        slug="number-of-connected-components-in-an-undirected-graph",
        title="Number of Connected Components",
        difficulty="Medium",
        sig="def count_components(n: int, edges: List[List[int]]) -> int:",
        desc="""
You have `n` nodes labelled `0` to `n - 1` and a list of undirected `edges`. Return the number of connected components.

**Constraints**
- `1 <= n <= 2000`
- `0 <= len(edges) <= 5000`; no repeated edges.
""",
        hints=["Start with n components. Every edge that joins two different components reduces the count by one, and union-find makes this easy to track."],
        solution="""
def count_components(n: int, edges: List[List[int]]) -> int:
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            components -= 1
    return components
""",
        explanation="""
Use union-find with path compression. Each successful union merges two components. Counting DFS/BFS launches over unvisited nodes works just as well.

- **Time:** O(n + E · α(n))
- **Space:** O(n)
""",
        examples=[([5, [[0, 1], [1, 2], [3, 4]]], 2), ([5, [[0, 1], [1, 2], [2, 3], [3, 4]]], 1)],
        tests=[[1, []], [4, []], [6, [[0, 1], [2, 3], [4, 5], [1, 2]]], [3, [[0, 1], [1, 2], [0, 2]]]],
    ),
]
