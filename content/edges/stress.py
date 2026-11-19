# Stress tests: every task also gets hidden tests built from its examples (scripts/build_problems.py, stress_cases()):
#   "big"      every number moved up by 10**15 (floats by 10**9); not more, since JavaScript is exact only up to 2**53
#   "negative" every number moved down by 10**15
#   "long"     every string / list / dict argument stretched to ~1000 items by repeating its own contents
# A case is dropped automatically when the reference solution errors or is slow on it. STRESS_SKIP turns kinds off where the
# input would break the task's own rules, so two correct solutions could disagree (a weekday can't be 10**15, a grade can't
# be negative, two-sum must have exactly one answer). Huge values past LeetCode's stated limits are kept on purpose: a correct
# solution shouldn't depend on a sentinel like 10**4 + 1.

EDGES = {}

STRESS_SKIP = {
    # ---- Learn Python: values with a fixed range or meaning
    "py-grade": {"big", "negative"},  # a score is 0-100
    "py-is-weekend": {"big", "negative"},  # days are 1-7
    "py-zero-pad": {"big", "negative"},  # ticket numbers are 4 digits
    "py-receipt-line": "all",  # the line is exactly 20 characters
    "py-colour-code": {"big", "negative"},  # each channel is 0-255
    "py-ternary-label": {"big", "negative"},  # hour is 0-23
    "py-place-grid-paths": {"big", "negative"},  # cells are 0 (open) or 1 (rock)
    "py-change-due": {"big", "negative"},  # you always pay enough
    "py-average-of-two": {"big", "negative"},  # exact float text: (a + b) / 2 and a / 2 + b / 2 can round differently when huge
    "py-close-enough": {"big", "negative"},  # relative and absolute tolerances disagree at 10**9
    "py-namedtuple-points": {"big", "negative"},  # huge float distances can tie, so "first furthest" depends on the method
    # ---- Learn Python: counts, sizes and bit patterns that are never negative
    "py-power-of": {"negative"},  # exp is never negative
    "py-share-sweets": {"negative"},
    "py-double-until": {"negative"},
    "py-digit-sum": {"negative"},  # n is 0 or more
    "py-halvings": {"negative"},  # halving a negative number with // never reaches 0
    "py-last-n": {"negative"},  # n may be 0, not below
    "py-rotate-left": {"negative"},
    "py-review-batches-needed": {"negative"},
    "py-restock-list": {"negative"},  # stock can't be below 0
    "py-make-counter": {"negative"},  # number of calls
    "py-rate-limiter": {"negative"},
    "py-count-calls": {"negative"},
    "py-factorial": {"negative"},  # n! is defined from 0
    "py-chunks": {"negative"},  # batch size
    "py-review-throttle": {"negative"},  # cooldown
    "py-minutes-seconds": {"negative"},
    "py-average-pace": {"negative"},
    "py-to-binary": {"negative"},  # n is 0 or more
    "py-to-hex": {"negative"},
    "py-to-octal": {"negative"},
    "py-count-one-bits": {"negative"},
    "py-is-odd-bit": {"negative"},
    "py-power-of-two": {"negative"},  # sizes are positive
    "py-permission-flags": {"negative"},  # flags are bits
    "py-review-feature-flags": {"negative"},
    "py-sortable-money": {"negative"},  # "-$3.05" vs "$-3.05" isn't specified
    "py-k-smallest": {"negative"},  # k
    "py-memo-fib": {"negative"},  # n from 0 up to 300
    "py-largest-number": {"negative"},  # the numbers are non-negative
    "py-gcd-of-list": {"negative"},  # each at least 1
    "py-place-to-binary": {"negative"},
    "py-place-top-words": {"negative"},  # k
    "py-place-rain-water": {"negative"},  # wall heights
    # ---- Blind 75: inputs whose structure a shift or a repeat would break
    "two-sum": "all",  # exactly one pair must add up to target
    "top-k-frequent-elements": {"big", "negative"},  # k is at most the number of distinct values
    "container-with-most-water": {"negative"},  # heights are 0 or more
    "find-minimum-in-rotated-sorted-array": {"long"},  # a repeated rotated array isn't a rotated sorted array
    "search-in-rotated-sorted-array": {"long"},
    "kth-smallest-element-in-a-bst": {"big", "negative"},  # k is at most the number of nodes
    "lowest-common-ancestor-of-a-binary-search-tree": {"long"},  # a repeated level order isn't a BST
    "clone-graph": {"long"},  # the adjacency list numbers its nodes
    "course-schedule": {"long"},  # prerequisite pairs are distinct
    "graph-valid-tree": "all",  # n nodes numbered 0..n-1, no repeated edges
    "number-of-connected-components-in-an-undirected-graph": {"long"},  # no repeated edges
    "climbing-stairs": {"negative"},  # n is at least 1
    "house-robber": {"negative"},  # amounts are 0 or more
    "house-robber-ii": {"negative"},
    "jump-game": {"negative"},  # jump lengths are 0 or more
    "number-of-1-bits": {"big", "negative"},  # n is a 32-bit unsigned int
    "counting-bits": {"negative"},
    "reverse-bits": {"big", "negative"},  # 32-bit
    "sum-of-two-integers": {"big", "negative"},  # the bit trick works on 32-bit values
    "missing-number": "all",  # the values are 0..n with exactly one missing
}
