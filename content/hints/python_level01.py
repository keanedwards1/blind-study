# Hints for Learn Python level 1 (First steps), keyed by task slug. See content/hints/blind75.py for the rules.

HINTS = {
    # ------------------------------------------------------------------ return and + − *
    "py-one-less": [
        "Your function receives a number called `n`. Whatever comes after the word `return` is what the function hands back as its answer.",
        "The number just before another one is that number minus one. Python uses `-` for subtraction.",
        "Write `return` followed by a calculation that uses `n`. Check it on the example: for 5 you should get 4.",
    ],
    "py-double-it": [
        "\"Twice\" a number means the number multiplied by 2.",
        "Python's multiplication sign is `*` (not `x` or `×`).",
        "Return the calculation in one line. For 3 you should get 6, and for 0 you should get 0.",
    ],
    "py-rectangle-area": [
        "The area of a rectangle is its width multiplied by its height.",
        "Both values arrive as the function's inputs (its parameters), so you can use their names directly in a calculation.",
        "Return the product of the two parameters using `*`.",
    ],
    "py-change-due": [
        "First work out what you spent in total, then take that away from what you paid.",
        "The total cost is the price of one item times how many items you bought.",
        "Python does `*` before `-` (just like in maths), so you can write the whole thing in one expression. Add brackets if it makes it clearer to you.",
    ],
    # ------------------------------------------------------------------ division
    "py-average-of-two": [
        "The average of two numbers is their total divided by 2.",
        "In Python, `/` always gives a float (a number with a decimal point), which is exactly what's asked for.",
        "Add the numbers first and then divide. Without brackets, Python divides only the second number, because `/` happens before `+`.",
    ],
    "py-share-sweets": [
        "Two different questions: how many whole sweets each child gets, and how many are left over.",
        "`//` divides and throws away the remainder (whole-number division). `%` gives just the remainder.",
        "Return a list with both answers inside square brackets, in the order `[each, left_over]`. For 7 sweets and 2 kids that's `[3, 1]`.",
    ],
    "py-is-even": [
        "A number is even when dividing it by 2 leaves nothing over.",
        "`%` gives the remainder after division, and `==` checks whether two values are equal. A comparison is already `True` or `False`.",
        "Return the comparison directly; you don't need an `if`. Remember 0 is even too.",
    ],
    "py-power-of": [
        "\"Raised to the power\" means multiplying the base by itself `exp` times. For example, 2 to the power 3 is 2 × 2 × 2 = 8.",
        "Python has a power operator: two stars, `**`.",
        "Anything to the power 0 is 1, and the operator already handles that for you.",
    ],
    # ------------------------------------------------------------------ comparisons
    "py-can-vote": [
        "You need a yes/no answer, which in Python is `True` or `False`.",
        "A comparison like `x > 5` already produces `True` or `False`, so you can return it directly.",
        "Be careful at exactly 18: someone aged 18 *can* vote, so use \"greater than or equal to\", which is `>=`.",
    ],
    "py-not-equal": [
        "You're asking \"are these two numbers different?\", and the answer is `True` or `False`.",
        "Python's \"not equal\" operator is `!=` (an exclamation mark followed by an equals sign).",
        "Return the comparison itself; no `if` is needed.",
    ],
    "py-is-nonzero": [
        "Python treats every number as \"true-ish\" or \"false-ish\" (truthy or falsy): 0 counts as false, and any other number counts as true.",
        "The built-in function `bool(...)` turns a value into exactly `True` or `False` using that rule.",
        "Return the result of calling it on `n`. Negative numbers are truthy too.",
    ],
    # ------------------------------------------------------------------ if / elif / else
    "py-sign": [
        "There are three cases (positive, negative, zero), and each one returns a different number.",
        "`if` checks the first condition, `elif` (\"else if\") checks the next one, and `else` catches everything left over.",
        "Check `n > 0` first, then `n < 0`; whatever is left must be zero. Note that 0 is neither positive nor negative.",
    ],
    "py-grade": [
        "Check the grades from the top down: once a score is 90 or more you know it's an A, and you don't need to check anything else.",
        "Use `if` for the first band and `elif` for the following ones. Each branch returns its letter, which is text in quotes.",
        "Because you check from the top, the B test only needs `score >= 80`: anything 90 or more was already caught by the A test. Mind the edges: exactly 90 is an A, exactly 80 a B.",
    ],
    "py-fizzbuzz-one": [
        "\"Divisible by 3\" means dividing by 3 leaves no remainder, so `n % 3 == 0`.",
        "Order matters. Check \"divisible by both\" first, because 15 is also divisible by 3 and by 5 on its own. (Divisible by both 3 and 5 is the same as divisible by 15.)",
        "If none of the checks match, return the number as text. `str(...)` turns a number into a string.",
    ],
    # ------------------------------------------------------------------ and / or / not
    "py-in-range": [
        "\"Between `lo` and `hi`, including both ends\" means `x` is at least `lo` AND at most `hi`.",
        "You can join two comparisons with `and`. Python also lets you chain them like maths: `a <= b <= c`.",
        "Use `<=` (not `<`) on both sides, so the ends themselves count.",
    ],
    "py-is-weekend": [
        "The weekend is day 6 or day 7. Any other day isn't.",
        "`or` is `True` when at least one side is `True`.",
        "Compare `day` with each weekend number using `==` and join the two comparisons with `or`. (Writing `day == 6 or 7` is a common mistake: the `7` on its own is always truthy.)",
    ],
    "py-exactly-one": [
        "There are four combinations of two booleans. You want `True` only for (True, False) and (False, True).",
        "Put another way: at least one is true (`or`), and they're not both true (`not` combined with `and`).",
        "Combine those two ideas with `and`. Use brackets so Python groups them the way you mean.",
    ],
    # ------------------------------------------------------------------ conversions
    "py-add-one-text": [
        "The input is text (a string), and you can't add 1 to text: `\"41\" + 1` is an error.",
        "`int(...)` turns text made of digits into a whole number.",
        "Convert first, then add one, and return the number (not text).",
    ],
    "py-number-to-text": [
        "You need the same digits, but as text (a string) instead of a number.",
        "`str(...)` turns any value into its text form.",
        "Return the result of calling `str` on `n`. Negative numbers keep their minus sign.",
    ],
    "py-chop-decimals": [
        "You want to drop everything after the decimal point, without rounding up or down.",
        "`int(...)` on a float does exactly that: it cuts the decimals off (truncation, towards zero).",
        "That's why `-2.7` becomes `-2`, not `-3`. `round` would give a different answer, so don't use it here.",
    ],
    "py-text-times-two": [
        "The input is text that looks like a decimal number, such as `\"2.5\"`.",
        "`float(...)` turns that text into a decimal number you can do maths with. (`int` would fail, because of the decimal point.)",
        "Convert it first, then multiply by 2, and return the float.",
    ],
    # ------------------------------------------------------------------ abs, round, min, max
    "py-distance": [
        "The distance between two numbers is their difference, but distance is never negative.",
        "`abs(...)` (absolute value) removes a minus sign: `abs(-4)` is `4`.",
        "Subtract one number from the other and wrap the result in `abs`. Then the order you subtract in doesn't matter.",
    ],
    "py-round-price": [
        "Prices have two decimal places, so round to 2 places.",
        "`round(value, digits)` rounds to that many decimal places. With only one argument it rounds to a whole number, which isn't what you want here.",
        "Pass `x` and the number of decimal places, and return the result.",
    ],
    "py-largest-of-three": [
        "You need whichever of the three numbers is biggest.",
        "`max(...)` accepts as many numbers as you like, separated by commas, and returns the largest.",
        "One call with all three inputs is enough. Negative numbers work too.",
    ],
    "py-clamp": [
        "Two limits: the answer can't go above `hi`, and it can't go below `lo`.",
        "`min(x, hi)` keeps a number from going above `hi` (it picks the smaller of the two). `max(..., lo)` keeps it from going below `lo`.",
        "Apply one limit, then apply the other to that result, by putting one call inside the other. Test all three cases: below, inside and above the range.",
    ],
    # ------------------------------------------------------------------ print
    "py-say-hello": [
        "This task checks what you *print* on the screen, not what you return.",
        "`print(...)` shows text. You can join pieces of text with `+`: the greeting, the name, then the exclamation mark.",
        "Watch the exact output: `Hello, ` has a comma and a space after it, and the `!` comes straight after the name with no space.",
    ],
    "py-two-lines": [
        "Each `print` call finishes with a new line automatically.",
        "So printing one thing and then printing the other puts them on separate lines.",
        "Use two `print` calls, `a` first and then `b`.",
    ],
    "py-dashed": [
        "When you give `print` several values separated by commas, it puts a space between them by default.",
        "The `sep=` option changes what goes between the values, for example `sep=\"*\"`.",
        "Print all three numbers in one call and set the separator to a dash.",
    ],
    "py-same-line": [
        "Normally each `print` ends with a new line. Here the first one mustn't.",
        "The `end=` option changes what `print` adds at the very end; an empty string `\"\"` adds nothing.",
        "Give the first `print` an empty ending and leave the second one as normal, so the line still ends after `b`.",
    ],
    # ------------------------------------------------------------------ input
    "py-echo-name": [
        "`input()` waits for one line of typed text and gives it back as a string. The tests type the name for you.",
        "Store what `input()` returns in a variable, then print a greeting with it.",
        "`print` with two values separated by a comma puts exactly one space between them, which matches `Hello Ada`.",
    ],
    "py-add-inputs": [
        "Read two lines with two `input()` calls; each one gives you text.",
        "Text doesn't add up like numbers do (`\"2\" + \"3\"` is `\"23\"`), so convert each line with `int(...)` first.",
        "Then print the sum of the two numbers.",
    ],
}
