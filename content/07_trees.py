CATEGORY = "Trees"

TREE_NOTE = "\n\n_Trees are shown in level order (`None` marks a missing child); your function receives `TreeNode` objects._"

EX_TREE = [3, 9, 20, None, None, 15, 7]
BST = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]

PROBLEMS = [
    dict(
        slug="invert-binary-tree",
        title="Invert Binary Tree",
        difficulty="Easy",
        sig="def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        **{"in": ["tree"]},
        out="tree",
        desc="""
Given the `root` of a binary tree, mirror it: swap the left and right child of every node. Return the root.

**Constraints**
- `0 <=` number of nodes `<= 100`
""" + TREE_NOTE,
        hints=["Swap the children at the root, then invert each subtree recursively."],
        solution="""
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
""",
        explanation="""
Use recursion: an inverted tree has the inverted right subtree on the left and the inverted left subtree on the right. BFS with a queue works too.

- **Time:** O(n)
- **Space:** O(h) recursion depth
""",
        examples=[([[4, 2, 7, 1, 3, 6, 9]], [4, 7, 2, 9, 6, 3, 1]), ([[2, 1, 3]], [2, 3, 1]), ([[]], [])],
        tests=[[[1]], [[1, 2]], [[1, None, 2, 3]], [[5, 3, 8, 1, 4, 7, 9, 0]]],
    ),
    dict(
        slug="maximum-depth-of-binary-tree",
        title="Maximum Depth of Binary Tree",
        difficulty="Easy",
        sig="def max_depth(root: Optional[TreeNode]) -> int:",
        **{"in": ["tree"]},
        desc="""
Return the maximum depth of a binary tree, which is the number of nodes on the longest path from the root down to a leaf. An empty tree has depth 0.

**Constraints**
- `0 <=` number of nodes `<= 10^4`
""" + TREE_NOTE,
        hints=["Use the recurrence depth(node) = 1 + max(depth(left), depth(right))."],
        solution="""
def max_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""",
        explanation="""
Use post-order recursion: a node's depth is one more than its deeper child's depth. Level-order BFS that counts levels is the iterative alternative.

- **Time:** O(n)
- **Space:** O(h)
""",
        examples=[([EX_TREE], 3), ([[1, None, 2]], 2)],
        tests=[[[]], [[1]], [[1, 2, None, 3, None, 4]], [[1, 2, 3, 4, 5, 6, 7]]],
    ),
    dict(
        slug="same-tree",
        title="Same Tree",
        difficulty="Easy",
        sig="def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:",
        **{"in": ["tree", "tree"]},
        desc="""
Given the roots of two binary trees `p` and `q`, return `True` if they have the same shape and the same value at every node.

**Constraints**
- Each tree has `0..100` nodes.
""" + TREE_NOTE,
        hints=["Two trees are equal if their roots match and both pairs of subtrees are equal."],
        solution="""
def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    if not p or not q:
        return p is q
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
""",
        explanation="""
Compare the trees recursively. If both nodes are empty, they are equal; if exactly one is empty, they are not; otherwise, the values and both pairs of subtrees must match.

- **Time:** O(n)
- **Space:** O(h)
""",
        examples=[([[1, 2, 3], [1, 2, 3]], True), ([[1, 2], [1, None, 2]], False), ([[1, 2, 1], [1, 1, 2]], False)],
        tests=[[[], []], [[1], []], [[5, 4, 6], [5, 4, 6]], [[1, 2, 3, 4], [1, 2, 3, None, 4]]],
    ),
    dict(
        slug="subtree-of-another-tree",
        title="Subtree of Another Tree",
        difficulty="Easy",
        sig="def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:",
        **{"in": ["tree", "tree"]},
        desc="""
Given the roots of two binary trees `root` and `sub_root`, return `True` if some node of `root` is the top of a subtree that is **identical** to `sub_root`. That means the node and **all** of its descendants match.

**Constraints**
- `root` has `1..2000` nodes; `sub_root` has `1..1000` nodes.
""" + TREE_NOTE,
        hints=["Reuse a same-tree check: try it at every node of `root`."],
        solution="""
def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    def same(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

    if not sub_root:
        return True
    if not root:
        return False
    return same(root, sub_root) or is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
""",
        explanation="""
For every node in `root`, check whether the subtree starting there equals `sub_root`. Note the trap: a matching *top* isn't enough; the descendants must match exactly too.

- **Time:** O(n · m) worst case (serialising both trees and doing a substring search gets O(n + m))
- **Space:** O(h)
""",
        examples=[([[3, 4, 5, 1, 2], [4, 1, 2]], True), ([[3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]], False)],
        tests=[[[1, 1], [1]], [[1], [2]], [[12], [2]], [[3, 4, 5, 1, None, 2], [3, 1, 2]], [[1, 2, 3], [3]]],
    ),
    dict(
        slug="lowest-common-ancestor-of-a-binary-search-tree",
        title="Lowest Common Ancestor of a BST",
        difficulty="Medium",
        sig="def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:",
        params=["root", "p", "q"],
        uses=["tree"],
        driver="""
def driver(ns, values, p, q):
    root = build_tree(values)
    def find(node, v):
        while node and node.val != v:
            node = node.left if v < node.val else node.right
        return node
    res = resolve(ns, "lowest_common_ancestor")(root, find(root, p), find(root, q))
    if res is not None and not isinstance(res, TreeNode):
        raise TypeError("return the TreeNode itself, not its value")
    return res.val if res else None
""",
        desc="""
Given a **binary search tree** and two of its nodes `p` and `q`, return their lowest common ancestor: the deepest node that has both `p` and `q` as descendants. A node counts as a descendant of itself.

In the examples, `p` and `q` are shown by value and the output shows the value of the returned node. Your function receives and returns `TreeNode` objects.

**Constraints**
- `2 <=` number of nodes `<= 10^5`; all values unique; `p != q`, both exist in the tree.
""",
        hints=["Use the BST ordering: if both values are smaller than the current node go left; if both are larger go right; otherwise you've found the split point."],
        solution="""
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
""",
        explanation="""
Starting at the root, move toward the side that contains both nodes. The first node where `p` and `q` split (or that equals one of them) is the LCA.

- **Time:** O(h)
- **Space:** O(1)
""",
        examples=[([BST, 2, 8], 6), ([BST, 2, 4], 2), ([[2, 1], 2, 1], 2)],
        tests=[[BST, 3, 5], [BST, 7, 9], [BST, 0, 5], [BST, 3, 9]],
    ),
    dict(
        slug="binary-tree-level-order-traversal",
        title="Binary Tree Level Order Traversal",
        difficulty="Medium",
        sig="def level_order(root: Optional[TreeNode]) -> List[List[int]]:",
        **{"in": ["tree"]},
        desc="""
Return the node values of a binary tree level by level, from top to bottom and left to right within each level, as a list of lists.

**Constraints**
- `0 <=` number of nodes `<= 2000`
""" + TREE_NOTE,
        hints=["Use BFS with a queue, and process exactly `len(queue)` nodes per level."],
        solution="""
def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
""",
        explanation="""
Use a breadth-first search. At the start of each round the queue holds exactly one level; pop that many nodes, record their values, and enqueue their children.

- **Time:** O(n)
- **Space:** O(n)
""",
        examples=[([EX_TREE], [[3], [9, 20], [15, 7]]), ([[1]], [[1]]), ([[]], [])],
        tests=[[[1, 2, 3, 4, 5, 6, 7]], [[1, 2, None, 3, None, 4]], [[1, None, 2, None, 3]]],
    ),
    dict(
        slug="validate-binary-search-tree",
        title="Validate Binary Search Tree",
        difficulty="Medium",
        sig="def is_valid_bst(root: Optional[TreeNode]) -> bool:",
        **{"in": ["tree"]},
        desc="""
Return `True` if the binary tree is a valid **binary search tree**:

- every value in a node's left subtree is **strictly less** than the node's value,
- every value in its right subtree is **strictly greater**, and
- both subtrees are themselves BSTs.

**Constraints**
- `1 <=` number of nodes `<= 10^4`
""" + TREE_NOTE,
        hints=["Checking only a node against its direct children is not enough.", "Pass down the allowed (low, high) range for each subtree."],
        solution="""
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    def valid(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, float("-inf"), float("inf"))
""",
        explanation="""
Each node must lie in an open interval inherited from its ancestors. Going left tightens the upper bound to the parent's value; going right tightens the lower bound. (An in-order traversal must be strictly increasing, which is an equivalent check.)

- **Time:** O(n)
- **Space:** O(h)
""",
        examples=[([[2, 1, 3]], True), ([[5, 1, 4, None, None, 3, 6]], False)],
        tests=[[[1]], [[2, 2, 2]], [[5, 4, 6, None, None, 3, 7]], [[10, 5, 15, None, None, 6, 20]], [[3, 1, 5, 0, 2, 4, 6]], [[-2147483648, None, 2147483647]]],
    ),
    dict(
        slug="kth-smallest-element-in-a-bst",
        title="Kth Smallest Element in a BST",
        difficulty="Medium",
        sig="def kth_smallest(root: Optional[TreeNode], k: int) -> int:",
        **{"in": ["tree", None]},
        desc="""
Given the `root` of a binary search tree and an integer `k`, return the `k`-th smallest value in the tree (1-indexed).

**Constraints**
- `1 <= k <=` number of nodes `<= 10^4`
""" + TREE_NOTE,
        hints=["An in-order traversal of a BST visits values in sorted order. Stop after k visits."],
        solution="""
def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
""",
        explanation="""
Iterative in-order traversal with an explicit stack visits nodes in ascending order; return the k-th one visited. This stops early instead of building the full sorted list.

- **Time:** O(h + k)
- **Space:** O(h)
""",
        examples=[([[3, 1, 4, None, 2], 1], 1), ([[5, 3, 6, 2, 4, None, None, 1], 3], 3)],
        tests=[[[1], 1], [[2, 1, 3], 3], [[5, 3, 6, 2, 4, None, None, 1], 6], [[4, 2, 6, 1, 3, 5, 7], 4]],
    ),
    dict(
        slug="construct-binary-tree-from-preorder-and-inorder-traversal",
        title="Construct Binary Tree from Preorder and Inorder Traversal",
        difficulty="Medium",
        sig="def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:",
        out="tree",
        uses=["tree"],
        desc="""
Given the `preorder` and `inorder` traversals of a binary tree with **unique** values, rebuild the tree and return its root.

**Constraints**
- `1 <= len(preorder) == len(inorder) <= 3000`
""" + TREE_NOTE,
        hints=["`preorder[0]` is the root of the tree.", "Find the root in `inorder`: everything to its left belongs to the left subtree, and everything to its right belongs to the right subtree.", "Store inorder positions in a dict to avoid repeated `.index()` calls."],
        solution="""
def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    pos = {v: i for i, v in enumerate(inorder)}
    it = iter(preorder)

    def build(lo, hi):
        if lo > hi:
            return None
        val = next(it)
        node = TreeNode(val)
        mid = pos[val]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)
""",
        explanation="""
Consume `preorder` left to right: each value is the root of the current inorder range. Its inorder index splits the range into left and right subtrees. Build the left subtree first, because preorder lists it first.

- **Time:** O(n) with the index map
- **Space:** O(n)
""",
        examples=[([[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]], EX_TREE), ([[-1], [-1]], [-1])],
        tests=[[[1, 2], [2, 1]], [[1, 2], [1, 2]], [[1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7]], [[3, 1, 2, 4], [1, 2, 3, 4]]],
    ),
    dict(
        slug="binary-tree-maximum-path-sum",
        title="Binary Tree Maximum Path Sum",
        difficulty="Hard",
        sig="def max_path_sum(root: Optional[TreeNode]) -> int:",
        **{"in": ["tree"]},
        desc="""
A **path** is a sequence of nodes where each consecutive pair is joined by an edge, and no node appears more than once. It doesn't have to pass through the root. A path's sum is the total of its node values.

Return the maximum sum of any non-empty path.

**Constraints**
- `1 <=` number of nodes `<= 3 * 10^4`
- `-1000 <= Node.val <= 1000`
""" + TREE_NOTE,
        hints=["For each node, compute the best *downward* path starting at it (it can extend into only one child).", "The best path that *peaks* at a node is node.val + best_down(left) + best_down(right), ignoring negative branches."],
        solution="""
def max_path_sum(root: Optional[TreeNode]) -> int:
    best = float("-inf")

    def down(node):
        nonlocal best
        if not node:
            return 0
        left = max(down(node.left), 0)
        right = max(down(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    down(root)
    return best
""",
        explanation="""
DFS returns the best sum of a path going *down* from each node (it can use only one child). At each node, also consider the path that bends through it: `val + left + right`, with negative branches clamped to 0. The global max over all nodes is the answer.

- **Time:** O(n)
- **Space:** O(h)
""",
        examples=[([[1, 2, 3]], 6), ([[-10, 9, 20, None, None, 15, 7]], 42)],
        tests=[[[-3]], [[2, -1]], [[1, -2, 3]], [[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]], [[-1, -2, -3]]],
    ),
    dict(
        slug="serialize-and-deserialize-binary-tree",
        title="Serialize and Deserialize Binary Tree",
        difficulty="Hard",
        params=["root"],
        uses=["tree"],
        starter="""class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        pass

    def deserialize(self, data: str) -> Optional[TreeNode]:
        pass
""",
        driver="""
def driver(ns, values):
    Codec = resolve_class(ns, "Codec")
    data = Codec().serialize(build_tree(values))
    if not isinstance(data, str):
        raise TypeError(f"serialize must return a str, got {type(data).__name__}")
    return tree_to_arr(Codec().deserialize(data))
""",
        desc="""
Design a `Codec` class with:

- `serialize(root)`, which turns a binary tree into a string, and
- `deserialize(data)`, which rebuilds the identical tree from that string.

You choose the string format. The tests serialize with one `Codec` instance and deserialize with a **fresh** one, then check that the rebuilt tree matches the original.

**Constraints**
- `0 <=` number of nodes `<= 10^4`
- `-1000 <= Node.val <= 1000`
""" + TREE_NOTE,
        hints=["A preorder DFS that writes a marker such as `N` for each missing child captures the shape completely.", "To deserialize, split on commas and consume tokens recursively in the same preorder."],
        solution="""
class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        out = []

        def dfs(node):
            if not node:
                out.append("N")
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = iter(data.split(","))

        def build():
            tok = next(tokens)
            if tok == "N":
                return None
            node = TreeNode(int(tok))
            node.left = build()
            node.right = build()
            return node

        return build()
""",
        explanation="""
Preorder with null markers is unambiguous: every node is followed by its full left subtree and then its full right subtree. Deserialize by reading tokens in the same order.

- **Time:** O(n) for both
- **Space:** O(n)
""",
        examples=[([[1, 2, 3, None, None, 4, 5]], [1, 2, 3, None, None, 4, 5]), ([[]], [])],
        tests=[[[1]], [[1, None, 2, None, 3]], [[-1, 0, 1]], [[5, 4, 7, 3, None, 2, None, -1, None, 9]], [[1000, -1000]]],
    ),
]
