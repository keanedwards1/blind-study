# Hints for Learn Python level 3 (Loops & lists), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ for loops
    "py-loop-sum": [
        "Keep a running total that starts at 0, and add each number to it as you go.",
        "`for x in nums:` runs the indented lines once for each item, with `x` set to that item.",
        "Inside the loop, add the current item to the total (`+=` adds to a variable). Return the total *after* the loop finishes, not inside it.",
    ],
    "py-count-negatives": [
        "You're counting, so start a counter at 0.",
        "Loop over the numbers, and use an `if` inside the loop to check whether the current number is below zero.",
        "Only add 1 to the counter when the check passes. Zero isn't negative.",
    ],
    "py-loop-max": [
        "Keep track of the biggest number you've seen so far.",
        "Start with the first item (`nums[0]`) as your best guess, not with 0: if every number is negative, 0 would be wrong.",
        "Loop over every number; whenever one is bigger than your current best, it becomes the new best.",
    ],
    "py-count-letter": [
        "A `for` loop over a string gives you one character at a time.",
        "Start a counter at 0 and compare each character with `letter` using `==`.",
        "Add 1 for each match. Upper and lower case are different characters, so `\"A\"` doesn't match `\"a\"`.",
    ],
    # ------------------------------------------------------------------ range
    "py-one-to-n": [
        "`range(start, stop)` counts from `start` up to, but **not including**, `stop`.",
        "To include `n` itself, the stop needs to be one more than `n`.",
        "`range` gives numbers one at a time; wrap it in `list(...)` to get an actual list. When `n` is 0 it's empty automatically.",
    ],
    "py-evens-up-to": [
        "Even numbers go 0, 2, 4, …, which is counting in steps of 2.",
        "`range` takes an optional third number, the step: `range(start, stop, step)`.",
        "Start at 0, step by 2, and make the stop one past `n` so that `n` is included when it's even. Wrap it in `list(...)`.",
    ],
    "py-countdown-list": [
        "Counting down means a step of `-1`.",
        "With a negative step, `range` stops *before* reaching the stop value, just as it does going up.",
        "Start at `n` and stop at 0 so the last number is 1. Wrap it in `list(...)`.",
    ],
    "py-sum-of-squares": [
        "You need 1×1 + 2×2 + … + n×n: loop over the numbers from 1 to `n`.",
        "`range(1, n + 1)` gives exactly 1 to `n`.",
        "Keep a running total, and add each number multiplied by itself.",
    ],
    "py-multiplication-row": [
        "This task checks what you print: five lines, for 1 to 5.",
        "Loop over `range(1, 6)` and print one line per number.",
        "An f-string makes the line easy: put the loop number, the `n` and their product inside braces. Match the spacing exactly: `1 x 3 = 3`.",
    ],
    # ------------------------------------------------------------------ while, break, continue
    "py-digit-sum": [
        "`% 10` gives the last digit of a number (`123 % 10` is 3), and `// 10` removes the last digit (`123 // 10` is 12).",
        "A `while` loop keeps going as long as its condition is true; here, as long as there are digits left (the number is above 0).",
        "Each time round: add the last digit to a total, then chop it off. When `n` is 0 the total is 0.",
    ],
    "py-first-negative": [
        "Walk through the positions with a counter that starts at 0.",
        "`break` jumps straight out of the loop, so you can stop the moment you find a negative number.",
        "After the loop, work out whether you stopped early (found one) or ran off the end (none found, so the answer is `-1`).",
    ],
    "py-halvings": [
        "Count how many times you can do `n //= 2` before `n` becomes 0.",
        "A `while` loop with a step counter: keep halving while `n` is above 0, adding 1 each time.",
        "Check the example: 8 → 4 → 2 → 1 → 0 is 4 halvings. Starting at 0, the answer is 0.",
    ],
    "py-sum-skip-negatives": [
        "Add up the numbers, but leave the negative ones out.",
        "`continue` skips the rest of the loop body for this item and moves straight on to the next one.",
        "At the top of the loop, if the number is negative, `continue`. Otherwise add it to the total.",
    ],
    # ------------------------------------------------------------------ list methods
    "py-add-to-end": [
        "\"In place\" means changing the list you were given, not making a new one. The function returns nothing.",
        "Lists have a method that adds one item to the end.",
        "Call `append` on `items`. Don't write `items = ...` and don't `return` anything.",
    ],
    "py-add-to-front": [
        "There's no `append` for the front, but there is a method that adds an item at any position.",
        "`.insert(position, item)` puts `item` at that position and shifts everything else along.",
        "Position 0 is the very front.",
    ],
    "py-join-lists": [
        "You want every item of `b` added to the end of `a`, changing `a` itself.",
        "`.append(b)` would add the whole list `b` as one single item. `.extend(b)` adds its items one by one.",
        "Call `extend` on `a`, passing `b`. Don't return anything.",
    ],
    "py-remove-value": [
        "`.remove(x)` deletes the first `x` it finds, but it crashes (raises an error) if `x` isn't in the list.",
        "Check first with `x in items`.",
        "Only call `remove` when the check passes; otherwise do nothing.",
    ],
    "py-pop-last": [
        "You need to take the last item out of the list *and* give it back.",
        "`.pop()` does both: it removes the last item and returns it.",
        "Return what `pop` gives you.",
    ],
    "py-sort-in-place": [
        "Sort the list itself (in place) rather than making a sorted copy.",
        "`.sort()` sorts a list in place, smallest first by default.",
        "Pass `reverse=True` to get largest first. `.sort()` returns `None`, so don't return its result.",
    ],
    "py-position-and-count": [
        "Two answers: where `x` first appears, and how many times it appears.",
        "`.index(x)` gives the first position; `.count(x)` counts occurrences.",
        "Return both inside a list, position first.",
    ],
    # ------------------------------------------------------------------ list slicing
    "py-last-n": [
        "A slice starting `n` places from the end gives the last `n` items.",
        "The start position for the last `n` items is the length minus `n`. Slices that go past the start of the list just begin at the beginning.",
        "Watch out for `n == 0`: a slice starting at `-0` is the same as starting at 0, which gives the *whole* list. Handle 0 separately.",
    ],
    "py-copy-then-change": [
        "If you write `copy = items`, both names point at the **same** list (no copy is made), so changing one changes the other.",
        "A full slice `[:]` makes a real, separate copy of a list.",
        "Copy, change the copy's first item to 0, then return both lists. The original must stay as it was.",
    ],
    "py-apply-slice": [
        "A slice like `items[1:5:2]` can also be described as an object: `slice(1, 5, 2)`.",
        "`None` in a slice object means \"use the default\", just like leaving a number out of `a[::]`.",
        "Build a `slice` from the three inputs and use it inside square brackets.",
    ],
    "py-rotate-left": [
        "Rotating left by `k` = the items from position `k` onward, followed by the first `k` items.",
        "If `k` is bigger than the list, rotating by the length brings you back to the start, so only the remainder matters: `k % len(items)`.",
        "Use two slices and join them with `+`. An empty list needs special care, because `% 0` is an error.",
    ],
    # ------------------------------------------------------------------ enumerate and zip
    "py-numbered-list": [
        "You need each item together with its number.",
        "`enumerate(items)` gives `(position, item)` pairs. `start=1` makes the counting begin at 1 instead of 0.",
        "Loop over those pairs, build each string with an f-string (number, dot, space, item) and add it to a result list.",
    ],
    "py-even-positions": [
        "You need each item's position to decide whether to keep it.",
        "`for i, x in enumerate(items):` gives the position `i` and the item `x` together.",
        "Keep the item when its position is even (`% 2` leaves 0).",
    ],
    "py-pairwise-sum": [
        "Add the first items together, then the second items, and so on.",
        "`zip(a, b)` walks both lists side by side, giving pairs `(a item, b item)`, and stops at the shorter list.",
        "Loop over those pairs and add each pair's sum to a result list.",
    ],
    "py-count-matches": [
        "Compare the two strings position by position.",
        "`zip` pairs up characters from both strings and stops at the shorter one, which is exactly what's asked.",
        "Count the pairs where the two characters are equal. A counter in a loop works, or `sum` over a generator of 1s.",
    ],
    "py-index-pairs": [
        "Each name goes with the score at the same position.",
        "`zip(names, scores)` gives you `(name, score)` pairs.",
        "Turn each pair into `\"NAME: SCORE\"` with an f-string and collect them in a list.",
    ],
    # ------------------------------------------------------------------ sum, sorted, reversed
    "py-average-list": [
        "Average = total ÷ how many numbers there are.",
        "`sum(...)` and `len(...)` give you those two numbers.",
        "An empty list would divide by zero, so return `0.0` for it first.",
    ],
    "py-top-three": [
        "Sort the scores from highest to lowest, then take the first three.",
        "`sorted(...)` returns a *new* sorted list and leaves the original alone; `reverse=True` sorts highest first.",
        "A slice of the first three items is safe even when there are fewer than three.",
    ],
    "py-reversed-list": [
        "`reversed(items)` walks the list backwards, but it gives you a reversed *view*, not a list.",
        "Wrap it in `list(...)` to turn it into a real new list.",
        "The original list must stay unchanged, so don't call `.reverse()` on it.",
    ],
    "py-median": [
        "The median is the middle value of the *sorted* numbers, so sort first (with `sorted`, which doesn't change the input).",
        "The middle index is the length divided by 2 (whole-number division).",
        "Odd length: return the value at the middle. Even length: average the two middle values (the one at the middle index and the one just before it).",
    ],
    "py-range-of-values": [
        "The spread is the gap between the biggest and smallest numbers.",
        "`max(...)` and `min(...)` both work on a whole list.",
        "Subtract the smallest from the largest. A list with one number has a spread of 0.",
    ],
    # ------------------------------------------------------------------ any and all
    "py-no-zeros": [
        "0 is \"falsy\" (counts as false), and every other number is \"truthy\".",
        "`all(...)` is `True` only if every item is truthy.",
        "So passing the list straight to `all` answers the question. An empty list counts as `True`.",
    ],
    "py-all-positive": [
        "For each number, ask \"is it greater than 0?\"",
        "A generator expression like `(check for x in nums)` produces one `True` or `False` per number.",
        "Pass that to `all(...)`. Zero isn't positive.",
    ],
    "py-has-digit": [
        "You need just one digit anywhere in the string.",
        "`any(...)` is `True` if at least one item is true; `c.isdigit()` tests a single character.",
        "Check each character with `isdigit` inside `any`.",
    ],
    "py-strong-password": [
        "Four separate rules, and all of them must hold.",
        "The length rule uses `len`. The other three each need \"at least one character that…\", which is `any(...)` with `isdigit`, `isupper` or `islower`.",
        "Join the four checks with `and`. A long expression can be wrapped in brackets so it can span lines.",
    ],
    # ------------------------------------------------------------------ nested loops
    "py-grid-total": [
        "A grid is a list of rows, and each row is a list of numbers.",
        "Use a loop inside a loop: the outer one goes over the rows, the inner one over the numbers in the current row.",
        "Add every number to one running total.",
    ],
    "py-row-sums": [
        "Each row is just a list of numbers.",
        "`sum(row)` adds up one row.",
        "Do that for every row and collect the results in a list (a loop with `append`, or a list comprehension).",
    ],
    "py-column-sums": [
        "Column `c` is made of item `c` from every row.",
        "Start with one running total per column: a list of zeros as long as a row.",
        "Loop over the rows, and inside that loop over each row's items with their positions (`enumerate`), adding each item to its column's total.",
    ],
    "py-make-grid": [
        "Build the grid one row at a time.",
        "The outer loop counts rows; for each row, an inner loop counts columns and builds that row's list.",
        "Each cell holds row number × column number. Append the finished row to the grid after the inner loop ends.",
    ],
}
