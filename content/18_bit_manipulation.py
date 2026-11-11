CATEGORY = "Bit Manipulation"

PROBLEMS = [
    dict(
        slug="number-of-1-bits",
        title="Number of 1 Bits",
        difficulty="Easy",
        sig="def hamming_weight(n: int) -> int:",
        desc="""
Given a non-negative integer `n`, return how many `1` bits its binary representation contains.

**Constraints**
- `0 <= n <= 2^32 - 1`
""",
        hints=["`n & (n - 1)` clears the lowest set bit."],
        solution="""
def hamming_weight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
""",
        explanation="""
Use Brian Kernighan's trick: `n & (n - 1)` removes the lowest 1-bit, so the loop runs once per set bit. (`bin(n).count("1")` works in Python, but interviewers usually want the bit trick.)

- **Time:** O(number of set bits) ≤ 32
- **Space:** O(1)
""",
        examples=[([11], 3), ([128], 1), ([2147483645], 30)],
        tests=[[0], [1], [4294967295], [255], [1 << 31]],
    ),
    dict(
        slug="counting-bits",
        title="Counting Bits",
        difficulty="Easy",
        sig="def count_bits(n: int) -> List[int]:",
        desc="""
Given `n`, return a list `ans` of length `n + 1` where `ans[i]` is the number of `1` bits in `i`.

**Constraints**
- `0 <= n <= 10^5`

**Follow-up:** O(n) in a single pass, without counting the bits of each number separately?
""",
        hints=["`i >> 1` is i with its last bit removed, and you have already computed its answer."],
        solution="""
def count_bits(n: int) -> List[int]:
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans
""",
        explanation="""
Use DP on the bits: `i` has the same bits as `i >> 1` plus its lowest bit. Each entry is O(1).

- **Time:** O(n)
- **Space:** O(1) besides the output
""",
        examples=[([2], [0, 1, 1]), ([5], [0, 1, 1, 2, 1, 2])],
        tests=[[0], [1], [16], [100]],
    ),
    dict(
        slug="reverse-bits",
        title="Reverse Bits",
        difficulty="Easy",
        sig="def reverse_bits(n: int) -> int:",
        desc="""
Treat `n` as a **32-bit unsigned** integer. Reverse the order of its 32 bits and return the result as an integer.

For example, `0b00000010100101000001111010011100` becomes `0b00111001011110000010100101000000`.

**Constraints**
- `0 <= n <= 2^32 - 1`
""",
        hints=["Loop 32 times: shift the result left, add n's lowest bit, then shift n right."],
        solution="""
def reverse_bits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
""",
        explanation="""
Pop bits off the bottom of `n` and push them onto the bottom of `result`. After 32 steps the order is reversed. The fixed 32 iterations make sure leading zeros become trailing zeros.

- **Time:** O(32)
- **Space:** O(1)
""",
        examples=[([43261596], 964176192), ([4294967293], 3221225471)],
        tests=[[0], [1], [4294967295], [2], [1 << 31]],
    ),
    dict(
        slug="missing-number",
        title="Missing Number",
        difficulty="Easy",
        sig="def missing_number(nums: List[int]) -> int:",
        desc="""
`nums` contains `n` distinct numbers taken from the range `[0, n]`, so exactly one number in that range is missing. Return it.

**Constraints**
- `1 <= n <= 10^4`

**Follow-up:** O(1) extra space and O(n) time?
""",
        hints=["XOR every index 0..n with every value. Matching pairs cancel out, leaving the missing number.", "Alternatively, compute n·(n+1)/2 − sum(nums)."],
        solution="""
def missing_number(nums: List[int]) -> int:
    missing = len(nums)
    for i, x in enumerate(nums):
        missing ^= i ^ x
    return missing
""",
        explanation="""
XOR is its own inverse. XOR-ing every index `0..n` with every value cancels each present number, leaving the missing one. The arithmetic-sum formula also works, and Python has no overflow to worry about.

- **Time:** O(n)
- **Space:** O(1)
""",
        examples=[([[3, 0, 1]], 2), ([[0, 1]], 2), ([[9, 6, 4, 2, 3, 5, 7, 0, 1]], 8)],
        tests=[[[0]], [[1]], [list(range(1, 1001))], [list(range(500)) + list(range(501, 1001))]],
    ),
    dict(
        slug="sum-of-two-integers",
        title="Sum of Two Integers",
        difficulty="Medium",
        sig="def get_sum(a: int, b: int) -> int:",
        desc="""
Return `a + b` **without using the `+` or `-` operators**. (The tests can't enforce that rule; it's on your honour.)

**Constraints**
- `-1000 <= a, b <= 1000`
""",
        hints=["`a ^ b` adds the bits without carrying, and `(a & b) << 1` is the carry.", "Python ints don't have a fixed width, so mask to 32 bits and convert back to a signed value at the end."],
        solution="""
def get_sum(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    while b & mask:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    a &= mask
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
""",
        explanation="""
Repeat until there is no carry: the partial sum is `a ^ b` and the carry is `(a & b) << 1`. Because Python integers are unbounded, mask everything to 32 bits so negative numbers terminate. Then turn the 32-bit result back into a signed int (`~(a ^ mask)` when the sign bit is set).

- **Time:** O(32)
- **Space:** O(1)
""",
        examples=[([1, 2], 3), ([2, 3], 5)],
        tests=[[-1, 1], [-12, -8], [1000, -1000], [0, 0], [-2, 3], [-1000, -1000]],
    ),
]
