# Beginner lessons for Learn Python level 7 (Classes & the standard library). See python_level01.py for the style.

LESSONS = {
    "classes": r"""
**In one sentence:** a class is a blueprint for making objects that keep their own data and know how to work with it.

### The idea
```python
class Counter:
    def __init__(self, start=0):    # runs when you make one
        self.value = start          # data stored on this object

    def increment(self):            # something the object can do
        self.value += 1
        return self.value

c = Counter()
c.increment()    # 1
c.increment()    # 2
```

- `class Counter:` is the blueprint (a *class*). `Counter()` makes one thing from it (an *object*, or *instance*).
- `__init__` is the set-up step that runs when an object is made (the *constructor*).
- A function inside a class is called a *method*. Its first input, `self`, is the object it's working on.
- `self.value = ...` stores data on that object (an *attribute*).

Each object keeps its **own** data: two `Counter()`s count separately.

### Common mistakes
- Forgetting `self` as the first input of a method, or writing `value` instead of `self.value`.
""",
    "dunder-methods": r"""
**In one sentence:** special methods with double underscores let your objects work with `==`, `<`, `+`, `len()` and `print`.

### The idea
Methods named like `__this__` (pronounced "dunder", for *d*ouble *under*score) hook your class into Python's built-in operations:

| Write this method | And this starts working |
|---|---|
| `__repr__(self)` | `repr(obj)`, and how it shows up when printed in a list |
| `__eq__(self, other)` | `a == b` |
| `__lt__(self, other)` | `a < b`, and therefore `sorted()`, `min()` and heaps |
| `__add__(self, other)` | `a + b` |
| `__len__(self)` | `len(obj)` |

```python
class Money:
    def __init__(self, cents):
        self.cents = cents
    def __lt__(self, other):
        return self.cents < other.cents
    def __repr__(self):
        return f"Money({self.cents})"

sorted([Money(5), Money(2)])    # [Money(2), Money(5)]
```

### Common mistakes
- Expecting `==` to compare contents without `__eq__`. By default it only checks whether both names point at the **same** object.
""",
    "decorated-methods": r"""
**In one sentence:** three decorators change how a method behaves: as a value, as a plain helper, or as a way to build objects.

### @property: a method that looks like a value
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

t = Temperature(100)
t.fahrenheit      # 212.0   no brackets, it reads like a normal value
```
A second method with the same name, decorated with `@fahrenheit.setter`, lets people assign to it as well (`t.fahrenheit = 32`).

### @staticmethod: a helper that lives in the class
It gets no `self`; it's a plain function kept with the class it relates to: `Date.is_leap(2024)`.

### @classmethod: another way to build an object
It receives the class itself (written `cls`) instead of an object, so it can create new objects. It's often used to build an object from a different starting point:

```python
@classmethod
def from_string(cls, text):
    y, m, d = map(int, text.split("-"))
    return cls(y, m, d)
```
""",
    "inheritance": r"""
**In one sentence:** a class can start as a copy of another class and change only what's different.

### The idea
```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):                 # a Dog is an Animal
    def speak(self):               # replace just this method
        return f"{self.name} says woof"

Dog("Rex").speak()    # 'Rex says woof'
```

- `class Dog(Animal):` makes `Dog` start with everything `Animal` has (`Dog` *inherits* from `Animal`, its *parent class*).
- Writing a method with the same name replaces the parent's version (*overriding*).
- `super().__init__(...)` runs the parent's set-up from inside the child's, so you don't repeat it.

### object
Every class is ultimately built on `object`. A bare `object()` makes a brand-new, unique value, which is a handy "nothing was passed" marker (a *sentinel*) when even `None` is a valid input.
""",
    "attribute-tools": r"""
**In one sentence:** these functions read and change an object's data when you only have the attribute's name as text.

### The idea
Normally you write `obj.name`. But sometimes the name is in a variable, such as `field = "name"`:

| Write | Same as |
|---|---|
| `getattr(obj, field)` | `obj.name` |
| `getattr(obj, field, None)` | `obj.name`, or `None` if it doesn't exist |
| `setattr(obj, field, 5)` | `obj.name = 5` |
| `hasattr(obj, field)` | "does `obj.name` exist?" |
| `delattr(obj, field)` | `del obj.name` |

And two for looking around:

- `vars(obj)`: the object's own data, as a dict.
- `dir(obj)`: every name you can use on it, including methods and many built-in `__dunder__` names.

### When you'd use it
Filling an object from a dict of settings, or checking which fields an object has.
""",
    "collections": r"""
**In one sentence:** the `collections` toolbox has upgraded versions of dicts, lists and tuples for common jobs.

### The idea
Everything here is already imported in your editor.

```python
Counter("banana")                  # Counter({'a': 3, 'n': 2, 'b': 1})   counts for you
Counter("banana").most_common(1)   # [('a', 3)]

groups = defaultdict(list)         # missing keys start as an empty list
groups["a"].append("apple")        # no setdefault needed

q = deque([1, 2, 3])
q.appendleft(0)                    # fast at BOTH ends
q.popleft()                        # 0
recent = deque(maxlen=3)           # keeps only the last 3 items

Point = namedtuple("Point", "x y")
p = Point(3, 4)
p.x                                # 3   a tuple whose parts have names
```

- `defaultdict(int)` starts missing keys at 0, which is perfect for counting.
- A `deque` (said "deck", short for *double-ended queue*) is quick to add to and remove from at both ends; a list is slow at the front.
""",
    "heapq-bisect": r"""
**In one sentence:** `heapq` always gives you the smallest item quickly, and `bisect` finds where something belongs in a sorted list.

### heapq
A *heap* is a list arranged so the smallest item is always first:

```python
h = []
heappush(h, 5); heappush(h, 1); heappush(h, 3)
h[0]            # 1    peek at the smallest
heappop(h)      # 1    take the smallest out
heapify(nums)   # turn an existing list into a heap
nsmallest(2, [5, 1, 3])   # [1, 3]
```

For the **largest** first, push negative numbers (`-x`) and flip them back when you pop.

### bisect
For a list that's **already sorted**:

```python
a = [10, 20, 30]
bisect_left(a, 20)    # 1    where 20 would go (before any equal items)
bisect_right(a, 20)   # 2    where it would go (after equal items)
insort(a, 25)         # a is now [10, 20, 25, 30]
```

### Common mistakes
- Using `bisect` on an unsorted list: the answers will be wrong.
""",
    "itertools": r"""
**In one sentence:** `itertools` has ready-made loops for groups, pairings and running totals.

### The idea
```python
list(combinations([1, 2, 3], 2))   # [(1, 2), (1, 3), (2, 3)]   groups, order doesn't matter
list(permutations([1, 2], 2))      # [(1, 2), (2, 1)]           every ordering
list(product("ab", [1, 2]))        # [('a', 1), ('a', 2), ('b', 1), ('b', 2)]   every pairing
list(accumulate([1, 2, 3]))        # [1, 3, 6]     running totals
list(accumulate([1, 3, 2], max))   # [1, 3, 3]     running maximum
list(itertools.chain([1], [2, 3])) # [1, 2, 3]     one after another
[(k, len(list(g))) for k, g in itertools.groupby("aabccc")]   # [('a', 2), ('b', 1), ('c', 3)]
```

`groupby` groups **neighbouring** equal items into runs.

### Common mistakes
- Forgetting `list(...)`: these hand out results one at a time.
- Using `groupby` on unsorted data and expecting every equal item in one group. It only groups items that sit next to each other.
""",
    "functools-math": r"""
**In one sentence:** `functools` adds superpowers to functions, and `math` has the maths functions Python doesn't build in.

### functools
```python
@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```
- `@cache` remembers every answer a function has given, so the same input is never worked out twice. That turns slow recursion into fast code (a technique called *dynamic programming*).
- `reduce(f, items)` combines a list into one value, two at a time: `reduce(lambda a, b: a * b, [2, 3, 4])` is `24`.
- `cmp_to_key(f)` sorts using a function that compares two items and returns a negative number, 0 or a positive number.

### math
```python
math.gcd(12, 18)   # 6     greatest common divisor
math.lcm(4, 6)     # 12    lowest common multiple
math.isqrt(17)     # 4     exact whole-number square root
math.sqrt(16)      # 4.0
math.floor(2.7), math.ceil(2.1)   # 2, 3
math.comb(5, 2)    # 10    ways to choose 2 from 5
```
""",
    "files": r"""
**In one sentence:** `open` reads and writes files, and `with` makes sure each file is closed properly.

### The idea
```python
with open(path) as f:          # open for reading
    text = f.read()            # the whole file as one string

with open(path) as f:
    for line in f:             # one line at a time (each ends with "\n")
        print(line.strip())

with open(path, "w") as f:     # "w" writes, replacing what was there
    f.write("hello\n")         # write doesn't add a new line for you
```

- The second input to `open` is the *mode*: `"r"` reads (the default), `"w"` writes over the file, `"a"` adds to the end.
- `with` closes the file automatically when the indented block ends, even if an error happens.

In these tasks the tests create a real temporary file and pass you its path.

### Common mistakes
- Forgetting `"\n"` when writing lines, so everything ends up on one line.
- Opening with `"w"` when you meant to add: it erases the file first.
""",
}
