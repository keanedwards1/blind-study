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
- **Loop over indices:** `for idx in range(len(xs)):` gives you `idx = 0, 1, 2, …` up to the last index.
- **Start a loop partway through:** `range(start, stop)`. For example, `range(i + 1, len(nums))` starts one past `i`.
- **Nested loop:** put a second `for` indented inside the first.
- **Access by index:** `nums[i]`, `nums[j]`
- **Compare:** `if items[pos] == items[j]:` (two equals signs compare; one equals sign assigns)
- **Exit early:** `return True` inside the `if` ends the whole function right away.
- **Fallback:** `return False` goes after both loops, at the function's indentation level, not inside a loop.
- **Indentation is the structure:** each block (`for`, `if`) is indented 4 spaces deeper than the line that opens it.
## Faster version: remember what you've seen
- **Empty set:** `been = set()` (not `{}`, which makes an empty dict).
- **Membership:** `x in seen` gives `True` or `False`, in O(1).
- **Add:** `seen.add(x)` puts a value in the set.
- **Loop over values directly:** `for item in xs:` gives each value, with no indices.
- **One-liner:** `len(set(nums)) != len(nums)`. A set drops duplicates, so it's shorter exactly when there was one.
""",
    "valid-anagram": r"""
## Quick checks
- **Length:** `len(s)` is the number of characters.
- **Not equal:** `!=`. For example, `if len(word) != len(pattern): return False`.
## Counting characters with a dict
- **Empty dict:** `counter = {}`
- **Loop over characters:** `for ch in text:` gives one character at a time.
- **Read with a default:** `counts.get(c, 0)` gives the stored count, or `0` if `c` isn't a key yet.
- **Read with a default:** `d.get(key, 0)` gives the stored value, or `0` when the key is missing.
- **Store under a key:** `d[key] = value`
- **Add one / subtract one:** `n + 1`, `n - 1`
- **Walk two strings side by side:** `for lhs, rhs in zip(word, pattern):` gives `lhs` from `word` and `rhs` from `pattern` at the same position.
- **All the counts:** `counts.values()`
- **Every item passes a test:** `all(...)` is `True` only when every item is truthy, e.g. `all([True, True])` is `True`.
- **A test for each item:** a generator like `(n > 0 for n in numbers)` produces one `True`/`False` per item.
## Shortcuts
- **Counter:** `Counter(s)` builds the count dict in one call (already imported). `Counter(s) == Counter(t)` compares two of them.
- **Sorting:** `sorted(s)` returns the characters as a sorted list, so `sorted(s) == sorted(t)` also works (O(n log n)).
""",
    "two-sum": r"""
## Simple version: try every pair
- **Outer loop:** `for pos in range(len(xs)):`
- **Inner loop starting after i:** `for m in range(k + 1, len(items)):`. Starting at `k + 1` means an element never pairs with itself.
- **Check a pair:** `if values[pos] + values[col_i] == aim:`
- **Return a list:** `return [k, m]` (square brackets build a list).
## Faster version: a dict from value to index
- **Empty dict:** `lookup = {}`
- **Index and value together:** `for ix, magnitude in enumerate(xs):`
- **The partner you need:** `required = aim - count_n`
- **Is it a key?** `need in index_of` gives `True`/`False` in O(1).
- **Look it up:** `index_of[need]` gives the stored index.
- **Store:** `lookup[count_n] = pos`
- **Order matters:** check for the partner first, then store `n`, so a number can't pair with itself.
- **Fallback:** `return []` after the loop, so the function always returns something.
""",
    "group-anagrams": r"""
## Making a key that every anagram shares
- **Sort a string:** `sorted("tea")` gives the list `['a', 'e', 't']`.
- **Glue a list of strings:** `"".join(['a', 'e', 't'])` gives `"aet"`. Together: `"".join(sorted(s))`.
- **Dict keys must be unchangeable:** strings and tuples can be keys, lists can't. `tuple(some_list)` converts.
- **26 counters:** `counter = [0] * 26` makes a list of 26 zeros.
- **Character code:** `ord("c")` is `99`; letters have consecutive codes.
- **Position in the alphabet (0-25):** subtract the code of `"a"` from a letter's code.
- **Add one in place:** `counter[i] += 1`
## Grouping
- **Dict of lists:** `slots = defaultdict(list)` (already imported). A missing key starts as an empty list.
- **Add to a group:** `groups[key].append(s)`, with no need to check whether the key exists.
- **Plain-dict alternative:** `groups.setdefault(key, []).append(s)`
- **The answer:** `list(groups.values())` turns all the groups into a list.
""",
    "top-k-frequent-elements": r"""
## Counting
- **Count everything:** `counter = Counter(values)` maps each value to how often it appears.
- **Loop over pairs:** `for val, how_often in total.items():`
## Simple version: sort by frequency
- **Sort keys by their counts, biggest first:** `sorted(count, key=count.get, reverse=True)`
- **Take the first k:** the slice `[:k]`.
- **Built-in:** `count.most_common(k)` gives the k most common `(value, freq)` pairs. `[v for v, _ in count.most_common(k)]` keeps just the values.
## Faster version: buckets indexed by frequency
- **Separate empty lists:** `[[] for _ in range(3)]` gives `[[], [], []]`, three independent lists. (`[[]] * 3` repeats the *same* list three times.)
- **`_` for unused loop variables:** a convention for a variable you never read.
- **Add to a list inside a list:** `groups[2].append("x")`
- **Count down:** `range(5, 0, -1)` gives `5, 4, 3, 2, 1`. The third argument is the step; the stop isn't included.
- **Collect and stop:** `found.append(amount)`, then `if len(out) == kk: return out`.
""",
    "encode-and-decode-strings": r"""
## Two functions
- **Write both:** `def encode(strs):` and `def decode(s):` are separate functions, each with its own `return`.
## Encoding
- **f-strings:** `f"{len(s)}#{s}"` puts values inside a string. For `"abc"` it gives `"3#abc"`.
- **Glue strings together:** `"".join(parts)` joins a list of strings with nothing between them.
- **Join pieces:** `"".join(["ab", "cd"])` gives `"abcd"`.
- **Build text from values:** `f"{n}:{word}"` puts values inside a string.
## Decoding
- **Two variables at once:** `out, kk = [], 0`
- **A loop where you control the jumps:** `while idx < len(word):`
- **Find a character:** `s.index("#", i)` gives the index of the first `#` at or after position `i`.
- **Slice:** `s[i:j]` is the text from `i` up to, but not including, `j`.
- **Text to number:** `int("12")` gives `12`.
- **Slice a stretch:** `text[start:start + size]` takes `size` characters from `start`.
- **Move a position forward:** `place = place + step`
""",
    "product-of-array-except-self": r"""
## Setting up
- **Length:** `number = len(values)`
- **A list of ones:** `outcome = [1] * size`
## Left-to-right pass
- **Loop forwards:** `for place in range(count_n):`
- **Store the running product so far:** `outcome[k] = so_far` (start with `so_far = 1`).
- **Multiply in place:** `before_prod *= xs[idx]` is short for `before_prod = before_prod * items[idx]`.
## Right-to-left pass
- **Loop backwards to 0:** `range(4, -1, -1)` gives `4, 3, 2, 1, 0`. The stop is `-1` because the stop is never included.
- **Same thing, more readable:** `for k in reversed(range(size)):`
- **Multiply into the answer:** `outcome[place] *= trailing`, then `trailing *= items[place]`.
## Note
- **No division needed:** `/` always gives a float in Python and fails on zeros; this approach avoids it.
""",
    "longest-consecutive-sequence": r"""
## Simple version: sort first
- **Sort:** `nums.sort()` sorts in place; `sorted(nums)` returns a new list.
- **Compare with the previous item:** `nums[i] == nums[i - 1] + 1` continues a run; `nums[i] == nums[i - 1]` is a duplicate to skip.
- **Empty input:** `if not items: return 0` (an empty list counts as false).
## Faster version: a set
- **Set from a list:** `numbers = set(xs)` drops duplicates and gives O(1) lookups.
- **Not in:** `x - 1 not in values` is the opposite of `in`.
- **Loop over the set:** `for entry in items:`
- **Count up a run:** `while v + size in items: size += 1` repeats as long as the condition holds.
- **Keep the best:** `peak_val = max(peak_val, size)`, starting from `peak_val = 0`.
""",
    # ------------------------------------------------------------------ Two Pointers
    "valid-palindrome": r"""
## Simple version: clean, then compare
- **Filter and lowercase:** `tidied = "".join(letter.lower() for letter in word if letter.isalnum())`
- **Reverse a string:** `tidied[::-1]` is a reversed copy, so `return tidied == tidied[::-1]`.
## Two pointers (no copy)
- **Two names at once:** `a, rhs = 1, 2`
- **Last index:** `len(text) - 1`
- **Until they meet:** `while l_end < r_end:`
- **Move inward:** `lead += 1`, `rear -= 1`
- **Letter or digit?** `"a".isalnum()` is `True`; `" ".isalnum()` is `False`.
- **Flip a boolean:** `not`
- **Skip junk:** `while l_end < r_end and not line[l_end].isalnum(): l_end += 1`. `and` stops early, so keep the bound check first.
- **Lower case:** `"Q".lower()` gives `"q"`.
- **Not equal:** `!=`
- **Exit and fallback:** `return False` on a mismatch; `return True` after the loop.
""",
    "three-sum": r"""
## Sorting
- **Sorted copy:** `items = sorted(items)` (or `items.sort()` to sort in place).
## Outer loop
- **Index and value:** `for ix, lhs in enumerate(xs):`
- **Stop the loop entirely:** `break`. For example, `if p > 0: break`, since everything after is positive too.
- **Skip to the next round:** `continue`. For example, `if k > 0 and p == xs[k - 1]: continue` skips a repeated first value.
- **Why `pos > 0` first:** `items[-1]` is the *last* element in Python, so `items[pos - 1]` at `pos = 0` silently reads the end.
## Inner two pointers
- **Two names at once:** `p, q = 1, 2`
- **Loop:** `while low < high:`
- **Three-way branch:** `if acc < 0: … elif acc > 0: … else: …` (`elif` means "else if").
- **Add a list as one item:** `rows.append([1, 2, 3])`
- **Skip repeats:** `while low < high and xs[low] == xs[low - 1]: low += 1`
""",
    "container-with-most-water": r"""
## Simple version: every pair
- **Nested loops:** `for idx in range(n):` and `for col_i in range(idx + 1, n):`
- **Smaller of two:** `min(3, 7)` gives `3`.
- **Distance between two indices:** `b - a`
## Two pointers
- **Two names at once:** `a, q = 1, 2`
- **Last index:** `len(items) - 1`
- **Until they meet:** `while l_end < r_end:`
- **Width:** `right - left`
- **Running best:** `most = max(most, area)`, starting from `high_mark = 0`.
- **Move one side:** `if n_high[l_end] < n_high[r_end]: l_end += 1` / `else: r_end -= 1`
""",
    # ------------------------------------------------------------------ Sliding Window
    "best-time-to-buy-and-sell-stock": r"""
## Simple version: every buy/sell pair
- **Sell after buying:** `for idx in range(n):` then `for col_i in range(idx + 1, n):`, profit `quotes[col_i] - quotes[idx]`.
## One pass
- **Infinity as a starting minimum:** `floor_price = float("inf")` is bigger than any price (`inf` is also pre-imported).
- **Loop over values:** `for queue_ in quotes:`
- **Running minimum:** `floor_price = min(floor_price, pt)`
- **Keep the larger:** `max(a, b)`
- **Update a variable from itself:** `acc = acc + 1` (the right side is worked out first).
- **Start best at 0:** if prices only fall, you don't trade and the answer is 0.
""",
    "longest-substring-without-repeating-characters": r"""
## Window basics
- **Set two variables to 0:** `lo_end = high_mark = 0` (fine for numbers; don't do this with lists).
- **Right edge and character:** `for rear, letr in enumerate(word):`
- **Window length:** `right - left + 1`
- **Keep the larger:** `max(a, b)`
- **Window size from two ends:** `end - start + 1` (both ends included).
## Option A: a set of what's in the window
- **Empty set:** `frame = set()`
- **Shrink until c is gone:** `while ch in frame: frame.remove(word[front]); front += 1`
- **Add the new character:** `window.add(c)`
## Option B: a dict of last-seen positions
- **Empty dict:** `seen_at = {}`
- **Jump left past a repeat:** `if ch in where_seen and where_seen[ch] >= front: front = where_seen[ch] + 1`
- **Record the position:** `where_seen[ch] = rear`
""",
    "longest-repeating-character-replacement": r"""
## Window pieces
- **Several zeros at once:** `lo_end = higher = high_mark = 0`
- **Right edge and character:** `for rear, letr in enumerate(word):`
- **Empty dict:** `{}`
- **Read with a default:** `d.get(key, 0)`
- **Store under a key:** `d[key] = value`
- **Keep the larger:** `max(a, b)`
- **All the values of a dict:** `d.values()`
- **Window length:** `right - left + 1`
- **Window size from two ends:** `end - start + 1`
## Shrinking
- **Shrink while too many:** `while (r_end - lo_end + 1) - higher > limit:`
- **Subtract in place:** `d[key] -= 1`
- **Add one in place:** `idx += 1`
""",
    "minimum-window-substring": r"""
## What you still need
- **Count the target:** `wanted = Counter(other)`. A Counter returns 0 for a missing key, so `required[letter]` never raises a KeyError (a plain dict would).
- **Characters still missing:** `lacking = len(pattern)`
## Growing the window
- **Right edge:** `for right_end, glyph in enumerate(line):`
- **Did this character help?** `if required[ch] > 0: still_needed -= 1`
- **Use it up:** `required[ch] -= 1` (it can go negative, which just means extras).
## Shrinking while valid
- **Loop while the window has everything:** `while still_needed == 0:`
- **A tuple of values:** `pattern = (3, 0, 4)`; read parts with `pattern[0]`, `pattern[1]`, `pattern[2]`.
- **Start best as "nothing yet":** `peak_val = (float("inf"), 0, 0)`
- **Add in place:** `d[key] += 1`
- **Check a count:** `d[key] > 0`
## Returning
- **One-line if/else:** `a if condition else b`
- **Infinity:** `float("inf")` is bigger than every number.
""",
    # ------------------------------------------------------------------ Stack
    "valid-parentheses": r"""
## A list as a stack
- **Empty stack:** `heap_list = []`
- **Push:** `todo.append(letter)`
- **Pop:** `pile.pop()` removes and returns the last item.
- **Peek:** `stack[-1]` reads the last item without removing it.
- **Is it empty?** `not stack` is `True` for an empty list.
## Matching brackets
- **Closer to opener:** `closing_for = {")": "(", "]": "[", "}": "{"}`
- **Is it a closer?** `c in pairs` checks the dict's keys.
- **Mismatch check:** `if not todo or todo[-1] != matching[ch]: return False`. `or` stops early, so `todo[-1]` is never read on an empty stack.
- **Openers:** an `else:` branch pushes them.
- **Final answer:** `return not heap_list`. Every opener must have been closed.
""",
    # ------------------------------------------------------------------ Binary Search
    "find-minimum-in-rotated-sorted-array": r"""
## Simple version
- **Built-in:** `min(nums)` works, but it's O(n); the problem wants O(log n).
## Binary search
- **Two names at once:** `a, rhs = 1, 2`
- **Last index:** `len(items) - 1`
- **Loop until they meet:** `while low < high:`
- **Whole-number division:** `7 // 2` is `3`. `/` gives a float (`3.5`), which can't be an index.
- **Compare with the right end:** `if items[middle] > items[high]: low = middle + 1` / `else: high = middle`
- **Answer:** `return xs[left_i]`
""",
    "search-in-rotated-sorted-array": r"""
## Binary search
- **Two names at once:** `a, rhs = 1, 2`
- **Last index:** `len(items) - 1`
- **Inclusive loop:** `while lower_limit <= upper_limit:` (`<=` so a one-element range still gets checked).
- **Whole-number division:** `7 // 2` is `3`.
- **Found it:** `if values[half] == aim: return half`
## Which half is sorted?
- **Left half sorted:** `if xs[left_i] <= xs[half]:`
- **Chained comparison:** `1 <= x < 5` means both `1 <= x` and `x < 5`.
- **Nested if/else:** an `if`/`else` inside each branch of the outer `if`/`else`.
- **Narrow:** `upper_limit = middle - 1` or `lower_limit = middle + 1`
- **Not found:** `return -1` after the loop.
""",
    # ------------------------------------------------------------------ Linked List
    "reverse-linked-list": r"""
## Linked-list basics
- **Fields:** `node.val` is the value, `node.next` is the next node, and `None` marks the end.
- **Walk until the end:** `while here:` stops once `here` is `None`.
## Iterative reversal
- **Start:** `trailing = None`, `stepper = start_node`
- **Save the rest first:** `upcoming = current.next`
- **Point backwards:** `here.next = trailing`
- **Step forward:** `earlier = stepper`, then `stepper = upcoming`.
- **New head:** `return trailing`
- **All at once:** `here.next, earlier, here = earlier, here, here.next`. The whole right side is evaluated before anything is assigned.
## Recursive version
- **Base case:** `if not start_node or not start_node.next: return start_node`
- **Recurse:** `flipped = reverse_list(front.next)`
- **Flip one link:** `start_node.next.next = start_node`, then `start_node.next = None`, then `return flipped`.
""",
    "merge-two-sorted-lists": r"""
## Dummy head
- **Two names, one new node:** `guard = closing = ListNode()`. You build after `closing` and return `anchor.next`.
## Merging
- **While both have nodes:** `while first_list and second_list:`
- **Compare values:** `if la.val <= lb.val:`
- **Attach and advance:** `end_node.next = la`, then `la = la.next`.
- **Move the tail:** `rear = rear.next`
- **Attach whatever's left:** `final.next = la or lb`. `or` gives the first value that isn't `None`.
- **Answer:** `return anchor.next`
""",
    "reorder-list": r"""
## Modify in place
- **Returns nothing:** the signature says `-> None`. Change the links and don't return the list.
## Simple version: a list of nodes
- **Collect:** `members = []`, then `while walker: members.append(walker); walker = walker.next`.
- **Two indices from both ends:** `i, m = 0, len(members) - 1` and `while i < m:`
- **Relink:** `members[i].next = members[col_i]`, then move `i`, then `members[col_i].next = members[i]`, and so on.
- **End the list:** set the last node's `.next = None`, or the list loops forever.
## O(1) space: middle, reverse, weave
- **Find the middle:** `walker, quick = front, front.next`, then `while hare and hare.next: walker, hare = walker.next, hare.next.next`.
- **Cut:** `latter = tortoise.next`, then `tortoise.next = None`.
- **Reverse the second half:** the `prev`/`cur` loop from Reverse Linked List.
- **Weave:** save both nexts first, `next_a, after_b = leader.next, pair_b.next`, then `leader.next = pair_b`, `pair_b.next = next_a`, `leader, pair_b = next_a, after_b`.
""",
    "remove-nth-node-from-end-of-list": r"""
## Simple version: two passes
- **Count the nodes:** `span_len = 0`, then `while walker: span_len += 1; walker = walker.next`.
- **Walk to the node before the target:** `length - n` steps from a dummy node.
## One pass with a gap
- **Dummy before the head:** `guard = ListNode(0, front)`. Removing the head is then no special case.
- **Two pointers:** `slow_one = quick = anchor`
- **Repeat n times:** `for _ in range(size): runner = runner.next`
- **Move both until fast is last:** `while runner.next: walker, runner = walker.next, runner.next`
- **Skip a node:** `walker.next = walker.next.next`
- **Answer:** `return anchor.next`
""",
    "linked-list-cycle": r"""
## Simple version: remember nodes
- **Nodes can go in a set:** `met = set()`, then `if here in met: return True` and `met.add(here)`.
- **Walk:** `item = item.next` inside `while item:`
## O(1) space: slow and fast
- **Both start at the head:** `stepper = quick = front`
- **Safe loop condition:** `while hare and hare.next:`. Both checks are needed before reading `fast.next.next`.
- **Steps:** `stepper = stepper.next`, `quick = quick.next.next`
- **Same node?** `if tortoise is hare: return True`. `is` checks for the same object, not equal values.
- **No cycle:** `return False` after the loop.
""",
    "merge-k-sorted-lists": r"""
## Simple version: collect and sort
- **Every value:** walk each list and `values.append(node.val)`.
- **Sort:** `values.sort()`
- **Build a new list:** `back.next = ListNode(v)`, then `back = back.next`.
## Heap version (heapq is pre-imported)
- **Push:** `heappush(heap, item)`. **Pop the smallest:** `heappop(heap)`. **Peek:** `heap[0]`.
- **Heapify a list in place:** `heapify(pq)`
- **Tuples compare item by item:** push `(node.val, i, node)`. The index `i` breaks ties, so two `ListNode`s are never compared (that raises a TypeError).
- **Build with a filter:** `[(node.val, i, node) for i, node in enumerate(lists) if node]` skips empty lists.
- **Unpack and ignore:** `_, idx, spot = heappop(pile)`
- **Refill from the same list:** `if item.next: heappush(pile, (item.next.val, k, item.next))`
- **Dummy head:** `guard = final = ListNode()`, then `return guard.next`.
""",
    # ------------------------------------------------------------------ Trees
    "invert-binary-tree": r"""
## Tree basics
- **Fields:** `root.val`, `root.left`, `root.right`. A missing child is `None`.
- **Recursion:** the function calls itself on `root.left` and `root.right`.
- **Base case:** `if not base: return None` handles the empty tree and stops the recursion.
## Swapping
- **Swap without a temp variable:** `top_node.left, top_node.right = top_node.right, top_node.left`
- **Recurse on both:** `invert_tree(root.left)` and `invert_tree(root.right)`
- **Return the node:** `return top_node`
- **Swap two values in one line:** `a, rhs = rhs, a`
- **Call your own function on a child:** `f(node.left)`
""",
    "maximum-depth-of-binary-tree": r"""
## Recursive
- **Base case:** `if not base: return 0`
- **Bigger of two:** `max(a, b)`
- **Call your own function on a child:** `f(node.left)`
- **Larger of two:** `max(a, b)`
## Level by level (BFS)
- **Queue:** `line_q = deque([top_node])` (pre-imported). `line_q.popleft()` removes from the front.
- **One level per round:** `for _ in range(len(waiting)):`, and add 1 to the depth after each round.
""",
    "same-tree": r"""
## Base cases
- **Both empty:** `if not pt and not queue_: return True`
- **Only one empty:** `if not pt or not queue_: return False`
- **Compact version:** `if not pt or not queue_: return pt is queue_`. `pt is queue_` is `True` only when both are `None`.
- **Different values:** `if pt.val != queue_.val: return False`
## Recursion
- **Chain with `and`:** `a and b and c` stops at the first `False`.
- **Compare values:** `x.val == y.val`
""",
    "subtree-of-another-tree": r"""
## A helper function
- **Nested def:** write `def identical(p, q):` inside `is_subtree`. It's the Same Tree check.
- **Its base case:** `if not lhs or not rhs: return lhs is rhs`
## Main function
- **Empty sub_root is always a subtree:** `if not small_root: return True`
- **Ran out of tree:** `if not base: return False`
- **Chain with `or`:** `a or b or c` stops at the first `True`.
- **Call your own function on a child:** `f(node.left, other)`
""",
    "lowest-common-ancestor-of-a-binary-search-tree": r"""
## Inputs are nodes
- **Compare values:** `p` and `q` are `TreeNode` objects, so use `p.val` and `q.val`.
- **Return a node:** return the `TreeNode` itself, not its `.val`.
## Walking down
- **Start:** `spot = top_node`, then `while spot:`
- **Both smaller:** `if pt.val < here.val and queue_.val < here.val: here = here.left`
- **Both bigger:** `elif pt.val > item.val and queue_.val > item.val: item = item.right`
- **They split (or one is here):** `else: return node`
## Recursive alternative
- **Same branches:** `return lowest_common_ancestor(top_node.left, pt, queue_)` in the "both smaller" case, and so on.
""",
    "binary-tree-level-order-traversal": r"""
## Queue
- **Empty tree:** `if not base: return []`
- **Start the queue:** `line_q = deque([top_node])` (pre-imported).
- **Take from the front:** `queue.popleft()` is O(1). (`list.pop(0)` works but is O(n).)
- **Add to the back:** `line_q.append(cell.left)`
- **Only real children:** `if here.left:` and `if here.right:` before appending.
## One level at a time
- **Outer loop:** `while line_q:`
- **Exactly this level's nodes:** `for _ in range(len(waiting)):`. `range` reads the length once, before new children are added.
- **Collect the level:** `band = []`, `band.append(here.val)`, then `answer.append(band)` after the inner loop.
""",
    "validate-binary-search-tree": r"""
## Recursion with bounds
- **Helper with extra arguments:** `def ok(cell, lower_limit, upper_limit):`
- **Empty is valid:** `if not here: return True`
- **Chained comparison:** `lower_limit < item.val < upper_limit`. Use `if not (lower_limit < item.val < upper_limit): return False`.
- **Pass extra information down:** a helper can take more parameters than the main function, e.g. `def check(node, low, high):`.
- **Chain with `and`:** `a and b`
- **Infinity:** `float("inf")` and `float("-inf")` are bigger/smaller than every number.
## Alternative: in-order values
- **In-order visits a BST in sorted order:** collect values left, node, right.
- **Strictly increasing?** `all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))`
""",
    "kth-smallest-element-in-a-bst": r"""
## Simple version: in-order into a list
- **Helper:** `def inorder(here):`, with `if not here: return` (a bare `return` just stops).
- **Left, node, right:** `inorder(node.left)`, then `vals.append(node.val)`, then `inorder(node.right)`.
- **Appending to an outer list:** works inside the helper without any extra keyword.
- **k is 1-based:** `return vals[kk - 1]`
## Iterative, stopping early
- **Start:** `pile, spot = [], top_node`
- **Loop:** `while todo or here:`
- **Go left as far as possible:** `while here: pile.append(here); here = here.left`
- **Visit:** `entry = pile.pop()`, then `cap -= 1` and `if kk == 0: return here.val`.
- **Then go right:** `spot = spot.right`
""",
    "construct-binary-tree-from-preorder-and-inorder-traversal": r"""
## Pieces
- **New node:** `spot = TreeNode(value)`, then set `item.left = …` and `item.right = …`.
- **The root:** `preorder[0]`
- **Find a position:** `inorder.index(val)` (O(n)), or build a dict once.
- **Dict comprehension:** `{k: len(k) for k in words}` builds a dict in one line.
- **Index and value together:** `enumerate(items)` gives `(index, value)` pairs.
## Simple version: slicing
- **Split inorder:** `inorder[:mid]` (left) and `inorder[mid + 1:]` (right).
- **Split preorder:** `preorder[1:mid + 1]` (left) and `preorder[mid + 1:]` (right).
- **Empty input:** `if not pre: return None`
## Faster version: indices and an iterator
- **Iterator:** `source = iter(order_a)`. Each `next(stream)` gives the next value.
- **Helper over an inorder range:** `def make(low, high):`, with `if low > high: return None`.
- **Build left before right:** that's the order preorder lists them in.
""",
    "binary-tree-maximum-path-sum": r"""
## Updating an outer variable from a helper
- **Start very low:** `high_mark = float("-inf")`, since values can be negative.
- **Nested helper:** `def gain(here):`
- **`nonlocal most`:** the first line of the helper. It lets you reassign `most`; without it, `record = …` makes a new local variable and raises `UnboundLocalError`.
- **Alternative:** `most = [float("-inf")]` and update `most[0]`. Changing a list's item doesn't need `nonlocal`.
## The helper's logic
- **Empty node:** `if not here: return 0`
- **Never below zero:** `max(x, 0)`
- **Keep the larger:** `max(a, b)`
- **Larger of two:** `max(a, b)`
## Calling it
- **Run, then answer:** `gain(base)`, then `return high_mark`.
""",
    "serialize-and-deserialize-binary-tree": r"""
## Classes
- **Methods take self first:** `def serialize(self, root):`. You call it as `codec.serialize(root)`.
## Serializing
- **Collect tokens:** `found = []`, with `found.append("N")` for `None`.
- **Number to text:** `str(node.val)`
- **Recursive helper:** `def walk(here):`, with a bare `return` after appending `"N"`.
- **Preorder:** append the value, then `explore(item.left)`, then `explore(item.right)`.
- **One string:** `",".join(out)`
## Deserializing
- **Back to a list:** `data.split(",")`
- **Split text:** `"a,b".split(",")` gives `["a", "b"]`.
- **An iterator:** `stream = iter(items)`; `next(stream)` hands out the next item each call.
- **Text to number:** `int(tok)`
- **Make a node:** `TreeNode(5)`
- **Text to number:** `int("-3")` gives `-3`.
- **Attach a child:** `cell.left = other`
""",
    # ------------------------------------------------------------------ Tries
    "implement-trie-prefix-tree": r"""
## Classes
- **Constructor:** `def __init__(self):`, with `self.root = {}`. Anything stored on `self` is kept between method calls.
- **Methods that return nothing:** `-> None`, so no `return` value.
- **Private helper method:** `def _follow(self, text):`, called as `self._walk(word)`.
## Nested dicts as nodes
- **Each key is a character, each value is the child dict:** `{"a": {"p": {...}}}`
- **Child, created if missing:** `spot = spot.setdefault(letter, {})`
- **Mark the end of a word:** `item["$"] = True` (`"$"` is never a letter).
- **Missing letter:** `if char not in item: return None`, otherwise `spot = spot[ch]`.
- **Word or just a prefix?** `"$" in node`
- **Check for a node:** `node is not None`
## Class-based alternative
- **Node class:** `class TrieNode:` with `self.children = {}` and `self.end = False` in its `__init__`.
""",
    "design-add-and-search-words-data-structure": r"""
## Adding
- **Same as a trie:** `spot = spot.setdefault(ch, {})` for each letter, then `spot["$"] = True`.
## Searching with wildcards
- **Recursive helper inside the method:** `def walk(here, idx):`. It can read `w` from the outer method.
- **End of the word:** `if idx == len(term): return "$" in here`
- **Current letter:** `glyph = term[pos]`
- **Wildcard:** `if ch == ".":`
- **All children:** `here.items()` gives `(k_name, kid)` pairs. Skip the marker with `if k_name != "$"`.
- **At least one passes:** `any(...)` is `True` if any item is truthy.
- **Key and value together:** `for kk, x in d.items():`
- **Key present?** `key in d`
- **Chain with `and`:** `a and b`
- **Start:** `return explore(self.root, 0)`
""",
    "word-search-ii": r"""
## Build a trie of the words
- **Nested dicts:** `spot = spot.setdefault(letr, {})` for each letter.
- **Store the word at its end:** `here["$"] = term`, so you know which word you found.
## Grid basics
- **Grid size:** `len(grid)` is the number of rows; `len(grid[0])` is the number of columns.
- **A cell:** `board[r][c]`
- **Every cell:** `for rix in range(height):` with `for letr in range(width):` inside.
- **Loop over pairs:** `for lhs, rhs in ((1, 0), (0, 1)):`
- **Two names at once:** `x, other = 1, 2`
- **In bounds?** `0 <= nr < rows and 0 <= nc < cols`
## DFS with marking
- **Change a grid cell:** `grid[1][2] = "#"`
- **Remove a key and get its value:** `d.pop(key)`
- **Add to a list:** `out.append(x)`
- **Prune empty branches:** `if not item: up.pop(symbol)` (an empty dict counts as false).
""",
    # ------------------------------------------------------------------ Heap / Priority Queue
    "find-median-from-data-stream": r"""
## Classes
- **State on self:** `self.low = []` and `self.high = []` in `__init__`. They persist between calls.
## Simple version: keep a sorted list
- **Insert in sorted position:** `insort(self.nums, num)` (bisect is pre-imported).
- **Middle by index:** `count_n = len(self.nums)`, then `self.nums[count_n // 2]`, or the average of `self.nums[count_n // 2 - 1]` and `self.nums[count_n // 2]` when `count_n` is even.
## Two heaps (heapq is pre-imported)
- **Push / pop smallest / peek:** `heappush(h, x)`, `heappop(h)`, `h[0]`
- **Max-heap trick:** heapq only does min-heaps, so push `-num` and negate when you read: `-self.low[0]`.
- **Take the smallest from a heap:** `heappop(heap)`
- **Add to a heap:** `heappush(heap, x)`
- **Flip a sign:** `-x`
- **Balance by size:** `if len(self.high) > len(self.low):`
- **Average:** `(a + b) / 2`. `/` always gives a float. `float(x)` converts an int.
""",
    # ------------------------------------------------------------------ Backtracking
    "combination-sum": r"""
## Setup
- **Results and the current path:** `out, picked = [], []`
- **Recursive helper:** `def search(from_i, rest_amt):`
- **Outer lists in a helper:** you can `append`/`pop` them without `nonlocal`, because you change them rather than reassign them.
## The helper
- **Found one:** `if left_over == 0: found.append(trail[:]); return`
- **Copy the path:** `path[:]` (or `list(path)`). Appending `path` itself stores a reference that keeps changing.
- **Choices from start onwards:** `for place in range(begin, len(options)):`. This avoids the same combination in a different order.
- **Prune:** `if choices[k] <= rest_amt:`
- **Add to the end:** `items.append(x)`
- **Remove from the end:** `items.pop()`
- **Call your own function again:** `f(i, amount - 3)`
- **Why `i`, not `i + 1`:** the same number can be reused.
## Start it
- **Call, then answer:** `explore(0, goal)`, then `return answer`.
""",
    "word-search": r"""
## Grid basics
- **Grid size:** `len(grid)` rows, `len(grid[0])` columns.
- **Inside a range:** `0 <= x < limit`
- **Flip a boolean:** `not`
## Recursive helper
- **Arguments:** `def explore(row_i, ch, k):`, where `k` is how many letters are matched so far.
- **Matched the whole word:** `if idx == len(w): return True`
- **Wrong cell:** `if not (…in bounds…) or field[row_i][char] != term[pos]: return False`
- **Remember a value before changing it:** `previous = grid[1][2]`
- **Change a grid cell:** `grid[1][2] = "#"`
- **Try four directions:** `dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or …`. `or` stops at the first `True`.
## Start from every cell
- **Two `for`s in one expression:** `(x * y for x in range(2) for y in range(3))` works like a nested loop.
- **At least one passes:** `any(...)`
""",
    # ------------------------------------------------------------------ Graphs
    "number-of-islands": r"""
## Grid basics
- **Cells are strings:** compare with `"1"`, not the number `1`.
- **Grid size:** `len(grid)` rows, `len(grid[0])` columns.
- **Every cell:** `for rix in range(height):` with `for symbol in range(width):` inside.
- **Count:** `sum_so_far += 1` for each new island.
## Flood fill with a stack
- **Stack of tuples:** `heap_list = [(rix, char)]`, then `pos, q = heap_list.pop()` unpacks one.
- **Change a grid cell:** `board[1][2] = "x"`
- **Neighbours:** `for next_row, next_col in ((k + 1, col_i), (k - 1, col_i), (k, col_i + 1), (k, col_i - 1)):`
- **Valid land neighbour:** `if 0 <= di < height and 0 <= dj < width and board[di][dj] == "1":`
## Recursive alternative
- **Helper:** `def sink(r, c):` that returns if out of bounds or not `"1"`, sets the cell to `"0"`, and calls itself on the four neighbours.
""",
    "clone-graph": r"""
## Node basics
- **New node:** `Node(n.val)`
- **Neighbours:** `n.neighbors` is a list of `Node`s (note the US spelling).
## Remember copies
- **Original to copy:** `built = {}`. Nodes can be dict keys.
- **Already copied:** `if count_n in clones: return clones[count_n]`. This is what stops cycles.
- **Store before recursing:** `clones[size] = clone_n`, then fill in neighbours.
- **List comprehension:** `[f(x) for x in items]` applies `f` to every item.
## Empty input
- **One-line if/else:** `a if condition else b`
""",
    "pacific-atlantic-water-flow": r"""
## Sets of cells
- **Tuples as cells:** `(r, c)`. Tuples can go in sets; lists can't.
- **Start a set from a list:** `been = set(sources)`
- **Add a cell:** `met.add((rr, cc))`. The double brackets are the call plus the tuple.
- **Not visited yet:** `(nr, nc) not in seen`
## Start cells along the edges
- **Comprehensions:** `[(0, c) for c in range(cols)]` is the top row.
- **Join two lists:** `[1, 2] + [3]` gives `[1, 2, 3]`.
- **List of pairs:** `[(0, i) for i in range(3)]` gives `[(0, 0), (0, 1), (0, 2)]`.
## Search (DFS with a stack)
- **Copy the starts to a stack:** `heap_list = list(sources)`
- **At least as high:** `>=`
## Combining
- **Cells in both sets:** `pacific & atlantic` (set intersection).
- **In both sets:** `a & b`
- **Sort:** `sorted(items)`
- **Pair to list:** `[x, y]`
""",
    "course-schedule": r"""
## Building the graph
- **Separate empty lists:** `[[] for _ in range(3)]` gives `[[], [], []]`.
- **Counts:** `blockers = [0] * total_courses`
- **Unpack each pair:** `for unit, requires in rules:`
- **Add to a list inside a list:** `adj[0].append(4)`
- **Add one in place:** `counts[k] += 1`
## Topological order (Kahn's algorithm)
- **A queue:** `deque(items)`; `append` adds to the back and `popleft()` takes from the front.
- **Keep matching items:** `(i for i in range(5) if i % 2 == 0)`
- **Take one:** `present = line_q.popleft()`, then `finished_n += 1`.
- **Unlock what it leads to:** `for following in links[walker]: deps[following] -= 1`, and `if deps[following] == 0: waiting.append(following)`.
- **Return a comparison directly:** `return finished == n_courses`
## DFS alternative
- **States per course:** `status = [0] * total_courses` (0 = new, 1 = in progress, 2 = done). Seeing a 1 again means a cycle.
""",
    "graph-valid-tree": r"""
## Quick check
- **A tree has exactly n − 1 edges:** `if len(pairs_list) != size - 1: return False`
## Union-find
- **Numbers as a list:** `list(range(4))` gives `[0, 1, 2, 3]`.
- **Find the root:** `def root_of(v):` with `while boss[val] != val: val = boss[val]`, then `return v`.
- **Look up twice:** `arr[arr[i]]` uses one item's value as the next index.
- **Changing a list from a helper:** `up[...] = …` works without `nonlocal`.
- **Unpack each edge:** `for lhs, rhs in pairs_list:`
- **Two names at once:** `val, other = f(1), f(2)`
- **Same root means a cycle:** `if root_a == root_b: return False`
- **Union:** `boss[root_a] = root_b`
## DFS alternative
- **Undirected adjacency:** `links = defaultdict(list)`, with both `links[p].append(q)` and `links[q].append(p)`.
- **Everything reached?** `len(seen) == n`
""",
    "number-of-connected-components-in-an-undirected-graph": r"""
## Union-find
- **Numbers as a list:** `list(range(4))` gives `[0, 1, 2, 3]`.
- **Find:** `def root_of(v):` with `while up[item] != item: item = up[item]`, then `return v`.
- **Unpack pairs in a loop:** `for p, q in pairs:`
- **Two names at once:** `v, other = f(1), f(2)`
- **Merge two groups:** `if root_a != root_b: boss[root_a] = root_b; groups_left -= 1`
## DFS alternative
- **Undirected adjacency:** `links = defaultdict(list)`, adding each edge both ways.
- **Visited set:** `visited = set()`
- **Count starts:** `for here in range(size): if here not in met:`, add 1 and explore everything reachable.
""",
    # ------------------------------------------------------------------ Advanced Graphs
    "alien-dictionary": r"""
## Every letter
- **Dict comprehension over two loops:** `{ch: 0 for word in ["ab", "c"] for ch in word}` gives `{"a": 0, "b": 0, "c": 0}`.
- **Empty set:** `set()`
- **Loop over a dict's keys:** `blockers = {symbol: 0 for symbol in adj}`
## Comparing neighbouring words
- **Adjacent pairs:** `for lhs, rhs in zip(terms, terms[1:]):` gives `(vocab[0], vocab[1])`, `(vocab[1], vocab[2])`, …
- **Letter by letter:** `for value, partner in zip(p, q):`. It stops at the shorter word.
- **First difference:** `if v != partner:`, add the edge, then `break`.
- **Don't double-count:** `if yy not in links[item]: links[item].add(yy); deps[yy] += 1`
- **`for … else`:** the `else:` block runs only if the loop finished *without* `break`. Here that means one word is a prefix of the other, and `if len(p) > len(q): return ""`.
## Topological order
- **A queue:** `deque(items)`; `popleft()` takes from the front.
- **Sort:** `sorted(items)` gives a predictable order.
- **Process:** `letr = line_q.popleft()`, `sequence.append(letr)`, then lower each neighbour's indegree.
- **Join characters:** `"".join(["a", "b"])` gives `"ab"`.
- **One-line if/else:** `a if condition else b`
""",
    # ------------------------------------------------------------------ 1-D Dynamic Programming
    "climbing-stairs": r"""
## List version
- **Table:** `table = [0] * (size + 1)`
- **Base cases:** `memo[0] = memo[1] = 1`
- **Fill:** `for k in range(2, num + 1): table[k] = table[k - 1] + table[k - 2]`
- **Answer:** `return memo[size]`
## Two variables
- **Start:** `p, queue_ = 1, 1`
- **Repeat n times:** `for _ in range(size):`
- **Shift forward:** `p, queue_ = queue_, p + queue_`. The right side is computed first, so no temp variable is needed.
- **Answer:** `return lhs`
## Memoized recursion
- **Cache a helper:** put `@cache` on the line above `def ways(i):` (pre-imported). Repeated calls return the stored result.
""",
    "house-robber": r"""
## List version
- **Table:** `table = [0] * (len(xs) + 1)`, where `table[i]` is the best from the first `i` houses.
- **Rob or skip:** `memo[i] = max(memo[i - 1], memo[i - 2] + items[i - 1])`
## Two variables
- **Start:** `older = recent = 0`
- **Loop over values:** `for entry in xs:`
- **Update two names together:** `a, rhs = rhs, a + rhs` (the right side is worked out first, using the old values).
- **Larger of two:** `max(a, b)`
- **Answer:** `return recent`
""",
    "house-robber-ii": r"""
## Reuse a helper
- **Nested def:** `def row_text(homes):` holds the House Robber logic for a straight row.
- **Set two names to the same value:** `lhs = rhs = 0`
- **Update two names together:** `p, q = q, p + q`
## Breaking the circle
- **All but the last:** `nums[:-1]`
- **All but the first:** `nums[1:]`
- **One house:** `if len(values) == 1: return values[0]`
- **All but the last:** `items[:-1]`; **all but the first:** `items[1:]`
- **Larger of two:** `max(a, b)`
""",
    "longest-palindromic-substring": r"""
## Simple version: check every substring
- **Every start and end:** `for idx in range(n):` and `for col_i in range(idx + 1, n + 1):`
- **Is it a palindrome?** `pattern_tree = line[pos:m]`, then `pattern_tree == pattern_tree[::-1]`.
- **Keep the longest:** `if len(pattern_tree) > len(top_score): top_score = pattern_tree`
## Expand around centres
- **Each centre:** `for centre in range(len(text)):`
- **Odd and even in one loop:** `for li, ri in ((pivot, pivot), (pivot, pivot + 1)):`
- **Expand:** `while low >= 0 and high < len(text) and text[low] == text[high]: low -= 1; high += 1`. Keep the bounds checks first.
- **After the loop:** the palindrome is `s[lo + 1:hi]`, with length `hi - lo - 1`.
- **Track it:** `begin, stop_at = low + 1, high` when it's longer, then `return line[begin:stop_at]`.
""",
    "palindromic-substrings": r"""
## Expand around centres
- **Counter:** `counter = 0`
- **Each centre:** `for my_pivot in range(len(word)):`
- **Odd and even in one loop:** `for smallest, biggest in ((mid_i, mid_i), (mid_i, mid_i + 1)):`
- **Expand and count:** `while li >= 0 and ri < len(text) and text[li] == text[ri]:`, then `counter += 1`, `li -= 1`, `ri += 1`.
- **Answer:** `return total`
## Simple version
- **Every substring:** two loops over `i` and `j`, adding 1 when `s[i:j] == s[i:j][::-1]`.
""",
    "decode-ways": r"""
## Characters are strings
- **Characters are text:** compare with `"0"`, not the number `0`.
- **Two characters as a number:** `int("26")` gives `26`.
- **Slice two characters:** `text[3:5]`
- **In range:** `10 <= value <= 26` (chained comparison).
## List version
- **Table:** `table = [0] * (len(word) + 1)`, with `table[0] = 1` (one way to decode nothing).
- **Fill:** `for idx in range(1, len(line) + 1):`. Add `memo[idx - 1]` if the single digit is valid, and `memo[idx - 2]` if `idx >= 2` and the two digits are.
- **Answer:** `return table[len(text)]`
## Two variables
- **One-line if/else:** `a if condition else b`
- **Loop from 2:** `for limit in range(2, len(text) + 1):`, with `spot = 0`, then `spot += last1` / `spot += last2`.
- **Shift forward:** `two_back, recent = recent, walker`
""",
    "coin-change": r"""
## Table
- **Repeat a value:** `[9] * 3` gives `[9, 9, 9]`.
- **Join lists:** `[0] + [5, 5]` gives `[0, 5, 5]`.
- **Or use infinity:** `[float("inf")] * (target_amt + 1)`, with `table[0] = 0`.
## Filling
- **Every amount:** `for pt in range(1, goal + 1):`
- **Every coin:** `for letr in pieces:`
- **Only if it fits:** `if ch <= lhs:`, so `lhs - ch` never goes negative.
- **Better with this coin?** `table[lhs] = min(table[lhs], table[lhs - char] + 1)`
## Answer
- **One-line if/else:** `a if condition else b`
""",
    "maximum-product-subarray": r"""
## Running values
- **Chain assignment:** `high_mark = biggest = smallest = values[0]`
- **Skip the first element:** `for entry in xs[1:]:`
- **A tuple:** `(1, 2, 3)`
- **Max and min of them:** `max(candidates)`, `min(candidates)`
- **Largest / smallest of several:** `max(t)`, `min(t)`
- **Update two names together:** `a, rhs = f(val), g(val)`
- **Running best:** `peak_val = max(peak_val, upper_limit)`
## Why track the minimum
- **Negatives flip signs:** the smallest product times a negative can become the largest.
""",
    "word-break": r"""
## Lookups
- **Set of words:** `lexicon = set(dictionary)`
- **Set comprehension:** `{x % 3 for x in nums}` collects the distinct results.
## Table
- **Repeat a value:** `[False] * 3` gives `[False, False, False]`.
- **Join lists:** `[True] + [False]`
- **Fill:** `for ix in range(1, len(word) + 1):`
- **Last L characters before i:** `s[i - L : i]`
- **At least one passes:** `any(...)`
- **Chain with `and`:** `a and b and c`
- **Substring in a set:** `text[2:5] in words`
- **Last item:** `items[-1]`
## Alternatives
- **Prefix test:** `s.startswith(w, i)` checks whether `w` appears at position `i`.
- **Memoized recursion:** `@cache` on `def can(i):`, trying each word that starts at `i`.
""",
    "longest-increasing-subsequence": r"""
## Simple version: O(n²) table
- **Table of ones:** `table = [1] * len(xs)`
- **Every earlier element:** `for k in range(len(items)):` then `for m in range(k):`
- **Extend if smaller:** `if values[col_i] < values[pos]: table[pos] = max(table[pos], table[col_i] + 1)`
- **Biggest entry:** `return max(memo)`
## Faster version: binary search
- **Sorted list of tails:** `tops = []`
- **Where x would go:** `ix = bisect_left(lasts, item)` (pre-imported) gives the index that keeps `lasts` sorted.
- **Append or replace:** `if pos == len(lasts): lasts.append(item)`, else `tops[pos] = val`.
- **Answer:** `return len(lasts)`
""",
    # ------------------------------------------------------------------ 2-D Dynamic Programming
    "unique-paths": r"""
## 2-D table
- **Grid of ones:** `table = [[1] * size for _ in range(q)]` makes `q` separate rows. (`[[1] * size] * q` repeats one row m times.)
- **Cell:** `dp[r][c]`
- **Loops from 1:** `for row_i in range(1, mins):` with `for symbol in range(1, num):` inside.
- **From above plus from the left:** `table[ri][char] = table[ri - 1][char] + table[ri][char - 1]`
- **Bottom-right:** `return memo[-1][-1]`
## One row
- **Repeat a value:** `[1] * 4` gives `[1, 1, 1, 1]`.
- **The item before:** `xs[i - 1]`
- **Add in place:** `acc += x`
## Maths
- **Combinations:** `math.comb(m + n - 2, m - 1)`
""",
    "longest-common-subsequence": r"""
## 2-D table
- **Extra row and column of zeros:** `table = [[0] * (size + 1) for _ in range(m + 1)]`, where `m, size = len(first_text), len(second_text)`.
- **Loops from 1:** `for pos in range(1, m + 1):` with `for m in range(1, count_n + 1):` inside.
- **Offset by one:** compare `text1[i - 1] == text2[j - 1]`, because `dp` has the extra row and column.
- **Match:** `table[k][col_i] = table[k - 1][col_i - 1] + 1`
- **No match:** `memo[idx][m] = max(memo[idx - 1][m], memo[idx][m - 1])`
- **One-line if/else:** `table[pos][col_i] = table[pos - 1][col_i - 1] + 1 if lhs == rhs else max(table[pos - 1][col_i], table[pos][col_i - 1])`
- **Answer:** `return memo[m][num]`
## Two rows
- **Keep only the previous row:** `earlier` and `here` lists, then `earlier = here` after each row.
""",
    # ------------------------------------------------------------------ Greedy
    "maximum-subarray": r"""
## Simple version
- **Every start and end:** `for idx in range(n):` with a running `acc += xs[j]` for `j` from `idx` on.
## Kadane's algorithm
- **Start from the first element:** `my_top_score = spot = values[0]`. Not 0, because every number could be negative.
- **Skip the first element:** `for entry in xs[1:]:`
- **Larger of two:** `max(a, b)`
- **Running best:** `peak_val = max(peak_val, current)`
""",
    "jump-game": r"""
## Furthest reach
- **Start:** `furthest = 0`
- **Index and value:** `for ix, leap in enumerate(xs):`
- **Stuck:** `if pos > max_reach: return False`
- **Keep the larger:** `max(a, b)`
- **Made it:** `return True`
## Backwards alternative
- **Goal post:** `wanted = len(xs) - 1`
- **Loop backwards:** `for pos in range(len(items) - 1, -1, -1):`
- **Move the goal:** `if k + values[k] >= wanted: wanted = k`
- **Answer:** `return wanted == 0`
""",
    # ------------------------------------------------------------------ Intervals
    "insert-interval": r"""
## Pieces of an interval
- **Unpack:** `begin, stop_at = extra`
- **Start and end by index:** `intervals[i][0]`, `intervals[i][1]`
## Three phases with one index
- **Index and length:** `idx, magnitude = 0, len(ranges)`
- **Before the new one:** `while k < count_n and ranges[k][1] < from_i: out.append(ranges[k]); k += 1`
- **Loop while a condition holds:** `while idx < num and ok:`
- **Smaller / larger:** `min(a, b)`, `max(a, b)`
- **Start and end of an interval:** `iv[0]`, `iv[1]`
- **Add the merged one:** `found.append([begin, finish])`
- **Add several items:** `out.extend([4, 5])`. `append` would add the whole list as one item.
- **From a position to the end:** `items[i:]`
""",
    "merge-intervals": r"""
## Sorting
- **Lists sort by first item, then second:** `sorted(intervals)` orders by start.
- **Explicit key:** `intervals.sort(key=lambda x: x[0])`
## Merging
- **Unpack while looping:** `for opening, stop_at in sorted(spans):`
- **Last item:** `items[-1]`; a part of it: `items[-1][1]`
- **Check non-empty first:** `if answer and from_i <= answer[-1][1]:`. An empty list is false, so `result[-1]` isn't reached.
- **Change part of the last item:** `items[-1][1] = 9`
- **Larger of two:** `max(a, b)`
- **New interval:** `else: result.append([start, end])`
""",
    "non-overlapping-intervals": r"""
## Sort by end
- **Sort by part of each item:** `sorted(pairs, key=lambda p: p[0])` sorts by the first part.
## Greedy keep or remove
- **Start:** `skipped = 0`, `stop_time = float("-inf")`
- **Unpack:** `for from_ix, to_ix in sorted(ranges, k_name=lambda item: item[1]):`
- **No overlap (touching is fine):** `if begin >= edge: edge = finish`
- **Overlap:** `else: removed += 1`
- **Answer:** `return skipped`
""",
    "meeting-rooms": r"""
## Sort, then compare neighbours
- **Sort by start:** `periods = sorted(periods)` (or `ranges.sort()`).
- **From the second meeting on:** `for pos in range(1, len(ranges)):`
- **Clash:** `if ranges[k][0] < ranges[k - 1][1]: return False`. Touching (`[1, 5]` then `[5, 10]`) is fine.
- **Fallback:** `return True`
## One-liner
- **Every item passes:** `all(...)`
- **Compare with the previous item:** `items[i]` and `items[i - 1]`
- **Loop from the second index:** `range(1, len(items))`
""",
    "meeting-rooms-ii": r"""
## Min-heap of end times (heapq is pre-imported)
- **Empty heap:** `end_times = []`
- **Sorted by start:** `for from_ix, to_ix in sorted(ranges):`
- **Earliest finish:** `ends[0]`
- **A room frees up:** `if stops and stops[0] <= begin: heappop(stops)`
- **Use a room:** `heappush(finishes, finish)`
- **Rooms needed:** `return len(stops)`
## Two sorted lists alternative
- **Starts and ends separately:** `sources = sorted(idx[0] for idx in spans)`, `stops = sorted(idx[1] for idx in spans)`, then walk both with two pointers.
""",
    # ------------------------------------------------------------------ Math & Geometry
    "rotate-image": r"""
## Modify in place
- **Returns nothing:** the signature says `-> None`. Change `matrix` itself.
- **Replace contents if you build a new one:** `board[:] = new_rows`. (`board = new_rows` only rebinds your local name.)
## Transpose, then reverse rows
- **Size:** `number = len(grid)`
- **Upper triangle only:** `for ix in range(size):` with `for c2 in range(ix + 1, size):` inside, so each pair is swapped once.
- **Swap two values in one line:** `a, q = q, a` (works with grid cells too).
- **Reverse each row in place:** `for cells in board: cells.reverse()`. `cells` is the real list, not a copy.
- **Reversed copy instead:** `row[::-1]` doesn't change anything unless you assign it.
## One-liner
- **Columns with zip:** `zip(*rows)` gives the columns, so `matrix[:] = [list(r) for r in zip(*matrix[::-1])]` rotates.
""",
    "spiral-matrix": r"""
## Four boundaries
- **Several names at once:** `a, b, letter = 1, 2, 3`
- **Grid size:** `len(grid)` rows, `len(grid[0])` columns.
- **Loop while there's something left:** `while upper <= lower and l_end <= r_end:`
## Walking each side
- **Forwards, including the end:** `range(left, right + 1)`
- **Backwards, including the end:** `range(5, 1, -1)` gives `5, 4, 3, 2`; to include 2, the stop must be 1.
- **Read cells:** `matrix[top][c]` along the top, `matrix[r][right]` down the right side.
- **Shrink after each side:** `summit += 1`, `rear -= 1`, `bottom_row -= 1`, `lead += 1`
- **Re-check before the last two sides:** `if upper <= lower:` before the bottom row, `if l_end <= r_end:` before the left column.
- **Collect:** `result.append(…)`
""",
    "set-matrix-zeroes": r"""
## Modify in place
- **Returns nothing:** the signature says `-> None`.
## Simple version: remember rows and columns
- **Two sets:** `zero_rows, zero_cols_set = set(), set()`
- **First pass:** `if grid[ri][char] == 0: zero_rows.add(ri); zero_cols_set.add(char)`
- **Second pass:** `if ri in zero_rows or ch in zero_cols_set: board[ri][ch] = 0`
## O(1) space: use the first row and column as markers
- **At least one passes:** `any(x == 0 for x in row)`
- **Skip the first row:** `for rix in range(1, height):`
- **Change a grid cell:** `grid[1][2] = 0`
- **Apply marks:** `if board[ri][0] == 0 or board[0][char] == 0: board[ri][char] = 0`
- **Finish with the first column, then the first row.**
""",
    # ------------------------------------------------------------------ Bit Manipulation
    "number-of-1-bits": r"""
## Bit by bit
- **Last bit:** `n & 1` is 1 if `n` is odd.
- **Drop the last bit:** `count_n >>= 1` (shift right).
- **Until nothing's left:** `while num:` stops at 0.
## Faster trick
- **Clear the lowest 1 bit:** `magnitude &= magnitude - 1`. Count how many times you can do it.
## Built-ins
- **Binary string:** `bin(11)` gives `'0b1011'`, so `bin(n).count("1")` counts ones.
- **Method:** `n.bit_count()`
""",
    "counting-bits": r"""
## Table
- **List of zeros:** `[0] * 4` gives `[0, 0, 0, 0]`.
- **From 1:** `for kk in range(1, num + 1):`
- **Half and last bit:** `i >> 1` is `i // 2`; `i & 1` is `i % 2`.
- **Drop the last bit:** `x >> 1`
- **Last bit:** `x & 1`
- **Brackets matter:** `+` happens before `&`, so wrap `&` in brackets when adding.
## Simple version
- **Count each one:** `[bin(i).count("1") for i in range(n + 1)]`
""",
    "reverse-bits": r"""
## Bit by bit
- **Exactly 32 rounds:** `for _ in range(32):`
- **Make room:** `result << 1` shifts left.
- **Shift left one bit:** `x << 1`
- **OR in a bit:** `x | 1`
- **Last bit:** `x & 1`
- **Next input bit:** `number >>= 1`
## String version
- **32-character binary string with leading zeros:** `format(n, "032b")`
- **Reverse and parse:** `int(format(n, "032b")[::-1], 2)`. The `2` means base 2.
""",
    "missing-number": r"""
## Maths version
- **Sum of 0…n:** `size * (size + 1) // 2`, where `size = len(xs)`.
- **Built-in sum:** `sum(nums)`, so the answer is the difference.
## XOR version
- **XOR:** `^`. `x ^ x` is 0, `x ^ 0` is `x`, and order doesn't matter, so pairs cancel.
- **Start with n:** `wanted_n = len(values)`
- **Cancel indices against values:** `for k, v in enumerate(values): short ^= k ^ v`
## Set version
- **Set difference:** `(set(range(len(nums) + 1)) - set(nums)).pop()`
""",
    "sum-of-two-integers": r"""
## Bit pieces (no + or −)
- **Sum without carries:** `a ^ b`
- **The carries:** `(a & b) << 1`
- **Repeat until no carry:** `while rhs:` with `lhs, rhs = lhs ^ rhs, (lhs & rhs) << 1`. This alone works for non-negative numbers.
## 32-bit masking for negatives
- **Python ints never overflow,** so negative numbers would loop forever. Keep only 32 bits.
- **Hex literal for 32 ones:** `low32 = 0xFFFFFFFF`
- **XOR / AND / shift:** `x ^ y`, `x & y`, `x << 1`
- **Keep 32 bits:** `x & 0xFFFFFFFF`
- **Largest positive 32-bit number:** `0x7FFFFFFF`. Anything above it is a negative number in 32-bit.
- **Back to a Python negative:** `~(a ^ mask)`. `~x` equals `-x - 1`.
- **One-line if/else:** `a if condition else b`
- **Bitwise NOT:** `~x`
""",
}
