"""Plain-language templates and example questions for each Python concept."""

TEMPLATES = {
    "dict": {
        "exampleSlug": "two-sum",
        "code": """def two_sum(nums, target):
    # Map each number we have already passed to the index where it appeared.
    index_by_number = {}

    # Visit numbers from left to right, keeping the current position as well.
    for index, number in enumerate(nums):
        # The partner needed to reach the target is target minus this number.
        needed = target - number

        # A dictionary lookup quickly tells us whether that partner came earlier.
        if needed in index_by_number:
            # Return the earlier position and the current position as the answer.
            return [index_by_number[needed], index]

        # Save this number only after checking, so we never use one item twice.
        index_by_number[number] = index

    # The prompt promises an answer; this is a fallback if that promise is broken.
    return []""",
    },
    "set": {
        "exampleSlug": "contains-duplicate",
        "code": """def contains_duplicate(nums):
    # A set keeps one copy of each value, no matter how many times it appears.
    unique_numbers = set(nums)

    # If the set is shorter, at least one input value was repeated.
    return len(unique_numbers) != len(nums)""",
    },
    "membership": {
        "exampleSlug": "longest-consecutive-sequence",
        "code": """def longest_consecutive(nums):
    # Store the values in a set so each membership check is fast on average.
    values = set(nums)
    longest = 0

    # Try each value as a possible beginning of a consecutive run.
    for value in values:
        # If value - 1 exists, this value is inside a run that started earlier.
        if value - 1 in values:
            continue

        # Otherwise count upward from this run's first value.
        length = 1
        while value + length in values:
            length += 1

        # Keep the largest run length found so far.
        longest = max(longest, length)

    # Return the best length, or zero when the input had no numbers.
    return longest""",
    },
    "list-stack": {
        "exampleSlug": "valid-parentheses",
        "code": """def is_valid(text):
    # For each closing bracket, record which opening bracket should match it.
    opening_for = {")": "(", "]": "[", "}": "{"}

    # The list stores opening brackets that have not been matched yet.
    stack = []

    # Read the string one character at a time from left to right.
    for char in text:
        # Opening brackets wait on the stack until a closing bracket matches.
        if char in "([{":
            stack.append(char)

        # A closing bracket must match the most recently seen opening bracket.
        elif not stack or stack.pop() != opening_for[char]:
            # No opening bracket, or the wrong one, means the string is invalid.
            return False

    # A valid string used every opening bracket; none should remain waiting.
    return not stack""",
    },
    "counter": {
        "exampleSlug": "group-anagrams",
        "code": """# defaultdict(list) makes a new empty list the first time a key is used.
from collections import defaultdict

def group_anagrams(words):
    # Each key will identify one group, and its value will collect the words.
    groups = defaultdict(list)

    # Process every word once.
    for word in words:
        # Sorting letters gives anagrams the same key, such as "aet" for "eat".
        key = "".join(sorted(word))

        # defaultdict(list) creates an empty list the first time this key appears.
        groups[key].append(word)

    # The required answer is the list of grouped word lists.
    return list(groups.values())""",
    },
    "deque": {
        "exampleSlug": "binary-tree-level-order-traversal",
        "code": """# deque supports fast removal from the front of the queue.
from collections import deque

def level_order(root):
    # There are no levels to visit when the tree has no root node.
    if root is None:
        return []

    # A queue visits older waiting nodes before newer ones (first in, first out).
    queue = deque([root])
    levels = []

    # Keep going until every discovered node has been processed.
    while queue:
        # The current queue length is exactly the number of nodes on this level.
        level_size = len(queue)
        current_level = []

        # Remove only those nodes, leaving their children for the next level.
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            # Add existing children at the back of the queue to visit them later.
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        # Save this level before moving on to the next one.
        levels.append(current_level)

    # Return the values grouped by level, from top to bottom.
    return levels""",
    },
    "heapq": {
        "exampleSlug": "merge-k-sorted-lists",
        "code": """# heapq keeps the smallest tuple at position zero.
import heapq

def merge_sorted_lists(lists):
    # The heap stores the smallest not-yet-merged node from each list.
    heap = []

    # Add the first node from each nonempty list as its current candidate.
    for list_index, node in enumerate(lists):
        if node is not None:
            # The index breaks ties safely and remembers which list to advance.
            heapq.heappush(heap, (node.val, list_index, node))

    # A dummy node makes it simple to append the first result node too.
    dummy = tail = ListNode()

    # Repeatedly take the smallest available node across all lists.
    while heap:
        value, list_index, node = heapq.heappop(heap)
        tail.next = node
        tail = node

        # Replace the removed node with the next node from that same list.
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, list_index, node.next))

    # Skip the temporary dummy and return the head of the merged list.
    return dummy.next""",
    },
    "bisect": {
        "exampleSlug": "longest-increasing-subsequence",
        "code": """# bisect_left finds an insertion position in a sorted list.
from bisect import bisect_left

def length_of_lis(nums):
    # tails[i] is the smallest ending value found for a subsequence of length i+1.
    tails = []

    # Each number may extend a subsequence or improve one of the existing tails.
    for number in nums:
        # Find the first tail that is greater than or equal to this number.
        position = bisect_left(tails, number)

        # If no tail is that large, this number extends the longest subsequence.
        if position == len(tails):
            tails.append(number)
        # Otherwise replace the tail with a smaller ending value for that length.
        else:
            tails[position] = number

    # The number of tracked lengths is the answer (not the tail values themselves).
    return len(tails)""",
    },
    "slicing": {
        "exampleSlug": "encode-and-decode-strings",
        "question": "Given one encoded string with a length marker before each original string, decode it back into the original list of strings.",
        "code": """def decode(encoded):
    # This list will hold each original string after we read it from the input.
    words = []
    position = 0

    # Continue while there are still characters left to read.
    while position < len(encoded):
        # Find the separator after the next string's written length.
        separator = encoded.find("#", position)

        # Parse only the length digits between position and the separator.
        length = int(encoded[position:separator])

        # Move past the separator so the next slice starts at the string itself.
        position = separator + 1

        # Slice exactly length characters, preserving even empty or special strings.
        words.append(encoded[position:position + length])

        # Advance to the start of the next length field.
        position += length

    # Return the recovered strings in their original order.
    return words""",
    },
    "loops-range": {
        "exampleSlug": "product-of-array-except-self",
        "code": """def product_except_self(nums):
    # Make one output slot per input number; each slot will become an answer.
    answer = [1] * len(nums)

    # Multiply by all values to the left of each position.
    prefix = 1
    for index in range(len(nums)):
        answer[index] = prefix
        prefix *= nums[index]

    # Multiply by all values to the right of each position.
    suffix = 1
    for index in range(len(nums) - 1, -1, -1):
        answer[index] *= suffix
        suffix *= nums[index]

    # Each slot now contains the product of every other input value.
    return answer""",
    },
    "enumerate-zip": {
        "exampleSlug": "valid-anagram",
        "code": """def same_letters(first, second):
    # Unequal lengths cannot contain exactly the same letters.
    if len(first) != len(second):
        return False

    # Count letters from the first word; missing letters start at zero.
    counts = {}
    for letter in first:
        counts[letter] = counts.get(letter, 0) + 1

    # zip pairs same-position letters; equal lengths ensure neither word is cut short.
    for first_letter, second_letter in zip(first, second):
        # Add one occurrence from the first word and cancel one from the second.
        counts[first_letter] = counts.get(first_letter, 0) + 1
        counts[second_letter] = counts.get(second_letter, 0) - 1

    # Anagrams cancel to zero for every character, regardless of letter order.
    return all(count == 0 for count in counts.values())""",
    },
    "comprehensions": {
        "exampleSlug": "top-k-frequent-elements",
        "code": """# Counter counts values; it is a concise way to build a frequency table.
from collections import Counter

def top_k_frequent(nums, k):
    # Counter builds a mapping from each number to the number of times it occurs.
    counts = Counter(nums)

    # Sort distinct numbers by their frequency, largest frequency first.
    ranked = sorted(counts, key=lambda number: counts[number], reverse=True)

    # A slice keeps just the first k items from that sorted list.
    return ranked[:k]""",
    },
    "unpacking": {
        "exampleSlug": "two-sum",
        "code": """def two_sum(nums, target):
    # Keep a value and its position together as a pair when saving it.
    seen = {}

    # enumerate gives both the current position and the current value.
    for index, number in enumerate(nums):
        # Compute the partner needed to make the requested total.
        needed = target - number

        # If that partner appeared earlier, unpack its saved position and return.
        if needed in seen:
            previous_index = seen[needed]
            return [previous_index, index]

        # Save the current value's position for later numbers to find.
        seen[number] = index

    # The problem promises a pair; return an empty list only as a fallback.
    return []""",
    },
    "any-all": {
        "exampleSlug": "design-add-and-search-words-data-structure",
        "code": """def search(node, word, index):
    # Reaching the end means the entire pattern matched this path.
    if index == len(word):
        return node.is_word

    # A dot can match any one next character, so try every outgoing child.
    if word[index] == ".":
        return any(
            search(child, word, index + 1)
            for child in node.children.values()
        )

    # For a normal character, only follow the child with that exact label.
    child = node.children.get(word[index])
    return child is not None and search(child, word, index + 1)""",
    },
    "min-max": {
        "exampleSlug": "container-with-most-water",
        "code": """def max_area(heights):
    # Start with the widest possible container: the two end positions.
    left, right = 0, len(heights) - 1
    best = 0

    # Each move makes the container narrower, so keep the best area seen.
    while left < right:
        # The shorter side limits how much water this pair can hold.
        width = right - left
        height = min(heights[left], heights[right])
        best = max(best, width * height)

        # Moving the taller side cannot help while the shorter side is unchanged.
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    # Return the greatest area found during the scan.
    return best""",
    },
    "iterators": {
        "exampleSlug": "serialize-and-deserialize-binary-tree",
        "code": """def serialize(root):
    # Store values in preorder: node, then left subtree, then right subtree.
    values = []

    def visit(node):
        # Write a marker for an empty child so the tree shape can be rebuilt.
        if node is None:
            values.append("#")
            return

        # Write this node before recursively writing either child.
        values.append(str(node.val))
        visit(node.left)
        visit(node.right)

    # Begin the traversal at the root, including the empty-tree case.
    visit(root)

    # Join tokens with commas to make one string.
    return ",".join(values)

def deserialize(data):
    # iter creates a one-way reader over the comma-separated tokens.
    tokens = iter(data.split(","))

    def build():
        # next consumes exactly one token each time a node position is visited.
        value = next(tokens)

        # The marker means this position represents an empty child.
        if value == "#":
            return None

        # Create the node, then consume tokens for its left and right children.
        node = TreeNode(int(value))
        node.left = build()
        node.right = build()
        return node

    # Rebuild and return the root represented by the serialized string.
    return build()""",
    },
    "loop-else": {
        "exampleSlug": "alien-dictionary",
        "question": "Given two words and an alien alphabet order, decide whether the first word comes before the second. Compare the first position where their letters differ; if one word is a prefix of the other, the shorter word comes first.",
        "code": """def appears_before(first, second, order):
    # Compare the words at their first position where the letters differ.
    for left, right in zip(first, second):
        if left != right:
            # The order table says which of these two letters comes first.
            return order[left] < order[right]

    # The loop's else runs only if no different pair caused an early return.
    else:
        # A shorter shared prefix must come before its longer continuation.
        return len(first) <= len(second)""",
    },
    "sorting": {
        "exampleSlug": "three-sum",
        "code": """def three_sum(nums):
    # Sorting makes it possible to move two pointers based on the current sum.
    nums.sort()
    triplets = []

    # Choose each number once as the first value in a possible triplet.
    for first in range(len(nums) - 2):
        # Skip repeated first values so the output has no duplicate triplets.
        if first and nums[first] == nums[first - 1]:
            continue

        # Search the remaining sorted portion from both ends.
        left, right = first + 1, len(nums) - 1
        while left < right:
            total = nums[first] + nums[left] + nums[right]

            # A small total needs a larger left value; a large one needs smaller.
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                # Save a matching triplet, then move past duplicate values.
                triplets.append([nums[first], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1

    # Return each distinct triplet found by the scan.
    return triplets""",
    },
    "recursion": {
        "exampleSlug": "maximum-depth-of-binary-tree",
        "code": """def max_depth(node):
    # Base case: an empty tree has depth zero and stops the recursive calls.
    if node is None:
        return 0

    # Solve the same smaller question for each child subtree.
    left_depth = max_depth(node.left)
    right_depth = max_depth(node.right)

    # Add this node's level to whichever child path is deeper.
    return 1 + max(left_depth, right_depth)""",
    },
    "closures": {
        "exampleSlug": "validate-binary-search-tree",
        "code": """def is_valid_bst(root):
    def check(node, low, high):
        # Empty branches satisfy every bound, so they are valid.
        if node is None:
            return True

        # This node must be strictly between all ancestor-imposed limits.
        if not (low < node.val < high):
            return False

        # The left side inherits the upper limit; the right gets the lower limit.
        return (check(node.left, low, node.val)
                and check(node.right, node.val, high))

    # Begin with no finite value restrictions around the root.
    return check(root, float("-inf"), float("inf"))""",
    },
    "classes": {
        "exampleSlug": "implement-trie-prefix-tree",
        "code": """# A TrieNode is one position in the character-by-character tree.
class TrieNode:
    def __init__(self):
        # Each node maps a character to the next node along that word path.
        self.children = {}
        # This flag marks that a complete word ends exactly at this node.
        self.is_word = False

# Trie groups the nodes together and provides the operations users call.
class Trie:
    def __init__(self):
        # The empty prefix is represented by the root node.
        self.root = TrieNode()

    def insert(self, word):
        # Start following the path from the root for every new word.
        node = self.root
        for char in word:
            # Create the next node only when this character path is missing.
            if char not in node.children:
                node.children[char] = TrieNode()
            # Move along the matching character edge before reading next char.
            node = node.children[char]
        # Mark the last node so a prefix alone is not mistaken for a whole word.
        node.is_word = True

    def search(self, word):
        # Start at the root and follow the path named by the requested word.
        node = self.root
        for char in word:
            # A missing edge means no stored word can match this entire path.
            if char not in node.children:
                return False
            node = node.children[char]
        # The path must end at a complete word, not just a stored prefix.
        return node.is_word

    def starts_with(self, prefix):
        # Start at the root and follow each character in the requested prefix.
        node = self.root
        for char in prefix:
            # A missing edge means the trie has no word with this prefix.
            if char not in node.children:
                return False
            node = node.children[char]
        # Every character was found, so at least one stored word has this prefix.
        return True""",
    },
    "node-refs": {
        "exampleSlug": "reverse-linked-list",
        "code": """def reverse_list(head):
    # previous is the already-reversed part; current is the next node to handle.
    previous = None
    current = head

    # Continue until current moves past the original list's final node.
    while current is not None:
        # Save the rest before changing the current node's next pointer.
        next_node = current.next

        # Point this node backward to the part that has already been reversed.
        current.next = previous

        # Advance both references by one node for the next iteration.
        previous = current
        current = next_node

    # previous now points at the original tail, which is the new list head.
    return previous""",
    },
    "infinity": {
        "exampleSlug": "best-time-to-buy-and-sell-stock",
        "code": """def max_profit(prices):
    # Infinity is larger than any price, so the first real price replaces it.
    lowest_price = float("inf")
    best_profit = 0

    # Consider each price as a possible day to sell.
    for price in prices:
        # Update the cheapest buying day seen before or on this day.
        lowest_price = min(lowest_price, price)

        # Selling today earns today's price minus the lowest earlier price.
        best_profit = max(best_profit, price - lowest_price)

    # Return zero if every possible trade would lose money.
    return best_profit""",
    },
    "int-division": {
        "exampleSlug": "find-minimum-in-rotated-sorted-array",
        "code": """def find_min(nums):
    # Keep a search range that always contains the smallest value.
    left, right = 0, len(nums) - 1

    # A midpoint splits the remaining range into two smaller parts.
    while left < right:
        middle = (left + right) // 2

        # If middle is larger than the right end, the rotation break is after it.
        if nums[middle] > nums[right]:
            left = middle + 1
        # Otherwise the minimum is at middle or somewhere to its left.
        else:
            right = middle

    # The range has shrunk to the one index containing the minimum.
    return nums[left]""",
    },
    "bits": {
        "exampleSlug": "number-of-1-bits",
        "code": """def count_ones(number):
    # Begin with zero set bits counted.
    count = 0

    # number & (number - 1) clears one 1-bit each time this loop runs.
    while number:
        number &= number - 1
        count += 1

    # The number of loop turns equals the number of 1-bits in the input.
    return count""",
    },
    "strings": {
        "exampleSlug": "valid-palindrome",
        "code": """def is_palindrome(text):
    # Keep only letters and digits, and make letter case irrelevant.
    clean = "".join(char.lower() for char in text if char.isalnum())

    # A string is the same backward when it equals its reversed slice.
    return clean == clean[::-1]""",
    },
}
