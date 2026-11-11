CATEGORY = "Heap / Priority Queue"

PROBLEMS = [
    dict(
        slug="find-median-from-data-stream",
        title="Find Median from Data Stream",
        difficulty="Hard",
        kind="class",
        cls="MedianFinder",
        starter="""class MedianFinder:
    def __init__(self):
        pass

    def add_num(self, num: int) -> None:
        pass

    def find_median(self) -> float:
        pass
""",
        desc="""
Design a `MedianFinder` that tracks a growing stream of integers:

- `MedianFinder()` creates an empty structure.
- `add_num(num)` adds an integer.
- `find_median()` returns the median of everything added so far. With an even count, that's the mean of the two middle values.

**Constraints**
- `-10^5 <= num <= 10^5`
- `find_median` is only called when at least one number exists.
- Up to `5 * 10^4` calls; make `add_num` O(log n) and `find_median` O(1).

_Tests call the methods in the order listed in `operations`, using the matching entry of `arguments`. Answers within 1e-5 are accepted._
""",
        hints=["Keep the smaller half in a max-heap and the larger half in a min-heap.", "Rebalance so the sizes differ by at most one. The median is then at one or both heap tops."],
        solution="""
class MedianFinder:
    def __init__(self):
        self.low = []   # max-heap (negated values)
        self.high = []  # min-heap

    def add_num(self, num: int) -> None:
        heappush(self.low, -num)
        heappush(self.high, -heappop(self.low))
        if len(self.high) > len(self.low):
            heappush(self.low, -heappop(self.high))

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
""",
        explanation="""
Two heaps split the numbers into a lower half (max-heap, stored negated) and an upper half (min-heap). Each insert routes the number through `low` into `high`, then moves one back if `high` grows larger, so `low` always has the same size or one more. The median comes from the heap tops.

- **Time:** `add_num` O(log n), `find_median` O(1)
- **Space:** O(n)
""",
        examples=[(
            [["MedianFinder", "add_num", "add_num", "find_median", "add_num", "find_median"], [[], [1], [2], [], [3], []]],
            [None, None, None, 1.5, None, 2.0],
        )],
        tests=[
            [["MedianFinder", "add_num", "find_median", "add_num", "find_median", "add_num", "find_median", "add_num", "find_median"], [[], [-1], [], [-2], [], [-3], [], [-4], []]],
            [["MedianFinder", "add_num", "add_num", "add_num", "add_num", "add_num", "find_median"], [[], [6], [10], [2], [6], [5], []]],
            [["MedianFinder", "add_num", "add_num", "find_median", "add_num", "add_num", "find_median"], [[], [5], [5], [], [100], [-100], []]],
        ],
    ),
]
