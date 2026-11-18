# Hints for the Blind 75 problems, keyed by slug. They replace the `hints` in content/NN_*.py when the problems are built.
#
# Each problem has 2-4 hints that build on each other and never give the code away:
#   1. what the problem is really asking / what to notice,
#   2. the tool or approach that fits, and why,
#   3. the plan in plain-English steps,
#   4. the tricky part (an edge case or a common mistake).
# scripts/build_problems.py checks the count and that no hint repeats a line of the solution.

HINTS = {
    # ------------------------------------------------------------------ Arrays & Hashing
    "contains-duplicate": [
        "You only need a yes/no answer: has any value shown up before? You don't need to know which one or how many times.",
        "A set answers \"have I seen this before?\" instantly, no matter how big it gets. Checking a list for a value means scanning the whole list each time.",
        "Walk through the numbers once. For each one, first check whether it's already in your set; if it is, you've found a duplicate. Otherwise add it and keep going.",
        "If you reach the end without finding a repeat, every value was unique. An empty list has no duplicates.",
    ],
    "valid-anagram": [
        "Two words are anagrams when they use exactly the same letters the same number of times. Order doesn't matter, only the counts.",
        "If the lengths differ, they can't be anagrams, so you can stop early.",
        "Count how many times each letter appears in the first string (a dict works well), then subtract the counts for the second string.",
        "At the end every count must be exactly zero. A count that's still positive or has gone negative means the letters don't match.",
    ],
    "two-sum": [
        "For each number `n`, the partner you need is `target - n`. The question becomes: have I already seen that partner?",
        "Checking every pair is slow (n × n). A dict that maps each value you've seen to its index lets you check for the partner instantly.",
        "Go through the list with both the index and the value. Before storing the current number, look up its partner in the dict; if it's there, you have both indices.",
        "Look up the partner *before* you store the current number, so a number can't pair with itself (e.g. target 6 with a single 3).",
    ],
    "group-anagrams": [
        "Anagrams share the same letters with the same counts. If you can turn each word into a \"signature\" that's identical for all its anagrams, you can group by that signature.",
        "Two good signatures: the word's letters sorted (`\"eat\"` and `\"tea\"` both become `\"aet\"`), or a tuple of 26 letter counts.",
        "Use a dict from signature to a list of words. For each word, compute its signature and append the word to that signature's list.",
        "Dict keys must be unchangeable (hashable): use a tuple or a string as the signature, not a list. Return the dict's values as a list of lists.",
    ],
    "top-k-frequent-elements": [
        "First you need to know how often each value appears; then you need the `k` values with the biggest counts.",
        "`Counter` (or a dict) gives you the counts. Sorting values by count works but costs O(n log n).",
        "For O(n): make \"buckets\" where bucket `f` holds every value that appears exactly `f` times. No value can appear more than `len(nums)` times, so you need `len(nums) + 1` buckets.",
        "Walk the buckets from the highest count down, collecting values until you have `k` of them.",
    ],
    "encode-and-decode-strings": [
        "The strings can contain any character, so no single separator is safe: whatever you pick might appear inside a string.",
        "Instead of marking where a string ends, record how long it is. If decode knows the length, it can read exactly that many characters, whatever they are.",
        "Encode each string as its length, then a marker character like `#`, then the string itself, and join them all together.",
        "To decode: read digits up to the first `#` to get the length, take that many characters after it, then continue from just past them. Empty strings (length 0) must survive too.",
    ],
    "product-of-array-except-self": [
        "The answer at position `i` is (product of everything to the left of `i`) × (product of everything to the right of `i`).",
        "You can't divide, so build those two products separately with running totals.",
        "Pass 1, left to right: store in `answer[i]` the product of everything before `i`, then multiply the running product by `nums[i]`. Pass 2, right to left: multiply `answer[i]` by the product of everything after `i`.",
        "Start both running products at 1 (the empty product), so the first and last positions come out right. Zeros in the input are handled automatically.",
    ],
    "longest-consecutive-sequence": [
        "Sorting would make runs easy to see, but that's O(n log n). Can you find runs without sorting?",
        "Put every number in a set so \"is `x + 1` here?\" is instant.",
        "Only start counting from numbers that begin a run: `x` is a start when `x - 1` is *not* in the set. From a start, count upwards while `x + 1`, `x + 2`, … are present.",
        "Starting only at run beginnings is what keeps it O(n): each number is counted once. Loop over the set, not the list, so duplicates don't repeat work.",
    ],
    # ------------------------------------------------------------------ Two Pointers
    "valid-palindrome": [
        "Ignore everything that isn't a letter or digit, and treat upper and lower case as the same. Then check it reads the same both ways.",
        "Two pointers, one at each end, walking towards each other, let you compare without building a cleaned-up copy.",
        "Move the left pointer forward past non-alphanumeric characters (`str.isalnum()`), and the right pointer backward the same way. Compare the two characters in lowercase.",
        "Stop when the pointers meet or cross. A string with no letters at all (like `\" \"`) counts as a palindrome.",
    ],
    "three-sum": [
        "Fix one number, and the problem becomes Two Sum on the rest: find two numbers that add up to minus the fixed one.",
        "Sort the list first. On a sorted list, two pointers (one at each end) can find pairs: if the sum is too small move the left pointer right; if too big, move the right pointer left.",
        "For each index `i`, run the two-pointer search on the part of the list after `i`. Record every triplet that sums to zero.",
        "Skipping duplicates is the tricky part: skip an `i` whose value equals the previous one, and after finding a triplet, move the left pointer past repeated values.",
    ],
    "container-with-most-water": [
        "The water held is limited by the shorter of the two lines, times the distance between them.",
        "Start with the widest container (the first and last lines) and use two pointers moving inwards.",
        "At each step, record the area, then move the pointer at the *shorter* line inwards.",
        "Why move the shorter one? Moving the taller line can never help: the width shrinks and the height is still capped by the shorter line.",
    ],
    # ------------------------------------------------------------------ Sliding Window
    "best-time-to-buy-and-sell-stock": [
        "For each day, the best sale is that day's price minus the cheapest price on any *earlier* day.",
        "You don't need to check every pair. Keep track of the cheapest price seen so far as you walk forward.",
        "For each price: update the cheapest-so-far, then compare today's price minus the cheapest with your best profit.",
        "If prices only fall, no trade makes money: the answer is 0, not a negative number.",
    ],
    "longest-substring-without-repeating-characters": [
        "Think of a window `[left, right]` over the string that never contains a repeated character. You want its biggest size.",
        "Grow the window by moving `right` one step at a time. When the new character is already inside the window, move `left` just past its previous position.",
        "A dict mapping each character to the last index where you saw it tells you instantly where to move `left`.",
        "Only jump `left` forward if that previous position is inside the current window; `left` must never move backwards.",
    ],
    "longest-repeating-character-replacement": [
        "A window can be turned into one repeated letter if (window length − count of its most common letter) ≤ `k`. Those are the letters you'd change.",
        "Use a sliding window with a dict of letter counts inside it.",
        "Extend `right` each step and update the counts and the highest count. While the window needs more than `k` changes, shrink it from the left.",
        "Track the best window length as you go. It's fine if the stored highest count is slightly out of date when shrinking; the answer only grows when a genuinely better count appears.",
    ],
    "minimum-window-substring": [
        "You need the shortest stretch of `s` that contains every character of `t`, with repeats counted.",
        "Count what you still need (a `Counter` of `t`) and keep a number `missing` = how many characters are still needed in total.",
        "Grow the window to the right until `missing` hits 0. Then shrink from the left as long as the window stays valid, recording the smallest window seen.",
        "When the shrinking removes a character you needed, `missing` goes back up and you resume growing. If `missing` never reaches 0, return `\"\"`.",
    ],
    # ------------------------------------------------------------------ Stack
    "valid-parentheses": [
        "Every closing bracket must match the most recent opening bracket that hasn't been closed yet.",
        "\"Most recent first\" is exactly what a stack does: add with `append`, take the newest with `pop`.",
        "Push opening brackets. On a closing bracket, check the top of the stack is the matching opener, then pop it. A dict from closer to opener makes the check easy.",
        "Two easy-to-miss failures: a closer arriving when the stack is empty, and openers left over at the end (the stack must be empty).",
    ],
    # ------------------------------------------------------------------ Binary Search
    "find-minimum-in-rotated-sorted-array": [
        "The list is two sorted runs glued together, and the minimum is where the second run starts.",
        "O(log n) means binary search: look at the middle and throw away half each time.",
        "Compare the middle value with the value at the right end. If the middle is bigger, the drop (and the minimum) is to the right of the middle; otherwise it's at the middle or to its left.",
        "Keep the middle when it could be the answer (don't skip past it), and stop when the low and high pointers meet.",
    ],
    "search-in-rotated-sorted-array": [
        "At any middle point, at least one half (left or right) is properly sorted.",
        "Binary search still works if you first work out which half is sorted, by comparing the middle with the low end.",
        "If the target lies within the range of the sorted half, search that half; otherwise search the other one.",
        "Watch the comparisons at the edges: use `<=` where the target could equal an end value, and return the index as soon as the middle matches.",
    ],
    # ------------------------------------------------------------------ Linked List
    "reverse-linked-list": [
        "Reversing means every node's `next` should point to the node that used to come *before* it.",
        "Walk the list with two references: the node before (starts as `None`) and the current node.",
        "At each node: save its `next`, point its `next` back at the previous node, then step both references forward.",
        "Save `next` before you overwrite it, or you lose the rest of the list. When the current node is `None`, the previous node is the new head.",
    ],
    "merge-two-sorted-lists": [
        "Both lists are already sorted, so the smallest remaining node is always at the front of one of them.",
        "A dummy starting node saves you from special-casing the first node of the result.",
        "Keep a `tail` pointer. Repeatedly attach whichever front node is smaller, move that list forward, and move `tail` forward.",
        "When one list runs out, attach the rest of the other list in one go: it's already sorted.",
    ],
    "reorder-list": [
        "The new order alternates nodes from the front and the back. That's three smaller jobs.",
        "Step 1: find the middle with a slow pointer (one step) and a fast pointer (two steps). Step 2: reverse the second half.",
        "Step 3: weave the two halves together, taking one node from the first half, then one from the reversed second half, and so on.",
        "Cut the list at the middle (set the middle node's `next` to `None`) before reversing, otherwise you'll create a loop.",
    ],
    "remove-nth-node-from-end-of-list": [
        "To remove a node you need the node *before* it, and \"n from the end\" is hard to find in one pass unless you use a gap.",
        "Put two pointers `n` nodes apart. When the front one reaches the end, the back one is just before the node to remove.",
        "Start both at a dummy node placed before the head, move the front pointer `n` steps, then move both together until the front one's `next` is `None`.",
        "The dummy node handles removing the head itself (when `n` equals the length). Return the dummy's `next`, not the old head.",
    ],
    "linked-list-cycle": [
        "Following `next` either reaches the end (`None`) or goes round a loop forever.",
        "Use two runners: a slow one moving one step at a time and a fast one moving two. If there's a loop, the fast one eventually laps the slow one.",
        "Move them together; if they ever point at the *same node* (`is`), there's a cycle. If the fast one reaches `None`, there isn't.",
        "Check `fast` and `fast.next` exist before taking two steps. (A set of visited nodes also works, but uses extra memory.)",
    ],
    "merge-k-sorted-lists": [
        "At every step, the next node in the answer is the smallest of the current fronts of all `k` lists.",
        "A min-heap (`heapq`) hands you the smallest of many items quickly, so keep each list's front node in it.",
        "Pop the smallest, attach it to your result, and push that node's `next` (if any) into the heap.",
        "Nodes can't be compared to each other, so store `(value, index, node)` tuples; the index breaks ties between equal values.",
    ],
    # ------------------------------------------------------------------ Trees
    "invert-binary-tree": [
        "Mirroring a tree means: at every node, the left and right children swap places.",
        "Trees are naturally recursive: inverting a tree = swap the children, then invert each child tree.",
        "For a node, swap its left and right subtrees (inverting them along the way), then return the node.",
        "An empty tree (`None`) is already inverted; return it unchanged. That's your base case.",
    ],
    "maximum-depth-of-binary-tree": [
        "The depth of a tree is 1 (for the root) plus the depth of its deeper subtree.",
        "Recursion fits: ask each child for its depth and combine the answers.",
        "Return 0 for an empty tree; otherwise return 1 + the larger of the left and right depths.",
        "Count nodes, not edges: a single node has depth 1.",
    ],
    "same-tree": [
        "Two trees match when the roots have equal values and the left subtrees match and the right subtrees match.",
        "Write it recursively, comparing the two trees node by node in step.",
        "Base cases: if both nodes are missing they match; if only one is missing they don't.",
        "Check the values before recursing, and combine the three checks with `and` so it stops at the first difference.",
    ],
    "subtree-of-another-tree": [
        "You need a \"same tree\" check, and you need to try it at every node of the big tree.",
        "Write a helper that compares two trees exactly (values and shape).",
        "At each node of `root`: is the tree starting here the same as `sub_root`? If not, try the left subtree, then the right subtree.",
        "An empty `sub_root` is a subtree of anything; an empty `root` can't contain a non-empty `sub_root`.",
    ],
    "lowest-common-ancestor-of-a-binary-search-tree": [
        "In a BST, smaller values are always to the left and bigger ones to the right. Use that instead of searching both sides.",
        "Start at the root. If both `p` and `q` are smaller than the current node, the answer is in the left subtree; if both are bigger, it's in the right.",
        "As soon as they split (one on each side, or one of them *is* the current node), the current node is the lowest common ancestor.",
        "Compare values (`.val`), and return the node itself, not its value.",
    ],
    "binary-tree-level-order-traversal": [
        "You need nodes grouped by depth, top to bottom. That's breadth-first search (visiting by levels).",
        "A queue (`collections.deque`) processes nodes in the order they were added, which visits a tree level by level.",
        "While the queue isn't empty: note how many nodes it holds right now (that's one whole level), take exactly that many, record their values, and add their children.",
        "Taking the length *before* the inner loop is what separates the levels. An empty tree returns `[]`.",
    ],
    "validate-binary-search-tree": [
        "It isn't enough to compare each node with its direct children: every node in the left subtree must be smaller than *all* ancestors it sits to the left of.",
        "Pass down an allowed range (`low`, `high`) for each node.",
        "The root can be anything (−∞ to +∞). Going left, the node's value becomes the new upper bound; going right, it becomes the new lower bound.",
        "Values must be *strictly* inside the range; duplicates make it invalid. An empty subtree is valid.",
    ],
    "kth-smallest-element-in-a-bst": [
        "Visiting a BST in order (left subtree, node, right subtree) gives the values from smallest to largest.",
        "So you just need the `k`-th node in an in-order walk.",
        "Do the walk with a stack: go as far left as possible pushing nodes, pop one (that's the next smallest), count it, then move to its right child.",
        "Stop as soon as the count reaches `k`; there's no need to visit the rest of the tree.",
    ],
    "construct-binary-tree-from-preorder-and-inorder-traversal": [
        "Preorder lists the root first. In the inorder list, everything left of the root belongs to the left subtree and everything right of it to the right subtree.",
        "Build recursively: take the next value from preorder as the root, then build its left and right subtrees from the matching inorder ranges.",
        "A dict from value to its inorder index finds the root's position instantly instead of searching each time.",
        "Build the left subtree before the right one, because preorder lists all of the left subtree first. An empty range means `None`.",
    ],
    "binary-tree-maximum-path-sum": [
        "A path can bend at one node: it comes up from the left, through the node, and down to the right.",
        "For each node, compute the best sum of a path going *down* from it into one side only. Its parent can extend that.",
        "At each node: get the best downward sums from the left and right (treat negatives as 0, i.e. don't take that side), update the overall best with node + left + right, and return node + the larger side.",
        "Start the overall best at −∞, not 0: a tree of all negative values still has an answer (its largest single node).",
    ],
    "serialize-and-deserialize-binary-tree": [
        "You get to pick the format, as long as it records the tree's shape including where children are missing.",
        "A preorder walk (node, left, right) that writes a marker like `N` for every missing child captures the shape exactly.",
        "Serialize: walk preorder, writing values and `N` markers, joined with commas. Deserialize: read the tokens in the same order, building a node for each value and `None` for each `N`.",
        "Use a single shared iterator over the tokens while rebuilding, so each recursive call reads the next one. Negative values and multi-digit values must survive.",
    ],
    # ------------------------------------------------------------------ Tries
    "implement-trie-prefix-tree": [
        "A trie stores words letter by letter: words that share a beginning share the same path.",
        "Each node can be a dict from letter to child node, plus a special key (like `\"$\"`) meaning \"a word ends here\".",
        "Insert: walk the letters, creating child dicts where missing (`setdefault`), then mark the end. Search and prefix-check both walk the letters too.",
        "The difference between `search` and `starts_with`: a full word needs the end marker at the last node; a prefix only needs the path to exist.",
    ],
    "design-add-and-search-words-data-structure": [
        "Adding words is a normal trie insert. The new part is `.`, which can match any letter.",
        "When you meet a `.`, you can't follow one path: you have to try every child at that point.",
        "Search recursively with (node, position in word). For a normal letter, follow that child; for `.`, try each child and succeed if any of them does.",
        "Skip your end-of-word marker key when looping over children, and only return `True` at the end if the word really ends there.",
    ],
    "word-search-ii": [
        "Searching the board separately for each word repeats a lot of work. Put all the words in a trie and search for all of them at once.",
        "Start a depth-first search from each cell, moving through the trie as you move across the board. Stop as soon as no word continues with the current letter.",
        "Mark a cell as used while you're on it (and restore it on the way back) so a word can't reuse a cell.",
        "Remove a word from the trie once found so it isn't added twice, and prune empty trie branches to keep the search fast.",
    ],
    # ------------------------------------------------------------------ Heap / Priority Queue
    "find-median-from-data-stream": [
        "The median only depends on the middle of the sorted values. Keep the lower half and the upper half separately.",
        "Keep the lower half in a max-heap and the upper half in a min-heap. Python's `heapq` only does min-heaps, so store the lower half as negative numbers.",
        "When adding, push through one heap into the other so every value in the low half stays ≤ every value in the high half, then rebalance so the low half has the same size or one more.",
        "Median: if the low half is bigger, it's the top of the low half; otherwise it's the average of the two tops. Return a float.",
    ],
    # ------------------------------------------------------------------ Backtracking
    "combination-sum": [
        "You're building lists of numbers one choice at a time, and you need every list that hits the target exactly.",
        "Backtracking: add a candidate, explore what can follow, then remove it and try the next candidate.",
        "Track the remaining amount. When it reaches 0, save a copy of the current list; skip candidates bigger than what remains.",
        "To avoid the same combination in a different order, only allow candidates from the current index onward. Pass the *same* index again so a number can be reused.",
    ],
    "word-search": [
        "From each cell that matches the word's first letter, try to trace the rest of the word through neighbouring cells.",
        "Depth-first search with backtracking: step into a neighbour that matches the next letter, and undo the step if it leads nowhere.",
        "Your search function needs the cell and how far into the word you are. Succeed when you've matched every letter.",
        "Mark a cell as used while it's part of the current path (and restore it afterwards) so it can't be reused in the same word. Check the grid edges before reading a cell.",
    ],
    # ------------------------------------------------------------------ Graphs
    "number-of-islands": [
        "An island is a group of land cells connected up, down, left or right. Each time you find unvisited land, you've found a new island.",
        "When you find new land, explore the whole island at once (depth-first or breadth-first search) and mark every cell of it as visited.",
        "Scan every cell. On unvisited land: add 1 to the count, then flood-fill from it, marking land as visited (for example by turning it into water).",
        "Check the grid edges before looking at a neighbour, and mark cells when you add them to your stack or queue so they aren't added twice.",
    ],
    "clone-graph": [
        "Every original node needs exactly one copy, and the copies must link to each other the same way.",
        "A dict from original node to its copy lets you reuse a copy you've already made (this matters because graphs have cycles).",
        "To clone a node: if it's already in the dict, return its copy. Otherwise make the copy, store it in the dict *first*, then clone each neighbour and attach them.",
        "Storing the copy before cloning neighbours is what stops infinite loops. An empty input returns `None`.",
    ],
    "pacific-atlantic-water-flow": [
        "Checking every cell's downhill paths separately repeats a lot of work. Think backwards from the oceans instead.",
        "Start from all cells touching the Pacific and walk *uphill* (to neighbours at least as high). Every cell you reach can drain to the Pacific. Do the same for the Atlantic.",
        "Run that search twice, collecting a set of reachable cells for each ocean.",
        "The answer is the cells in both sets. Remember the condition flips when walking backwards: you move to neighbours with height ≥ the current one.",
    ],
    "course-schedule": [
        "Courses and prerequisites form a directed graph. You can finish everything exactly when that graph has no cycle.",
        "Count each course's prerequisites still outstanding (its in-degree). Courses with 0 can be taken right away.",
        "Put all 0-prerequisite courses in a queue. Take one, count it, and reduce the count for each course that depended on it; any that drop to 0 join the queue.",
        "If you managed to take every course, there was no cycle. Courses stuck in a cycle never reach 0.",
    ],
    "graph-valid-tree": [
        "A tree on `n` nodes is connected, has no cycles, and always has exactly `n - 1` edges.",
        "If the edge count isn't `n - 1`, you can answer `False` immediately.",
        "Then check for a cycle with union-find (each node points to a representative): for each edge, find both ends' representatives; if they're already the same, this edge closes a cycle.",
        "Otherwise join the two groups. With `n - 1` edges and no cycle, the graph must be connected.",
    ],
    "number-of-connected-components-in-an-undirected-graph": [
        "Start with every node in its own group: `n` groups. Each edge that joins two different groups reduces the count by 1.",
        "Union-find keeps track of which group each node is in: every node points towards a representative.",
        "For each edge, find the representatives of both ends. If they differ, link one to the other and subtract one from the count.",
        "Edges between nodes already in the same group don't change anything. (A depth-first search counting starts also works.)",
    ],
    # ------------------------------------------------------------------ Advanced Graphs
    "alien-dictionary": [
        "Neighbouring words in the sorted list tell you one fact each: the first letter where they differ shows which letter comes first.",
        "Turn those facts into a graph of letters (an edge from `x` to `y` means `x` comes before `y`), then put the letters in an order that respects every edge (a topological sort).",
        "Compare each pair of adjacent words up to their first difference and add that edge. Then repeatedly output letters with no remaining incoming edges.",
        "Two ways to fail: a cycle (you can't output every letter) and a longer word listed before its own prefix (like `\"abc\"` before `\"ab\"`). Both return `\"\"`.",
    ],
    # ------------------------------------------------------------------ 1-D DP
    "climbing-stairs": [
        "Your last move was either 1 step or 2 steps, so the ways to reach step `n` = ways to reach `n - 1` + ways to reach `n - 2`.",
        "That's the Fibonacci pattern. You only ever need the last two answers.",
        "Start with the counts for the bottom (1 way to stand on step 0, 1 way to reach step 1) and build upwards one step at a time.",
        "Keep two running variables instead of a whole list; update them together each step.",
    ],
    "house-robber": [
        "At each house you choose: rob it (and you must have skipped the previous one) or skip it.",
        "The best total up to house `i` = the larger of (best up to `i - 1`) and (best up to `i - 2` + this house).",
        "Walk through the houses keeping just two numbers: the best total up to the previous house and up to the one before that.",
        "Update both together each step. An empty street gives 0.",
    ],
    "house-robber-ii": [
        "In a circle, the first and last houses are neighbours, so you can't rob both.",
        "That splits into two ordinary House Robber problems: skip the first house, or skip the last house.",
        "Solve the straight-line version on `nums` without the last house and on `nums` without the first, and take the bigger answer.",
        "With only one house, both versions would be empty, so return that house's value directly.",
    ],
    "longest-palindromic-substring": [
        "Every palindrome mirrors around a centre. The centre is either one character (odd length) or the gap between two characters (even length).",
        "Try every possible centre and expand outwards while the characters on both sides match.",
        "For each index, expand from (i, i) and from (i, i + 1), and remember the longest stretch found.",
        "Keep start and end positions rather than building strings while expanding, and slice once at the end.",
    ],
    "palindromic-substrings": [
        "Each palindrome has a centre (a character or the gap between two), and expanding from that centre finds every palindrome around it.",
        "Every successful expansion step is one more palindromic substring.",
        "For each index, expand from (i, i) and from (i, i + 1), adding 1 to the count each time both ends match.",
        "Stop expanding as soon as the ends differ or you run off either end of the string.",
    ],
    "decode-ways": [
        "At each position you can decode one digit (if it's 1-9) or two digits (if they form 10-26).",
        "So ways(up to i) = ways(up to i − 1) if the single digit is valid, plus ways(up to i − 2) if the two-digit number is valid.",
        "Walk the string once, keeping only the last two counts.",
        "Zeros are the trap: `\"0\"` alone can't be decoded, and `\"06\"` isn't a valid pair. A string starting with `0` has 0 ways.",
    ],
    "coin-change": [
        "The fewest coins for an amount = 1 + the fewest coins for (amount − some coin), using whichever coin gives the smallest result.",
        "Build answers for every amount from 0 up to the target (a list where position `a` holds the fewest coins for amount `a`).",
        "Amount 0 needs 0 coins. For each amount, try every coin that fits and keep the best.",
        "Fill the list with an \"impossible\" value (bigger than any real answer) to start. If the target is still impossible at the end, return −1.",
    ],
    "maximum-product-subarray": [
        "Unlike sums, a negative number can flip the smallest product into the biggest one.",
        "So track both the largest and the smallest product of a subarray ending at the current position.",
        "For each number, the new largest and smallest come from three candidates: the number alone, number × old largest, number × old smallest.",
        "Compute both new values from the *old* ones before overwriting, and update the overall best each step. A zero resets everything.",
    ],
    "word-break": [
        "The string can be split if some word matches its ending and the part before that word can also be split.",
        "Keep a list where position `i` says whether the first `i` characters can be split. The empty prefix (position 0) always can.",
        "For each `i`, check every word length: if the last part of the prefix is a word and the part before it is splittable, mark `i` as splittable.",
        "Put the words in a set for fast checks. The answer is the value for the whole string.",
    ],
    "longest-increasing-subsequence": [
        "A simple O(n²) approach: for each position, the longest run ending there = 1 + the longest run ending at any earlier, smaller value.",
        "The faster idea: keep a list `tails` where `tails[L]` is the smallest possible last value of an increasing subsequence of length `L + 1`.",
        "For each number, binary search (`bisect_left`) for where it fits in `tails`: replace that entry, or append if it's bigger than everything.",
        "`tails` itself isn't a real subsequence, but its length is the answer. Use `bisect_left` so equal values don't count as increasing.",
    ],
    # ------------------------------------------------------------------ 2-D DP
    "unique-paths": [
        "You can only arrive at a cell from above or from the left.",
        "So paths to a cell = paths to the cell above + paths to the cell on its left.",
        "Every cell in the top row and left column has exactly 1 path. Fill in the rest row by row.",
        "You only need one row at a time: updating each entry by adding its left neighbour in place gives the next row.",
    ],
    "longest-common-subsequence": [
        "Compare the strings one character at a time from the start. Build a table where entry (i, j) is the answer for the first `i` characters of one and the first `j` of the other.",
        "If the two current characters match, the answer is 1 + the answer without both of them. If they don't, it's the better of dropping one character from either string.",
        "Fill the table row by row; the bottom-right entry is the answer.",
        "Add an extra row and column of zeros for empty prefixes, so you never need special cases at the edges.",
    ],
    # ------------------------------------------------------------------ Greedy
    "maximum-subarray": [
        "As you walk the list, keep the best sum of a subarray that ends at the current position.",
        "If that running sum ever becomes negative, it can only hurt what comes next, so start fresh from the next number instead.",
        "At each number, the best sum ending here is the larger of (the number alone) and (the running sum + the number). Track the overall best too.",
        "Start everything from the first element, not 0, so a list of all negative numbers returns its largest value.",
    ],
    "jump-game": [
        "You don't need to find the actual jumps, only whether the end is reachable.",
        "Track the farthest index you can reach so far.",
        "Walk the list; at each index, update the farthest reach with index + jump length.",
        "If you ever stand on an index beyond the farthest reach, you're stuck: return `False`.",
    ],
    # ------------------------------------------------------------------ Intervals
    "insert-interval": [
        "The existing intervals are sorted and don't overlap, so the result has three parts: ones entirely before the new interval, ones that overlap it, and ones entirely after.",
        "Walk through them in order, handling each part in turn.",
        "Copy intervals that end before the new one starts. While intervals start before (or when) the new one ends, merge them into it by widening its start and end. Then copy the rest.",
        "Intervals that touch (one's end equals the other's start) count as overlapping here, so use `<=` in the merge check.",
    ],
    "merge-intervals": [
        "Overlaps are easy to spot once the intervals are sorted by their start.",
        "After sorting, each interval either overlaps the last merged one or starts a new one.",
        "Walk the sorted intervals: if this one starts at or before the last merged end, extend that end; otherwise add it as a new interval.",
        "Extend to the *larger* of the two ends: a long earlier interval can fully contain a later one.",
    ],
    "non-overlapping-intervals": [
        "Turn it around: keep as many intervals as possible; everything you don't keep must be removed.",
        "Greedy choice: always keep the interval that ends earliest, because it leaves the most room for the rest.",
        "Sort by end time. Walk through: keep an interval if it starts at or after the last kept end; otherwise count it as removed.",
        "Touching intervals (`[1,2]` and `[2,3]`) don't overlap, so the check is start ≥ previous end.",
    ],
    "meeting-rooms": [
        "One person can attend everything only if no two meetings overlap.",
        "Sort the meetings by start time; then you only need to compare each meeting with the one just before it.",
        "If any meeting starts before the previous one ends, there's a clash.",
        "A meeting starting exactly when the previous one ends is fine. An empty list means `True`.",
    ],
    "meeting-rooms-ii": [
        "The number of rooms needed is the largest number of meetings happening at the same moment.",
        "Process meetings in start order, and keep the end times of meetings currently using a room in a min-heap, so the earliest-ending one is on top.",
        "For each meeting: if the earliest-ending room is already free (its end ≤ this start), reuse it by popping it. Then push this meeting's end time.",
        "The heap's size at the end is the number of rooms. Equal end and start times mean the room can be reused.",
    ],
    # ------------------------------------------------------------------ Math & Geometry
    "rotate-image": [
        "A 90° clockwise turn can be done in two simple flips you can do in place.",
        "First flip over the main diagonal (swap `matrix[i][j]` with `matrix[j][i]`), then reverse each row.",
        "For the diagonal flip, only swap pairs where `j > i`, or you'll swap everything back.",
        "Modify `matrix` itself; don't build and return a new one.",
    ],
    "spiral-matrix": [
        "The spiral peels off the outer ring, then the next ring in, and so on.",
        "Keep four boundaries: top, bottom, left and right. Walk the top row, the right column, the bottom row (backwards), then the left column (upwards).",
        "After each side, move that boundary inwards by one.",
        "Before walking the bottom row and the left column, check the boundaries haven't crossed; this matters for single rows or columns.",
    ],
    "set-matrix-zeroes": [
        "You must find all the original zeros before you start writing new ones, or new zeros will spread too far.",
        "The simple way: remember which rows and which columns contain a zero (two sets), then zero them in a second pass.",
        "To use no extra memory, use the first row and first column as the record instead, keeping separate notes about whether they themselves had a zero.",
        "Zero the first row and column last; they hold your notes until the very end.",
    ],
    # ------------------------------------------------------------------ Bit Manipulation
    "number-of-1-bits": [
        "You're counting how many 1s are in the number's binary form.",
        "Option one: look at the last bit (`n & 1`), then shift right (`n >>= 1`), until `n` is 0.",
        "Option two: `n & (n - 1)` removes the lowest 1 bit, so count how many times you can do that before `n` is 0.",
        "Both stop when `n` reaches 0; the second loops once per 1 bit instead of once per bit.",
    ],
    "counting-bits": [
        "You need the bit count for every number from 0 to `n`, and the answers reuse each other.",
        "`i >> 1` is `i` with its last bit removed, and you've already computed its answer.",
        "So bits(i) = bits(i >> 1) + (the last bit of i, which is `i & 1`). Fill a list from 1 upwards.",
        "Start with `ans[0] = 0`, and make the list `n + 1` long.",
    ],
    "reverse-bits": [
        "Read the bits of `n` from the right and write them into the result from the left.",
        "Repeat exactly 32 times, even if `n` becomes 0 early, so leading zeros end up in the right place.",
        "Each round: shift the result left by one, copy `n`'s last bit into it (`|` with `n & 1`), then shift `n` right by one.",
        "Python integers don't overflow, so after exactly 32 rounds the result is the correct 32-bit number.",
    ],
    "missing-number": [
        "The numbers `0..n` are all there except one. Comparing what should be there with what is there finds it.",
        "One way: the sum of `0..n` minus the sum of the list is the missing number.",
        "A bit trick: XOR (`^`) cancels equal numbers. XOR together every index, every value, and `n`, and only the missing number is left.",
        "Don't forget `n` itself: the indices only go up to `n - 1`.",
    ],
    "sum-of-two-integers": [
        "Adding in binary: XOR (`^`) adds the bits without carrying, and AND (`&`) shifted left by one gives the carries.",
        "Repeat: the new value is the XOR, the new carry is the AND shifted left, until there's no carry left.",
        "Python integers are unbounded, so keep everything within 32 bits with a mask (`& 0xFFFFFFFF`), or negative numbers loop forever.",
        "At the end, a result bigger than `0x7FFFFFFF` represents a negative number; convert it back to Python's negative form.",
    ],
}
