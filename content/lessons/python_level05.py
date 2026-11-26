# Beginner lessons for Learn Python level 5 (Functions). See python_level01.py for the style.

LESSONS = {
    "defaults-kwargs": r"""
**Overview:** a function's inputs can have fallback values, and callers can name the inputs they're giving.

### The idea
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ada")                    # 'Hello, Ada!'   greeting left out, so the fallback is used
greet("Ada", "Hi")              # 'Hi, Ada!'
greet("Ada", greeting="Hey")    # 'Hey, Ada!'     naming the input you're giving
```

- `greeting="Hello"` gives that input a fallback value (a *default*).
- `greeting="Hey"` in the call names the input (a *keyword argument*), which makes calls easier to read.
- Inputs with fallbacks must come **after** the ones without.
- A lone `*` in the inputs means everything after it **must** be named: `def banner(text, *, upper=False):`.

### Common mistakes
- **Using a list as a fallback value.** `def add(item, bag=[]):` creates that list only **once**, and every call shares it. Use `None` instead and make a new list inside:

```python
def add(item, bag=None):
    if bag is None:
        bag = []
    bag.append(item)
    return bag
```
""",
    "args-kwargs": r"""
**Overview:** one or two stars let a function accept any number of inputs.

### The idea
```python
def total(*nums):
    return sum(nums)

total(1, 2, 3)    # 6
total()           # 0
```

- One star (`*nums`) collects all the plain inputs into a tuple (*args*, short for "arguments").
- Two stars (`**details`) collect all the **named** inputs into a dict (*kwargs*, short for "keyword arguments").

```python
def profile(name, **details):
    return {"name": name, **details}

profile("Ada", city="London")    # {'name': 'Ada', 'city': 'London'}
```

### Stars in a call
The same stars work the other way when **calling** a function: they unpack a list or dict into separate inputs.

```python
nums = [1, 2, 3]
total(*nums)              # the same as total(1, 2, 3)
profile("Bo", **{"age": 4})
```

### Common mistakes
- Forgetting that `*args` arrives as a **tuple**, not a list (you can loop over it and use `len`, but not `append`).
""",
    "lambda-key": r"""
**Overview:** a `lambda` is a tiny one-line function, perfect for telling `sorted`, `min` and `max` what to compare.

### The idea
```python
double = lambda x: x * 2
double(4)     # 8
```

That's the same as `def double(x): return x * 2`, written in one line (an *anonymous function*).

### Sorting by something
`sorted`, `min` and `max` take a `key=`: a function that works out **what to compare** for each item.

```python
words = ["kiwi", "fig", "banana"]
sorted(words, key=len)                  # ['fig', 'kiwi', 'banana']   by length
max(words, key=len)                     # 'banana'
sorted(words, key=lambda w: w[-1])      # by last letter
```

### Sorting by two things
Make the key give back a tuple. Python compares the first parts, and only looks at the second parts on a tie:

```python
sorted(words, key=lambda w: (len(w), w))   # by length, then alphabetically
sorted(scores, key=lambda s: -s)           # a minus sign flips to largest first
```

### Common mistakes
- Writing `key=len()` with brackets. Pass the function itself: `key=len`.
""",
    "map-filter": r"""
**Overview:** `map` changes every item; `filter` keeps only some items.

### The idea
```python
list(map(int, ["1", "20"]))                    # [1, 20]        apply int to every item
list(map(lambda x: x * x, [1, 2, 3]))          # [1, 4, 9]
list(filter(lambda x: x > 0, [3, -1, 2]))      # [3, 2]         keep items that pass
list(filter(None, ["a", "", "b"]))             # ['a', 'b']     None means "keep truthy items"
```

Both are *lazy*: they don't do any work until you ask for the results, which is why you wrap them in `list(...)` to see them.

### When you'd use it
`map(int, ...)` is a very common way to turn a list of number-strings into numbers. For anything more complicated, a comprehension (the next lesson) is usually easier to read.

### Common mistakes
- Printing a `map` directly and seeing `<map object ...>`. Wrap it in `list(...)`.
- A `map` or `filter` can only be used **once**; after that it's empty.
""",
    "comprehensions": r"""
**Overview:** a comprehension builds a list (or dict, or set) in a single line.

### The idea
These two do exactly the same thing:

```python
squares = []
for x in [1, 2, 3]:
    squares.append(x * x)

squares = [x * x for x in [1, 2, 3]]    # [1, 4, 9]
```

Read it as: "give me `x * x` **for** each `x` **in** the list". Add an `if` at the end to keep only some items:

```python
[x for x in [3, -1, 2] if x > 0]      # [3, 2]
```

### Other kinds
```python
{w: len(w) for w in ["hi", "hello"]}    # {'hi': 2, 'hello': 5}   a dict
{len(w) for w in ["a", "bb", "cc"]}     # {1, 2}                  a set
sum(x * x for x in [1, 2, 3])           # 14   inside a call: no extra brackets
[c for row in [[1, 2], [3]] for c in row]   # [1, 2, 3]   two loops, outer first
```

That last-but-one form, in round brackets, makes items one at a time instead of building a list (a *generator expression*).

### Common mistakes
- Squeezing too much into one line. If it's hard to read, a normal loop is fine.
""",
    "recursion": r"""
**Overview:** a recursive function solves a problem by calling itself on a smaller version of the same problem.

### The idea
```python
def total(n):
    if n == 0:                 # the smallest case: answer it directly
        return 0
    return n + total(n - 1)    # otherwise: a little work + a smaller problem

total(3)    # 3 + 2 + 1 + 0 = 6
```

Every recursive function needs two parts:

1. **A stopping point** (the *base case*): the tiny version you can answer straight away.
2. **A smaller step** (the *recursive case*): do a little work, then call yourself on something smaller.

Each call must move **closer** to the stopping point, or it never ends.

### When you'd use it
Problems that contain smaller copies of themselves: nested lists, family trees, and later the tree and backtracking problems in the Blind 75.

### Common mistakes
- No stopping point, or one that's never reached. Python gives up after about 1,000 calls and raises a `RecursionError`.
""",
    "closures": r"""
**Overview:** a function can build and hand back another function that remembers values from where it was made.

### The idea
Functions are values, just like numbers: you can store them, pass them around and return them.

```python
def make_adder(n):
    def add(x):
        return x + n        # uses n from the outer function
    return add              # hand back the function itself, not its result

add5 = make_adder(5)
add5(10)    # 15
```

`add` remembers `n` even after `make_adder` has finished. A function that carries remembered values like this is called a *closure*.

### Changing a remembered value
To **change** (not just read) a variable from the outer function, say so with `nonlocal`:

```python
def make_counter():
    count = 0
    def step():
        nonlocal count
        count += 1
        return count
    return step
```

`callable(x)` tells you whether `x` can be called like a function.

### Common mistakes
- `return add()` instead of `return add`. The brackets call it straight away.
""",
    "iterators-generators": r"""
**Overview:** a generator hands out values one at a time, only when they're asked for.

### Taking items one at a time
```python
it = iter([10, 20])     # something that hands out items one by one (an *iterator*)
next(it)                # 10
next(it)                # 20
next(it, "done")        # 'done'   the fallback once it's run out
```

Without a fallback, `next` raises a `StopIteration` error when there's nothing left. A `for` loop does all of this for you behind the scenes.

### Writing your own: yield
A function that uses `yield` instead of `return` becomes a *generator*. Each `yield` hands out one value and pauses until the next one is asked for:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

list(countdown(3))    # [3, 2, 1]
```

### When you'd use it
Producing a long (or even endless) series without building a huge list in memory, and reading things piece by piece.

### Common mistakes
- Using a generator twice: once it's run out, it stays empty.
- (`aiter` and `anext` are the same ideas for *asynchronous* code, which runs several things at once; you won't need them here.)
""",
    "decorators": r"""
**Overview:** a decorator wraps a function to add extra behaviour, without changing the function's own code.

### The idea
```python
def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()   # call the original, then change its answer
    return wrapper

@shout
def greet(name):
    return f"hi {name}"

greet("ada")    # 'HI ADA'
```

- `shout` takes a function and returns a new one (the *wrapper*) that calls the original.
- `@shout` above `def greet` is shorthand for `greet = shout(greet)`.
- `*args, **kwargs` lets the wrapper accept any inputs and pass them straight on.

### When you'd use it
Adding the same extra behaviour to many functions: timing them, counting calls, retrying on errors, or remembering answers (`@cache`, in world 7, does exactly that).

### Common mistakes
- Forgetting to `return` the wrapper from the decorator, or forgetting to return the original's result from the wrapper.
""",
}
