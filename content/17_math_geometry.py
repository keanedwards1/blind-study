CATEGORY = "Math & Geometry"

PROBLEMS = [
    dict(
        slug="rotate-image",
        title="Rotate Image",
        difficulty="Medium",
        sig="def rotate(matrix: List[List[int]]) -> None:",
        mutate=0,
        desc="""
Rotate an `n x n` matrix **90° clockwise, in place**. Modify `matrix` directly instead of building a new one. The tests check `matrix` after your function returns.

**Constraints**
- `1 <= n <= 20`
""",
        hints=["A clockwise rotation equals a transpose followed by reversing each row."],
        solution="""
def rotate(matrix: List[List[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
""",
        explanation="""
Transpose (swap across the main diagonal), then reverse every row. Both steps are in place. Rotating four cells at a time layer by layer also works.

- **Time:** O(n²)
- **Space:** O(1)
""",
        examples=[([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]), ([[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]], [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])],
        tests=[[[[1]]], [[[1, 2], [3, 4]]], [[[i * 5 + j for j in range(5)] for i in range(5)]]],
    ),
    dict(
        slug="spiral-matrix",
        title="Spiral Matrix",
        difficulty="Medium",
        sig="def spiral_order(matrix: List[List[int]]) -> List[int]:",
        desc="""
Return all elements of an `m x n` matrix in **clockwise spiral order**, starting at the top-left corner.

**Constraints**
- `1 <= m, n <= 10`
""",
        hints=["Keep four boundaries (top, bottom, left, right) and shrink one after walking each side."],
        solution="""
def spiral_order(matrix: List[List[int]]) -> List[int]:
    result = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1
    return result
""",
        explanation="""
Walk the top row, right column, bottom row, then left column, shrinking the matching boundary after each. The two `if` checks stop single rows or columns from being visited twice.

- **Time:** O(m · n)
- **Space:** O(1) besides the output
""",
        examples=[([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [1, 2, 3, 6, 9, 8, 7, 4, 5]), ([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])],
        tests=[[[[1]]], [[[1], [2], [3]]], [[[1, 2, 3]]], [[[1, 2], [3, 4], [5, 6]]], [[[i * 4 + j for j in range(4)] for i in range(4)]]],
    ),
    dict(
        slug="set-matrix-zeroes",
        title="Set Matrix Zeroes",
        difficulty="Medium",
        sig="def set_zeroes(matrix: List[List[int]]) -> None:",
        mutate=0,
        desc="""
Given an `m x n` integer matrix, wherever an element is `0`, set its **entire row and column** to `0`. Modify `matrix` in place; the tests check it after your function returns.

**Constraints**
- `1 <= m, n <= 200`

**Follow-up:** can you do it with O(1) extra space?
""",
        hints=["First record which rows and columns contain a zero, then zero them out in a second pass.", "For O(1) space, use the first row and first column as the markers (and track row 0 separately)."],
        solution="""
def set_zeroes(matrix: List[List[int]]) -> None:
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    for r in range(1, rows):
        for c in range(cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if matrix[0][0] == 0:
        for r in range(rows):
            matrix[r][0] = 0
    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0
""",
        explanation="""
Use the first row and first column as marker storage. Remember up front whether row 0 itself had a zero. Mark from rows 1 onward, zero the interior using the markers, then handle column 0 (via `matrix[0][0]`) and finally row 0.

- **Time:** O(m · n)
- **Space:** O(1)

The simpler version with two sets of row/column indices uses O(m + n) space and is a fine first answer.
""",
        examples=[([[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]), ([[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])],
        tests=[[[[1]]], [[[0]]], [[[1, 0]]], [[[1], [0], [1]]], [[[1, 2, 3, 4], [5, 0, 7, 8], [0, 10, 11, 12], [13, 14, 15, 0]]]],
    ),
]
