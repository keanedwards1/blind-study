# Guardian mini-game content for Learn Python worlds 1-7, plus the question audit.
#
# BOSS[world]:
#   exprs - short expressions for "Falling expressions": the build runs each one to get the value you have to type.
#   facts - (statement, check) for the "Lightning round": the build evaluates `check` to decide true or false,
#           so a statement can never be marked wrong by mistake.
# Match pairs come from the world's predict-the-output questions, and coding strikes from its shortest tasks
# (both picked automatically by scripts/python_levels.py).
#
# AUDIT replaces (or, with None, removes) guardian questions that were trick questions or tested things the lessons
# never taught. Keys are "world:concept:index" of the original question.
from _helpers import Q

BOSS = {
    1: dict(
        exprs=["7 // 2", "7 % 2", "2 ** 4", "abs(-9)", "max(3, 8, 5)", "int(3.9)", "10 / 4", "str(12) + '3'",
               "int('7') + 1", "not True", "min(4, -1)", "3 * 2 + 1", "5 > 3 and 2 > 4", "round(2.567, 1)"],
        facts=[("`7 // 2` equals 3", "7 // 2 == 3"), ("`6 / 2` gives the int 3", "isinstance(6 / 2, int)"),
               ("`round(2.5)` is 3", "round(2.5) == 3"), ("`int(3.9)` is 3", "int(3.9) == 3"),
               ("`'5' + '5'` is `'10'`", "'5' + '5' == '10'"), ("`bool(0)` is `False`", "bool(0) is False"),
               ("`abs(-3)` is 3", "abs(-3) == 3"), ("`max(2, 9, 4)` is 4", "max(2, 9, 4) == 4"),
               ("`10 % 3` is 1", "10 % 3 == 1"), ("`2 ** 3` is 6", "2 ** 3 == 6"), ("`not (3 > 2)` is `True`", "(not (3 > 2)) is True")],
    ),
    2: dict(
        exprs=["len('acorn')", "'ab' * 3", "'python'[0]", "'python'[-1]", "'python'[1:3]", "'hello'.upper()",
               "'-'.join('abc')", "'banana'.count('a')", "'cat' in 'concat'", "ord('b') - ord('a')", "'Hi'.lower()",
               "'  x '.strip()", "'abc'[::-1]", "'a,b'.split(',')"],
        facts=[("`'abc'[0]` is `'a'`", "'abc'[0] == 'a'"), ("`len('hello')` is 4", "len('hello') == 4"),
               ("`'Hi'.upper()` is `'HI'`", "'Hi'.upper() == 'HI'"), ("`'abc'[::-1]` is `'cba'`", "'abc'[::-1] == 'cba'"),
               ("`'a b'.split()` has 3 items", "len('a b'.split()) == 3"), ("`'py' * 2` is `'pypy'`", "'py' * 2 == 'pypy'"),
               ("`'cat' in 'concatenate'` is `True`", "'cat' in 'concatenate'"), ("`'hello'.find('z')` is 0", "'hello'.find('z') == 0"),
               ("`ord('a')` is 97", "ord('a') == 97"), ("`'3'.isdigit()` is `True`", "'3'.isdigit()")],
    ),
    3: dict(
        exprs=["sum([1, 2, 3])", "len([4, 5])", "list(range(3))", "[1, 2] + [3]", "sorted([3, 1, 2])", "[0] * 3",
               "max([2, 9, 4])", "[1, 2, 3][-1]", "list(range(1, 4))", "all([1, 0])", "any([0, 2])", "len(list(range(5)))",
               "[1, 2, 3][1:]", "list(reversed([1, 2]))"],
        facts=[("`list(range(3))` is `[1, 2, 3]`", "list(range(3)) == [1, 2, 3]"), ("`sum([])` is 0", "sum([]) == 0"),
               ("`sorted([3, 1])` is `[1, 3]`", "sorted([3, 1]) == [1, 3]"), ("`len([[1, 2], [3]])` is 3", "len([[1, 2], [3]]) == 3"),
               ("`[1, 2, 3][-1]` is 3", "[1, 2, 3][-1] == 3"), ("`all([])` is `True`", "all([])"), ("`any([0, 0])` is `True`", "any([0, 0])"),
               ("`list(range(5, 0, -1))[0]` is 5", "list(range(5, 0, -1))[0] == 5"), ("`[1, 2] + [3]` is `[1, 2, 3]`", "[1, 2] + [3] == [1, 2, 3]"),
               ("`[0] * 3` is `[0, 0, 0]`", "[0] * 3 == [0, 0, 0]")],
    ),
    4: dict(
        exprs=["len({1, 1, 2})", "{'a': 1}.get('b', 0)", "{'a': 1}['a']", "sorted({3, 1})", "len({'x': 1, 'y': 2})",
               "'a' in {'a': 1}", "{1, 2} & {2, 3}", "(1, 2)[1]", "list({'a': 1, 'b': 2})", "len((5,))",
               "sorted({1, 2} - {1})", "{'a': 1}.get('z')"],
        facts=[("`{'a': 1}.get('b')` is `None`", "{'a': 1}.get('b') is None"), ("`len({1, 1, 2})` is 3", "len({1, 1, 2}) == 3"),
               ("`type({})` is `set`", "type({}) is set"), ("`(1, 2)[0]` is 1", "(1, 2)[0] == 1"),
               ("`{1, 2} & {2, 3}` is `{2}`", "{1, 2} & {2, 3} == {2}"), ("`'a' in {'a': 1}` is `True`", "'a' in {'a': 1}"),
               ("`1 in {'a': 1}` is `True`", "1 in {'a': 1}"), ("`{1, 2} <= {1, 2, 3}` is `True`", "{1, 2} <= {1, 2, 3}"),
               ("`len((5,))` is 1", "len((5,)) == 1"), ("`(5)` is a tuple", "isinstance((5), tuple)")],
    ),
    5: dict(
        exprs=["(lambda x: x * 3)(4)", "list(map(str, [1, 2]))", "[x * x for x in range(3)]", "sum(x for x in [1, 2, 3])",
               "sorted(['bb', 'a'], key=len)", "max(['aa', 'b'], key=len)", "list(filter(None, [0, 1, 2]))",
               "{w: len(w) for w in ['hi']}", "len([c for c in 'hello' if c == 'l'])", "next(iter([7, 8]))",
               "(lambda *a: len(a))(1, 2, 3)"],
        facts=[("`(lambda x: x + 1)(2)` is 3", "(lambda x: x + 1)(2) == 3"), ("`sorted(['bb', 'a'], key=len)[0]` is `'a'`", "sorted(['bb', 'a'], key=len)[0] == 'a'"),
               ("`[x for x in range(4) if x % 2]` is `[1, 3]`", "[x for x in range(4) if x % 2] == [1, 3]"),
               ("`list(map(int, ['1']))` is `[1]`", "list(map(int, ['1'])) == [1]"),
               ("`{x % 2 for x in range(5)}` has 5 items", "len({x % 2 for x in range(5)}) == 5"),
               ("`max(['aa', 'b'], key=len)` is `'b'`", "max(['aa', 'b'], key=len) == 'b'"),
               ("`next(iter([]), 'none')` is `'none'`", "next(iter([]), 'none') == 'none'"),
               ("`(lambda *a: a)(1, 2)` is a list", "isinstance((lambda *a: a)(1, 2), list)"),
               ("`sum(x * x for x in [1, 2])` is 5", "sum(x * x for x in [1, 2]) == 5")],
    ),
    6: dict(
        exprs=["divmod(17, 5)", "bin(5)", "int('ff', 16)", "5 & 3", "5 | 3", "1 << 4", "hex(16)", "-7 // 2", "abs(3 + 4j)",
               "type(2.5).__name__", "isinstance(True, int)", "len('é'.encode())", "pow(2, 10)", "'big' if 7 > 5 else 'small'"],
        facts=[("`divmod(7, 2)` is `(3, 1)`", "divmod(7, 2) == (3, 1)"), ("`-7 // 2` is -3", "-7 // 2 == -3"),
               ("`bin(4)` is `'0b100'`", "bin(4) == '0b100'"), ("`int('11', 2)` is 3", "int('11', 2) == 3"),
               ("`5 & 1` is 1", "5 & 1 == 1"), ("`1 << 3` is 6", "1 << 3 == 6"), ("`0.1 + 0.2 == 0.3` is `True`", "0.1 + 0.2 == 0.3"),
               ("`isinstance(True, int)` is `True`", "isinstance(True, int)"), ("`abs(3 + 4j)` is 5.0", "abs(3 + 4j) == 5.0"),
               ("`len('é'.encode())` is 1", "len('é'.encode()) == 1")],
    ),
    7: dict(
        exprs=["math.gcd(12, 18)", "math.isqrt(17)", "Counter('banana').most_common(1)", "len(list(combinations('abc', 2)))",
               "list(accumulate([1, 2, 3]))", "bisect_left([1, 3, 5], 3)", "nsmallest(2, [5, 1, 3])", "list(deque([1, 2], maxlen=1))",
               "reduce(lambda a, b: a * b, [2, 3, 4])", "math.comb(4, 2)", "len(list(permutations('ab')))"],
        facts=[("`math.gcd(8, 12)` is 4", "math.gcd(8, 12) == 4"), ("`Counter('aab')['a']` is 2", "Counter('aab')['a'] == 2"),
               ("`math.isqrt(10)` is 3", "math.isqrt(10) == 3"), ("`bisect_left([1, 2, 2, 3], 2)` is 2", "bisect_left([1, 2, 2, 3], 2) == 2"),
               ("`list(accumulate([1, 1, 1]))` is `[1, 2, 3]`", "list(accumulate([1, 1, 1])) == [1, 2, 3]"),
               ("`len(list(combinations('abcd', 2)))` is 6", "len(list(combinations('abcd', 2))) == 6"),
               ("`deque([1, 2]).popleft()` is 2", "deque([1, 2]).popleft() == 2"),
               ("`reduce(lambda a, b: a + b, [1, 2, 3])` is 6", "reduce(lambda a, b: a + b, [1, 2, 3]) == 6"),
               ("`nsmallest(1, [4, 2])` is `[2]`", "nsmallest(1, [4, 2]) == [2]"), ("`math.comb(5, 2)` is 20", "math.comb(5, 2) == 20")],
    ),
}

AUDIT = {
    # world 1
    "1:boolean-logic:0": Q("Which line is `True` when `day` is 6 or 7?", "`day == 6 or day == 7`", "`day == 6 or 7`", "`day == (6 or 7)`", "`day == 6 and day == 7`",
                           why="Each side of `or` needs its own full comparison."),
    "1:boolean-logic:2": Q("What does this print?", "True", "False", "error", "None", code="x = 5\nprint(x > 3 and x < 10)", predict=True,
                           why="Both comparisons are true, so `and` is true."),
    # world 2
    "2:searching:1": Q("What does this print?", "3", "1", "2", "0", code="print('banana'.count('a'))", predict=True, why="`banana` has three `a`s."),
    "2:searching:2": Q("What does this print?", "True", "False", "0", "error", code="print('cat' in 'concatenate')", predict=True,
                       why="`in` looks for the text anywhere inside."),
    # world 3
    "3:range:2": Q("What does this print?", "[5, 4, 3, 2, 1]", "[]", "[1, 2, 3, 4, 5]", "[5, 4, 3, 2, 1, 0]", code="print(list(range(5, 0, -1)))", predict=True,
                   why="A step of -1 counts down and stops before 0."),
    # world 5
    "5:defaults-kwargs:0": Q("Why should you avoid `def f(items=[]):`?", "The same list is shared between every call", "Lists can't be parameters",
                             "It's slower than a tuple", "It makes `items` read-only",
                             why="A default value is created once, so every call that leaves it out shares that one list."),
    "5:map-filter:0": Q("What does this print?", "[2, 4]", "<map object>", "[1, 2]", "error", code="print(list(map(lambda x: x * 2, [1, 2])))", predict=True,
                        why="`map` doubles each item; `list(...)` collects the results."),
    "5:closures:1": Q("Which keyword lets an inner function change a variable of the outer function?", "`nonlocal`", "`global`", "`outer`", "`self`",
                      why="`nonlocal` says the name belongs to the enclosing function."),
    "5:iterators-generators:1": Q("What are `aiter` and `anext` for?", "The same jobs as `iter` and `next`, in asynchronous code",
                                  "Reading files", "Sorting lists faster", "Making a list from a generator",
                                  why="They're the async versions of `iter` and `next`; the lesson mentions them but you won't need them here."),
    # world 6
    "6:complex-numbers:0": Q("What does this print?", "5.0", "7", "25", "(3+4j)", code="print(abs(3 + 4j))", predict=True,
                             why="`abs` of a complex number is its distance from 0."),
    "6:dynamic-code:0": Q("What does this print?", "5", "'2 + 3'", "None", "error", code="print(eval('2 + 3'))", predict=True,
                          why="`eval` works out the expression and gives its value."),
    "6:interpreter-helpers:2": Q("What does `a is b` check?", "Whether both names point at the very same object", "Whether the values are equal",
                                 "Whether both are the same type", "Whether `a` contains `b`",
                                 why="`is` compares identity (the same object, the same `id`), not equality."),
    # world 7
    "7:attribute-tools:2": Q("What does `getattr(obj, 'name', None)` give when `obj` has no `name`?", "`None`", "an error", "`'name'`", "`obj`",
                             why="The third argument is the fallback."),
}
