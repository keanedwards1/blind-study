# One guide per problem category: how to recognise it, a code template, and a quick quiz.
# Templates are compiled (not run) at build time.

PATTERNS = [
    dict(
        category="Arrays & Hashing",
        summary="This pattern trades memory for speed. You store what you have already seen in a dict or set, so each later lookup takes O(1) time instead of another scan through the input.",
        signals=["The problem asks you to find a pair, a duplicate, or a complement.", "The problem asks you to group items that share some property.", "You need to count how often values occur.", "Your brute-force solution uses a nested loop whose inner loop only *searches* for something."],
        template="""def solve(nums, target):
    seen = {}                      # value -> index (or count, or list)
    for i, x in enumerate(nums):
        if target - x in seen:     # look up what you need
            return [seen[target - x], i]
        seen[x] = i                # record what you've seen
""",
        complexity="These solutions usually run in O(n) time and use O(n) extra space, compared with O(n²) time for the brute-force approach.",
        pitfalls=["Add each element to the map only *after* you check for its complement; otherwise an element can be paired with itself.", "Lists cannot be used as dict keys because they are mutable, so convert them to tuples first.", "Sorting can be the better choice when memory matters: it takes O(n log n) time but needs only O(1) extra space."],
        quiz=[dict(q="A nested-loop solution checks every pair to find two numbers summing to a target. What does a hash map change?",
                   options=["Each partner lookup becomes O(1), so O(n) total", "It sorts the array", "It reduces space to O(1)", "Nothing, it's still O(n²)"], answer=0,
                   why="You replace the inner search loop with a constant-time dictionary lookup.")],
    ),
    dict(
        category="Two Pointers",
        summary="You keep two indices into a sequence (usually a sorted one) and move them toward each other or in the same direction. Each move rules out a group of candidates, so you never recheck the same work.",
        signals=["The input is sorted, or sorting it would not lose any information you need.", "You need to compare elements from both ends, as in palindrome checks.", "The problem asks for a pair or triplet with a target sum.", "The solution must use O(1) extra space."],
        template="""def solve(nums, target):
    nums.sort()
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        if s < target:
            lo += 1        # need bigger
        else:
            hi -= 1        # need smaller
""",
        complexity="Each scan takes O(n) time (O(n log n) overall if you sort first) and uses O(1) extra space.",
        pitfalls=["Skip over duplicate values, or the same answer will be reported more than once.", "Make sure every iteration moves at least one pointer; otherwise the loop never ends.", "Choose the loop condition (`lo < hi` or `lo <= hi`) deliberately, based on whether the two pointers may point at the same element."],
        quiz=[dict(q="In a sorted array, `nums[lo] + nums[hi]` is **too small**. Which pointer moves?",
                   options=["lo moves right", "hi moves left", "both move", "restart from the middle"], answer=0,
                   why="Moving `lo` to the right is the only move that can increase the sum.")],
    ),
    dict(
        category="Sliding Window",
        summary="You maintain a contiguous window, `[left, right]`, over the input. The right edge advances one step at a time, and whenever the window breaks the problem's rule, the left edge moves forward until the window is valid again. Every element enters the window once and leaves it at most once.",
        signals=["The problem asks for the longest or shortest **substring** or **subarray** that satisfies some condition.", "The answer is a contiguous range of the input.", "The condition can be updated incrementally as elements enter and leave (for example, counts, sums, or the number of distinct characters)."],
        template="""def longest(s):
    window = {}
    left = best = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1        # expand
        while window[ch] > 1:                     # invalid? shrink
            window[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)        # record
    return best
""",
        complexity="The algorithm runs in O(n) time because each pointer moves forward at most n times. The extra space is whatever you need to describe the window, such as a dictionary of character counts.",
        pitfalls=["Record the answer at the right moment: for the longest window, record it after shrinking; for the shortest window, record it while the window is still valid, before each shrink.", "Subsequence problems are not sliding-window problems, because a subsequence does not have to be contiguous."],
        quiz=[dict(q="Why is a sliding window O(n) even though it has a `while` loop inside a `for` loop?",
                   options=["`left` only moves forward, at most n times in total", "The while loop runs at most once", "Python optimises nested loops", "It isn't. It's O(n²)"], answer=0,
                   why="Count total pointer moves (amortised analysis): right moves n times and left moves at most n times.")],
    ),
    dict(
        category="Stack",
        summary="A stack is last in, first out. You push items that are waiting to be matched or resolved, and you pop them when the matching item arrives. Handling the most recent item first is exactly what nested structures require.",
        signals=["The input contains matching brackets or some other nested structure.", "The problem asks for the next greater (or smaller) element, which calls for a monotonic stack.", "You need to undo actions or keep backtracking state.", "You need to evaluate an arithmetic expression."],
        template="""def balanced(s):
    pairs = {")": "(", "]": "["}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack
""",
        complexity="These solutions run in O(n) time and use up to O(n) space for the stack.",
        pitfalls=["Check that the stack is not empty before you pop or peek; otherwise you will get an IndexError.", "If items are left on the stack at the end, something was never matched, which usually means the answer is a failure."],
        quiz=[dict(q="After scanning `\"(()\"` with the bracket-matching template, what's left on the stack?",
                   options=["['(']", "[]", "['(', '(']", "[')']"], answer=0, why="The second `(` is matched by the `)`, but the first one is never closed, so it stays on the stack.")],
    ),
    dict(
        category="Binary Search",
        summary="Binary search halves the search space at each step by asking a yes-or-no question about the middle element. It works on sorted arrays and, more generally, on any **monotonic** condition: one that is false for every value up to some point and true for every value after it.",
        signals=["The input is sorted, or it is a sorted array that has been rotated.", "The problem asks for the smallest (or largest) value that satisfies some condition.", "The problem requires O(log n) time.", "The answer lies in a numeric range, and you can test whether any candidate value is large enough."],
        template="""def first_true(lo, hi, ok):
    # smallest x in [lo, hi] with ok(x) True (ok is monotonic)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid          # mid might be the answer
        else:
            lo = mid + 1      # answer is to the right
    return lo
""",
        complexity="The loop runs O(log n) times, and each iteration does a constant amount of work.",
        pitfalls=["Off-by-one errors are common. Pair `lo < hi` with `hi = mid`, or pair `lo <= hi` with `hi = mid - 1`, and stay consistent within one solution.", "Make sure every branch shrinks the range; otherwise the loop can run forever.", "For a rotated array, first work out which half is sorted, and then decide which half to search."],
        quiz=[dict(q="Roughly how many iterations does binary search need for 1,000,000 items?",
                   options=["About 20", "About 1,000", "About 500,000", "About 6"], answer=0, why="Each step halves the range, and log₂(1,000,000) is about 20.")],
    ),
    dict(
        category="Linked List",
        summary="Linked-list problems are about rewiring `next` pointers. The key tools are a dummy head node, slow and fast pointers (for finding the middle or detecting a cycle), and in-place reversal.",
        signals=["The input is a `ListNode`.", "The problem asks you to work in place or to use O(1) extra space.", "You need the middle node, the n-th node from the end, or to detect a cycle."],
        template="""def reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # save before overwriting
        cur.next = prev
        prev, cur = cur, nxt
    return prev

def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow
""",
        complexity="These solutions usually run in O(n) time and use O(1) extra space.",
        pitfalls=["If you overwrite `node.next` before saving it, you lose the rest of the list.", "If you forget to terminate the new list (`tail.next = None`), you can accidentally create a cycle.", "Check for `None` before following a pointer, for example with `while fast and fast.next`."],
        quiz=[dict(q="Slow moves 1 step and fast moves 2. When fast reaches the end, where is slow?",
                   options=["At the middle", "At the head", "One from the end", "At the end too"], answer=0,
                   why="Fast covers twice the distance that slow does, so slow has covered half the list.")],
    ),
    dict(
        category="Trees",
        summary="Most tree problems are solved either with a depth-first search that combines the answers from the left and right subtrees, or with a breadth-first search that processes the tree level by level. Before writing code, decide what each recursive call **returns** to its parent and what, if anything, it records globally.",
        signals=["The input is a `TreeNode`.", "The problem asks about depth, height, paths, or ancestors.", "The problem asks you to process the tree level by level, which calls for BFS.", "The tree is a binary search tree, so an in-order traversal visits the values in sorted order."],
        template="""def dfs(node):
    if not node:
        return 0                     # base case
    left = dfs(node.left)
    right = dfs(node.right)
    # combine: what does this subtree report to its parent?
    return 1 + max(left, right)
""",
        complexity="A traversal takes O(n) time. Recursion uses O(h) space, where h is the height of the tree: about log n for a balanced tree and up to n for a completely skewed one.",
        pitfalls=["Keep the value you return to the parent separate from the global answer; in Maximum Path Sum, for example, they are different quantities.", "Checking that a tree is a valid BST requires bounds inherited from all ancestors, not just a comparison with the parent.", "Remember the base case for an empty tree (`if not node`)."],
        quiz=[dict(q="Which traversal visits the values of a BST in sorted order?",
                   options=["In-order (left, node, right)", "Pre-order", "Post-order", "Level-order"], answer=0,
                   why="Everything in the left subtree is smaller and everything in the right is larger.")],
    ),
    dict(
        category="Tries",
        summary="A trie is a tree of characters in which each path from the root spells out a prefix. A lookup costs O(length of the word), no matter how many words are stored, and a search can stop early as soon as a prefix does not exist.",
        signals=["Many of the words share prefixes.", "The problem involves \"starts with\" queries or autocomplete.", "You need to search a grid for many words at once."],
        template="""class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True            # end-of-word marker

    def starts_with(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node:
                return False
            node = node[c]
        return True
""",
        complexity="Each insert or search takes O(L) time, where L is the length of the word. The trie uses space proportional to the total number of characters inserted.",
        pitfalls=["Mark the end of each word explicitly: 'app' is a prefix of 'apple', but it is not necessarily a stored word.", "In Word Search II, remove each word from the trie once you find it, so it is not reported twice and the search stays fast."],
        quiz=[dict(q="Why use a trie instead of a set of words for prefix queries?",
                   options=["A prefix check is O(prefix length) instead of scanning every word", "It uses less memory", "Sets can't store strings", "Tries are sorted"], answer=0,
                   why="With a set, you would have to test `w.startswith(p)` against every stored word.")],
    ),
    dict(
        category="Heap / Priority Queue",
        summary="Use a heap when you repeatedly need the smallest (or largest) item while new items keep arriving. A heap supports push and pop in O(log n) time and lets you peek at the top item in O(1) time.",
        signals=["The problem asks for the k largest, smallest, or closest items.", "You need to merge several sorted lists or streams.", "You need a running median.", "You need to schedule items by their earliest time."],
        template="""import heapq

def k_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)    # drop the smallest
    return heap                    # the k largest
""",
        complexity="Finding the top k of n items with a heap of size k takes O(n log k) time and O(k) space.",
        pitfalls=["Python's `heapq` is a min-heap only, so negate the values if you need a max-heap.", "When you push tuples, include a unique tiebreaker (such as an index) so that Python never has to compare the objects themselves."],
        quiz=[dict(q="To keep the **k largest** items, which heap do you maintain?",
                   options=["A min-heap of size k", "A max-heap of size n", "A min-heap of size n", "A max-heap of size k"], answer=0,
                   why="The min-heap's top is the weakest of the current top k, which is the one to evict.")],
    ),
    dict(
        category="Backtracking",
        summary="Backtracking builds a solution one choice at a time. When a partial solution cannot lead to a valid answer, you undo the last choice and try the next one. The rhythm is always the same: choose, explore, then un-choose.",
        signals=["The problem asks for all combinations, permutations, or subsets.", "You are searching under constraints, as in finding a word in a grid or placing N queens.", "The input is small enough that an exponential-time search is acceptable."],
        template="""def combos(candidates, target):
    out, path = [], []
    def bt(start, remaining):
        if remaining == 0:
            out.append(path[:])           # copy!
            return
        for i in range(start, len(candidates)):
            if candidates[i] <= remaining:
                path.append(candidates[i])          # choose
                bt(i, remaining - candidates[i])    # explore
                path.pop()                          # un-choose
    bt(0, target)
    return out
""",
        complexity="Backtracking takes exponential time in the worst case. Pruning branches that cannot succeed is what makes it fast enough in practice.",
        pitfalls=["Append a copy of the current path (`path[:]`) to the results, not the path itself, which keeps changing.", "Restore any state you changed (for example, un-mark visited cells) before returning from a call.", "Pass a start index into each call so the same combination is not generated in several different orders."],
        quiz=[dict(q="Why `out.append(path[:])` instead of `out.append(path)`?",
                   options=["path keeps changing; you need a snapshot", "It's faster", "path is a tuple", "No difference"], answer=0,
                   why="Without a copy, every stored result would refer to the same list, which is empty by the time the search finishes.")],
    ),
    dict(
        category="Graphs",
        summary="A graph is a set of nodes connected by edges. You explore it with DFS or BFS while tracking which nodes you have visited; union-find answers connectivity questions, and topological sort handles dependencies.",
        signals=["The input is a grid of cells, as in island-counting or flood-fill problems.", "The problem involves prerequisites or other dependencies.", "You need to count or compare connected components.", "The input is given explicitly as nodes and edges."],
        template="""from collections import deque

def bfs(start, neighbors):
    seen = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for nxt in neighbors(node):
            if nxt not in seen:
                seen.add(nxt)          # mark when enqueued
                q.append(nxt)
    return seen
""",
        complexity="A traversal takes O(V + E) time and space, where V is the number of nodes and E the number of edges. For a grid, that becomes O(rows × cols).",
        pitfalls=["Mark a node as visited when you **push** it, not when you pop it; otherwise the same node can be queued many times.", "Check the grid boundaries before you read a neighbouring cell.", "Be clear about whether the edges are directed or undirected, and add them to the adjacency list accordingly."],
        quiz=[dict(q="Which algorithm detects whether course prerequisites contain a cycle?",
                   options=["Topological sort (Kahn's)", "Binary search", "Dijkstra", "Two pointers"], answer=0,
                   why="If some nodes never reach an in-degree of 0, those nodes form a cycle.")],
    ),
    dict(
        category="Advanced Graphs",
        summary="In these problems, you first have to *build* the graph from the input, and then run a standard algorithm on it, such as topological sort, Dijkstra's algorithm, or a minimum spanning tree.",
        signals=["The input hides ordering constraints that you need to extract.", "The problem asks for shortest paths in a weighted graph.", "The problem asks for the minimum cost to connect everything."],
        template="""from collections import deque

def topo_order(nodes, edges):
    graph = {n: [] for n in nodes}
    indeg = {n: 0 for n in nodes}
    for a, b in edges:
        graph[a].append(b)
        indeg[b] += 1
    q = deque(n for n in nodes if indeg[n] == 0)
    order = []
    while q:
        n = q.popleft()
        order.append(n)
        for m in graph[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    return order if len(order) == len(nodes) else None   # None = cycle
""",
        complexity="Topological sort runs in O(V + E) time.",
        pitfalls=["Avoid adding the same edge twice, because duplicate edges inflate the in-degree counts.", "Handle invalid input separately; in Alien Dictionary, for example, a word that comes before its own prefix makes the ordering impossible."],
        quiz=[dict(q="Kahn's algorithm outputs fewer nodes than exist. What does that mean?",
                   options=["The graph has a cycle", "The graph is disconnected", "There are duplicate nodes", "It's a tree"], answer=0,
                   why="Nodes on a cycle never reach in-degree 0.")],
    ),
    dict(
        category="1-D Dynamic Programming",
        summary="In 1-D dynamic programming, the answer for position i is built from the answers for smaller positions. Define what `dp[i]` means, write the recurrence, set the base cases, and then, if possible, keep only the last few values instead of the whole table.",
        signals=["The problem asks for the number of ways, the minimum cost, or the maximum value.", "Each step involves a choice that affects which choices are available later.", "A brute-force recursive solution would recompute the same subproblems many times."],
        template="""def rob(nums):
    # dp[i] = best using the first i houses
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
""",
        complexity="These solutions usually take O(n) or O(n · k) time and between O(1) and O(n) space.",
        pitfalls=["State the meaning of `dp[i]` in words before you write any code.", "Double-check the base cases and the table size (does it need n or n + 1 entries?).", "A greedy approach often looks correct but fails; Coin Change is the classic example."],
        quiz=[dict(q="What's the core sign that a problem needs DP rather than plain recursion?",
                   options=["Overlapping subproblems get recomputed", "The input is sorted", "It uses a tree", "It asks for all solutions"], answer=0,
                   why="Memoizing or tabulating the results means each subproblem is solved only once.")],
    ),
    dict(
        category="2-D Dynamic Programming",
        summary="Here the state needs two indices, such as a position in each of two strings or a cell in a grid. You fill a table in which each cell depends on neighbouring cells (typically the one above, the one to the left, and the diagonal).",
        signals=["You are comparing two sequences, as in Longest Common Subsequence or edit distance.", "You are counting or optimising paths through a grid.", "The state is naturally described as \"the first i items with capacity j\"."],
        template="""def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return dp[0][0]
""",
        complexity="These solutions take O(m · n) time. They use O(m · n) space for the full table, which can often be reduced to a single row.",
        pitfalls=["Build the table with a comprehension (`[[0] * n for _ in range(m)]`), not `[[0] * n] * m`, which repeats the same row object.", "Fill the table in an order that computes every cell's dependencies before the cell itself."],
        quiz=[dict(q="In LCS, when `a[i] != b[j]`, dp[i][j] is…",
                   options=["max(dp[i+1][j], dp[i][j+1])", "dp[i+1][j+1] + 1", "0", "dp[i+1][j+1]"], answer=0,
                   why="You skip a character from one string or the other, and keep whichever result is better.")],
    ),
    dict(
        category="Greedy",
        summary="A greedy algorithm makes the locally best choice at each step and never revisits it. It only works when you can argue that a locally best choice never prevents a globally best answer.",
        signals=["The problem asks whether something is reachable or possible.", "A single pass that tracks a running best value seems sufficient.", "You can make an exchange argument: swapping any solution's choice for the greedy choice never makes it worse."],
        template="""def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)   # extend or restart
        best = max(best, cur)
    return best
""",
        complexity="Greedy solutions usually take O(n) time, or O(n log n) if they sort first.",
        pitfalls=["Greedy code is easy to write and easy to get wrong, so try to find a counterexample before you commit to it.", "If the greedy approach fails, the problem usually needs dynamic programming instead."],
        quiz=[dict(q="In Kadane's algorithm, why restart the running sum at `x` when `cur + x < x`?",
                   options=["A negative prefix can only lower future sums", "To save memory", "Because x is positive", "To handle sorting"], answer=0,
                   why="Dropping a negative running sum always helps whatever comes next.")],
    ),
    dict(
        category="Intervals",
        summary="Sort the intervals by their start (or end) times, and then sweep through them once, merging overlaps or counting conflicts as you go.",
        signals=["The input is a list of `[start, end]` pairs.", "The problem is about meetings, bookings, or ranges.", "You need to detect overlaps, merge intervals, or find the minimum number of removals."],
        template="""def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)   # overlap -> extend
        else:
            out.append([s, e])
    return out
""",
        complexity="Sorting takes O(n log n) time, and the sweep afterwards takes O(n).",
        pitfalls=["Decide whether intervals that only touch at an endpoint count as overlapping, and use `<` or `<=` accordingly.", "To keep the maximum number of non-overlapping intervals, sort by **end** time, not start time."],
        quiz=[dict(q="To keep the most non-overlapping intervals, sort by…",
                   options=["End time", "Start time", "Length", "No sort needed"], answer=0,
                   why="The interval that finishes earliest leaves the most room for the intervals after it.")],
    ),
    dict(
        category="Math & Geometry",
        summary="These problems involve manipulating matrices and doing arithmetic on indices. Work out how positions map to new positions (for example, a rotation is a transpose followed by a reversal), and handle the boundaries carefully.",
        signals=["You need to transform a 2-D matrix.", "The problem requires you to work in place.", "You need to traverse a matrix in a spiral or layer by layer."],
        template="""def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]   # transpose
    for row in m:
        row.reverse()                              # mirror
""",
        complexity="Processing an n × n matrix takes O(n²) time, and an in-place solution uses O(1) extra space.",
        pitfalls=["When you shrink the boundaries in a spiral traversal, re-check `top <= bottom` (and `left <= right`) partway through each loop.", "If you mark cells in place, make sure the markers do not overwrite information you still need."],
        quiz=[dict(q="A 90° clockwise rotation equals…",
                   options=["Transpose, then reverse each row", "Reverse each row, then transpose", "Transpose twice", "Reverse rows, then columns"], answer=0,
                   why="Try it on a 2 × 2 matrix to convince yourself.")],
    ),
    dict(
        category="Bit Manipulation",
        summary="Treat integers as arrays of bits. XOR cancels out pairs of equal values, `n & (n - 1)` clears the lowest set bit, and shifts move bits left or right.",
        signals=["The problem forbids arithmetic operators or demands O(1) space for a numeric task.", "You need to count the set bits in a number.", "You need to find a single missing or unpaired value."],
        template="""def count_ones(n):
    count = 0
    while n:
        n &= n - 1     # drop lowest set bit
        count += 1
    return count
""",
        complexity="These solutions take time proportional to the number of bits, which is constant for fixed-width integers.",
        pitfalls=["Python integers have no fixed size, so mask with `0xFFFFFFFF` when a problem assumes 32-bit integers.", "Bitwise operators have lower precedence than comparisons and arithmetic, so wrap bit operations in parentheses."],
        quiz=[dict(q="XOR all of [4, 1, 2, 1, 2]. What's the result?", code="r = 0\nfor x in [4, 1, 2, 1, 2]:\n    r ^= x\nprint(r)",
                   options=["4", "0", "10", "1"], answer=0, predict=True, why="Equal pairs cancel out (x ^ x = 0), which leaves only the unpaired 4.")],
    ),
]
