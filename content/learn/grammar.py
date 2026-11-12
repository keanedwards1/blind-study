# "Learn mode" building blocks: for each problem, the Python grammar you could need to write an answer.
#
# Format of each entry:
#   ## Section title        starts a section
#   - **Label:** text       one building block (Markdown; put code in backticks)
#
# scripts/learn.py parses these into sections and fails the build if a problem is missing.
# Everything from collections, heapq, bisect, functools, itertools and math is pre-imported in the editor.

GRAMMAR = {
    # ------------------------------------------------------------------ Arrays & Hashing
    "contains-duplicate": r"""
## Simple version: compare every pair
- **Loop over indices:** `for i in range(len(nums)):` gives you `i = 0, 1, 2, …` up to the last index.
- **Start a loop partway through:** `range(start, stop)`. For example, `range(i + 1, len(nums))` starts one past `i`.
- **Nested loop:** put a second `for` indented inside the first.
- **Access by index:** `nums[i]`, `nums[j]`
- **Compare:** `if nums[i] == nums[j]:` (two equals signs compare; one equals sign assigns)
- **Exit early:** `return True` inside the `if` ends the whole function right away.
- **Fallback:** `return False` goes after both loops, at the function's indentation level, not inside a loop.
- **Indentation is the structure:** each block (`for`, `if`) is indented 4 spaces deeper than the line that opens it.
## Faster version: remember what you've seen
- **Empty set:** `seen = set()` (not `{}`, which makes an empty dict).
- **Membership:** `x in seen` gives `True` or `False`, in O(1).
- **Add:** `seen.add(x)` puts a value in the set.
- **Loop over values directly:** `for x in nums:` gives each value, with no indices.
- **One-liner:** `len(set(nums)) != len(nums)`. A set drops duplicates, so it's shorter exactly when there was one.
""",
    "valid-anagram": r"""
## Quick checks
- **Length:** `len(s)` is the number of characters.
- **Not equal:** `!=`. For example, `if len(s) != len(t): return False`.
## Counting characters with a dict
- **Empty dict:** `counts = {}`
- **Loop over characters:** `for c in s:` gives one character at a time.
- **Read with a default:** `counts.get(c, 0)` gives the stored count, or `0` if `c` isn't a key yet.
- **Add one:** `counts[c] = counts.get(c, 0) + 1`
- **Subtract one (for the other string):** `counts[c] = counts.get(c, 0) - 1`
- **Walk two strings side by side:** `for a, b in zip(s, t):` gives `a` from `s` and `b` from `t` at the same position.
- **All the counts:** `counts.values()`
- **Check every item:** `all(v == 0 for v in counts.values())` is `True` only if every count is zero.
## Shortcuts
- **Counter:** `Counter(s)` builds the count dict in one call (already imported). `Counter(s) == Counter(t)` compares two of them.
- **Sorting:** `sorted(s)` returns the characters as a sorted list, so `sorted(s) == sorted(t)` also works (O(n log n)).
""",
    "two-sum": r"""
## Simple version: try every pair
- **Outer loop:** `for i in range(len(nums)):`
- **Inner loop starting after i:** `for j in range(i + 1, len(nums)):`. Starting at `i + 1` means an element never pairs with itself.
- **Check a pair:** `if nums[i] + nums[j] == target:`
- **Return a list:** `return [i, j]` (square brackets build a list).
## Faster version: a dict from value to index
- **Empty dict:** `index_of = {}`
- **Index and value together:** `for i, n in enumerate(nums):`
- **The partner you need:** `need = target - n`
- **Is it a key?** `need in index_of` gives `True`/`False` in O(1).
- **Look it up:** `index_of[need]` gives the stored index.
- **Store:** `index_of[n] = i`
- **Order matters:** check for the partner first, then store `n`, so a number can't pair with itself.
- **Fallback:** `return []` after the loop, so the function always returns something.
""",
    "group-anagrams": r"""
## Making a key that every anagram shares
- **Sort a string:** `sorted("tea")` gives the list `['a', 'e', 't']`.
- **Glue a list of strings:** `"".join(['a', 'e', 't'])` gives `"aet"`. Together: `"".join(sorted(s))`.
- **Dict keys must be unchangeable:** strings and tuples can be keys, lists can't. `tuple(some_list)` converts.
- **26 counters:** `count = [0] * 26` makes a list of 26 zeros.
- **Letter to index:** `ord(c) - ord('a')` turns `'a'…'z'` into `0…25`, so `count[ord(c) - ord('a')] += 1` counts a letter.
## Grouping
- **Dict of lists:** `groups = defaultdict(list)` (already imported). A missing key starts as an empty list.
- **Add to a group:** `groups[key].append(s)`, with no need to check whether the key exists.
- **Plain-dict alternative:** `groups.setdefault(key, []).append(s)`
- **The answer:** `list(groups.values())` turns all the groups into a list.
""",
    "top-k-frequent-elements": r"""
## Counting
- **Count everything:** `count = Counter(nums)` maps each value to how often it appears.
- **Loop over pairs:** `for value, freq in count.items():`
## Simple version: sort by frequency
- **Sort keys by their counts, biggest first:** `sorted(count, key=count.get, reverse=True)`
- **Take the first k:** the slice `[:k]`.
- **Built-in:** `count.most_common(k)` gives the k most common `(value, freq)` pairs. `[v for v, _ in count.most_common(k)]` keeps just the values.
## Faster version: buckets indexed by frequency
- **A list of separate empty lists:** `buckets = [[] for _ in range(len(nums) + 1)]`. (Don't write `[[]] * n`, which repeats the *same* list n times.)
- **`_` for unused loop variables:** a convention for a variable you never read.
- **Drop into a bucket:** `buckets[freq].append(value)`
- **Count down:** `range(len(buckets) - 1, 0, -1)` goes from the last index down to 1. The third argument is the step.
- **Collect and stop:** `result.append(value)`, then `if len(result) == k: return result`.
""",
    "encode-and-decode-strings": r"""
## Two functions
- **Write both:** `def encode(strs):` and `def decode(s):` are separate functions, each with its own `return`.
## Encoding
- **f-strings:** `f"{len(s)}#{s}"` puts values inside a string. For `"abc"` it gives `"3#abc"`.
- **Glue strings together:** `"".join(parts)` joins a list of strings with nothing between them.
- **Join a generator:** `"".join(f"{len(s)}#{s}" for s in strs)` builds each piece and joins them in one line.
## Decoding
- **Two variables at once:** `result, i = [], 0`
- **A loop where you control the jumps:** `while i < len(s):`
- **Find a character:** `s.index("#", i)` gives the index of the first `#` at or after position `i`.
- **Slice:** `s[i:j]` is the text from `i` up to, but not including, `j`.
- **Text to number:** `int("12")` gives `12`, so `length = int(s[i:j])`.
- **Take exactly length characters:** `s[j + 1 : j + 1 + length]`
- **Jump past them:** `i = j + 1 + length`
""",
    "product-of-array-except-self": r"""
## Setting up
- **Length:** `n = len(nums)`
- **A list of ones:** `answer = [1] * n`
## Left-to-right pass
- **Loop forwards:** `for i in range(n):`
- **Store the running product so far:** `answer[i] = prefix` (start with `prefix = 1`).
- **Multiply in place:** `prefix *= nums[i]` is short for `prefix = prefix * nums[i]`.
## Right-to-left pass
- **Loop backwards:** `range(n - 1, -1, -1)` gives `n-1, n-2, …, 0`. The stop is `-1` because the stop is never included.
- **Same thing, more readable:** `for i in reversed(range(n)):`
- **Multiply into the answer:** `answer[i] *= suffix`, then `suffix *= nums[i]`.
## Note
- **No division needed:** `/` always gives a float in Python and fails on zeros; this approach avoids it.
""",
    "longest-consecutive-sequence": r"""
## Simple version: sort first
- **Sort:** `nums.sort()` sorts in place; `sorted(nums)` returns a new list.
- **Compare with the previous item:** `nums[i] == nums[i - 1] + 1` continues a run; `nums[i] == nums[i - 1]` is a duplicate to skip.
- **Empty input:** `if not nums: return 0` (an empty list counts as false).
## Faster version: a set
- **Set from a list:** `values = set(nums)` drops duplicates and gives O(1) lookups.
- **Not in:** `x - 1 not in values` is the opposite of `in`.
- **Loop over the set:** `for x in values:`
- **Count up a run:** `while x + length in values: length += 1` repeats as long as the condition holds.
- **Keep the best:** `best = max(best, length)`, starting from `best = 0`.
""",
    # ------------------------------------------------------------------ Two Pointers
    "valid-palindrome": r"""
## Simple version: clean, then compare
- **Filter and lowercase:** `cleaned = "".join(c.lower() for c in s if c.isalnum())`
- **Reverse a string:** `cleaned[::-1]` is a reversed copy, so `return cleaned == cleaned[::-1]`.
## Two pointers (no copy)
- **Both ends:** `left, right = 0, len(s) - 1` (the last index is `len - 1`).
- **Until they meet:** `while left < right:`
- **Move inward:** `left += 1`, `right -= 1`
- **Letter or digit?** `c.isalnum()`. `not` flips it: `not s[left].isalnum()` is `True` for spaces and punctuation.
- **Skip junk:** `while left < right and not s[left].isalnum(): left += 1`. `and` stops early, so keep the bound check first.
- **Case-insensitive compare:** `s[left].lower() != s[right].lower()`
- **Exit and fallback:** `return False` on a mismatch; `return True` after the loop.
""",
    "three-sum": r"""
## Sorting
- **Sorted copy:** `nums = sorted(nums)` (or `nums.sort()` to sort in place).
## Outer loop
- **Index and value:** `for i, a in enumerate(nums):`
- **Stop the loop entirely:** `break`. For example, `if a > 0: break`, since everything after is positive too.
- **Skip to the next round:** `continue`. For example, `if i > 0 and a == nums[i - 1]: continue` skips a repeated first value.
- **Why `i > 0` first:** `nums[-1]` is the *last* element in Python, so `nums[i - 1]` at `i = 0` silently reads the end.
## Inner two pointers
- **Set them:** `lo, hi = i + 1, len(nums) - 1`
- **Loop:** `while lo < hi:`
- **Three-way branch:** `if total < 0: … elif total > 0: … else: …` (`elif` means "else if").
- **List of lists:** `result.append([a, nums[lo], nums[hi]])`
- **Skip repeats:** `while lo < hi and nums[lo] == nums[lo - 1]: lo += 1`
""",
    "container-with-most-water": r"""
## Simple version: every pair
- **Nested loops:** `for i in range(n):` and `for j in range(i + 1, n):`
- **Area of a pair:** `min(height[i], height[j]) * (j - i)`. The shorter line caps the water.
## Two pointers
- **Both ends:** `left, right = 0, len(height) - 1`
- **Until they meet:** `while left < right:`
- **Width:** `right - left`
- **Running best:** `best = max(best, area)`, starting from `best = 0`.
- **Move one side:** `if height[left] < height[right]: left += 1` / `else: right -= 1`
""",
    # ------------------------------------------------------------------ Sliding Window
    "best-time-to-buy-and-sell-stock": r"""
## Simple version: every buy/sell pair
- **Sell after buying:** `for i in range(n):` then `for j in range(i + 1, n):`, profit `prices[j] - prices[i]`.
## One pass
- **Infinity as a starting minimum:** `cheapest = float("inf")` is bigger than any price (`inf` is also pre-imported).
- **Loop over values:** `for p in prices:`
- **Running minimum:** `cheapest = min(cheapest, p)`
- **Running best:** `best = max(best, p - cheapest)`
- **Start best at 0:** if prices only fall, you don't trade and the answer is 0.
""",
    "longest-substring-without-repeating-characters": r"""
## Window basics
- **Set two variables to 0:** `left = best = 0` (fine for numbers; don't do this with lists).
- **Right edge and character:** `for right, c in enumerate(s):`
- **Window length:** `right - left + 1`
- **Keep the best:** `best = max(best, right - left + 1)`
## Option A: a set of what's in the window
- **Empty set:** `window = set()`
- **Shrink until c is gone:** `while c in window: window.remove(s[left]); left += 1`
- **Add the new character:** `window.add(c)`
## Option B: a dict of last-seen positions
- **Empty dict:** `last_seen = {}`
- **Jump left past a repeat:** `if c in last_seen and last_seen[c] >= left: left = last_seen[c] + 1`
- **Record the position:** `last_seen[c] = right`
""",
    "longest-repeating-character-replacement": r"""
## Window pieces
- **Several zeros at once:** `left = top = best = 0`
- **Right edge and character:** `for right, c in enumerate(s):`
- **Count in a dict:** `count = {}`, then `count[c] = count.get(c, 0) + 1`.
- **Most common so far:** `top = max(top, count[c])`. Or `max(count.values())` gives it directly (at most 26 keys, so it's cheap).
- **Window length:** `right - left + 1`
- **Replacements needed:** `(right - left + 1) - top`
## Shrinking
- **Shrink while too many:** `while (right - left + 1) - top > k:`
- **Drop the left character:** `count[s[left]] -= 1`, then `left += 1`.
- **Record:** `best = max(best, right - left + 1)`
""",
    "minimum-window-substring": r"""
## What you still need
- **Count the target:** `need = Counter(t)`. A Counter returns 0 for a missing key, so `need[c]` never raises a KeyError (a plain dict would).
- **Characters still missing:** `missing = len(t)`
## Growing the window
- **Right edge:** `for right, c in enumerate(s):`
- **Did this character help?** `if need[c] > 0: missing -= 1`
- **Use it up:** `need[c] -= 1` (it can go negative, which just means extras).
## Shrinking while valid
- **Loop while the window has everything:** `while missing == 0:`
- **Record the best as a tuple:** `best = (right - left + 1, left, right + 1)`. Read parts with `best[0]`, `best[1]`, `best[2]`.
- **Start best as "nothing yet":** `best = (float("inf"), 0, 0)`
- **Give back the left character:** `need[s[left]] += 1`, then `if need[s[left]] > 0: missing += 1`, then `left += 1`.
## Returning
- **One-line if/else:** `"" if best[0] == float("inf") else s[best[1]:best[2]]`
""",
    # ------------------------------------------------------------------ Stack
    "valid-parentheses": r"""
## A list as a stack
- **Empty stack:** `stack = []`
- **Push:** `stack.append(c)`
- **Pop:** `stack.pop()` removes and returns the last item.
- **Peek:** `stack[-1]` reads the last item without removing it.
- **Is it empty?** `not stack` is `True` for an empty list.
## Matching brackets
- **Closer to opener:** `pairs = {")": "(", "]": "[", "}": "{"}`
- **Is it a closer?** `c in pairs` checks the dict's keys.
- **Mismatch check:** `if not stack or stack[-1] != pairs[c]: return False`. `or` stops early, so `stack[-1]` is never read on an empty stack.
- **Openers:** an `else:` branch pushes them.
- **Final answer:** `return not stack`. Every opener must have been closed.
""",
    # ------------------------------------------------------------------ Binary Search
    "find-minimum-in-rotated-sorted-array": r"""
## Simple version
- **Built-in:** `min(nums)` works, but it's O(n); the problem wants O(log n).
## Binary search
- **Bounds:** `lo, hi = 0, len(nums) - 1`
- **Loop until they meet:** `while lo < hi:`
- **Middle index:** `mid = (lo + hi) // 2`. `//` is floor division and gives an int; `/` gives a float, which can't be an index.
- **Compare with the right end:** `if nums[mid] > nums[hi]: lo = mid + 1` / `else: hi = mid`
- **Answer:** `return nums[lo]`
""",
    "search-in-rotated-sorted-array": r"""
## Binary search
- **Bounds:** `lo, hi = 0, len(nums) - 1`
- **Inclusive loop:** `while lo <= hi:` (`<=` so a one-element range still gets checked).
- **Middle:** `mid = (lo + hi) // 2`
- **Found it:** `if nums[mid] == target: return mid`
## Which half is sorted?
- **Left half sorted:** `if nums[lo] <= nums[mid]:`
- **Chained comparison:** `nums[lo] <= target < nums[mid]` means both `nums[lo] <= target` and `target < nums[mid]`.
- **Nested if/else:** an `if`/`else` inside each branch of the outer `if`/`else`.
- **Narrow:** `hi = mid - 1` or `lo = mid + 1`
- **Not found:** `return -1` after the loop.
""",
    # ------------------------------------------------------------------ Linked List
    "reverse-linked-list": r"""
## Linked-list basics
- **Fields:** `node.val` is the value, `node.next` is the next node, and `None` marks the end.
- **Walk until the end:** `while cur:` stops once `cur` is `None`.
## Iterative reversal
- **Start:** `prev = None`, `cur = head`
- **Save the rest first:** `nxt = cur.next`
- **Point backwards:** `cur.next = prev`
- **Step forward:** `prev = cur`, then `cur = nxt`.
- **New head:** `return prev`
- **All at once:** `cur.next, prev, cur = prev, cur, cur.next`. The whole right side is evaluated before anything is assigned.
## Recursive version
- **Base case:** `if not head or not head.next: return head`
- **Recurse:** `new_head = reverse_list(head.next)`
- **Flip one link:** `head.next.next = head`, then `head.next = None`, then `return new_head`.
""",
    "merge-two-sorted-lists": r"""
## Dummy head
- **Two names, one new node:** `dummy = tail = ListNode()`. You build after `tail` and return `dummy.next`.
## Merging
- **While both have nodes:** `while list1 and list2:`
- **Compare values:** `if list1.val <= list2.val:`
- **Attach and advance:** `tail.next = list1`, then `list1 = list1.next`.
- **Move the tail:** `tail = tail.next`
- **Attach whatever's left:** `tail.next = list1 or list2`. `or` gives the first value that isn't `None`.
- **Answer:** `return dummy.next`
""",
    "reorder-list": r"""
## Modify in place
- **Returns nothing:** the signature says `-> None`. Change the links and don't return the list.
## Simple version: a list of nodes
- **Collect:** `nodes = []`, then `while cur: nodes.append(cur); cur = cur.next`.
- **Two indices from both ends:** `i, j = 0, len(nodes) - 1` and `while i < j:`
- **Relink:** `nodes[i].next = nodes[j]`, then move `i`, then `nodes[j].next = nodes[i]`, and so on.
- **End the list:** set the last node's `.next = None`, or the list loops forever.
## O(1) space: middle, reverse, weave
- **Find the middle:** `slow, fast = head, head.next`, then `while fast and fast.next: slow, fast = slow.next, fast.next.next`.
- **Cut:** `second = slow.next`, then `slow.next = None`.
- **Reverse the second half:** the `prev`/`cur` loop from Reverse Linked List.
- **Weave:** save both nexts first, `n1, n2 = first.next, second.next`, then `first.next = second`, `second.next = n1`, `first, second = n1, n2`.
""",
    "remove-nth-node-from-end-of-list": r"""
## Simple version: two passes
- **Count the nodes:** `length = 0`, then `while cur: length += 1; cur = cur.next`.
- **Walk to the node before the target:** `length - n` steps from a dummy node.
## One pass with a gap
- **Dummy before the head:** `dummy = ListNode(0, head)`. Removing the head is then no special case.
- **Two pointers:** `slow = fast = dummy`
- **Repeat n times:** `for _ in range(n): fast = fast.next`
- **Move both until fast is last:** `while fast.next: slow, fast = slow.next, fast.next`
- **Skip a node:** `slow.next = slow.next.next`
- **Answer:** `return dummy.next`
""",
    "linked-list-cycle": r"""
## Simple version: remember nodes
- **Nodes can go in a set:** `seen = set()`, then `if node in seen: return True` and `seen.add(node)`.
- **Walk:** `node = node.next` inside `while node:`
## O(1) space: slow and fast
- **Both start at the head:** `slow = fast = head`
- **Safe loop condition:** `while fast and fast.next:`. Both checks are needed before reading `fast.next.next`.
- **Steps:** `slow = slow.next`, `fast = fast.next.next`
- **Same node?** `if slow is fast: return True`. `is` checks for the same object, not equal values.
- **No cycle:** `return False` after the loop.
""",
    "merge-k-sorted-lists": r"""
## Simple version: collect and sort
- **Every value:** walk each list and `values.append(node.val)`.
- **Sort:** `values.sort()`
- **Build a new list:** `tail.next = ListNode(v)`, then `tail = tail.next`.
## Heap version (heapq is pre-imported)
- **Push:** `heappush(heap, item)`. **Pop the smallest:** `heappop(heap)`. **Peek:** `heap[0]`.
- **Heapify a list in place:** `heapify(heap)`
- **Tuples compare item by item:** push `(node.val, i, node)`. The index `i` breaks ties, so two `ListNode`s are never compared (that raises a TypeError).
- **Build with a filter:** `[(node.val, i, node) for i, node in enumerate(lists) if node]` skips empty lists.
- **Unpack and ignore:** `_, i, node = heappop(heap)`
- **Refill from the same list:** `if node.next: heappush(heap, (node.next.val, i, node.next))`
- **Dummy head:** `dummy = tail = ListNode()`, then `return dummy.next`.
""",
    # ------------------------------------------------------------------ Trees
    "invert-binary-tree": r"""
## Tree basics
- **Fields:** `root.val`, `root.left`, `root.right`. A missing child is `None`.
- **Recursion:** the function calls itself on `root.left` and `root.right`.
- **Base case:** `if not root: return None` handles the empty tree and stops the recursion.
## Swapping
- **Swap without a temp variable:** `root.left, root.right = root.right, root.left`
- **Recurse on both:** `invert_tree(root.left)` and `invert_tree(root.right)`
- **Return the node:** `return root`
- **All in one line:** `root.left, root.right = invert_tree(root.right), invert_tree(root.left)`
""",
    "maximum-depth-of-binary-tree": r"""
## Recursive
- **Base case:** `if not root: return 0`
- **Bigger of two:** `max(a, b)`
- **Recurrence:** `return 1 + max(max_depth(root.left), max_depth(root.right))`
## Level by level (BFS)
- **Queue:** `queue = deque([root])` (pre-imported). `queue.popleft()` removes from the front.
- **One level per round:** `for _ in range(len(queue)):`, and add 1 to the depth after each round.
""",
    "same-tree": r"""
## Base cases
- **Both empty:** `if not p and not q: return True`
- **Only one empty:** `if not p or not q: return False`
- **Compact version:** `if not p or not q: return p is q`. `p is q` is `True` only when both are `None`.
- **Different values:** `if p.val != q.val: return False`
## Recursion
- **Chain with `and`:** `return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)`. `and` stops at the first `False`.
""",
    "subtree-of-another-tree": r"""
## A helper function
- **Nested def:** write `def same(a, b):` inside `is_subtree`. It's the Same Tree check.
- **Its base case:** `if not a or not b: return a is b`
## Main function
- **Empty sub_root is always a subtree:** `if not sub_root: return True`
- **Ran out of tree:** `if not root: return False`
- **Try here, then left, then right:** `return same(root, sub_root) or is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)`. `or` stops at the first `True`.
""",
    "lowest-common-ancestor-of-a-binary-search-tree": r"""
## Inputs are nodes
- **Compare values:** `p` and `q` are `TreeNode` objects, so use `p.val` and `q.val`.
- **Return a node:** return the `TreeNode` itself, not its `.val`.
## Walking down
- **Start:** `node = root`, then `while node:`
- **Both smaller:** `if p.val < node.val and q.val < node.val: node = node.left`
- **Both bigger:** `elif p.val > node.val and q.val > node.val: node = node.right`
- **They split (or one is here):** `else: return node`
## Recursive alternative
- **Same branches:** `return lowest_common_ancestor(root.left, p, q)` in the "both smaller" case, and so on.
""",
    "binary-tree-level-order-traversal": r"""
## Queue
- **Empty tree:** `if not root: return []`
- **Start the queue:** `queue = deque([root])` (pre-imported).
- **Take from the front:** `queue.popleft()` is O(1). (`list.pop(0)` works but is O(n).)
- **Add to the back:** `queue.append(node.left)`
- **Only real children:** `if node.left:` and `if node.right:` before appending.
## One level at a time
- **Outer loop:** `while queue:`
- **Exactly this level's nodes:** `for _ in range(len(queue)):`. `range` reads the length once, before new children are added.
- **Collect the level:** `level = []`, `level.append(node.val)`, then `result.append(level)` after the inner loop.
""",
    "validate-binary-search-tree": r"""
## Recursion with bounds
- **Helper with extra arguments:** `def valid(node, low, high):`
- **Empty is valid:** `if not node: return True`
- **Chained comparison:** `low < node.val < high`. Use `if not (low < node.val < high): return False`.
- **Tighten the bounds:** `return valid(node.left, low, node.val) and valid(node.right, node.val, high)`
- **Infinite starting bounds:** `return valid(root, float("-inf"), float("inf"))`
## Alternative: in-order values
- **In-order visits a BST in sorted order:** collect values left, node, right.
- **Strictly increasing?** `all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))`
""",
    "kth-smallest-element-in-a-bst": r"""
## Simple version: in-order into a list
- **Helper:** `def inorder(node):`, with `if not node: return` (a bare `return` just stops).
- **Left, node, right:** `inorder(node.left)`, then `vals.append(node.val)`, then `inorder(node.right)`.
- **Appending to an outer list:** works inside the helper without any extra keyword.
- **k is 1-based:** `return vals[k - 1]`
## Iterative, stopping early
- **Start:** `stack, node = [], root`
- **Loop:** `while stack or node:`
- **Go left as far as possible:** `while node: stack.append(node); node = node.left`
- **Visit:** `node = stack.pop()`, then `k -= 1` and `if k == 0: return node.val`.
- **Then go right:** `node = node.right`
""",
    "construct-binary-tree-from-preorder-and-inorder-traversal": r"""
## Pieces
- **New node:** `node = TreeNode(val)`, then set `node.left = …` and `node.right = …`.
- **The root:** `preorder[0]`
- **Find a position:** `inorder.index(val)` (O(n)), or build a dict once.
- **Dict comprehension:** `pos = {v: i for i, v in enumerate(inorder)}` maps value to index.
## Simple version: slicing
- **Split inorder:** `inorder[:mid]` (left) and `inorder[mid + 1:]` (right).
- **Split preorder:** `preorder[1:mid + 1]` (left) and `preorder[mid + 1:]` (right).
- **Empty input:** `if not preorder: return None`
## Faster version: indices and an iterator
- **Iterator:** `it = iter(preorder)`. Each `next(it)` gives the next value.
- **Helper over an inorder range:** `def build(lo, hi):`, with `if lo > hi: return None`.
- **Build left before right:** that's the order preorder lists them in.
""",
    "binary-tree-maximum-path-sum": r"""
## Updating an outer variable from a helper
- **Start very low:** `best = float("-inf")`, since values can be negative.
- **Nested helper:** `def down(node):`
- **`nonlocal best`:** the first line of the helper. It lets you reassign `best`; without it, `best = …` makes a new local variable and raises `UnboundLocalError`.
- **Alternative:** `best = [float("-inf")]` and update `best[0]`. Changing a list's item doesn't need `nonlocal`.
## The helper's logic
- **Empty node:** `if not node: return 0`
- **Ignore negative branches:** `left = max(down(node.left), 0)`
- **Path through this node:** `best = max(best, node.val + left + right)`
- **Return one branch only:** `return node.val + max(left, right)`
## Calling it
- **Run, then answer:** `down(root)`, then `return best`.
""",
    "serialize-and-deserialize-binary-tree": r"""
## Classes
- **Methods take self first:** `def serialize(self, root):`. You call it as `codec.serialize(root)`.
## Serializing
- **Collect tokens:** `out = []`, with `out.append("N")` for `None`.
- **Number to text:** `str(node.val)`
- **Recursive helper:** `def dfs(node):`, with a bare `return` after appending `"N"`.
- **Preorder:** append the value, then `dfs(node.left)`, then `dfs(node.right)`.
- **One string:** `",".join(out)`
## Deserializing
- **Back to a list:** `data.split(",")`
- **One token at a time:** `tokens = iter(data.split(","))`, then `tok = next(tokens)`.
- **Text to number:** `int(tok)`
- **Build in the same order:** `node = TreeNode(int(tok))`, then `node.left = build()`, then `node.right = build()`.
""",
    # ------------------------------------------------------------------ Tries
    "implement-trie-prefix-tree": r"""
## Classes
- **Constructor:** `def __init__(self):`, with `self.root = {}`. Anything stored on `self` is kept between method calls.
- **Methods that return nothing:** `-> None`, so no `return` value.
- **Private helper method:** `def _walk(self, s):`, called as `self._walk(word)`.
## Nested dicts as nodes
- **Each key is a character, each value is the child dict:** `{"a": {"p": {...}}}`
- **Child, created if missing:** `node = node.setdefault(c, {})`
- **Mark the end of a word:** `node["$"] = True` (`"$"` is never a letter).
- **Missing letter:** `if c not in node: return None`, otherwise `node = node[c]`.
- **Word or just a prefix?** `"$" in node`
- **Check for a node:** `node is not None`
## Class-based alternative
- **Node class:** `class TrieNode:` with `self.children = {}` and `self.end = False` in its `__init__`.
""",
    "design-add-and-search-words-data-structure": r"""
## Adding
- **Same as a trie:** `node = node.setdefault(c, {})` for each letter, then `node["$"] = True`.
## Searching with wildcards
- **Recursive helper inside the method:** `def dfs(node, i):`. It can read `word` from the outer method.
- **End of the word:** `if i == len(word): return "$" in node`
- **Current letter:** `c = word[i]`
- **Wildcard:** `if c == ".":`
- **All children:** `node.items()` gives `(key, child)` pairs. Skip the marker with `if key != "$"`.
- **Any branch works:** `any(dfs(child, i + 1) for key, child in node.items() if key != "$")`
- **Normal letter:** `return c in node and dfs(node[c], i + 1)`
- **Start:** `return dfs(self.root, 0)`
""",
    "word-search-ii": r"""
## Build a trie of the words
- **Nested dicts:** `node = node.setdefault(c, {})` for each letter.
- **Store the word at its end:** `node["$"] = w`, so you know which word you found.
## Grid basics
- **Size:** `rows, cols = len(board), len(board[0])`
- **A cell:** `board[r][c]`
- **Every cell:** `for r in range(rows):` with `for c in range(cols):` inside.
- **Four directions:** `for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):`, then `nr, nc = r + dr, c + dc`.
- **In bounds?** `0 <= nr < rows and 0 <= nc < cols`
## DFS with marking
- **Mark visited:** `board[r][c] = "#"`, and restore with `board[r][c] = ch` afterwards.
- **Found a word:** `found.append(node.pop("$"))`. `pop` removes it, so each word is found once.
- **Prune empty branches:** `if not node: parent.pop(ch)` (an empty dict counts as false).
""",
    # ------------------------------------------------------------------ Heap / Priority Queue
    "find-median-from-data-stream": r"""
## Classes
- **State on self:** `self.low = []` and `self.high = []` in `__init__`. They persist between calls.
## Simple version: keep a sorted list
- **Insert in sorted position:** `insort(self.nums, num)` (bisect is pre-imported).
- **Middle by index:** `n = len(self.nums)`, then `self.nums[n // 2]`, or the average of `self.nums[n // 2 - 1]` and `self.nums[n // 2]` when `n` is even.
## Two heaps (heapq is pre-imported)
- **Push / pop smallest / peek:** `heappush(h, x)`, `heappop(h)`, `h[0]`
- **Max-heap trick:** heapq only does min-heaps, so push `-num` and negate when you read: `-self.low[0]`.
- **Move the top of one heap to the other:** `heappush(self.high, -heappop(self.low))`
- **Balance by size:** `if len(self.high) > len(self.low):`
- **Average:** `(a + b) / 2`. `/` always gives a float. `float(x)` converts an int.
""",
    # ------------------------------------------------------------------ Backtracking
    "combination-sum": r"""
## Setup
- **Results and the current path:** `result, path = [], []`
- **Recursive helper:** `def backtrack(start, remaining):`
- **Outer lists in a helper:** you can `append`/`pop` them without `nonlocal`, because you change them rather than reassign them.
## The helper
- **Found one:** `if remaining == 0: result.append(path[:]); return`
- **Copy the path:** `path[:]` (or `list(path)`). Appending `path` itself stores a reference that keeps changing.
- **Choices from start onwards:** `for i in range(start, len(candidates)):`. This avoids the same combination in a different order.
- **Prune:** `if candidates[i] <= remaining:`
- **Choose, explore, undo:** `path.append(candidates[i])`, then `backtrack(i, remaining - candidates[i])`, then `path.pop()`.
- **Why `i`, not `i + 1`:** the same number can be reused.
## Start it
- **Call, then answer:** `backtrack(0, target)`, then `return result`.
""",
    "word-search": r"""
## Grid basics
- **Size:** `rows, cols = len(board), len(board[0])`
- **Out of bounds?** `not (0 <= r < rows and 0 <= c < cols)`
## Recursive helper
- **Arguments:** `def dfs(r, c, i):`, where `i` is how many letters are matched so far.
- **Matched the whole word:** `if i == len(word): return True`
- **Wrong cell:** `if not (…in bounds…) or board[r][c] != word[i]: return False`
- **Mark visited (two assignments at once):** `saved, board[r][c] = board[r][c], "#"`
- **Try four directions:** `dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or …`. `or` stops at the first `True`.
- **Restore before returning:** `board[r][c] = saved`
## Start from every cell
- **Two `for`s in one expression:** `any(dfs(r, c, 0) for r in range(rows) for c in range(cols))` works like a nested loop.
""",
    # ------------------------------------------------------------------ Graphs
    "number-of-islands": r"""
## Grid basics
- **Cells are strings:** compare with `grid[r][c] == "1"`, not `== 1`.
- **Size:** `rows, cols = len(grid), len(grid[0])`
- **Every cell:** `for r in range(rows):` with `for c in range(cols):` inside.
- **Count:** `count += 1` for each new island.
## Flood fill with a stack
- **Stack of tuples:** `stack = [(r, c)]`, then `i, j = stack.pop()` unpacks one.
- **Sink to mark visited:** `grid[r][c] = "0"`
- **Neighbours:** `for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):`
- **Valid land neighbour:** `if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == "1":`
## Recursive alternative
- **Helper:** `def sink(r, c):` that returns if out of bounds or not `"1"`, sets the cell to `"0"`, and calls itself on the four neighbours.
""",
    "clone-graph": r"""
## Node basics
- **New node:** `Node(n.val)`
- **Neighbours:** `n.neighbors` is a list of `Node`s (note the US spelling).
## Remember copies
- **Original to copy:** `copies = {}`. Nodes can be dict keys.
- **Already copied:** `if n in copies: return copies[n]`. This is what stops cycles.
- **Store before recursing:** `copies[n] = copy`, then fill in neighbours.
- **List comprehension:** `copy.neighbors = [clone(nb) for nb in n.neighbors]`
## Empty input
- **One-line if/else:** `return clone(node) if node else None`
""",
    "pacific-atlantic-water-flow": r"""
## Sets of cells
- **Tuples as cells:** `(r, c)`. Tuples can go in sets; lists can't.
- **Start a set from a list:** `seen = set(starts)`
- **Add a cell:** `seen.add((nr, nc))`. The double brackets are the call plus the tuple.
- **Not visited yet:** `(nr, nc) not in seen`
## Start cells along the edges
- **Comprehensions:** `[(0, c) for c in range(cols)]` is the top row.
- **Join two lists:** `+`, as in `[(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]`
## Search (DFS with a stack)
- **Copy the starts to a stack:** `stack = list(starts)`
- **Walk uphill from the ocean:** `heights[nr][nc] >= heights[r][c]`
## Combining
- **Cells in both sets:** `pacific & atlantic` (set intersection).
- **Sorted list of lists:** `[[r, c] for r, c in sorted(pacific & atlantic)]`
""",
    "course-schedule": r"""
## Building the graph
- **Adjacency list:** `graph = [[] for _ in range(num_courses)]`
- **Counts:** `indegree = [0] * num_courses`
- **Unpack each pair:** `for course, pre in prerequisites:`
- **Add an edge:** `graph[pre].append(course)`, then `indegree[course] += 1`.
## Topological order (Kahn's algorithm)
- **Queue of courses with no prerequisites:** `queue = deque(i for i in range(num_courses) if indegree[i] == 0)`
- **Take one:** `cur = queue.popleft()`, then `taken += 1`.
- **Unlock what it leads to:** `for nxt in graph[cur]: indegree[nxt] -= 1`, and `if indegree[nxt] == 0: queue.append(nxt)`.
- **Return a comparison directly:** `return taken == num_courses`
## DFS alternative
- **States per course:** `state = [0] * num_courses` (0 = new, 1 = in progress, 2 = done). Seeing a 1 again means a cycle.
""",
    "graph-valid-tree": r"""
## Quick check
- **A tree has exactly n − 1 edges:** `if len(edges) != n - 1: return False`
## Union-find
- **Everyone is their own parent:** `parent = list(range(n))` gives `[0, 1, …, n-1]`.
- **Find the root:** `def find(x):` with `while parent[x] != x: x = parent[x]`, then `return x`.
- **Path compression (optional speed-up):** `parent[x] = parent[parent[x]]` inside that loop.
- **Changing a list from a helper:** `parent[...] = …` works without `nonlocal`.
- **Unpack each edge:** `for a, b in edges:`
- **Two finds at once:** `ra, rb = find(a), find(b)`
- **Same root means a cycle:** `if ra == rb: return False`
- **Union:** `parent[ra] = rb`
## DFS alternative
- **Undirected adjacency:** `graph = defaultdict(list)`, with both `graph[a].append(b)` and `graph[b].append(a)`.
- **Everything reached?** `len(seen) == n`
""",
    "number-of-connected-components-in-an-undirected-graph": r"""
## Union-find
- **Start:** `parent = list(range(n))`, `components = n`
- **Find:** `def find(x):` with `while parent[x] != x: x = parent[x]`, then `return x`.
- **Each edge:** `for a, b in edges:`, then `ra, rb = find(a), find(b)`.
- **Merge two groups:** `if ra != rb: parent[ra] = rb; components -= 1`
## DFS alternative
- **Undirected adjacency:** `graph = defaultdict(list)`, adding each edge both ways.
- **Visited set:** `seen = set()`
- **Count starts:** `for node in range(n): if node not in seen:`, add 1 and explore everything reachable.
""",
    # ------------------------------------------------------------------ Advanced Graphs
    "alien-dictionary": r"""
## Every letter
- **Dict comprehension over two loops:** `graph = {c: set() for w in words for c in w}` creates a key for every letter that appears.
- **Loop over a dict's keys:** `indegree = {c: 0 for c in graph}`
## Comparing neighbouring words
- **Adjacent pairs:** `for a, b in zip(words, words[1:]):` gives `(words[0], words[1])`, `(words[1], words[2])`, …
- **Letter by letter:** `for x, y in zip(a, b):`. It stops at the shorter word.
- **First difference:** `if x != y:`, add the edge, then `break`.
- **Don't double-count:** `if y not in graph[x]: graph[x].add(y); indegree[y] += 1`
- **`for … else`:** the `else:` block runs only if the loop finished *without* `break`. Here that means one word is a prefix of the other, and `if len(a) > len(b): return ""`.
## Topological order
- **Start queue:** `deque(sorted(c for c in indegree if indegree[c] == 0))`. `sorted` gives a predictable order.
- **Process:** `c = queue.popleft()`, `order.append(c)`, then lower each neighbour's indegree.
- **Cycle check and answer:** `return "".join(order) if len(order) == len(graph) else ""`
""",
    # ------------------------------------------------------------------ 1-D Dynamic Programming
    "climbing-stairs": r"""
## List version
- **Table:** `dp = [0] * (n + 1)`
- **Base cases:** `dp[0] = dp[1] = 1`
- **Fill:** `for i in range(2, n + 1): dp[i] = dp[i - 1] + dp[i - 2]`
- **Answer:** `return dp[n]`
## Two variables
- **Start:** `a, b = 1, 1`
- **Repeat n times:** `for _ in range(n):`
- **Shift forward:** `a, b = b, a + b`. The right side is computed first, so no temp variable is needed.
- **Answer:** `return a`
## Memoized recursion
- **Cache a helper:** put `@cache` on the line above `def ways(i):` (pre-imported). Repeated calls return the stored result.
""",
    "house-robber": r"""
## List version
- **Table:** `dp = [0] * (len(nums) + 1)`, where `dp[i]` is the best from the first `i` houses.
- **Rob or skip:** `dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])`
## Two variables
- **Start:** `prev2 = prev1 = 0`
- **Loop over values:** `for x in nums:`
- **Shift forward:** `prev2, prev1 = prev1, max(prev1, prev2 + x)`
- **Answer:** `return prev1`
""",
    "house-robber-ii": r"""
## Reuse a helper
- **Nested def:** `def line(houses):` holds the House Robber logic for a straight row.
- **Two variables inside:** `prev2 = prev1 = 0`, then `prev2, prev1 = prev1, max(prev1, prev2 + x)`.
## Breaking the circle
- **All but the last:** `nums[:-1]`
- **All but the first:** `nums[1:]`
- **One house:** `if len(nums) == 1: return nums[0]`
- **Best of both:** `return max(line(nums[:-1]), line(nums[1:]))`
""",
    "longest-palindromic-substring": r"""
## Simple version: check every substring
- **Every start and end:** `for i in range(n):` and `for j in range(i + 1, n + 1):`
- **Is it a palindrome?** `sub = s[i:j]`, then `sub == sub[::-1]`.
- **Keep the longest:** `if len(sub) > len(best): best = sub`
## Expand around centres
- **Each centre:** `for center in range(len(s)):`
- **Odd and even in one loop:** `for lo, hi in ((center, center), (center, center + 1)):`
- **Expand:** `while lo >= 0 and hi < len(s) and s[lo] == s[hi]: lo -= 1; hi += 1`. Keep the bounds checks first.
- **After the loop:** the palindrome is `s[lo + 1:hi]`, with length `hi - lo - 1`.
- **Track it:** `start, end = lo + 1, hi` when it's longer, then `return s[start:end]`.
""",
    "palindromic-substrings": r"""
## Expand around centres
- **Counter:** `count = 0`
- **Each centre:** `for center in range(len(s)):`
- **Odd and even in one loop:** `for lo, hi in ((center, center), (center, center + 1)):`
- **Expand and count:** `while lo >= 0 and hi < len(s) and s[lo] == s[hi]:`, then `count += 1`, `lo -= 1`, `hi += 1`.
- **Answer:** `return count`
## Simple version
- **Every substring:** two loops over `i` and `j`, adding 1 when `s[i:j] == s[i:j][::-1]`.
""",
    "decode-ways": r"""
## Characters are strings
- **Single digit valid?** `s[i - 1] != "0"`. Compare with `"0"`, not `0`.
- **Two digits as a number:** `int(s[i - 2 : i])`
- **In range:** `10 <= value <= 26` (chained comparison).
## List version
- **Table:** `dp = [0] * (len(s) + 1)`, with `dp[0] = 1` (one way to decode nothing).
- **Fill:** `for i in range(1, len(s) + 1):`. Add `dp[i - 1]` if the single digit is valid, and `dp[i - 2]` if `i >= 2` and the two digits are.
- **Answer:** `return dp[len(s)]`
## Two variables
- **One-line if/else in a start value:** `prev2, prev1 = 1, 1 if s[0] != "0" else 0`
- **Loop from 2:** `for i in range(2, len(s) + 1):`, with `cur = 0`, then `cur += prev1` / `cur += prev2`.
- **Shift forward:** `prev2, prev1 = prev1, cur`
""",
    "coin-change": r"""
## Table
- **Join lists:** `dp = [0] + [amount + 1] * amount`. Index 0 is 0, and every other amount starts as "too many coins".
- **Or use infinity:** `[float("inf")] * (amount + 1)`, with `dp[0] = 0`.
## Filling
- **Every amount:** `for a in range(1, amount + 1):`
- **Every coin:** `for c in coins:`
- **Only if it fits:** `if c <= a:`, so `a - c` never goes negative.
- **Better with this coin?** `dp[a] = min(dp[a], dp[a - c] + 1)`
## Answer
- **Impossible becomes -1:** `return dp[amount] if dp[amount] <= amount else -1`
""",
    "maximum-product-subarray": r"""
## Running values
- **Chain assignment:** `best = hi = lo = nums[0]`
- **Skip the first element:** `for x in nums[1:]:`
- **Three candidates:** `candidates = (x, hi * x, lo * x)` (a tuple).
- **Max and min of them:** `max(candidates)`, `min(candidates)`
- **Update both together:** `hi, lo = max(candidates), min(candidates)`. Both use the *old* values.
- **Running best:** `best = max(best, hi)`
## Why track the minimum
- **Negatives flip signs:** the smallest product times a negative can become the largest.
""",
    "word-break": r"""
## Lookups
- **Set of words:** `words = set(word_dict)`
- **Set comprehension:** `lengths = {len(w) for w in words}`
## Table
- **Join lists:** `dp = [True] + [False] * len(s)`. `dp[i]` means "the first `i` characters can be split".
- **Fill:** `for i in range(1, len(s) + 1):`
- **Last L characters before i:** `s[i - L : i]`
- **Any length works:** `dp[i] = any(L <= i and dp[i - L] and s[i - L : i] in words for L in lengths)`
- **Last item:** `return dp[-1]`
## Alternatives
- **Prefix test:** `s.startswith(w, i)` checks whether `w` appears at position `i`.
- **Memoized recursion:** `@cache` on `def can(i):`, trying each word that starts at `i`.
""",
    "longest-increasing-subsequence": r"""
## Simple version: O(n²) table
- **Table of ones:** `dp = [1] * len(nums)`
- **Every earlier element:** `for i in range(len(nums)):` then `for j in range(i):`
- **Extend if smaller:** `if nums[j] < nums[i]: dp[i] = max(dp[i], dp[j] + 1)`
- **Biggest entry:** `return max(dp)`
## Faster version: binary search
- **Sorted list of tails:** `tails = []`
- **Where x would go:** `i = bisect_left(tails, x)` (pre-imported) gives the index that keeps `tails` sorted.
- **Append or replace:** `if i == len(tails): tails.append(x)`, else `tails[i] = x`.
- **Answer:** `return len(tails)`
""",
    # ------------------------------------------------------------------ 2-D Dynamic Programming
    "unique-paths": r"""
## 2-D table
- **Grid of ones:** `dp = [[1] * n for _ in range(m)]` makes `m` separate rows. (`[[1] * n] * m` repeats one row m times.)
- **Cell:** `dp[r][c]`
- **Loops from 1:** `for r in range(1, m):` with `for c in range(1, n):` inside.
- **From above plus from the left:** `dp[r][c] = dp[r - 1][c] + dp[r][c - 1]`
- **Bottom-right:** `return dp[-1][-1]`
## One row
- **Row of ones:** `row = [1] * n`, then `row[c] += row[c - 1]` for each later row.
## Maths
- **Combinations:** `math.comb(m + n - 2, m - 1)`
""",
    "longest-common-subsequence": r"""
## 2-D table
- **Extra row and column of zeros:** `dp = [[0] * (n + 1) for _ in range(m + 1)]`, where `m, n = len(text1), len(text2)`.
- **Loops from 1:** `for i in range(1, m + 1):` with `for j in range(1, n + 1):` inside.
- **Offset by one:** compare `text1[i - 1] == text2[j - 1]`, because `dp` has the extra row and column.
- **Match:** `dp[i][j] = dp[i - 1][j - 1] + 1`
- **No match:** `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`
- **One-line if/else:** `dp[i][j] = dp[i - 1][j - 1] + 1 if a == b else max(dp[i - 1][j], dp[i][j - 1])`
- **Answer:** `return dp[m][n]`
## Two rows
- **Keep only the previous row:** `prev` and `cur` lists, then `prev = cur` after each row.
""",
    # ------------------------------------------------------------------ Greedy
    "maximum-subarray": r"""
## Simple version
- **Every start and end:** `for i in range(n):` with a running `total += nums[j]` for `j` from `i` on.
## Kadane's algorithm
- **Start from the first element:** `best = cur = nums[0]`. Not 0, because every number could be negative.
- **Skip the first element:** `for x in nums[1:]:`
- **Extend or start fresh:** `cur = max(x, cur + x)`
- **Running best:** `best = max(best, cur)`
""",
    "jump-game": r"""
## Furthest reach
- **Start:** `farthest = 0`
- **Index and value:** `for i, step in enumerate(nums):`
- **Stuck:** `if i > farthest: return False`
- **Extend:** `farthest = max(farthest, i + step)`
- **Made it:** `return True`
## Backwards alternative
- **Goal post:** `goal = len(nums) - 1`
- **Loop backwards:** `for i in range(len(nums) - 1, -1, -1):`
- **Move the goal:** `if i + nums[i] >= goal: goal = i`
- **Answer:** `return goal == 0`
""",
    # ------------------------------------------------------------------ Intervals
    "insert-interval": r"""
## Pieces of an interval
- **Unpack:** `start, end = new_interval`
- **Start and end by index:** `intervals[i][0]`, `intervals[i][1]`
## Three phases with one index
- **Index and length:** `i, n = 0, len(intervals)`
- **Before the new one:** `while i < n and intervals[i][1] < start: result.append(intervals[i]); i += 1`
- **Overlapping:** `while i < n and intervals[i][0] <= end:`, with `start = min(start, intervals[i][0])` and `end = max(end, intervals[i][1])`.
- **Add the merged one:** `result.append([start, end])`
- **Everything after:** `result.extend(intervals[i:])`. `extend` adds each item; `append` would add the whole list as one item.
""",
    "merge-intervals": r"""
## Sorting
- **Lists sort by first item, then second:** `sorted(intervals)` orders by start.
- **Explicit key:** `intervals.sort(key=lambda x: x[0])`
## Merging
- **Unpack while looping:** `for start, end in sorted(intervals):`
- **Last interval added:** `result[-1]`; its end is `result[-1][1]`.
- **Check non-empty first:** `if result and start <= result[-1][1]:`. An empty list is false, so `result[-1]` isn't reached.
- **Extend in place:** `result[-1][1] = max(result[-1][1], end)`
- **New interval:** `else: result.append([start, end])`
""",
    "non-overlapping-intervals": r"""
## Sort by end
- **Lambda key:** `sorted(intervals, key=lambda x: x[1])`. `lambda x: x[1]` is a tiny inline function returning the end.
## Greedy keep or remove
- **Start:** `removed = 0`, `prev_end = float("-inf")`
- **Unpack:** `for start, end in sorted(intervals, key=lambda x: x[1]):`
- **No overlap (touching is fine):** `if start >= prev_end: prev_end = end`
- **Overlap:** `else: removed += 1`
- **Answer:** `return removed`
""",
    "meeting-rooms": r"""
## Sort, then compare neighbours
- **Sort by start:** `intervals = sorted(intervals)` (or `intervals.sort()`).
- **From the second meeting on:** `for i in range(1, len(intervals)):`
- **Clash:** `if intervals[i][0] < intervals[i - 1][1]: return False`. Touching (`[1, 5]` then `[5, 10]`) is fine.
- **Fallback:** `return True`
## One-liner
- **all():** `return all(intervals[i][0] >= intervals[i - 1][1] for i in range(1, len(intervals)))`
""",
    "meeting-rooms-ii": r"""
## Min-heap of end times (heapq is pre-imported)
- **Empty heap:** `ends = []`
- **Sorted by start:** `for start, end in sorted(intervals):`
- **Earliest finish:** `ends[0]`
- **A room frees up:** `if ends and ends[0] <= start: heappop(ends)`
- **Use a room:** `heappush(ends, end)`
- **Rooms needed:** `return len(ends)`
## Two sorted lists alternative
- **Starts and ends separately:** `starts = sorted(i[0] for i in intervals)`, `ends = sorted(i[1] for i in intervals)`, then walk both with two pointers.
""",
    # ------------------------------------------------------------------ Math & Geometry
    "rotate-image": r"""
## Modify in place
- **Returns nothing:** the signature says `-> None`. Change `matrix` itself.
- **Replace contents if you build a new one:** `matrix[:] = new_rows`. (`matrix = new_rows` only rebinds your local name.)
## Transpose, then reverse rows
- **Size:** `n = len(matrix)`
- **Upper triangle only:** `for i in range(n):` with `for j in range(i + 1, n):` inside, so each pair is swapped once.
- **Swap two cells:** `matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]`
- **Reverse each row in place:** `for row in matrix: row.reverse()`. `row` is the real list, not a copy.
- **Reversed copy instead:** `row[::-1]` doesn't change anything unless you assign it.
## One-liner
- **Columns with zip:** `zip(*rows)` gives the columns, so `matrix[:] = [list(r) for r in zip(*matrix[::-1])]` rotates.
""",
    "spiral-matrix": r"""
## Four boundaries
- **Set them in one line:** `top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1`
- **Loop while there's something left:** `while top <= bottom and left <= right:`
## Walking each side
- **Forwards, including the end:** `range(left, right + 1)`
- **Backwards, including the end:** `range(right, left - 1, -1)`
- **Read cells:** `matrix[top][c]` along the top, `matrix[r][right]` down the right side.
- **Shrink after each side:** `top += 1`, `right -= 1`, `bottom -= 1`, `left += 1`
- **Re-check before the last two sides:** `if top <= bottom:` before the bottom row, `if left <= right:` before the left column.
- **Collect:** `result.append(…)`
""",
    "set-matrix-zeroes": r"""
## Modify in place
- **Returns nothing:** the signature says `-> None`.
## Simple version: remember rows and columns
- **Two sets:** `zero_rows, zero_cols = set(), set()`
- **First pass:** `if matrix[r][c] == 0: zero_rows.add(r); zero_cols.add(c)`
- **Second pass:** `if r in zero_rows or c in zero_cols: matrix[r][c] = 0`
## O(1) space: use the first row and column as markers
- **Remember the first row before overwriting it:** `first_row_zero = any(matrix[0][c] == 0 for c in range(cols))`
- **Skip the first row:** `for r in range(1, rows):`
- **Mark:** `matrix[r][0] = 0` and `matrix[0][c] = 0`
- **Apply marks:** `if matrix[r][0] == 0 or matrix[0][c] == 0: matrix[r][c] = 0`
- **Finish with the first column, then the first row.**
""",
    # ------------------------------------------------------------------ Bit Manipulation
    "number-of-1-bits": r"""
## Bit by bit
- **Last bit:** `n & 1` is 1 if `n` is odd.
- **Drop the last bit:** `n >>= 1` (shift right).
- **Until nothing's left:** `while n:` stops at 0.
## Faster trick
- **Clear the lowest 1 bit:** `n &= n - 1`. Count how many times you can do it.
## Built-ins
- **Binary string:** `bin(11)` gives `'0b1011'`, so `bin(n).count("1")` counts ones.
- **Method:** `n.bit_count()`
""",
    "counting-bits": r"""
## Table
- **List of zeros:** `ans = [0] * (n + 1)`
- **From 1:** `for i in range(1, n + 1):`
- **Half and last bit:** `i >> 1` is `i // 2`; `i & 1` is `i % 2`.
- **Reuse earlier answers:** `ans[i] = ans[i >> 1] + (i & 1)`. The brackets matter, because `+` binds tighter than `&`.
## Simple version
- **Count each one:** `[bin(i).count("1") for i in range(n + 1)]`
""",
    "reverse-bits": r"""
## Bit by bit
- **Exactly 32 rounds:** `for _ in range(32):`
- **Make room:** `result << 1` shifts left.
- **Set the new last bit:** `|` (OR), as in `result = (result << 1) | (n & 1)`.
- **Next input bit:** `n >>= 1`
## String version
- **32-character binary string with leading zeros:** `format(n, "032b")`
- **Reverse and parse:** `int(format(n, "032b")[::-1], 2)`. The `2` means base 2.
""",
    "missing-number": r"""
## Maths version
- **Sum of 0…n:** `n * (n + 1) // 2`, where `n = len(nums)`.
- **Built-in sum:** `sum(nums)`, so the answer is the difference.
## XOR version
- **XOR:** `^`. `x ^ x` is 0, `x ^ 0` is `x`, and order doesn't matter, so pairs cancel.
- **Start with n:** `missing = len(nums)`
- **Cancel indices against values:** `for i, x in enumerate(nums): missing ^= i ^ x`
## Set version
- **Set difference:** `(set(range(len(nums) + 1)) - set(nums)).pop()`
""",
    "sum-of-two-integers": r"""
## Bit pieces (no + or −)
- **Sum without carries:** `a ^ b`
- **The carries:** `(a & b) << 1`
- **Repeat until no carry:** `while b:` with `a, b = a ^ b, (a & b) << 1`. This alone works for non-negative numbers.
## 32-bit masking for negatives
- **Python ints never overflow,** so negative numbers would loop forever. Keep only 32 bits.
- **Hex literal for 32 ones:** `mask = 0xFFFFFFFF`
- **Trim:** `(a ^ b) & mask` and `((a & b) << 1) & mask`
- **Largest positive 32-bit number:** `0x7FFFFFFF`. Anything above it is a negative number in 32-bit.
- **Back to a Python negative:** `~(a ^ mask)`. `~x` equals `-x - 1`.
- **One-line if/else:** `return a if a <= 0x7FFFFFFF else ~(a ^ mask)`
""",
}
