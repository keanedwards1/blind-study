# Beginner lessons for Learn Python level 4 (Dicts, sets & tuples). See python_level01.py for the style.

LESSONS = {
    "dict-basics": r"""
**In one sentence:** a dict is a lookup table: you give it a name (a key) and it gives you back what's stored under it (a value).

### The idea
Think of a price board at a market: each item name points to a price.

```python
prices = {"jam": 5, "tea": 3}
prices["jam"]          # 5         look up a key
prices["bun"] = 2      # add a new key (or replace an existing one)
"tea" in prices        # True      is this key on the board?
```

This kind of table is called a *dictionary*, or *dict*. The left side of each pair is the *key*, the right side is the *value*.

### Missing keys and .get()
Asking for a key that isn't there with square brackets **crashes** (Python raises a `KeyError`). `.get()` is the safe way to ask:

```python
prices.get("tea")        # 3
prices.get("cake")       # None    no crash; None means "nothing"
prices.get("cake", 0)    # 0       your own fallback (a *default*)
```

### The counting pattern
The most useful three lines in Python:

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1
# counts is {"a": 2, "b": 1}
```

Read it as: "look up the count so far (0 if this is the first time), add one, and store it back".

### Why dicts are fast
Looking up a key takes about the same time whether the dict has 10 keys or 10 million (*constant time*, written *O(1)*). That's why dicts turn slow searches into fast ones.

### Common mistakes
- `"jam" in prices` checks the **keys**, never the values.
""",
    "dict-methods": r"""
**In one sentence:** dicts come with tools for listing, removing and merging what's inside them.

### The idea
```python
d = {"a": 1, "b": 2}
list(d.keys())      # ['a', 'b']
list(d.values())    # [1, 2]
list(d.items())     # [('a', 1), ('b', 2)]   key-value pairs
for k, v in d.items():
    print(k, v)     # a 1, then b 2
```

| Write | Does |
|---|---|
| `d.pop("a")` | removes the key and gives back its value |
| `d.pop("z", None)` | same, but gives `None` instead of crashing if it's missing |
| `d.update(other)` | copies every key from `other` into `d`, replacing matches |
| `d.setdefault(k, [])` | gives back `d[k]`, first creating it as `[]` if it's missing |
| `dict(zip(keys, values))` | builds a dict from two matching lists |

Dicts **remember the order** keys were added, and looping over a dict gives you its keys.

### Grouping with setdefault
```python
groups = {}
for word in ["apple", "bean", "avocado"]:
    groups.setdefault(word[0], []).append(word)
# {"a": ["apple", "avocado"], "b": ["bean"]}
```

### Common mistakes
- Changing a dict's size (adding or removing keys) while looping over it is an error. Loop over `list(d)` instead.
""",
    "sets": r"""
**In one sentence:** a set is a bag that holds each value only once, and can tell you instantly whether something is inside.

### The idea
```python
s = {3, 1, 3, 2}
print(s)             # {1, 2, 3}   the repeat is gone
len(set("hello"))    # 4           h, e, l, o
2 in s               # True
```

A set has **no order** and **no repeats**.

| Write | Does |
|---|---|
| `set(items)` | makes a set from a list (removing duplicates) |
| `s.add(x)` | adds a value |
| `s.remove(x)` | removes it (crashes if it isn't there) |
| `s.discard(x)` | removes it if it's there, no crash |

### Why sets are fast
Asking `x in some_list` checks every item one by one. Asking `x in some_set` is instant, however big it gets (*constant time*). If you check "have I seen this?" a lot, use a set.

### Common mistakes
- `{}` makes an empty **dict**, not an empty set. Write `set()`.
- Expecting a set to keep the order you added things in. It doesn't; sort it if you need order.
""",
    "set-operations": r"""
**In one sentence:** sets can be combined like Venn diagrams: in both, in either, in one but not the other.

### The idea
```python
a = {1, 2, 3}
b = {3, 4}
a & b      # {3}            in both          (the *intersection*)
a | b      # {1, 2, 3, 4}   in either        (the *union*)
a - b      # {1, 2}         in a, not b      (the *difference*)
a ^ b      # {1, 2, 4}      in exactly one   (the *symmetric difference*)
{1, 2} <= a   # True        is everything on the left also in a? (a *subset*)
```

Each one also has a method name if you prefer words: `a.intersection(b)`, `a.union(b)`, `a.difference(b)`, `a.issubset(b)`.

### When you'd use it
Which guests haven't arrived (`invited - arrived`), which products two shops share (`a & b`), whether you have every ingredient (`needed <= have`).

### Common mistakes
- Trying these operators on lists: `[1, 2] & [2]` is an error. Turn the lists into sets first.
""",
    "tuples": r"""
**In one sentence:** a tuple is a small, fixed bundle of values that can't be changed.

### The idea
```python
point = (3, 4)
point[0]          # 3
x, y = point      # unpack it into two names: x is 3, y is 4
```

A *tuple* is like a list that's been sealed: you can read it, but not change it (it's *immutable*).

### Unpacking tricks
```python
a, b = 1, 2
a, b = b, a                 # swap in one line: now a is 2, b is 1
first, *rest = [1, 2, 3]    # first is 1, rest is [2, 3]
```

Functions often return several values as a tuple: `return low, high`.

### When you'd use it
For a small group of values that belong together and won't change: a point, an `(item, price)` pair, an RGB colour. Because they can't change, tuples can be dict keys or go in a set; lists can't.

### Common mistakes
- A one-item tuple needs a comma: `(5,)`. Without it, `(5)` is just the number 5.
""",
    "hashing": r"""
**In one sentence:** only values that can't change can be dict keys or go in a set.

### The idea
Dicts and sets find things fast by turning each value into a number first (its *hash*, made with `hash(x)`). If a value could change after being stored, its number would change too and Python would lose track of it. So only unchangeable values are allowed (values that can be hashed are called *hashable*).

| Allowed as a key / in a set | Not allowed |
|---|---|
| numbers, text, tuples, `frozenset` | lists, dicts, sets |

```python
{(1, 2): "corner"}       # fine: a tuple key
{[1, 2]: "corner"}       # error: lists aren't hashable
tuple([1, 2])            # (1, 2): convert a list so it can be a key
```

### frozenset
A `frozenset` is a set that can't be changed, so it **can** be a dict key: handy for grouping words by which letters they use.

```python
frozenset("listen") == frozenset("silent")   # True
```

### Common mistakes
- Using a list as a dict key or putting lists in a set. Convert each one with `tuple(...)` first.
""",
}
