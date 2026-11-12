# One guide per problem category: how to recognise it, a code template, and a quick quiz.
# Templates are compiled (not run) at build time.

PATTERNS = [
    dict(
        category="Arrays & Hashing",
        summary="Remember the values you have already seen in a dictionary or set. Then you can usually check for a value in the same amount of time, no matter how many items there are (average O(1) lookup), instead of scanning the input again.",
        signals=["The problem asks for a pair, a duplicate, or a value that completes a pair to reach a target (a complement).", "The problem asks you to group items that share some property.", "You need to count how often values occur.", "Your simple solution uses a nested loop, and the inner loop only *searches* for something."],
        template="""def solve(nums, target):
    seen = {}                      # value -> index (or count, or list)
    for i, x in enumerate(nums):
        if target - x in seen:     # look up what you need
            return [seen[target - x], i]
        seen[x] = i                # record what you've seen
""",
        complexity="These solutions usually run in O(n) time and use O(n) extra space, compared with O(n²) time for the brute-force approach.",
        pitfalls=["Add each value to the dictionary only *after* checking for the value that completes its pair; otherwise a value can be paired with itself.", "Lists cannot be used as dictionary keys because they can change. Convert them to tuples first.", "Sorting can be a better choice when memory matters: it takes O(n log n) time but needs only O(1) extra space."],
        quiz=[dict(q="A nested-loop solution checks every pair to find two numbers summing to a target. What does a hash map change?",
                   options=["Each partner lookup becomes O(1), so O(n) overall", "The pairs come out sorted, so O(n log n) overall", "Space drops to O(1), but time stays O(n²)", "Each lookup is still O(n), so it stays O(n²)"], answer=0,
                   why="You replace the inner search loop with a constant-time dictionary lookup.")],
    ),
    dict(
        category="Two Pointers",
        summary="Track two indices in a sequence (the two-pointer technique) and move them toward each other or in the same direction. Each move lets you skip choices that cannot be the answer, so you do not check the same items again.",
        signals=["The input is sorted, or sorting it would not lose any information you need.", "You need to compare items from both ends, as when checking whether a word reads the same forward and backward (a palindrome check).", "The problem asks for a pair or triplet with a target sum.", "The solution must use O(1) extra space (constant extra space)."],
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
        pitfalls=["Skip over duplicate values, or the same answer will be reported more than once.", "Make sure every loop repeats only after moving at least one index; otherwise it never ends.", "Choose the loop condition (`lo < hi` or `lo <= hi`) based on whether both indices may refer to the same item."],
        quiz=[dict(q="In a sorted array, `nums[lo] + nums[hi]` is **too small**. Which index moves?",
                   options=["lo moves right", "hi moves left", "both move", "restart from the middle"], answer=0,
                   why="Moving `lo` to the right is the only move that can increase the sum.")],
    ),
    dict(
        category="Sliding Window",
        summary="Keep track of one continuous part of the input, from `left` to `right` (a sliding window). Move `right` forward to make the part larger. If it stops meeting the problem's rule, move `left` forward until it does again. Each item is added once and removed at most once.",
        signals=["The problem asks for the longest or shortest continuous part of a string or list (a substring or subarray) that satisfies a condition.", "The answer is a continuous range of the input.", "You can update the condition as items enter or leave the range, for example by updating counts, sums, or the number of different characters."],
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
        complexity="The algorithm runs in O(n) time because each index moves forward at most n times. The extra space is whatever you need to describe the range, such as a dictionary of character counts.",
        pitfalls=["Record the answer at the right moment: for the longest range, record it after shrinking; for the shortest range, record it while it still meets the rule, before each shrink.", "A subsequence can skip items, so it does not have to be continuous; sliding windows are only for continuous ranges."],
        quiz=[dict(q="Why is a sliding window O(n) even though it has a `while` loop inside a `for` loop?",
                   options=["`left` only moves forward, at most n times in total", "The inner `while` runs at most once per step of `right`", "Each `while` pass halves the window", "It isn't; nested loops make it O(n²)"], answer=0,
                   why="Count all moves: `right` moves n times, and `left` moves at most n times. This way of counting the total work is called amortized analysis.")],
    ),
    dict(
        category="Stack",
        summary="A stack lets you add (push) and remove (pop) items at the same end. The last item added is the first one removed (last in, first out, or LIFO). This is useful when you need to match nested items, such as brackets: add an opening bracket, then remove it when its closing bracket appears.",
        signals=["The input contains matching brackets or another structure nested inside itself.", "The problem asks for the next larger or smaller item; this can use a stack kept in increasing or decreasing order (a monotonic stack).", "You need to undo actions or remember choices while exploring different possibilities (backtracking).", "You need to evaluate an arithmetic expression."],
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
        summary="Binary search cuts the remaining choices in half at each step by checking the middle item. It works on sorted arrays and on any yes-or-no test whose answers change only once as values increase (a monotonic condition). For example, the answer can be false up to a cutoff and true after it.",
        signals=["The input is sorted, or it is a sorted array that has been rotated.", "The problem asks for the smallest or largest value that meets a condition.", "The problem needs only about 20 checks to search a million items (O(log n) time).", "The answer lies in a range of numbers, and you can test whether a possible answer is large enough."],
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
        summary="In a linked list, each node has a `next` link to the following node. Many problems are solved by changing those links (rewiring pointers). A temporary starter node (dummy head), two links that move at different speeds (slow and fast pointers), and reversing the links without making a copy (in-place reversal) are common tools.",
        signals=["The input is a `ListNode` (one item in a linked list).", "The problem asks you to change the existing list without making a copy (in place), or to use O(1) extra space.", "You need the middle item, the n-th item from the end, or to detect whether links form a loop (a cycle)."],
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
        summary="Most tree problems use one of two walks: visit each branch before moving to the next (depth-first search, DFS), or visit all nodes on one level before moving down (breadth-first search, BFS). Before writing code, decide what each call returns to the call that started it, and whether it also updates a shared answer.",
        signals=["The input is a `TreeNode` (one node in a tree).", "The problem asks about depth, height, paths, or ancestors.", "The problem asks you to process the tree level by level, which uses breadth-first search (BFS).", "The tree is a binary search tree, so visiting left subtree, node, then right subtree (in-order traversal) visits values in sorted order."],
        template="""def dfs(node):
    if not node:
        return 0                     # base case
    left = dfs(node.left)
    right = dfs(node.right)
    # combine: what does this subtree report to its parent?
    return 1 + max(left, right)
""",
        complexity="A traversal takes O(n) time. Recursion uses O(h) space, where h is the tree's height: about log n for a balanced tree and up to n for a very unbalanced tree.",
        pitfalls=["Keep the value you return to the parent separate from the global answer; in Maximum Path Sum, for example, they are different quantities.", "Checking that a tree is a valid BST requires bounds inherited from all ancestors, not just a comparison with the parent.", "Remember the base case for an empty tree (`if not node`)."],
        quiz=[dict(q="Which traversal visits the values of a BST in sorted order?",
                   options=["In-order (left, node, right)", "Pre-order (node, left, right)", "Post-order (left, right, node)", "Level-order (top to bottom)"], answer=0,
                   why="Everything in the left subtree is smaller and everything in the right is larger.")],
    ),
    dict(
        category="Tries",
        summary="A trie (pronounced “try”) stores words as paths of letters that share their beginnings. Each path from the top spells a word prefix. Finding a word takes time proportional to its length, regardless of how many words are stored, and the search can stop as soon as a needed prefix is missing.",
        signals=["Many of the words start with the same letters (they share prefixes).", "The problem asks which words start with some letters, or needs autocomplete.", "You need to search a grid for many words at once."],
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
                   options=["A prefix check costs O(prefix length), not a scan of every word", "A trie stores the same words in less memory than a set", "Set lookups are O(n) for strings, but trie lookups are O(1)", "A trie keeps words sorted, so prefixes can be binary searched"], answer=0,
                   why="With a set, you would have to test `w.startswith(p)` against every stored word.")],
    ),
    dict(
        category="Heap / Priority Queue",
        summary="Use a heap (a priority queue) when you repeatedly need the smallest or largest item as new items arrive. Adding or removing the top item takes O(log n) time; checking which item is on top takes O(1) time.",
        signals=["The problem asks for the k largest, smallest, or closest items.", "You need to combine several sorted lists or streams.", "You need the median as new values arrive (a running median).", "You need to schedule items by their earliest time."],
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
        summary="Build an answer one choice at a time. If a partial answer cannot lead to a valid result, undo the last choice and try another one. This method is called backtracking: choose, explore, then undo the choice.",
        signals=["The problem asks for all combinations, orderings, or subsets (permutations).", "You are searching under rules, such as finding a word in a grid or placing N queens.", "The input is small enough that trying many possible choices (an exponential-time search) is acceptable."],
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
        complexity="Backtracking may take exponential time in the worst case. Skipping choices that cannot lead to an answer (pruning) often makes it fast enough in practice.",
        pitfalls=["Append a copy of the current path (`path[:]`) to the results, not the path itself, which keeps changing.", "Restore any state you changed (for example, un-mark visited cells) before returning from a call.", "Pass a start index into each call so the same combination is not generated in several different orders."],
        quiz=[dict(q="Why `out.append(path[:])` instead of `out.append(path)`?",
                   options=["path keeps changing; you need a snapshot", "Slicing is faster than appending the list itself", "append can't store a list inside another list", "No difference; both store the same values"], answer=0,
                   why="Without a copy, every stored result would refer to the same list, which is empty by the time the search finishes.")],
    ),
    dict(
        category="Graphs",
        summary="A graph is a set of points (nodes) connected by links (edges). You can visit its nodes with depth-first search (DFS) or breadth-first search (BFS), marking which ones you have seen. Use a structure that joins connected groups (union-find) to check whether points are connected, or order tasks so every prerequisite comes first (topological sort).",
        signals=["The input is a grid of cells, as in island-counting or flood-fill problems.", "The problem involves prerequisites or other dependencies.", "You need to count or compare separate connected groups (connected components).", "The input lists points and links (nodes and edges)."],
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
        pitfalls=["Mark a node as visited when you add it to the queue or stack, not when you remove it; otherwise you may add the same node many times.", "Check the grid boundaries before you read a neighbouring cell.", "Be clear about whether links go one way (directed) or both ways (undirected). Store each node's neighbours in a list (an adjacency list)."],
        quiz=[dict(q="Which algorithm detects whether course prerequisites contain a cycle?",
                   options=["Topological sort (Kahn's)", "Dijkstra's shortest paths", "Union-find over the edges", "Minimum spanning tree (Kruskal's)"], answer=0,
                   why="If some courses still have a prerequisite after all available courses are processed, there is a cycle. Union-find detects cycles in undirected graphs, not in prerequisite (directed) graphs.")],
    ),
    dict(
        category="Advanced Graphs",
        summary="First work out which points are connected and build a graph from the input. Then use an algorithm suited to the question: order tasks around their dependencies (topological sort), find shortest paths when links have costs (Dijkstra's algorithm), or connect everything at the lowest total cost (minimum spanning tree).",
        signals=["The input hides rules about which items must come first, and you need to work out the order.", "The problem asks for shortest paths when links have different costs (a weighted graph).", "The problem asks for the cheapest way to connect everything."],
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
        pitfalls=["Avoid adding the same link twice. Duplicate links make the number of prerequisites for a node look too large (its in-degree).", "Handle invalid input separately; in Alien Dictionary, for example, a word that comes before its own prefix makes the ordering impossible."],
        quiz=[dict(q="Kahn's algorithm outputs fewer nodes than exist. What does that mean?",
                   options=["The graph has a cycle", "The graph is disconnected", "There are duplicate nodes", "It's a tree"], answer=0,
                   why="A course on a cycle always has a remaining prerequisite, so its in-degree (number of incoming prerequisite links) never reaches 0.")],
    ),
    dict(
        category="1-D Dynamic Programming",
        summary="For many problems, the answer at position `i` can be calculated from answers at earlier positions. This is one-dimensional dynamic programming (1-D DP). Write down what `dp[i]` means, the rule for calculating it from earlier answers (the recurrence), and the first answers you already know (base cases). If possible, keep only the most recent answers instead of the whole table.",
        signals=["The problem asks for the number of ways, the minimum cost, or the maximum value.", "Each step involves a choice that affects which choices are available later.", "A simple recursive solution would solve the same smaller questions many times (repeated subproblems)."],
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
                   options=["The same subproblems get solved again and again", "Each subproblem is independent of the others", "The input is sorted, so choices can be greedy", "It asks for every solution, not just the best"], answer=0,
                   why="Memoizing or tabulating the results means each subproblem is solved only once.")],
    ),
    dict(
        category="2-D Dynamic Programming",
        summary="Some problems need two positions to describe what remains, such as one position in each of two strings or a row and column in a grid. This is two-dimensional dynamic programming (2-D DP). Fill a table where each answer uses nearby answers, often the cell above, the cell to the left, and the diagonal cell.",
        signals=["You are comparing two sequences, as in Longest Common Subsequence or edit distance.", "You are counting or optimizing paths through a grid.", "Each answer depends on two values, such as how many items you have considered and how much capacity remains."],
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
                   options=["max(dp[i+1][j], dp[i][j+1])", "dp[i+1][j+1] + 1", "min(dp[i+1][j], dp[i][j+1])", "dp[i+1][j+1]"], answer=0,
                   why="You skip a character from one string or the other, and keep whichever result is better.")],
    ),
    dict(
        category="Greedy",
        summary="A greedy algorithm picks what looks best at each step and does not change that choice later. It works only when you can show that each choice still allows the best possible final answer.",
        signals=["The problem asks whether something is reachable or possible.", "A single pass that tracks the best value so far seems sufficient.", "You can show that replacing a choice in any valid solution with the greedy choice never makes the final answer worse (an exchange argument)."],
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
                   options=["A negative running sum can only lower later sums", "A positive x always starts a better subarray", "Restarting stops the sum from overflowing", "It keeps the subarray as short as possible"], answer=0,
                   why="Dropping a negative running sum always helps whatever comes next.")],
    ),
    dict(
        category="Intervals",
        summary="Sort the time ranges by their start or end, then scan the list once. As you go, combine ranges that overlap or count the ones that conflict.",
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
        complexity="Sorting takes O(n log n) time, and scanning the sorted list takes O(n).",
        pitfalls=["Decide whether intervals that only touch at an endpoint count as overlapping, and use `<` or `<=` accordingly.", "To keep the maximum number of non-overlapping intervals, sort by **end** time, not start time."],
        quiz=[dict(q="To keep the most non-overlapping intervals, sort by…",
                   options=["End time", "Start time", "Length", "No sort needed"], answer=0,
                   why="The interval that finishes earliest leaves the most room for the intervals after it.")],
    ),
    dict(
        category="Math & Geometry",
        summary="These problems involve changing a matrix or calculating new positions from old ones. For example, to turn a square matrix clockwise, swap rows and columns (transpose), then reverse each row. Keep careful track of the boundaries.",
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
        summary="Look at an integer as a row of 0s and 1s (bits). XOR cancels matching pairs, `n & (n - 1)` clears the rightmost 1 (the lowest set bit), and shift operators move all bits left or right.",
        signals=["The problem forbids arithmetic operators or requires constant extra space for a number problem (O(1) space).", "You need to count the 1s in a number's binary form (set bits).", "You need to find one missing or unpaired value."],
        template="""def count_ones(n):
    count = 0
    while n:
        n &= n - 1     # drop lowest set bit
        count += 1
    return count
""",
        complexity="These solutions take time proportional to the number of bits. If the number of bits is fixed (for example, 32-bit integers), this is constant time.",
        pitfalls=["Python integers have no fixed size, so mask with `0xFFFFFFFF` when a problem assumes 32-bit integers.", "Bitwise operators have lower precedence than comparisons and arithmetic, so wrap bit operations in parentheses."],
        quiz=[dict(q="XOR all of [4, 1, 2, 1, 2]. What's the result?", code="r = 0\nfor x in [4, 1, 2, 1, 2]:\n    r ^= x\nprint(r)",
                   options=["4", "0", "10", "1"], answer=0, predict=True, why="Equal pairs cancel out (x ^ x = 0), which leaves only the unpaired 4.")],
    ),
]
