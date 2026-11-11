CATEGORY = "Binary Search"

PROBLEMS = [
    dict(
        slug="find-minimum-in-rotated-sorted-array",
        title="Find Minimum in Rotated Sorted Array",
        difficulty="Medium",
        sig="def find_min(nums: List[int]) -> int:",
        desc="""
A list of **distinct** integers, sorted ascending, has been rotated some number of times (for example `[0,1,2,4,5,6,7]` might become `[4,5,6,7,0,1,2]`).

Return the minimum element in O(log n) time.

**Constraints**
- `1 <= len(nums) <= 5000`
- All values are unique.
""",
        hints=["Compare the middle element with the rightmost element. That tells you which half holds the rotation point."],
        solution="""
def find_min(nums: List[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
""",
        explanation="""
If `nums[mid] > nums[hi]`, the drop (and the minimum) is strictly right of `mid`; otherwise the minimum is at `mid` or to its left. Narrow until `lo == hi`.

- **Time:** O(log n)
- **Space:** O(1)
""",
        examples=[([[3, 4, 5, 1, 2]], 1), ([[4, 5, 6, 7, 0, 1, 2]], 0), ([[11, 13, 15, 17]], 11)],
        tests=[[[1]], [[2, 1]], [[5, 1, 2, 3, 4]], [list(range(500, 1000)) + list(range(0, 500))], [[2, 3, 4, 5, 1]]],
    ),
    dict(
        slug="search-in-rotated-sorted-array",
        title="Search in Rotated Sorted Array",
        difficulty="Medium",
        sig="def search(nums: List[int], target: int) -> int:",
        desc="""
`nums` is a list of **distinct** integers, sorted ascending and then rotated at an unknown pivot. Return the index of `target` in `nums`, or `-1` if it isn't present.

Your solution must run in O(log n).

**Constraints**
- `1 <= len(nums) <= 5000`
""",
        hints=["At every step, at least one half (left..mid or mid..right) is properly sorted.", "Check whether the target lies inside the sorted half's range; if so search there, otherwise search the other half."],
        solution="""
def search(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
""",
        explanation="""
Use binary search with one extra decision: figure out which side of `mid` is sorted (`nums[lo] <= nums[mid]` means the left side is). If the target falls within that sorted range, go there; otherwise go to the other side.

- **Time:** O(log n)
- **Space:** O(1)
""",
        examples=[([[4, 5, 6, 7, 0, 1, 2], 0], 4), ([[4, 5, 6, 7, 0, 1, 2], 3], -1), ([[1], 0], -1)],
        tests=[[[1], 1], [[3, 1], 1], [[5, 1, 3], 5], [[4, 5, 6, 7, 8, 1, 2, 3], 8], [[1, 3], 3], [[6, 7, 1, 2, 3, 4, 5], 6]],
    ),
]
