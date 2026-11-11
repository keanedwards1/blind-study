CATEGORY = "Two Pointers"

PROBLEMS = [
    dict(
        slug="valid-palindrome",
        title="Valid Palindrome",
        difficulty="Easy",
        sig="def is_palindrome(s: str) -> bool:",
        desc="""
A phrase is a palindrome if, after lowercasing it and removing every character that isn't a letter or digit, it reads the same forwards and backwards.

Given a string `s`, return `True` if it is a palindrome, otherwise `False`.

**Constraints**
- `1 <= len(s) <= 2 * 10^5`
- `s` contains printable ASCII characters.
""",
        hints=["Use one pointer at each end. Skip characters that aren't alphanumeric (`str.isalnum`)."],
        solution="""
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
""",
        explanation="""
Two pointers move inward from both ends, skipping non-alphanumeric characters and comparing lowercase forms. This avoids building a cleaned copy.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[(["A man, a plan, a canal: Panama"], True), (["race a car"], False), ([" "], True)],
        tests=[["0P"], ["ab_a"], ["Was it a car or a cat I saw?"], ["abc"], [".,"], ["No 'x' in Nixon"]],
    ),
    dict(
        slug="three-sum",
        title="3Sum",
        difficulty="Medium",
        sig="def three_sum(nums: List[int]) -> List[List[int]]:",
        compare="unordered_nested",
        desc="""
Given an integer list `nums`, return every **unique** triplet `[a, b, c]` of values taken from three different positions such that `a + b + c == 0`.

The output must not contain duplicate triplets. Triplets, and the numbers inside them, may be in any order.

**Constraints**
- `0 <= len(nums) <= 3000`
- `-10^5 <= nums[i] <= 10^5`
""",
        hints=["Sort first.", "Fix the first number, then run a two-pointer search for the other two on the rest of the list.", "Skip equal neighbouring values to avoid duplicate triplets."],
        solution="""
def three_sum(nums: List[int]) -> List[List[int]]:
    nums = sorted(nums)
    result = []
    for i, a in enumerate(nums):
        if a > 0:
            break
        if i > 0 and a == nums[i - 1]:
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            total = a + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([a, nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
    return result
""",
        explanation="""
After sorting, fix `a = nums[i]` and look for a pair summing to `-a` in the remaining suffix with two pointers. Skip repeated values of `a` and repeated `lo` values after a match to keep triplets unique.

- **Time:** O(n²)
- **Space:** O(1) extra besides the sort/output
""",
        examples=[([[-1, 0, 1, 2, -1, -4]], [[-1, -1, 2], [-1, 0, 1]]), ([[0, 1, 1]], []), ([[0, 0, 0]], [[0, 0, 0]])],
        tests=[[[]], [[0, 0, 0, 0]], [[-2, 0, 1, 1, 2]], [[3, -2, 1, 0]], [[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]], [[1, -1, -1, 0]]],
    ),
    dict(
        slug="container-with-most-water",
        title="Container With Most Water",
        difficulty="Medium",
        sig="def max_area(height: List[int]) -> int:",
        desc="""
You are given a list `height` where `height[i]` is the height of a vertical line drawn at x = `i`. Choose two lines that, together with the x-axis, form a container. The container holds `min(height[i], height[j]) * (j - i)` units of water.

Return the maximum amount of water any container can hold.

**Constraints**
- `2 <= len(height) <= 10^5`
- `0 <= height[i] <= 10^4`
""",
        hints=["Start with the widest container (both ends).", "Moving the taller line inward can never help, so always move the shorter one."],
        solution="""
def max_area(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
""",
        explanation="""
Begin at maximum width. The area is limited by the shorter line, so moving the taller line inward can only shrink width without raising the limit. Always move the shorter side and track the best area.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[1, 8, 6, 2, 5, 4, 8, 3, 7]], 49), ([[1, 1]], 1)],
        tests=[[[4, 3, 2, 1, 4]], [[1, 2, 1]], [[2, 3, 4, 5, 18, 17, 6]], [[0, 0]], [[1, 2, 4, 3]]],
    ),
]
