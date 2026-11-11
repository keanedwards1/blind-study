CATEGORY = "Stack"

PROBLEMS = [
    dict(
        slug="valid-parentheses",
        title="Valid Parentheses",
        difficulty="Easy",
        sig="def is_valid(s: str) -> bool:",
        desc="""
Given a string `s` made only of the characters `()[]{}`, return `True` if the brackets are balanced:

- every opening bracket is closed by the same type of bracket,
- brackets close in the correct order, and
- every closing bracket has a matching opener.

**Constraints**
- `0 <= len(s) <= 10^4`
""",
        hints=["Push openers onto a stack. A closer must match the top of the stack."],
        solution="""
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()
        else:
            stack.append(c)
    return not stack
""",
        explanation="""
A stack holds the unmatched openers. Each closer must match the most recent opener; at the end the stack must be empty.

- **Time:** O(n)
- **Space:** O(n)
""",
        examples=[(["()"], True), (["()[]{}"], True), (["(]"], False), (["([])"], True)],
        tests=[[""], ["("], ["]"], ["([)]"], ["{[]}"], ["((()))[]{}"], ["){"]],
    ),
]
