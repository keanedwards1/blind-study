CATEGORY = "Greedy"

PROBLEMS = [
    dict(
        slug="maximum-subarray",
        title="Maximum Subarray",
        difficulty="Medium",
        sig="def max_sub_array(nums: List[int]) -> int:",
        desc="""
Return the largest sum of any non-empty **contiguous** subarray of `nums`.

**Constraints**
- `1 <= len(nums) <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
""",
        hints=["If the running sum goes negative, it can only hurt what comes next, so restart from the current element."],
        solution="""
def max_sub_array(nums: List[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
""",
        explanation="""
Kadane's algorithm: the best subarray ending at `i` either extends the best one ending at `i − 1` or starts fresh at `nums[i]`. Track the overall maximum.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[-2, 1, -3, 4, -1, 2, 1, -5, 4]], 6), ([[1]], 1), ([[5, 4, -1, 7, 8]], 23)],
        tests=[[[-1]], [[-2, -1]], [[8, -19, 5, -4, 20]], [[-3, -2, -5]], [[1, 2, 3, -100, 4, 5]]],
    ),
    dict(
        slug="jump-game",
        title="Jump Game",
        difficulty="Medium",
        sig="def can_jump(nums: List[int]) -> bool:",
        desc="""
You start at index `0` of `nums`. From index `i` you may jump forward **up to** `nums[i]` positions. Return `True` if you can reach the last index.

**Constraints**
- `1 <= len(nums) <= 10^4`
- `0 <= nums[i] <= 10^5`
""",
        hints=["Track the farthest index reachable so far. If you ever stand on an index beyond it, you're stuck."],
        solution="""
def can_jump(nums: List[int]) -> bool:
    farthest = 0
    for i, step in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + step)
    return True
""",
        explanation="""
Track the greedy reach: sweep from left to right, extending `farthest = max(farthest, i + nums[i])`. If some index `i` lies beyond `farthest`, it's unreachable, and so is everything after it.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[2, 3, 1, 1, 4]], True), ([[3, 2, 1, 0, 4]], False)],
        tests=[[[0]], [[1, 0, 1]], [[2, 0, 0]], [[1, 1, 1, 0]], [[0, 2, 3]], [[2, 5, 0, 0]]],
    ),
]
