# One "key insight" question per problem. The correct option is listed first (answer=0);
# the UI shuffles options when it displays them.

def Q(q, right, *wrong, why="", code=None, predict=False):
    d = dict(q=q, options=[right, *wrong], answer=0, why=why)
    if code:
        d["code"] = code
    if predict:
        d["predict"] = True
    return d


INSIGHTS = {
    # Arrays & Hashing
    "contains-duplicate": Q("What's the simplest O(n) check for duplicates?", "Compare len(set(nums)) with len(nums)", "Sort, then binary search each element", "Use two nested loops", "Sum the numbers", why="A set drops duplicates, so its size shrinks exactly when a duplicate exists."),
    "valid-anagram": Q("Two strings are anagrams exactly when…", "Every character appears the same number of times in both", "They have the same length", "They share the same first and last letters", "Their sorted halves match", why="Their character counts must be equal, which you can check with `Counter(s) == Counter(t)`."),
    "two-sum": Q("Why insert `nums[i]` into the dict **after** checking for its complement?", "So an element can't pair with itself", "Dict inserts are slow", "To keep the dict sorted", "It doesn't matter", why="With target 6 and x = 3, checking first stops 3 from matching itself."),
    "group-anagrams": Q("What makes a good dictionary key for grouping anagrams?", "The sorted word or a 26-length count tuple", "The word's length", "The first letter", "The word itself", why="All anagrams map to the same canonical form."),
    "top-k-frequent-elements": Q("How does bucket sort get top-k in O(n)?", "Frequencies are at most n, so index buckets by frequency", "It sorts the counts with a faster algorithm", "It uses a heap internally", "It only scans k elements", why="Bucket i holds the values occurring i times; read the buckets from high to low."),
    "encode-and-decode-strings": Q("Why does `len + '#' + s` encoding survive strings that contain `#`?", "The decoder reads the length, then takes exactly that many characters without searching inside", "'#' is escaped automatically", "It doesn't. '#' breaks it", "Python strings can't contain '#'", why="Only the first '#' after the digits is a delimiter; the content is sliced by length."),
    "product-of-array-except-self": Q("answer[i] equals…", "prefix product before i × suffix product after i", "total product / nums[i]", "nums[i-1] × nums[i+1]", "sum of the other elements", why="That avoids division, and it handles zeros."),
    "longest-consecutive-sequence": Q("Why only start counting from x when `x - 1` isn't in the set?", "So each run is counted once, keeping the total O(n)", "To skip negative numbers", "Because sets are unordered", "To find the minimum", why="Starting mid-run would re-walk the same sequence many times."),
    # Two pointers
    "valid-palindrome": Q("How do you avoid building a cleaned copy of the string?", "Move two pointers inward, skipping non-alphanumeric characters", "Reverse the string in place", "Use recursion", "Sort the characters", why="This gives O(1) extra space."),
    "three-sum": Q("After sorting and fixing `nums[i]`, how are the other two found?", "Two pointers on the rest of the array", "Binary search for both", "A nested loop", "A heap", why="That makes it O(n²) overall instead of O(n³)."),
    "container-with-most-water": Q("Why move the **shorter** line inward?", "The area is capped by the shorter line, so moving the taller one can't help", "To keep the width the same", "It's random", "The taller line is always on the left", why="Moving the taller line only reduces width under the same height cap."),
    # Sliding window
    "best-time-to-buy-and-sell-stock": Q("What single value do you track while scanning?", "The minimum price seen so far", "The maximum price seen so far", "The average price", "The previous day's price", why="The best sale today is today's price minus the cheapest earlier price."),
    "longest-substring-without-repeating-characters": Q("When a repeated char is found inside the window, where does `left` jump?", "Just past that char's previous index", "To right", "Back to 0", "One step right", why="That's the smallest move that removes the duplicate."),
    "longest-repeating-character-replacement": Q("A window is valid when…", "window length − count of its most common char ≤ k", "it has at most k distinct letters", "its length ≤ k", "all its characters match", why="Every non-majority character must be replaced."),
    "minimum-window-substring": Q("When do you shrink the window from the left?", "As soon as it contains all required characters", "When it gets longer than t", "Never", "When a character repeats", why="Keep shrinking while it is still valid, recording the best window as you go."),
    # Stack
    "valid-parentheses": Q("Why is a stack the right structure?", "The most recently opened bracket must close first", "It sorts the brackets", "It counts brackets", "It handles unicode", why="The last bracket opened must be the first one closed, which is exactly last-in, first-out."),
    # Binary search
    "find-minimum-in-rotated-sorted-array": Q("If `nums[mid] > nums[hi]`, where is the minimum?", "Strictly to the right of mid", "At mid or to its left", "At index 0", "At hi", why="A larger value before a smaller one means the drop lies after mid."),
    "search-in-rotated-sorted-array": Q("What do you work out first at each step?", "Which half (lo..mid or mid..hi) is sorted", "Where the pivot is, with a separate scan", "Whether target is even", "The array's length", why="Then check whether the target falls in that sorted half's range."),
    # Linked list
    "reverse-linked-list": Q("What must you save before setting `cur.next = prev`?", "cur.next (the rest of the list)", "prev.next", "head", "Nothing", why="Otherwise you lose your only reference to the remaining nodes."),
    "merge-two-sorted-lists": Q("What does a dummy head node simplify?", "Attaching the first node without special-casing it", "Sorting the lists", "Detecting cycles", "Freeing memory", why="`tail.next = …` works the same for the first node and every node after it."),
    "reorder-list": Q("What are the three steps?", "Find the middle, reverse the second half, interleave the halves", "Sort, reverse, merge", "Copy to an array and rebuild", "Reverse the whole list twice", why="Each step is O(n) time and O(1) space."),
    "remove-nth-node-from-end-of-list": Q("How do you find the n-th node from the end in one pass?", "Keep a gap of n nodes between two pointers", "Count the length first", "Recursion", "Reverse the list", why="When the lead pointer hits the end, the trailing pointer is in position."),
    "linked-list-cycle": Q("Why do slow (1 step) and fast (2 steps) meet if there's a cycle?", "Inside the loop, fast closes the gap by one node per step", "They start at the same node", "Fast skips the cycle", "They only meet if the cycle is even-length", why="A gap that shrinks by 1 each step must reach 0."),
    "merge-k-sorted-lists": Q("Why push `(val, i, node)` into the heap instead of `(val, node)`?", "Ties on val would compare ListNodes, which raises TypeError", "To sort by list index", "Heaps need 3-tuples", "To save memory", why="The unique index i breaks ties before Python ever compares nodes."),
    # Trees
    "invert-binary-tree": Q("What does inverting do at every node?", "Swap its left and right children", "Reverse the node values", "Rotate the tree", "Sort the children", why="Apply it recursively and the whole tree is mirrored."),
    "maximum-depth-of-binary-tree": Q("Which recurrence gives the depth of a node?", "1 + max(depth(left), depth(right))", "depth(left) + depth(right)", "1 + min(…)", "number of leaves", why="An empty tree has depth 0."),
    "same-tree": Q("When are two trees identical?", "Roots match and both pairs of subtrees are identical", "Same number of nodes", "Same in-order traversal", "Same height", why="An in-order traversal alone doesn't capture the shape."),
    "subtree-of-another-tree": Q("Why isn't 'node values match at the top' enough?", "All descendants must match exactly, too", "Values can repeat", "Trees can be empty", "Because of recursion limits", why="Run a full same-tree check from each candidate node."),
    "lowest-common-ancestor-of-a-binary-search-tree": Q("When have you found the LCA in a BST?", "When p and q stop being on the same side of the current node", "At the root", "At the deepest node", "When you reach a leaf", why="That split point is the lowest node that has both as descendants."),
    "binary-tree-level-order-traversal": Q("How do you know where one level ends in BFS?", "Process exactly len(queue) nodes per round", "Track depth with recursion", "Insert None markers", "Count the leaves", why="At the start of each round the queue holds exactly one level."),
    "validate-binary-search-tree": Q("Why is comparing each node only with its children wrong?", "A deeper node can break a constraint set by a higher ancestor", "Children can be None", "BSTs allow duplicates", "It's actually fine", why="Pass down (low, high) bounds instead."),
    "kth-smallest-element-in-a-bst": Q("Which traversal visits BST values in ascending order?", "In-order", "Pre-order", "Post-order", "Level-order", why="Stop after k visits."),
    "construct-binary-tree-from-preorder-and-inorder-traversal": Q("What does `preorder[0]` tell you?", "It's the root, and its inorder position splits the left and right subtrees", "It's the leftmost leaf", "It's the tree's height", "Nothing on its own", why="Recurse on each side of the split."),
    "binary-tree-maximum-path-sum": Q("What does the recursive helper return to its parent?", "The best downward path starting at this node (one branch only)", "The best path anywhere in the subtree", "The subtree's total", "The node count", why="A path passing up through the parent can only continue down one side."),
    "serialize-and-deserialize-binary-tree": Q("Why include null markers ('N') when serializing?", "Without them, different shapes could produce the same string", "To make the string longer", "JSON requires them", "To sort the output", why="Preorder plus null markers determines the tree exactly."),
    # Tries
    "implement-trie-prefix-tree": Q("How does `search` differ from `starts_with`?", "search also requires an end-of-word marker at the last node", "search is recursive", "starts_with checks suffixes", "There's no difference", why="'app' can be a prefix of 'apple' without being a stored word."),
    "design-add-and-search-words-data-structure": Q("How is '.' handled during search?", "Branch into every child at that position (DFS)", "Skip the character", "Treat it as the letter 'a'", "Return False", why="A wildcard can match any letter."),
    "word-search-ii": Q("Why build a trie of the words instead of searching for each word separately?", "One DFS per cell explores all words at once, pruning dead prefixes", "Tries use less memory", "It's required by the grid", "To sort the output", why="Searching word by word repeats the same grid exploration for every word."),
    # Heap
    "find-median-from-data-stream": Q("What do the two heaps hold?", "Max-heap of the lower half, min-heap of the upper half", "Two copies of the data", "Even and odd numbers", "Positive and negative numbers", why="The median sits at the heap tops."),
    # Backtracking
    "combination-sum": Q("How do you allow reuse while avoiding duplicate combinations?", "Recurse with the same index i, never going back to earlier indices", "Sort the output and dedupe", "Use a set of tuples", "Recurse with i + 1", why="Staying at i allows reuse, and never going back stops reorderings."),
    "word-search": Q("How do you stop a path from reusing a cell?", "Temporarily mark the cell (e.g. '#') and restore it when backtracking", "Delete the cell from the board", "Copy the board at each step", "Track a global counter", why="Restoring the cell lets other paths use it."),
    # Graphs
    "number-of-islands": Q("What does the flood fill accomplish?", "It marks an entire island visited, so it's counted once", "It finds the largest island", "It sorts the grid", "It counts water cells", why="Count once per new land cell found, then sink the whole island."),
    "clone-graph": Q("Why record a node's copy in the map **before** cloning its neighbours?", "Cycles would otherwise recurse forever", "To keep the order", "Dicts need it", "To save memory", why="When a neighbour points back, it finds the existing copy."),
    "pacific-atlantic-water-flow": Q("What's the trick for efficiency?", "Search uphill from each ocean's border and intersect the reachable sets", "Simulate rain from every cell", "Sort cells by height", "Use binary search", why="That takes two traversals instead of one per cell."),
    "course-schedule": Q("What does it mean if the topological sort processes fewer courses than exist?", "There's a cycle, so it's impossible", "Some courses have no prerequisites", "The graph is a tree", "The answer is still True", why="Courses on a cycle never reach in-degree 0."),
    "graph-valid-tree": Q("A graph with n nodes and n − 1 edges is a tree if and only if…", "It's connected (equivalently, it has no cycle)", "It's sorted", "Every node has degree 2", "It's directed", why="With n − 1 edges, connected and acyclic imply each other."),
    "number-of-connected-components-in-an-undirected-graph": Q("In union-find, the component count drops by one when…", "An edge joins two nodes with different roots", "Any edge is processed", "Find is called", "A node has no edges", why="Edges inside an existing component don't merge anything."),
    # Advanced graphs
    "alien-dictionary": Q("What does one adjacent word pair tell you?", "The first differing characters give one ordering edge", "Every character in the first word comes first", "The words' lengths order the alphabet", "Nothing on its own", why="Characters after the first difference carry no information."),
    # 1-D DP
    "climbing-stairs": Q("Which recurrence gives ways(n), the number of ways to climb n stairs?", "ways(n − 1) + ways(n − 2)", "2 × ways(n − 1)", "n × (n − 1)", "ways(n − 1) + 1", why="The last move was either one step or two steps, which gives the Fibonacci recurrence."),
    "house-robber": Q("Which recurrence gives best(i), the most you can take from the first i houses?", "max(best(i − 1), best(i − 2) + nums[i])", "best(i − 1) + nums[i]", "max(nums[:i])", "best(i − 2) + nums[i − 1]", why="Either skip house i or rob it and skip i − 1."),
    "house-robber-ii": Q("How does the circle change House Robber?", "Solve twice: without the first house and without the last", "Double the array", "Rob every other house", "No change needed", why="The only new constraint is that the first and last houses can't both be robbed."),
    "longest-palindromic-substring": Q("How many centres do you expand from?", "2n − 1 (each char and each gap)", "n", "n / 2", "1", why="Odd-length palindromes are centred on a character, and even-length ones are centred on a gap."),
    "palindromic-substrings": Q("Each successful expansion step from a centre corresponds to…", "One more palindromic substring", "One palindrome per centre", "A longer palindrome only", "Nothing", why="Count every step, not just the maximum."),
    "decode-ways": Q("Which two-digit groups are valid?", "10 through 26", "01 through 26", "1 through 99", "Any pair", why="A leading zero isn't a valid letter code."),
    "coin-change": Q("Why does greedy (take the largest coin first) fail?", "With coins [1, 3, 4] and amount 6, greedy picks 4 + 1 + 1 but 3 + 3 is better", "Coins can be negative", "It's too slow", "It always works", why="DP checks every option at each amount."),
    "maximum-product-subarray": Q("Why track the minimum product too?", "A negative number turns the minimum into the maximum", "To handle zeros only", "For the empty subarray", "It isn't needed", why="Keep both extremes ending at each index."),
    "word-break": Q("When is dp[i] True?", "Some word ends at i and dp[i − len(word)] is True", "s[:i] is a word", "i is in the word list", "dp[i − 1] is True", why="The prefix before that word must also be breakable."),
    "longest-increasing-subsequence": Q("In the O(n log n) method, what does `tails[k]` store?", "The smallest tail of any increasing subsequence of length k + 1", "The LIS ending at k", "The k-th smallest number", "The actual subsequence", why="Keeping tails small leaves the most room to extend later."),
    # 2-D DP
    "unique-paths": Q("Which recurrence gives the number of paths to cell (r, c)?", "paths(r − 1, c) + paths(r, c − 1)", "r × c", "paths(r − 1, c − 1) + 1", "2^(r + c)", why="You arrive from above or from the left."),
    "longest-common-subsequence": Q("When a[i] == b[j], what is dp[i][j]?", "1 + dp[i + 1][j + 1]", "max(dp[i + 1][j], dp[i][j + 1])", "dp[i + 1][j + 1]", "0", why="Take the shared character and move both pointers."),
    # Greedy
    "maximum-subarray": Q("At each element, Kadane's algorithm chooses between…", "Extending the current subarray or starting fresh at this element", "Adding or skipping the element", "Sorting or not", "The left or right half", why="A negative running sum is never worth keeping."),
    "jump-game": Q("You can't reach the end exactly when…", "Some index i is beyond the farthest reachable index", "There's a 0 anywhere", "The array is odd-length", "nums[0] is small", why="Track `farthest = max(farthest, i + nums[i])`."),
    # Intervals
    "insert-interval": Q("Since the input is already sorted, insertion takes…", "One linear pass: before, overlapping (merge), after", "A sort, then a merge", "Binary search plus shifting", "A heap", why="That takes O(n) time."),
    "merge-intervals": Q("After sorting by start, an interval overlaps the last merged one when…", "start ≤ last merged end", "start < last merged start", "end ≤ last merged end", "They have equal length", why="Touching endpoints count as overlapping here."),
    "non-overlapping-intervals": Q("Which interval should you keep when two overlap?", "The one that ends first", "The longer one", "The one that starts first", "Either one", why="An earlier end leaves the most room for the rest."),
    "meeting-rooms": Q("After sorting by start time, a conflict exists if…", "Any meeting starts before the previous one ends", "Two meetings have the same length", "The first meeting starts at 0", "Meetings aren't sorted by end", why="Only neighbours need checking once sorted."),
    "meeting-rooms-ii": Q("What does the min-heap of end times represent?", "The rooms in use, with the soonest-free room on top", "Meetings sorted by length", "The meetings already finished", "Start times", why="The heap's final size is the peak number of concurrent meetings."),
    # Math & geometry
    "rotate-image": Q("How do you rotate a matrix 90° clockwise in place?", "Transpose, then reverse each row", "Reverse each row only", "Transpose only", "Reverse the list of rows, then transpose twice", why="Check it on a 2×2 example."),
    "spiral-matrix": Q("Why re-check `top <= bottom` before walking the bottom row?", "A single remaining row would otherwise be visited twice", "To handle negative numbers", "Python requires it", "To speed it up", why="The same goes for `left <= right` with a single column."),
    "set-matrix-zeroes": Q("How does the O(1)-space version remember which rows and columns to zero?", "It uses the first row and first column as marker storage", "It uses a set of indices", "It recurses", "It copies the matrix", why="Track row 0 separately, because it doubles as a marker row."),
    # Bit manipulation
    "number-of-1-bits": Q("What does `n & (n - 1)` do?", "Removes the lowest set bit", "Adds one", "Reverses the bits", "Halves n", why="Loop until n is 0, counting the iterations.", code=None),
    "counting-bits": Q("How can ans[i] be computed from an earlier answer?", "ans[i >> 1] + (i & 1)", "ans[i - 1] + 1", "i % 2", "ans[i // 4] × 2", why="i has the same bits as i >> 1, plus its last bit."),
    "reverse-bits": Q("Why loop exactly 32 times instead of 'while n'?", "Leading zeros must become trailing zeros", "To avoid infinite loops", "Python ints are 32-bit", "It's faster", why="Stopping early would drop the low zero bits of the result."),
    "missing-number": Q("What does this print?", "2", "0", "3", "5", why="XOR every index and value: matched pairs cancel, leaving the missing number.",
                         code="nums = [3, 0, 1]\nr = len(nums)\nfor i, x in enumerate(nums):\n    r ^= i ^ x\nprint(r)", predict=True),
    "sum-of-two-integers": Q("In bitwise addition, `(a & b) << 1` is…", "The carry", "The sum without carry", "The difference", "The overflow flag", why="`a ^ b` adds without carrying; repeat until the carry is 0."),
}
