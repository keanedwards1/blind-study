# Beginner lessons for Learn Python level 3 (Loops & lists). See python_level01.py for the style.

LESSONS = {
    "for-loops": r"""
**In one sentence:** a `for` loop repeats some lines once for every item in a list (or every character in some text).

### The idea
```python
total = 0
for x in [3, 1, 4]:
    total += x
print(total)    # 8
```

The indented line runs three times. The first time, `x` is 3; then 1; then 4. (`x` is the *loop variable*; you choose its name.)

`total += x` is short for `total = total + x`: "add `x` to the total".

### The running-total pattern
Most loops follow the same three steps (often called the *accumulator pattern*):

1. **Before** the loop, set up a variable: `total = 0`, `count = 0`, `best = items[0]` or `result = []`.
2. **Inside** the loop, update it a little each time.
3. **After** the loop, use it, usually by returning it.

Looping over text gives you one character at a time: `for ch in "hi":` runs with `"h"`, then `"i"`.

### Common mistakes
- Putting `return` inside the loop, so the function stops after the first item. Return after the loop finishes (one level less indented).
- Setting the running total up *inside* the loop, which resets it every time.
""",
    "range": r"""
**In one sentence:** `range` produces a row of numbers to count with.

### The idea
```python
range(5)          # 0, 1, 2, 3, 4      starts at 0, stops BEFORE 5
range(2, 6)       # 2, 3, 4, 5         start, stop
range(0, 10, 3)   # 0, 3, 6, 9         start, stop, step
range(5, 0, -1)   # 5, 4, 3, 2, 1      a negative step counts down
```

The stop number is never included, just like slicing.

`for i in range(3):` repeats something 3 times. `range` hands out its numbers one at a time; `list(range(3))` collects them into the list `[0, 1, 2]`.

### When you'd use it
Repeating something a fixed number of times, counting from 1 to `n`, or going through positions `0, 1, 2, …` of a list.

### Common mistakes
- **Off by one.** To count from 1 up to and including `n`, write `range(1, n + 1)`.
- Expecting `range(5)` to be a list. Wrap it in `list(...)` if you need one.
""",
    "while-break": r"""
**In one sentence:** a `while` loop keeps going as long as something stays true; `break` and `continue` let you jump out early.

### The idea
Use `while` when you don't know in advance how many rounds you'll need:

```python
n = 345
digits = 0
while n > 0:
    n //= 10        # chop off the last digit
    digits += 1
print(digits)       # 3
```

Something inside the loop **must** change the condition, or it runs forever (an *infinite loop*).

### break and continue
- `break` leaves the loop immediately.
- `continue` skips the rest of this round and moves on to the next one.

```python
for x in [1, 2, 3, 4]:
    if x == 2:
        continue      # skip 2
    if x == 4:
        break         # stop before 4
    print(x)          # prints 1, then 3
```

Both work in `for` loops as well as `while` loops.

### Common mistakes
- Forgetting to update the thing the condition checks, so the loop never ends.
""",
    "list-methods": r"""
**In one sentence:** lists can grow, shrink and be rearranged, using methods.

### The idea
A list holds several values in order: `[3, 1, 2]`. Unlike text, a list **can be changed** after it's made (it's *mutable*).

| Write | Does |
|---|---|
| `a.append(x)` | add `x` to the end |
| `a.extend([x, y])` | add every item of another list to the end |
| `a.insert(0, x)` | add `x` at a position (0 is the front) |
| `a.pop()` | remove the last item **and give it back** |
| `a.remove(x)` | remove the first `x` (crashes if it isn't there) |
| `a.index(x)` | the position of the first `x` |
| `a.count(x)` | how many times `x` appears |
| `a.sort()` | sort the list itself, smallest first |
| `a.reverse()` | reverse the list itself |

### Changing in place
Most of these change the list **itself** (they work *in place*) and give back nothing (`None`). Tasks marked "in place" want exactly that: change the list you were given, and don't return anything.

### Common mistakes
- `a = a.sort()`. `sort` gives back `None`, so now `a` is `None`. Write `a.sort()` on its own line.
- `a.append([4, 5])` adds the whole list as **one** item. Use `extend` to add its items.
""",
    "list-slicing": r"""
**In one sentence:** lists slice exactly like text, and a slice is a brand-new copy.

### The idea
```python
a = [10, 20, 30, 40]
a[1:3]    # [20, 30]
a[-2:]    # [30, 40]          the last two
a[::-1]   # [40, 30, 20, 10]  reversed
a[:]      # [10, 20, 30, 40]  a full copy
```

### Copying versus sharing
This is one of the most important ideas in Python.

```python
a = [1, 2]
b = a        # NOT a copy: both names point at the same list
b[0] = 99
print(a)     # [99, 2]   a changed too!

c = a[:]     # a real copy
c[0] = 0
print(a)     # [99, 2]   a is untouched
```

When two names point at the same list, that's called *aliasing*. A slice (`a[:]`) or `list(a)` makes a separate copy.

### The slice object
`slice(1, 3)` packages a slice up so you can store it: `a[slice(1, 3)]` is the same as `a[1:3]`. `None` means "leave this part out".

### Common mistakes
- `a[-0:]` is the **whole** list, because `-0` is just `0`.
""",
    "enumerate-zip": r"""
**In one sentence:** `enumerate` gives you each item with its position; `zip` walks two lists side by side.

### The idea
```python
for i, fruit in enumerate(["fig", "kiwi"]):
    print(i, fruit)        # 0 fig, then 1 kiwi

for i, fruit in enumerate(["fig", "kiwi"], start=1):
    print(i, fruit)        # 1 fig, then 2 kiwi

for name, score in zip(["Ada", "Bo"], [90, 75]):
    print(name, score)     # Ada 90, then Bo 75
```

- `enumerate` hands out `(position, item)` pairs, and the `for` line unpacks each pair into two names.
- `zip` pairs up the first items, then the second items, and so on. It stops at the end of the **shorter** list.

### When you'd use it
Numbering a list, finding the position of something, or combining two lists that belong together (names and scores).

### Common mistakes
- Writing `for i in range(len(items)):` and then `items[i]` everywhere. It works, but `enumerate` is clearer and harder to get wrong.
""",
    "list-builtins": r"""
**In one sentence:** Python has ready-made functions for the loops you'd write all the time.

### The idea
```python
nums = [3, 1, 2]
sum(nums)                    # 6          (0 for an empty list)
sorted(nums)                 # [1, 2, 3]  a NEW sorted list
sorted(nums, reverse=True)   # [3, 2, 1]  largest first
list(reversed(nums))         # [2, 1, 3]  backwards
min(nums), max(nums)         # 1, 3
```

### sorted() versus .sort()
- `sorted(nums)` makes a **new** list and leaves `nums` alone. It works on any group of items, even text.
- `nums.sort()` rearranges `nums` **itself** and gives back nothing (`None`).

Use `sorted` when you must not change the original.

### Common mistakes
- `min([])` and `max([])` crash on an empty list (a `ValueError`). Check the list isn't empty first.
- Forgetting `list(...)` around `reversed(...)`: on its own it gives a "reversed view", not a list.
""",
    "any-all": r"""
**In one sentence:** `any` asks "is at least one true?" and `all` asks "is every one true?".

### The idea
```python
any([False, True, False])   # True    at least one is true
all([True, True, False])    # False   not every one is true
all([])                     # True    nothing failed
any([])                     # False   nothing passed
```

They get really useful with a small loop written inside the brackets (a *generator expression*; you'll study these properly in world 5):

```python
nums = [4, 8, 15]
all(x > 0 for x in nums)          # True: every number is positive
any(x > 10 for x in nums)         # True: at least one is over 10
any(ch.isdigit() for ch in "a1")  # True: there's a digit
```

### Common mistakes
- Being surprised by empty lists: `all([])` is `True` and `any([])` is `False`.
""",
    "nested": r"""
**In one sentence:** a grid is a list of rows, and a loop inside a loop visits every cell.

### The idea
```python
grid = [[1, 2, 3],
        [4, 5, 6]]
grid[1][2]       # 6    row 1, then column 2
len(grid)        # 2    the number of rows
len(grid[0])     # 3    the number of columns
```

To visit every cell, put one loop inside another (*nested loops*):

```python
for row in grid:
    for value in row:
        print(value)     # 1, 2, 3, 4, 5, 6
```

### Building a grid
```python
rows, cols = 2, 3
grid = [[0] * cols for _ in range(rows)]   # [[0, 0, 0], [0, 0, 0]]
```

### Common mistakes
- `[[0] * cols] * rows` looks right, but it repeats the **same** row list several times, so changing one row changes them all. Build each row separately, as above.
""",
}
