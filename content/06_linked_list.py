CATEGORY = "Linked List"

LIST_NOTE = "\n\n_Linked lists are shown as Python lists in the examples; your function receives and returns `ListNode` objects._"

PROBLEMS = [
    dict(
        slug="reverse-linked-list",
        title="Reverse Linked List",
        difficulty="Easy",
        sig="def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:",
        **{"in": ["list"]},
        out="list",
        desc="""
Given the `head` of a singly linked list, reverse the list and return the new head.

**Constraints**
- `0 <=` number of nodes `<= 5000`

**Follow-up:** solve it both iteratively and recursively.
""" + LIST_NOTE,
        hints=["Walk the list keeping a `prev` pointer. For each node, point `node.next` back at `prev`."],
        solution="""
def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
""",
        explanation="""
Iteratively flip each `next` pointer. Save `cur.next` before overwriting it, then advance. When `cur` falls off the end, `prev` is the new head.

- **Time:** O(n)
- **Space:** O(1) (recursive version uses O(n) stack)
""",
        examples=[([[1, 2, 3, 4, 5]], [5, 4, 3, 2, 1]), ([[1, 2]], [2, 1]), ([[]], [])],
        tests=[[[1]], [[7, 7, 8]], [list(range(100))]],
    ),
    dict(
        slug="merge-two-sorted-lists",
        title="Merge Two Sorted Lists",
        difficulty="Easy",
        sig="def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:",
        **{"in": ["list", "list"]},
        out="list",
        desc="""
You are given the heads of two linked lists, each sorted in non-decreasing order. Splice their nodes together into one sorted list and return its head.

**Constraints**
- Each list has `0..50` nodes.
- `-100 <= Node.val <= 100`
""" + LIST_NOTE,
        hints=["A dummy head node removes the special case for the first element."],
        solution="""
def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = tail = ListNode()
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
""",
        explanation="""
Keep a `tail` pointer starting at a dummy node and repeatedly attach the smaller head. When one list runs out, attach the remainder of the other.

- **Time:** O(n + m)
- **Space:** O(1)
""",
        examples=[([[1, 2, 4], [1, 3, 4]], [1, 1, 2, 3, 4, 4]), ([[], []], []), ([[], [0]], [0])],
        tests=[[[5], [1, 2, 4]], [[-3, 0, 9], [-2, 10]], [[1, 1, 1], [1, 1]], [[2], []]],
    ),
    dict(
        slug="reorder-list",
        title="Reorder List",
        difficulty="Medium",
        sig="def reorder_list(head: Optional[ListNode]) -> None:",
        **{"in": ["list"]},
        mutate=0,
        out="list",
        desc="""
Given a linked list `L0 → L1 → … → Ln-1 → Ln`, rearrange it **in place** to

`L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`

Change the links between nodes, not the values. Return nothing; the tests inspect the list starting from the original head.

**Constraints**
- `1 <=` number of nodes `<= 5 * 10^4`
""" + LIST_NOTE,
        hints=["Find the middle of the list with slow and fast pointers.", "Reverse the second half.", "Merge the two halves by alternating nodes."],
        solution="""
def reorder_list(head: Optional[ListNode]) -> None:
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
""",
        explanation="""
The solution has three classic steps: (1) find the midpoint with slow/fast pointers and cut the list there; (2) reverse the second half; (3) interleave nodes from the first half and the reversed second half.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[1, 2, 3, 4]], [1, 4, 2, 3]), ([[1, 2, 3, 4, 5]], [1, 5, 2, 4, 3])],
        tests=[[[1]], [[1, 2]], [[1, 2, 3]], [list(range(1, 11))], [list(range(1, 12))]],
    ),
    dict(
        slug="remove-nth-node-from-end-of-list",
        title="Remove Nth Node From End of List",
        difficulty="Medium",
        sig="def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:",
        **{"in": ["list", None]},
        out="list",
        desc="""
Given the `head` of a linked list, remove the `n`-th node **from the end** and return the head of the resulting list.

**Constraints**
- The list has `sz` nodes, `1 <= sz <= 30`
- `1 <= n <= sz`

**Follow-up:** can you do it in one pass?
""" + LIST_NOTE,
        hints=["Move a `fast` pointer n steps ahead, then move `fast` and `slow` together until `fast` reaches the end.", "Start `slow` at a dummy node so removing the head isn't a special case."],
        solution="""
def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next
""",
        explanation="""
Keep a gap of `n` nodes between two pointers. When the leading pointer reaches the last node, the trailing pointer sits right before the node to delete. A dummy head handles deleting the first node.

- **Time:** O(sz), one pass
- **Space:** O(1)
""",
        examples=[([[1, 2, 3, 4, 5], 2], [1, 2, 3, 5]), ([[1], 1], []), ([[1, 2], 1], [1])],
        tests=[[[1, 2], 2], [[1, 2, 3], 3], [[1, 2, 3], 1], [[1, 2, 3, 4], 2]],
    ),
    dict(
        slug="linked-list-cycle",
        title="Linked List Cycle",
        difficulty="Easy",
        sig="def has_cycle(head: Optional[ListNode]) -> bool:",
        params=["head", "pos"],
        uses=["list"],
        driver="""
def driver(ns, values, pos):
    head = build_list(values)
    if pos >= 0:
        nodes, cur = [], head
        while cur:
            nodes.append(cur)
            cur = cur.next
        nodes[-1].next = nodes[pos]
    return resolve(ns, "has_cycle")(head)
""",
        desc="""
Given the `head` of a linked list, return `True` if following `next` pointers ever revisits a node (the list has a cycle), otherwise `False`.

In the examples, `pos` is the index of the node the tail links back to (`-1` means no cycle). `pos` is only used to build the test list; it is **not** passed to your function.

**Constraints**
- `0 <=` number of nodes `<= 10^4`

**Follow-up:** can you use O(1) memory?
""",
        hints=["Use Floyd's tortoise-and-hare method: a slow pointer moves one step at a time and a fast pointer moves two. If there is a cycle, they will meet."],
        solution="""
def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
""",
        explanation="""
This is Floyd's cycle-detection algorithm. If there is no cycle, `fast` reaches the end. If there is one, `fast` gains one step per iteration on `slow` inside the loop and must eventually land on it.

- **Time:** O(n)
- **Space:** O(1) (a visited set works too, at O(n) space)
""",
        examples=[([[3, 2, 0, -4], 1], True), ([[1, 2], 0], True), ([[1], -1], False)],
        tests=[[[], -1], [[1, 2, 3], -1], [[1], 0], [[1, 2, 3, 4, 5, 6], 5], [list(range(500)), 250]],
    ),
    dict(
        slug="merge-k-sorted-lists",
        title="Merge K Sorted Lists",
        difficulty="Hard",
        sig="def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:",
        **{"in": ["lists"]},
        out="list",
        desc="""
You are given a list of `k` linked lists, each sorted ascending. Merge them all into one sorted linked list and return its head.

**Constraints**
- `0 <= k <= 10^4`
- Each list has `0..500` nodes.
""" + LIST_NOTE,
        hints=["Put the head of every list into a min-heap.", "Pop the smallest, append it, and push its `next`. Use (value, index, node) tuples so ties don't compare nodes."],
        solution="""
def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heappush(heap, (node.next.val, i, node.next))
    return dummy.next
""",
        explanation="""
A min-heap always holds the current smallest unmerged node from each list. Each of the N total nodes is pushed and popped once.

- **Time:** O(N log k)
- **Space:** O(k)

Pairwise divide-and-conquer merging (merge lists 0+1, 2+3, …) has the same complexity.
""",
        examples=[([[[1, 4, 5], [1, 3, 4], [2, 6]]], [1, 1, 2, 3, 4, 4, 5, 6]), ([[]], []), ([[[]]], [])],
        tests=[[[[], [1]]], [[[5], [1], [3]]], [[[-2, -1, -1], [], [-3, 0]]], [[[1, 2, 3], [1, 2, 3], [1, 2, 3]]]],
    ),
]
