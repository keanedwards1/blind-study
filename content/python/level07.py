# Learn Python, level 7: classes and the standard library.
# kind="class" tasks: tests are [operations, arguments]; the first operation constructs the class (see README).
from _helpers import P, Q

LEVEL = dict(
    n=7,
    title="Classes & the standard library",
    summary="Designing your own types with classes, then the standard-library tools the Blind 75 leans on: collections, heapq, bisect, itertools, functools, math, and files.",
    concepts=[
        # ------------------------------------------------------------------ classes
        dict(
            id="classes",
            title="Classes, objects and methods",
            builtins=[],
            intro="""
A **class** bundles data with the functions that work on it.

```python
class Counter:
    def __init__(self, start=0):   # runs when you create one: Counter()
        self.value = start         # data stored on this object

    def increment(self):           # a method: always takes self first
        self.value += 1
        return self.value

c = Counter()
c.increment()   # 1
```

- `self` is the object the method was called on.
- Each object has its **own** attributes: two `Counter()`s count separately.
""",
            problems=[
                P("py-class-counter", "Counter Class", None,
                  """Write a class `Counter` with:

- `Counter(start)`: begins at `start`;
- `increment()`: adds 1 and returns the new value;
- `reset()`: goes back to the starting value (returns nothing).

**Constraints**
- `start` is a whole number from `-10^9` to `10^9`
- Up to 100 method calls
""",
                  "class Counter:\n    def __init__(self, start: int):\n        self.start = start\n        self.value = start\n\n    def increment(self) -> int:\n        self.value += 1\n        return self.value\n\n    def reset(self) -> None:\n        self.value = self.start\n",
                  [([["Counter", "increment", "increment", "reset", "increment"], [[5], [], [], [], []]], [None, 6, 7, None, 6])],
                  [[["Counter", "increment"], [[0], []]], [["Counter", "reset", "increment", "increment", "increment"], [[-2], [], [], [], []]]],
                  kind="class", cls="Counter",
                  starter="class Counter:\n    def __init__(self, start: int):\n        pass\n\n    def increment(self) -> int:\n        pass\n\n    def reset(self) -> None:\n        pass\n",
                  grammar="""
## Building blocks
- **Constructor:** `def __init__(self, from_i):`, storing values with `self.start = begin`.
- **Remember two things:** the starting value and the current value.
- **Methods change `self`:** `self.value += 1`
"""),
                P("py-class-bank-account", "Bank Account", None,
                  """Write a class `Account` with `deposit(amount)`, `withdraw(amount)` and `balance()`. A withdrawal larger than the balance is refused: it changes nothing and returns `False`; a successful one returns `True`. Accounts start at 0.

**Constraints**
- Every `amount` is a whole number from `0` to `10^4`
- Up to 100 method calls
""",
                  "class Account:\n    def __init__(self):\n        self._balance = 0\n\n    def deposit(self, amount: int) -> None:\n        self._balance += amount\n\n    def withdraw(self, amount: int) -> bool:\n        if amount > self._balance:\n            return False\n        self._balance -= amount\n        return True\n\n    def balance(self) -> int:\n        return self._balance\n",
                  [([["Account", "deposit", "withdraw", "withdraw", "balance"], [[], [100], [30], [500], []]], [None, None, True, False, 70])],
                  [[["Account", "balance", "withdraw"], [[], [], [1]]], [["Account", "deposit", "deposit", "withdraw", "balance"], [[], [5], [5], [10], []]]],
                  kind="class", cls="Account",
                  starter="class Account:\n    def __init__(self):\n        pass\n\n    def deposit(self, amount: int) -> None:\n        pass\n\n    def withdraw(self, amount: int) -> bool:\n        pass\n\n    def balance(self) -> int:\n        pass\n",
                  grammar="""
## Building blocks
- **Start at 0:** `self._balance = 0` in `__init__`. A leading `_` hints "internal, don't touch from outside".
- **Refuse early:** `if target_amt > self._balance: return False`
"""),
                P("py-class-stack", "Stack with Peek", None,
                  """Write a class `Stack` with `push(x)`, `pop()` (remove and return the top, or `None` if empty), `peek()` (return the top without removing it, or `None`) and `is_empty()`.

**Constraints**
- `x` can be a value of any type
- Up to 100 method calls
""",
                  "class Stack:\n    def __init__(self):\n        self.items = []\n\n    def push(self, x: int) -> None:\n        self.items.append(x)\n\n    def pop(self):\n        return self.items.pop() if self.items else None\n\n    def peek(self):\n        return self.items[-1] if self.items else None\n\n    def is_empty(self) -> bool:\n        return not self.items\n",
                  [([["Stack", "is_empty", "push", "push", "peek", "pop", "pop", "pop", "is_empty"], [[], [], [1], [2], [], [], [], [], []]], [None, True, None, None, 2, 2, 1, None, True])],
                  [[["Stack", "peek"], [[], []]], [["Stack", "push", "is_empty", "peek"], [[], [9], [], []]]],
                  kind="class", cls="Stack",
                  starter="class Stack:\n    def __init__(self):\n        pass\n\n    def push(self, x: int) -> None:\n        pass\n\n    def pop(self):\n        pass\n\n    def peek(self):\n        pass\n\n    def is_empty(self) -> bool:\n        pass\n",
                  grammar="""
## Building blocks
- **A list inside the object:** `self.items = []`
- **Top of the stack:** `self.items[-1]`
- **Empty?** `not self.items`
"""),
            ],
            quiz=[
                Q("What does this print?", "1 0", "1 1", "0 0", "error", code="class C:\n    def __init__(self):\n        self.n = 0\na, b = C(), C()\na.n += 1\nprint(a.n, b.n)", predict=True,
                  why="Each object has its own attributes."),
                Q("What's missing?", "self as the first parameter of hello", "a return statement", "an __init__ method", "nothing", code="class Greeter:\n    def hello():\n        return 'hi'\n\nGreeter().hello()",
                  why="Calling a method passes the object as the first argument, so the method must accept it."),
            ],
        ),
        # ------------------------------------------------------------------ dunder methods
        dict(
            id="dunder-methods",
            title="Special methods: __repr__, __eq__, __lt__, …",
            builtins=[],
            intro="""
Methods with double underscores ("dunder" methods) hook your class into Python's syntax:

| Method | Makes this work |
|---|---|
| `__repr__(self)` | `repr(obj)` and how it prints in lists |
| `__eq__(self, other)` | `a == b` |
| `__lt__(self, other)` | `a < b`, and so `sorted()`, `min()`, `heapq` |
| `__add__(self, other)` | `a + b` |
| `__len__(self)` | `len(obj)` |

Without `__eq__`, `==` only checks whether two names point to the same object.
""",
            problems=[
                P("py-point-class", "Point with == and repr", None,
                  """Write a class `Point(x, y)` where:

- `repr(Point(1, 2))` is `"Point(1, 2)"`;
- two points are `==` when their coordinates match.

The tests return `[repr of the first point, p == q, p == Point(0, 0)]`.

**Constraints**
- `len(p) == len(q) == 2`
- `-10^16 <= p[i], q[i] <= 10^16`
""",
                  "class Point:\n    def __init__(self, x: int, y: int):\n        self.x = x\n        self.y = y\n\n    def __repr__(self) -> str:\n        return f\"Point({self.x}, {self.y})\"\n\n    def __eq__(self, other) -> bool:\n        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)\n",
                  [([[1, 2], [1, 2]], ["Point(1, 2)", True, False]), ([[0, 0], [5, 5]], ["Point(0, 0)", False, True])], [[[-1, 3], [-1, 4]]],
                  params=["p", "q"],
                  starter="class Point:\n    def __init__(self, x: int, y: int):\n        pass\n",
                  driver='def driver(ns, p, q):\n    Point = resolve_class(ns, "Point")\n    a, b = Point(*p), Point(*q)\n    return [repr(a), a == b, a == Point(0, 0)]\n',
                  grammar="""
## Building blocks
- **Text for repr:** `def __repr__(self): return f"Point({self.x}, {self.y})"`
- **Equality:** `def __eq__(self, other): return (self.x, self.y) == (other.x, other.y)`
- **Comparing tuples** compares item by item.
"""),
                P("py-sortable-money", "Sortable Money", None,
                  """Write a class `Money(cents)` that can be **sorted** (by amount) and whose `repr` is like `"$3.05"` for 305 cents. The tests sort a list of `Money` objects and return their reprs.

**Constraints**
- `0 <= len(amounts_in_cents) <= 10^4`
- `0 <= amounts_in_cents[i] <= 10^16`
""",
                  "class Money:\n    def __init__(self, cents: int):\n        self.cents = cents\n\n    def __lt__(self, other) -> bool:\n        return self.cents < other.cents\n\n    def __repr__(self) -> str:\n        return f\"${self.cents // 100}.{self.cents % 100:02d}\"\n",
                  [([[305, 99, 1000]], ["$0.99", "$3.05", "$10.00"]), ([[]], [])], [[[1, 0, 100]]],
                  params=["amounts_in_cents"],
                  starter="class Money:\n    def __init__(self, cents: int):\n        pass\n",
                  driver='def driver(ns, cents):\n    Money = resolve_class(ns, "Money")\n    return [repr(m) for m in sorted(Money(c) for c in cents)]\n',
                  grammar="""
## Building blocks
- **Make objects sortable:** define `__lt__(self, other)`. `sorted` only needs `<`.
- **Dollars and cents:** `cents // 100` and `cents % 100`, padded with `:02d`.
"""),
                P("py-vector-add", "Vector Addition", None,
                  """Write a class `Vector(*components)` supporting `+` (adds matching components, giving a new `Vector`) and `len()` (number of components). It also needs a `components` attribute that is a list. The tests return `[(a + b).components, len(a)]`.

**Constraints**
- `1 <= len(a) <= 10^4`
- `len(b) == len(a)`
- `-10^16 <= a[i], b[i] <= 10^16`
""",
                  "class Vector:\n    def __init__(self, *components: int):\n        self.components = list(components)\n\n    def __add__(self, other: \"Vector\") -> \"Vector\":\n        return Vector(*(x + y for x, y in zip(self.components, other.components)))\n\n    def __len__(self) -> int:\n        return len(self.components)\n",
                  [([[1, 2], [10, 20]], [[11, 22], 2]), ([[5], [-5]], [[0], 1])], [[[1, 1, 1], [2, 2, 2]]],
                  params=["a", "b"], difficulty="Medium",
                  starter="class Vector:\n    def __init__(self, *components: int):\n        pass\n",
                  driver='def driver(ns, a, b):\n    Vector = resolve_class(ns, "Vector")\n    va, vb = Vector(*a), Vector(*b)\n    return [(va + vb).components, len(va)]\n',
                  grammar="""
## Building blocks
- **`+`:** `def __add__(self, other): return Vector(...)`, returning a new object.
- **`len()`:** `def __len__(self): return len(self.components)`
- **Pair components:** `zip(self.components, other.components)`
"""),
            ],
            quiz=[
                Q("What does this print?", "False", "True", "error", code="class A:\n    def __init__(self, v):\n        self.v = v\nprint(A(1) == A(1))", predict=True,
                  why="Without `__eq__`, `==` compares identity, and these are two different objects."),
                Q("Which method does `sorted(objects)` need?", "__lt__", "__eq__", "__repr__", "__len__", why="Sorting only compares with `<`."),
            ],
        ),
        # ------------------------------------------------------------------ property / staticmethod / classmethod
        dict(
            id="decorated-methods",
            title="property, staticmethod and classmethod",
            builtins=["property", "staticmethod", "classmethod"],
            intro="""
- `@property` makes a method look like an attribute: `t.fahrenheit` instead of `t.fahrenheit()`. Add a `@fahrenheit.setter` to allow assignment.
- `@staticmethod`: a plain function that lives in the class; no `self`.
- `@classmethod`: receives the **class** (`cls`) instead of an object. Often used for alternative constructors like `Date.from_string("2026-11-14")`.
""",
            problems=[
                P("py-temperature-property", "Temperature Property", None,
                  """Write a class `Temperature(celsius)` with a `fahrenheit` **property** (`celsius * 9 / 5 + 32`) that can also be **set** (which updates `celsius`). The tests read `fahrenheit`, set it, then read `celsius`.

**Constraints**
- `-273.15 <= celsius <= 10^16`
- `-459.67 <= new_fahrenheit <= 10^16`
""",
                  "class Temperature:\n    def __init__(self, celsius: float):\n        self.celsius = celsius\n\n    @property\n    def fahrenheit(self) -> float:\n        return self.celsius * 9 / 5 + 32\n\n    @fahrenheit.setter\n    def fahrenheit(self, value: float) -> None:\n        self.celsius = (value - 32) * 5 / 9\n",
                  [([100, 32], [212.0, 0.0]), ([0, 212], [32.0, 100.0])], [[-40, -40], [37, 98.6]],
                  params=["celsius", "new_fahrenheit"], require=["property"],
                  starter="class Temperature:\n    def __init__(self, celsius: float):\n        pass\n",
                  driver='def driver(ns, c, f):\n    t = resolve_class(ns, "Temperature")(c)\n    first = t.fahrenheit\n    t.fahrenheit = f\n    return [first, t.celsius]\n',
                  grammar="""
## Building blocks
- **Read like an attribute:** `@property` above `def fahrenheit(self):`
- **Allow assignment:** `@kelvin.setter` above a second `def fahrenheit(self, value):`
"""),
                P("py-date-from-string", "Alternative Constructor", None,
                  """Write a class `Date(year, month, day)` with a **classmethod** `from_string("YYYY-MM-DD")` that builds a `Date`, and a **staticmethod** `is_leap(year)`. The tests return `[d.year, d.month, d.day, Date.is_leap(d.year)]`.

**Constraints**
- `text` is a real date written as `YYYY-MM-DD`
""",
                  "class Date:\n    def __init__(self, year: int, month: int, day: int):\n        self.year, self.month, self.day = year, month, day\n\n    @classmethod\n    def from_string(cls, text: str) -> \"Date\":\n        y, m, d = map(int, text.split(\"-\"))\n        return cls(y, m, d)\n\n    @staticmethod\n    def is_leap(year: int) -> bool:\n        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n",
                  [(["2024-02-29"], [2024, 2, 29, True]), (["1900-01-01"], [1900, 1, 1, False])], [["2000-12-31"], ["2023-07-04"]],
                  params=["text"], require=["classmethod", "staticmethod"],
                  starter="class Date:\n    def __init__(self, year: int, month: int, day: int):\n        pass\n",
                  driver='def driver(ns, text):\n    Date = resolve_class(ns, "Date")\n    d = Date.from_string(text)\n    return [d.year, d.month, d.day, Date.is_leap(d.year)]\n',
                  grammar="""
## Building blocks
- **Classmethod:** `@classmethod` then `def from_string(cls, text):` … `return cls(w, mins, mapping)`
- **Parse the parts:** `map(int, text.split("-"))`
- **Staticmethod:** `@staticmethod` then `def is_leap(year):` with no `self`.
"""),
            ],
            quiz=[
                Q("What does this print?", "4", "<bound method …>", "error", "None", code="class Sq:\n    def __init__(self, s):\n        self.s = s\n    @property\n    def area(self):\n        return self.s ** 2\nprint(Sq(2).area)", predict=True,
                  why="A property is read without brackets."),
                Q("What does a classmethod receive as its first argument?", "The class itself", "The object", "Nothing", "The module", why="Conventionally named `cls`."),
            ],
        ),
        # ------------------------------------------------------------------ inheritance
        dict(
            id="inheritance",
            title="Inheritance, super() and object",
            builtins=["super", "object"],
            intro="""
A class can **inherit** from another and override what it needs:

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):                  # override
        return f"{self.name} says woof"
```

- `super().__init__(...)` runs the parent's version, so you don't repeat its setup.
- Every class ultimately inherits from `object`. A bare `object()` is a unique value, handy as a "nothing passed" marker when `None` is a valid value.
""",
            problems=[
                P("py-animal-sounds", "Animal Sounds", None,
                  """Write `Animal(name)` with `speak()` returning `"..."`, and subclasses `Dog` and `Cat` whose `speak()` returns `"NAME says woof"` / `"NAME says meow"`. The tests create one of each and return their `speak()` results.

**Constraints**
- `0 <= len(name) <= 10^4`
""",
                  'class Animal:\n    def __init__(self, name: str):\n        self.name = name\n\n    def speak(self) -> str:\n        return "..."\n\n\nclass Dog(Animal):\n    def speak(self) -> str:\n        return f"{self.name} says woof"\n\n\nclass Cat(Animal):\n    def speak(self) -> str:\n        return f"{self.name} says meow"\n',
                  [(["Rex"], ["...", "Rex says woof", "Rex says meow"])], [["Tom"]],
                  params=["name"],
                  starter="class Animal:\n    def __init__(self, name: str):\n        pass\n",
                  driver='def driver(ns, name):\n    return [resolve_class(ns, c)(name).speak() for c in ("Animal", "Dog", "Cat")]\n',
                  grammar="""
## Building blocks
- **Inherit:** `class Dog(Animal):`
- **Override:** define `speak` again in the subclass.
- **No `__init__` needed in the subclass:** it inherits `Animal.__init__`.
"""),
                P("py-square-super", "Square from Rectangle", None,
                  """Write `Rectangle(width, height)` with `area()`, and `Square(side)` that inherits from `Rectangle` and calls `super().__init__` with the side used twice. The tests return `[Square(s).area(), isinstance(Square(s), Rectangle)]`.

**Constraints**
- `0 <= side <= 10^16`
""",
                  "class Rectangle:\n    def __init__(self, width: int, height: int):\n        self.width = width\n        self.height = height\n\n    def area(self) -> int:\n        return self.width * self.height\n\n\nclass Square(Rectangle):\n    def __init__(self, side: int):\n        super().__init__(side, side)\n",
                  [([3], [9, True]), ([0], [0, True])], [[12]],
                  params=["side"], require=["super"],
                  starter="class Rectangle:\n    def __init__(self, width: int, height: int):\n        pass\n\n\nclass Square:\n    pass\n",
                  driver='def driver(ns, side):\n    Square, Rectangle = resolve_class(ns, "Square"), resolve_class(ns, "Rectangle")\n    sq = Square(side)\n    return [sq.area(), isinstance(sq, Rectangle)]\n',
                  grammar="""
## Building blocks
- **Inherit:** `class Square(Rectangle):`
- **Reuse the parent's setup:** `super()` gives you the parent class, so `super().__init__(...)` runs the parent's `__init__` with the values you pass.
"""),
                P("py-sentinel-default", "A Default That Isn't None", "def get_setting(settings: Dict, key: str, default=...):",
                  """Write `get_setting(settings, key, default)` that returns `settings[key]` if present. If the key is missing it returns `default` when one was passed, and raises `KeyError` when no default was passed. **`None` is a valid default**, so you can't use `None` to mean "not passed". Use an `object()` sentinel.

The tests try a present key, a missing key with default `None`, and a missing key with no default.

**Constraints**
- `1 <= len(settings) <= 10^4`
- Values can be of any type
""",
                  "_MISSING = object()\n\n\ndef get_setting(settings, key, default=_MISSING):\n    if key in settings:\n        return settings[key]\n    if default is _MISSING:\n        raise KeyError(key)\n    return default\n",
                  [([{"a": 1}], [1, None, "KeyError"])], [[{"a": 0}]],
                  params=["settings"], require=["object"],
                  starter="def get_setting(settings, key, default=None):\n    pass\n",
                  driver='def driver(ns, settings):\n    get = resolve(ns, "get_setting")\n    out = [get(settings, "a"), get(settings, "zzz", None)]\n    try:\n        get(settings, "zzz")\n        out.append("no error")\n    except KeyError:\n        out.append("KeyError")\n    return out\n',
                  difficulty="Medium",
                  grammar="""
## Building blocks
- **A unique marker:** `_NOT_GIVEN = object()` at module level.
- **Use it as the default:** `def get_setting(opts, lookup, dflt=_NOTHING):`
- **Was a default passed?** `default is _MISSING`
"""),
            ],
            quiz=[
                Q("What does this print?", "B A", "A B", "B", "A", code="class A:\n    def hi(self):\n        return 'A'\nclass B(A):\n    def hi(self):\n        return 'B ' + super().hi()\nprint(B().hi())", predict=True,
                  why="`super().hi()` calls the parent's version."),
                Q("What does this print?", "True", "False", code="class X:\n    pass\nprint(isinstance(X(), object))", predict=True, why="Everything is an `object`."),
            ],
        ),
        # ------------------------------------------------------------------ attributes by name
        dict(
            id="attribute-tools",
            title="getattr, setattr, hasattr, delattr, vars, dir",
            builtins=["getattr", "setattr", "hasattr", "delattr", "vars", "dir"],
            intro="""
Sometimes the attribute name is in a variable:

| | |
|---|---|
| `getattr(obj, "name", default)` | `obj.name`, or `default` if it's missing |
| `setattr(obj, "name", value)` | `obj.name = value` |
| `hasattr(obj, "name")` | does it exist? |
| `delattr(obj, "name")` | `del obj.name` |
| `vars(obj)` | the object's attributes as a dict |
| `dir(obj)` | every name you can use on it, including methods |
""",
            problems=[
                P("py-read-field", "Read a Field by Name", "def read(obj, name: str):",
                  """Return attribute `name` of `obj`, or `None` if it has no such attribute. The tests build an object with `x = 1` and `y = 2`.

**Constraints**
- `0 <= len(name) <= 100`
""",
                  "def read(obj, name: str):\n    return getattr(obj, name, None)\n",
                  [(["x"], 1), (["z"], None)], [["y"]],
                  params=["name"], require=["getattr"],
                  driver='def driver(ns, name):\n    class Obj:\n        pass\n    o = Obj()\n    o.x, o.y = 1, 2\n    return resolve(ns, "read")(o, name)\n',
                  grammar="""
## Building blocks
- **Attribute by name, with a default:** `getattr(obj, name, None)`
"""),
                P("py-fill-fields", "Fill Fields from a Dict", "def fill(obj, values: Dict[str, int]) -> None:",
                  """Set an attribute on `obj` for every key in `values`. The tests pass an empty object and then look at `vars(obj)`.

**Constraints**
- `0 <= len(values) <= 10^4`
- Every key is a valid attribute name
""",
                  "def fill(obj, values: Dict[str, int]) -> None:\n    for k, v in values.items():\n        setattr(obj, k, v)\n",
                  [([{"a": 1, "b": 2}], {"a": 1, "b": 2}), ([{}], {})], [[{"x": 0}]],
                  params=["values"], require=["setattr"],
                  driver='def driver(ns, values):\n    class Obj:\n        pass\n    o = Obj()\n    resolve(ns, "fill")(o, values)\n    return vars(o)\n',
                  grammar="""
## Building blocks
- **Set an attribute by name:** `setattr(obj, name, value)`
"""),
                P("py-has-all-fields", "Has Every Field?", "def has_all(obj, names: List[str]) -> bool:",
                  """Return `True` if `obj` has every attribute listed in `names`. The tests' object has `x` and `y`.

**Constraints**
- `0 <= len(names) <= 10^4`
""",
                  "def has_all(obj, names: List[str]) -> bool:\n    return all(hasattr(obj, n) for n in names)\n",
                  [([["x", "y"]], True), ([["x", "z"]], False), ([[]], True)], [[["y"]]],
                  params=["names"], require=["hasattr"],
                  driver='def driver(ns, names):\n    class Obj:\n        pass\n    o = Obj()\n    o.x, o.y = 1, 2\n    return resolve(ns, "has_all")(o, names)\n',
                  grammar="""
## Building blocks
- **Does it exist?** `hasattr(obj, name)`
- **Check one attribute:** `hasattr(thing, "x")`
- **Every item passes:** `all(...)`
"""),
                P("py-strip-private", "Remove Private Fields", "def strip_private(obj) -> Dict[str, int]:",
                  """Delete every attribute of `obj` whose name starts with `_`, then return `vars(obj)`. The tests build `obj` with the attributes in `fields` (name to value), so `{"a": 1, "_b": 2}` means `obj.a = 1` and `obj._b = 2`.

**Constraints**
- `0 <= len(fields) <= 10^4`
- Every key is a valid attribute name
""",
                  "def strip_private(obj) -> Dict[str, int]:\n    for name in list(vars(obj)):\n        if name.startswith(\"_\"):\n            delattr(obj, name)\n    return vars(obj)\n",
                  [([{"a": 1, "_b": 2, "_c": 3}], {"a": 1})], [[{}]],
                  params=["fields"], require=["delattr", "vars"],
                  driver='def driver(ns, fields):\n    class Obj:\n        pass\n    o = Obj()\n    for k, v in fields.items():\n        setattr(o, k, v)\n    return resolve(ns, "strip_private")(o)\n',
                  hints=["Changing a dict while looping over it is an error, so loop over `list(vars(obj))`."],
                  grammar="""
## Building blocks
- **The object's attributes:** `vars(obj)` (a dict).
- **Loop over a copy of the names:** `for person_name in list(vars(thing)):`
- **Delete by name:** `delattr(target, person)`
"""),
                P("py-public-methods", "Public Names", "def public_names(obj) -> List[str]:",
                  """Return every name in `dir(obj)` that doesn't start with `_`, in order. The tests build `obj` from a class with the methods named in `methods`, and give it the attributes named in `attrs`.

**Constraints**
- `0 <= len(methods), len(attrs) <= 10^4`
- Every name is a valid attribute name
""",
                  "def public_names(obj) -> List[str]:\n    return [n for n in dir(obj) if not n.startswith(\"_\")]\n",
                  [([["go", "stop"], ["speed"]], ["go", "speed", "stop"])], [[[], []]],
                  params=["methods", "attrs"], require=["dir"],
                  driver='def driver(ns, methods, attrs):\n    Thing = type("Thing", (), {m: (lambda self: None) for m in methods})\n    obj = Thing()\n    for a in attrs:\n        setattr(obj, a, 0)\n    return resolve(ns, "public_names")(obj)\n',
                  grammar="""
## Building blocks
- **Every usable name:** `dir(obj)`, already sorted, including methods and dunders.
- **Skip the underscored ones:** `if not size.startswith("_")`
"""),
            ],
            quiz=[
                Q("What does this print?", "{'a': 1}", "['a']", "{'a': 1, '__init__': ...}", "error", code="class C:\n    def __init__(self):\n        self.a = 1\nprint(vars(C()))", predict=True,
                  why="`vars` shows only the object's own attributes."),
                Q("What does this print?", "7", "None", "error", code="class C:\n    pass\nc = C()\nsetattr(c, 'n', 7)\nprint(getattr(c, 'n'))", predict=True,
                  why="`setattr(c, 'n', 7)` is `c.n = 7`."),
                Q("What does `__import__('math').sqrt(9)` return?", "3.0", "9", "an error", "'math'",
                  why="`__import__` is the function behind `import`; it returns the module. In normal code, use `import math` or `importlib.import_module`."),
            ],
            quiz_only=["__import__"],
        ),
        # ------------------------------------------------------------------ collections
        dict(
            id="collections",
            title="collections: Counter, defaultdict, deque, namedtuple",
            builtins=[],
            intro="""
`collections` (already imported here) has upgraded containers:

- `Counter(items)`: counts for you. `.most_common(k)` gives the top `k`.
- `defaultdict(list)`: missing keys start as an empty list (or `int` → 0, `set` → empty set).
- `deque`: a list with fast adds and removals at **both** ends (`appendleft`, `popleft`). `deque(maxlen=k)` keeps only the last `k` items.
- `namedtuple("Point", "x y")`: a tuple whose items have names: `p.x`.
""",
            problems=[
                P("py-most-common-letter", "Most Common Letter", "def most_common(s: str) -> str:",
                  """Return the most common character in `s` (the first one to reach that count, if tied).

**Constraints**
- `1 <= len(s) <= 10^4`
""",
                  "def most_common(s: str) -> str:\n    return Counter(s).most_common(1)[0][0]\n",
                  [(["banana"], "a"), (["abc"], "a")], [["zzzy"], ["mississippi"]],
                  require=["Counter"],
                  grammar="""
## Building blocks
- **Count everything:** `Counter(s)`
- **Top one:** `.most_common(1)` gives `[(char, count)]`, so take `[0][0]`.
"""),
                P("py-anagram-groups-dd", "Group Anagrams with defaultdict", "def group(words: List[str]) -> List[List[str]]:",
                  """Group words that are anagrams of each other, in the order each group first appears. Use `defaultdict(list)` with the sorted letters as the key.

**Constraints**
- `0 <= len(words) <= 10^4`
""",
                  "def group(words: List[str]) -> List[List[str]]:\n    groups = defaultdict(list)\n    for w in words:\n        groups[\"\".join(sorted(w))].append(w)\n    return list(groups.values())\n",
                  [([["eat", "tea", "tan", "ate", "nat"]], [["eat", "tea", "ate"], ["tan", "nat"]]), ([[]], [])], [[["a"]], [["ab", "ba", "abc"]]],
                  require=["defaultdict"],
                  grammar="""
## Building blocks
- **Lists that create themselves:** `piles = defaultdict(list)`
- **Key shared by anagrams:** `"".join(sorted(w))`
- **No setup needed:** `groups[key].append(w)`
"""),
                P("py-recent-items", "Last K Items", "def recent(items: List[int], k: int) -> List[int]:",
                  """Feed `items` one at a time into a `deque` that only keeps the last `k`, and return what's left as a list.

**Constraints**
- `0 <= len(items) <= 10^4`
- `1 <= k <= 10^16`
""",
                  "def recent(items: List[int], k: int) -> List[int]:\n    window = deque(maxlen=k)\n    for x in items:\n        window.append(x)\n    return list(window)\n",
                  [([[1, 2, 3, 4, 5], 3], [3, 4, 5]), ([[1], 3], [1])], [[[], 2], [list(range(100)), 1]],
                  require=["deque"],
                  grammar="""
## Building blocks
- **A bounded queue:** `deque(maxlen=k)` drops the oldest item automatically.
"""),
                P("py-namedtuple-points", "Named Points", "def furthest(points: List[List[int]]) -> List[int]:",
                  """Turn each `[x, y]` into a `namedtuple` `Point` with fields `x` and `y`, and return the coordinates `[x, y]` of the point furthest from the origin (the first one, if tied).

**Constraints**
- `1 <= len(points) <= 10^4`
- `-10^4 <= points[i][j] <= 10^4`
""",
                  "from collections import namedtuple\n\nPoint = namedtuple(\"Point\", \"x y\")\n\n\ndef furthest(points: List[List[int]]) -> List[int]:\n    pts = [Point(*p) for p in points]\n    best = max(pts, key=lambda p: p.x ** 2 + p.y ** 2)\n    return [best.x, best.y]\n",
                  [([[[1, 1], [3, 4], [0, 5]]], [3, 4]), ([[[0, 0]]], [0, 0])], [[[[-6, 0], [5, 5]]]],
                  require=["namedtuple"],
                  grammar="""
## Building blocks
- **Import it:** `from collections import namedtuple` (it isn't pre-imported).
- **Define it once:** `Spot = namedtuple("Point", "x y")`
- **Use names:** `p.x`, `p.y`
- **Biggest by a key:** `max(items, key=lambda it: it.size)`
- **Square:** `v ** 2`
"""),
            ],
            quiz=[
                Q("What does this print?", "[('a', 3), ('b', 2)]", "{'a': 3, 'b': 2}", "['a', 'b']", "[3, 2]", code="from collections import Counter\nprint(Counter('aaabbc').most_common(2))", predict=True,
                  why="`most_common` returns (item, count) pairs."),
                Q("Which is O(1) for removing from the front?", "deque.popleft()", "list.pop(0)", "both", "neither", why="`list.pop(0)` shifts every remaining item."),
            ],
        ),
        # ------------------------------------------------------------------ heapq and bisect
        dict(
            id="heapq-bisect",
            title="heapq and bisect",
            builtins=[],
            intro="""
**heapq** keeps a list arranged so the smallest item is always at index 0:

- `heappush(h, x)`, `heappop(h)` (smallest), `h[0]` (peek), `heapify(list)`
- `nsmallest(k, items)`, `nlargest(k, items)`
- For a max-heap, push negated values.

**bisect** works on a list that's already sorted:

- `bisect_left(a, x)`: where `x` would go (before any equal items)
- `insort(a, x)`: insert `x`, keeping the list sorted
""",
            problems=[
                P("py-k-smallest", "K Smallest", "def k_smallest(nums: List[int], k: int) -> List[int]:",
                  """Return the `k` smallest numbers in increasing order, using a heap (not by sorting the whole list).

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
- `0 <= k <= 10^16`
""",
                  "def k_smallest(nums: List[int], k: int) -> List[int]:\n    heap = list(nums)\n    heapify(heap)\n    return [heappop(heap) for _ in range(min(k, len(heap)))]\n",
                  [([[5, 1, 4, 2], 2], [1, 2]), ([[3], 5], [3])], [[[], 1], [[9, 9, 1], 3]],
                  require=["heappop"], forbid=["sorted", ".sort"],
                  grammar="""
## Building blocks
- **Heap in place:** `heapify(pq)` (copy the list first, so you don't change the input).
- **Smallest each time:** `heappop(heap)`
- **Or simply:** `nsmallest(k, nums)`
"""),
                P("py-insert-sorted", "Keep It Sorted (in place)", "def add_sorted(items: List[int], x: int) -> None:",
                  """Insert `x` into `items` so it stays sorted, in place, using `bisect`.

**Constraints**
- `0 <= len(items) <= 10^4`
- `items` is sorted from smallest to largest
- `-10^16 <= items[i], x <= 10^16`
""",
                  "def add_sorted(items: List[int], x: int) -> None:\n    insort(items, x)\n",
                  [([[1, 3, 5], 4], [1, 3, 4, 5]), ([[], 1], [1])], [[[1, 1], 1], [[2, 4], 0]],
                  mutate=0, require=["insort"],
                  grammar="""
## Building blocks
- **Insert in order:** `insort(things, v)` (from `bisect`, pre-imported).
"""),
                P("py-grade-bisect", "Grade with bisect", "def grade(score: int) -> str:",
                  """Grades: below 60 `"F"`, 60–69 `"D"`, 70–79 `"C"`, 80–89 `"B"`, 90+ `"A"`. Use `bisect` on the cut-offs `[60, 70, 80, 90]` instead of an if-chain.

**Constraints**
- `0 <= score <= 100`
""",
                  'def grade(score: int) -> str:\n    return "FDCBA"[bisect_right([60, 70, 80, 90], score)]\n',
                  [([95], "A"), ([60], "D"), ([59], "F")], [[90], [89], [0], [100], [70]],
                  require=["bisect_right"], forbid=["if"],
                  grammar="""
## Building blocks
- **How many cut-offs are at or below the score:** `bisect_right([60, 70, 80, 90], score)` gives 0–4.
- **Index into the grades:** `"FDCBA"[that]`
"""),
            ],
            quiz=[
                Q("What does this print?", "1 [2, 5]", "5 [1, 2]", "1 [5, 2]", "error", code="from heapq import heapify, heappop\nh = [5, 1, 2]\nheapify(h)\nprint(heappop(h), sorted(h))", predict=False,
                  why="`heappop` always removes the smallest item."),
                Q("What does this print?", "1", "2", "3", "4", code="from bisect import bisect_left\nprint(bisect_left([1, 3, 3, 5], 3))", predict=True,
                  why="`bisect_left` returns the position before any equal items: the first 3 is at index 1."),
            ],
        ),
        # ------------------------------------------------------------------ itertools
        dict(
            id="itertools",
            title="itertools",
            builtins=[],
            intro="""
`itertools` (already imported) has building blocks for looping:

- `combinations(items, k)`: every k-item group, order doesn't matter
- `permutations(items, k)`: every ordering
- `product(a, b)`: every pair, like nested loops
- `accumulate(nums)`: running totals (or running anything: `accumulate(nums, max)`)
- `itertools.chain(a, b)`: one after the other
- `itertools.groupby(items)`: runs of equal adjacent items
""",
            problems=[
                P("py-all-pairs", "Every Pair", "def pairs(items: List[int]) -> List[List[int]]:",
                  """Return every pair of items (order within a pair follows the list; each pair once), using `combinations`.

**Constraints**
- `0 <= len(items) <= 100`
- Items can be values of any type
""",
                  "def pairs(items: List[int]) -> List[List[int]]:\n    return [list(p) for p in combinations(items, 2)]\n",
                  [([[1, 2, 3]], [[1, 2], [1, 3], [2, 3]]), ([[1]], [])], [[[]], [[4, 5, 6, 7]]],
                  require=["combinations"],
                  grammar="""
## Building blocks
- **Every 2-item group:** `combinations(items, 2)` gives tuples.
- **As lists:** `[list(p) for p in ...]`
"""),
                P("py-running-max", "Running Maximum", "def running_max(nums: List[int]) -> List[int]:",
                  """Return the largest value seen so far at each position. Use `accumulate`.

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
""",
                  "def running_max(nums: List[int]) -> List[int]:\n    return list(accumulate(nums, max))\n",
                  [([[1, 3, 2, 5]], [1, 3, 3, 5]), ([[]], [])], [[[5, 4, 3]], [[-1, -2, 0]]],
                  require=["accumulate"],
                  grammar="""
## Building blocks
- **Running anything:** `accumulate(nums, max)`. With no function it's running totals.
"""),
                P("py-run-lengths", "Run-Length Encoding", "def encode(s: str) -> str:",
                  """Compress runs of the same character: write each character followed by how many times it repeats in a row. Use `itertools.groupby`.

**Constraints**
- `0 <= len(s) <= 10^4`
- `s` is English letters
""",
                  'def encode(s: str) -> str:\n    return "".join(f"{ch}{len(list(run))}" for ch, run in itertools.groupby(s))\n',
                  [(["aaabcc"], "a3b1c2"), ([""], ""), (["x"], "x1")], [["aabbaa"], ["zzzzzzzzzzzz"]],
                  require=["groupby"], difficulty="Medium",
                  grammar="""
## Building blocks
- **Runs of equal neighbours:** `itertools.groupby(s)` yields `(char, run)` pairs.
- **Length of a run:** `len(list(run))`
"""),
                P("py-every-outfit", "Every Outfit", "def outfits(tops: List[str], bottoms: List[str]) -> List[str]:",
                  """Return every `"top + bottom"` combination, tops in the outer order. Use `product`.

**Constraints**
- `0 <= len(tops), len(bottoms) <= 10^4`
""",
                  'def outfits(tops: List[str], bottoms: List[str]) -> List[str]:\n    return [f"{t} + {b}" for t, b in product(tops, bottoms)]\n',
                  [([["tee", "shirt"], ["jeans"]], ["tee + jeans", "shirt + jeans"]), ([[], ["x"]], [])], [[["a", "b"], ["c", "d"]]],
                  require=["product"],
                  grammar="""
## Building blocks
- **Every pairing:** `product(tops, bottoms)`, like two nested loops.
"""),
            ],
            quiz=[
                Q("What does this print?", "3 6", "6 3", "3 3", "6 6", code="from itertools import combinations, permutations\nprint(len(list(combinations('abc', 2))), len(list(permutations('abc', 2))))", predict=True,
                  why="Combinations ignore order; permutations count ab and ba separately."),
                Q("What does this print?", "[1, 3, 6]", "[1, 2, 3]", "6", "[6]", code="from itertools import accumulate\nprint(list(accumulate([1, 2, 3])))", predict=True, why="Running totals."),
            ],
        ),
        # ------------------------------------------------------------------ functools + math
        dict(
            id="functools-math",
            title="functools and math",
            builtins=[],
            intro="""
**functools**:

- `@cache` remembers a function's results, turning slow recursion into fast **dynamic programming**.
- `reduce(f, items)` folds a list into one value: `reduce(lambda a, b: a * b, nums)`.
- `cmp_to_key(f)` lets you sort with an old-style compare function (return negative / 0 / positive).

**math**: `gcd`, `lcm`, `isqrt` (exact integer square root), `comb`, `sqrt`, `floor`, `ceil`, `inf`.
""",
            problems=[
                P("py-memo-fib", "Fast Fibonacci", "def fib(n: int) -> int:",
                  """Return the `n`th Fibonacci number (`fib(0) = 0`, `fib(1) = 1`) **recursively**. Without caching it would take forever; add `@cache`.

**Constraints**
- `0 <= n <= 300`
""",
                  "@cache\ndef fib(n: int) -> int:\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n",
                  [([10], 55), ([0], 0), ([1], 1)], [[50], [90], [300]],
                  require=["recursion", "cache"],
                  grammar="""
## Building blocks
- **Remember results:** put `@cache` on the line above `def fib(n):`.
- **Base case:** `if size < 2: return size`
- **Recursive case:** the function calls itself on smaller inputs, e.g. `f(k - 1)`.
"""),
                P("py-product-reduce", "Product with reduce", "def product_of(nums: List[int]) -> int:",
                  """Return the product of all the numbers (1 for an empty list) using `reduce`.

**Constraints**
- `0 <= len(nums) <= 10^4`
- `-10^16 <= nums[i] <= 10^16`
""",
                  "def product_of(nums: List[int]) -> int:\n    return reduce(lambda a, b: a * b, nums, 1)\n",
                  [([[2, 3, 4]], 24), ([[]], 1)], [[[5]], [[-1, -1, -1]]],
                  require=["reduce"],
                  grammar="""
## Building blocks
- **Fold a list:** `reduce(lambda acc, x: acc + x, xs, 0)` adds everything up; the last argument is the starting value.
"""),
                P("py-largest-number", "Largest Number", "def largest_number(nums: List[int]) -> str:",
                  """Arrange the non-negative numbers to form the largest possible number, as text. Sort with a compare function: `a` goes first if `a + b > b + a` (as strings).

**Constraints**
- `1 <= len(nums) <= 10^4`
- `0 <= nums[i] <= 10^16`
""",
                  'def largest_number(nums: List[int]) -> str:\n    def cmp(a, b):\n        return -1 if a + b > b + a else (1 if a + b < b + a else 0)\n    text = "".join(sorted(map(str, nums), key=functools.cmp_to_key(cmp)))\n    return "0" if text[0] == "0" else text\n',
                  [([[3, 30, 34, 5, 9]], "9534330"), ([[10, 2]], "210"), ([[0, 0]], "0")], [[[1]], [[121, 12]], [[0, 9]]],
                  require=["cmp_to_key"], difficulty="Hard",
                  grammar="""
## Building blocks
- **Compare function:** returns negative if `a` should come first, positive if `b` should, 0 if equal.
- **Use it for sorting:** `sorted(strs, key=functools.cmp_to_key(cmp))`
- **Edge case:** all zeros should give `"0"`, not `"00"`.
"""),
                P("py-gcd-of-list", "GCD of a List", "def gcd_all(nums: List[int]) -> int:",
                  """Return the greatest common divisor of all the numbers.

**Constraints**
- `1 <= len(nums) <= 10^4`
- `1 <= nums[i] <= 10^16`
""",
                  "def gcd_all(nums: List[int]) -> int:\n    return reduce(math.gcd, nums)\n",
                  [([[12, 18, 24]], 6), ([[7]], 7), ([[5, 7]], 1)], [[[100, 75, 50]], [[2] * 10]],
                  require=["gcd"],
                  grammar="""
## Building blocks
- **GCD of two:** `math.gcd(a, b)`
- **Of many:** `reduce(math.gcd, nums)` (in Python 3.9+, `math.gcd(*nums)` also works).
"""),
                P("py-perfect-square", "Perfect Square?", "def is_square(n: int) -> bool:",
                  """Return `True` if `n` (which can be huge) is a perfect square. Use `math.isqrt`, which is exact for big numbers where `n ** 0.5` isn't.

**Constraints**
- `0 <= n <= 10^31`
""",
                  "def is_square(n: int) -> bool:\n    r = math.isqrt(n)\n    return r * r == n\n",
                  [([16], True), ([15], False), ([0], True)], [[1], [10 ** 30], [10 ** 30 + 1]],
                  require=["isqrt"],
                  grammar="""
## Building blocks
- **Exact integer square root:** `math.isqrt(n)` rounds down.
- **Check:** `r * r == n`
"""),
            ],
            quiz=[
                Q("What does `@cache` do to a function?", "Remembers results so repeated calls with the same arguments are instant", "Makes it run in parallel", "Saves it to disk", "Prevents recursion",
                  why="It's the simplest way to add memoisation for dynamic programming."),
                Q("What does this print?", "10", "24", "[1, 3, 6, 10]", "error", code="from functools import reduce\nprint(reduce(lambda a, b: a + b, [1, 2, 3, 4]))", predict=True,
                  why="((1 + 2) + 3) + 4."),
            ],
        ),
        # ------------------------------------------------------------------ files
        dict(
            id="files",
            title="Files: open and with",
            builtins=["open"],
            intro="""
```python
with open(path) as f:          # "r" (read) is the default mode
    text = f.read()            # the whole file as one string

with open(path) as f:
    for line in f:             # one line at a time, each ending in "\\n"
        ...

with open(path, "w") as f:     # "w" overwrites; "a" appends
    f.write("hello\\n")
```

`with` closes the file for you, even if an error happens. In these tasks the tests create a real temporary file and pass you its path.
""",
            problems=[
                P("py-count-lines", "Count Lines in a File", "def count_lines(path: str) -> int:",
                  """Return how many lines the file at `path` has. The examples show the file's contents.

**Constraints**
- The file has up to `10^4` characters
""",
                  "def count_lines(path: str) -> int:\n    with open(path) as f:\n        return sum(1 for _ in f)\n",
                  [(["one\ntwo\nthree\n"], 3), ([""], 0)], [["no newline at end"], ["a\n\nb\n"]],
                  params=["file_contents"], require=["open", "with"],
                  driver='import os, tempfile\n\ndef driver(ns, contents):\n    fd, path = tempfile.mkstemp(suffix=".txt")\n    with os.fdopen(fd, "w") as f:\n        f.write(contents)\n    try:\n        return resolve(ns, "count_lines")(path)\n    finally:\n        os.remove(path)\n',
                  grammar="""
## Building blocks
- **Open safely:** `with open(chosen) as fh:`
- **Lines one at a time:** `for text in file:`
- **Count them:** a counter, or `sum(1 for _ in f)`.
"""),
                P("py-word-count-file", "Words in a File", "def file_words(path: str) -> int:",
                  """Return how many words (separated by whitespace) are in the file at `path`.

**Constraints**
- The file has up to `10^4` characters
""",
                  "def file_words(path: str) -> int:\n    with open(path) as f:\n        return len(f.read().split())\n",
                  [(["the cat\nsat on\n\nthe mat"], 6), ([""], 0)], [["  spaced   out  "], ["one"]],
                  params=["file_contents"], require=["open"],
                  driver='import os, tempfile\n\ndef driver(ns, contents):\n    fd, path = tempfile.mkstemp(suffix=".txt")\n    with os.fdopen(fd, "w") as f:\n        f.write(contents)\n    try:\n        return resolve(ns, "file_words")(path)\n    finally:\n        os.remove(path)\n',
                  grammar="""
## Building blocks
- **Whole file as text:** `f.read()`
- **Words:** `.split()`
"""),
                P("py-write-lines", "Write Lines to a File", "def save_lines(path: str, lines: List[str]) -> None:",
                  """Write each string in `lines` to the file at `path`, one per line (each followed by a new line). The tests read the file back.

**Constraints**
- `0 <= len(lines) <= 10^4`
- No string in `lines` contains a new line
""",
                  "def save_lines(path: str, lines: List[str]) -> None:\n    with open(path, \"w\") as f:\n        for line in lines:\n            f.write(line + \"\\n\")\n",
                  [([["a", "b"]], "a\nb\n"), ([[]], "")], [[["only"]], [["", "x"]]],
                  params=["lines"], require=["open", "with"],
                  driver='import os, tempfile\n\ndef driver(ns, lines):\n    fd, path = tempfile.mkstemp(suffix=".txt")\n    os.close(fd)\n    try:\n        resolve(ns, "save_lines")(path, lines)\n        with open(path) as f:\n            return f.read()\n    finally:\n        os.remove(path)\n',
                  grammar="""
## Building blocks
- **Open for writing:** `open(path, "w")` (creates or overwrites the file).
- **Write text:** `f.write("hi")`. `write` doesn't add new lines for you.
- **A new line character:** `"\\n"`
"""),
            ],
            quiz=[
                Q("Why use `with open(...) as f:`?", "It closes the file automatically, even after an error", "It reads faster", "It's required to read text", "It locks the file",
                  why="Forgetting to close files can lose data or leak resources."),
                Q("What does mode `\"a\"` do?", "Appends to the end of the file", "Opens for reading", "Overwrites the file", "Opens in binary",
                  why="`\"w\"` overwrites, `\"a\"` adds to the end, `\"r\"` reads."),
            ],
        ),
    ],
)
