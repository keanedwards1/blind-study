# Test harness shared by the in-browser Pyodide worker and scripts/build_problems.py.
# Runs user code in an isolated namespace and checks results against expected outputs.
import ast
import contextlib
import copy
import io
import itertools
import json
import linecache
import math
import time
import traceback
import types as _types

USER_FILE = "solution.py"

PRELUDE = """
from typing import *
import collections, heapq, bisect, itertools, functools, math, string, re, random
from collections import deque, defaultdict, Counter, OrderedDict
from heapq import heappush, heappop, heapify, heappushpop, nlargest, nsmallest
from functools import lru_cache, cache, reduce
from bisect import bisect_left, bisect_right, insort
from itertools import accumulate, combinations, permutations, product
from math import inf
"""


# ---------------------------------------------------------------- data structures
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


class Node:
    """Graph node (used by Clone Graph)."""

    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"Node({self.val})"


def build_list(arr):
    dummy = cur = ListNode()
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_arr(head, limit=100_000):
    out = []
    while head is not None:
        if not isinstance(head, ListNode):
            raise TypeError(f"expected a ListNode, got {type(head).__name__}")
        out.append(head.val)
        if len(out) > limit:
            raise ValueError("returned list looks like it contains a cycle")
        head = head.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue, i = [root], 1
    qi = 0
    while qi < len(queue) and i < len(arr):
        node = queue[qi]
        qi += 1
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_arr(root, limit=100_000):
    if root is None:
        return []
    out, queue, qi = [], [root], 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
        if node is None:
            out.append(None)
            continue
        if not isinstance(node, TreeNode):
            raise TypeError(f"expected a TreeNode, got {type(node).__name__}")
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
        if len(queue) > limit:
            raise ValueError("returned tree is too large (cycle?)")
    while out and out[-1] is None:
        out.pop()
    return out


def build_graph(adj):
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nbrs]
    return nodes[0]


def collect_graph(node):
    if node is None:
        return []
    seen, stack, out = {id(node)}, [node], []
    while stack:
        cur = stack.pop()
        out.append(cur)
        for n in cur.neighbors:
            if id(n) not in seen:
                seen.add(id(n))
                stack.append(n)
    return out


def graph_to_adj(node):
    nodes = collect_graph(node)
    if not nodes:
        return []
    by_val = {n.val: n for n in nodes}
    return [[nb.val for nb in by_val[v].neighbors] for v in range(1, max(by_val) + 1) if v in by_val]


IN_ADAPTERS = {
    "list": build_list,
    "lists": lambda a: [build_list(x) for x in a],
    "tree": build_tree,
    "graph": build_graph,
    # JSON has no tuples or sets, so tasks that take them convert on the way in.
    "tuple": tuple,
    "set": set,
}
OUT_ADAPTERS = {
    "list": list_to_arr,
    "tree": tree_to_arr,
    "graph": graph_to_adj,
}


# ---------------------------------------------------------------- comparison
def normalize(x):
    if isinstance(x, (list, tuple)):
        return [normalize(i) for i in x]
    if isinstance(x, (set, frozenset)):
        return sorted((normalize(i) for i in x), key=_key)
    if isinstance(x, dict):
        return {str(k): normalize(v) for k, v in x.items()}
    if isinstance(x, (ListNode, TreeNode, Node)):
        return repr(x)
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return repr(x)
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    return repr(x)


def _key(x):
    return json.dumps(x, sort_keys=True, default=repr)


def typed_repr(x):
    """Canonical, type-preserving text for compare="strict": a tuple stays a tuple, a set a set, 1 differs from "1".

    Sets and dicts are ordered by their items' text so equal values always produce equal strings.
    Generators are consumed so their values can be compared, but are still labelled as generators.
    """
    if x is None or isinstance(x, (bool, int, str, bytes, bytearray, complex, range)):
        return repr(x)
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return repr(x)
        return repr(float(f"{x:.12g}"))
    if isinstance(x, list):
        return "[" + ", ".join(typed_repr(i) for i in x) + "]"
    if isinstance(x, tuple):
        inner = ", ".join(typed_repr(i) for i in x)
        return f"({inner},)" if len(x) == 1 else f"({inner})"
    if isinstance(x, (set, frozenset)):
        items = sorted(typed_repr(i) for i in x)
        body = "{" + ", ".join(items) + "}" if items else ""
        if isinstance(x, frozenset):
            return f"frozenset({body})"
        return body or "set()"
    if isinstance(x, dict):
        items = sorted((typed_repr(k), typed_repr(v)) for k, v in x.items())
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"
    if isinstance(x, _types.GeneratorType):
        return f"<generator yielding {typed_repr(list(itertools.islice(x, 10_000)))}>"
    return repr(x)


# ---------------------------------------------------------------- task rules (require / forbid)
class TaskRuleError(Exception):
    """The code runs, but doesn't use (or uses) something the task is about."""


_SYNTAX = {
    "listcomp": (ast.ListComp,), "dictcomp": (ast.DictComp,), "setcomp": (ast.SetComp,), "genexp": (ast.GeneratorExp,),
    "comprehension": (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp),
    "lambda": (ast.Lambda,), "yield": (ast.Yield, ast.YieldFrom), "with": (ast.With,), "try": (ast.Try,),
    "raise": (ast.Raise,), "while": (ast.While,), "for": (ast.For,), "if": (ast.If,), "class": (ast.ClassDef,),
    "fstring": (ast.JoinedStr,), "walrus": (ast.NamedExpr,), "slicing": (ast.Slice,), "ternary": (ast.IfExp,),
    "nonlocal": (ast.Nonlocal,), "global": (ast.Global,), "assert": (ast.Assert,), "del": (ast.Delete,),
    "import": (ast.Import, ast.ImportFrom), "augassign": (ast.AugAssign,), "unpack": (ast.Starred,), "match": (ast.Match,),
    "break": (ast.Break,), "continue": (ast.Continue,),
}
_OPS = {
    "+": ast.Add, "-": ast.Sub, "*": ast.Mult, "/": ast.Div, "//": ast.FloorDiv, "%": ast.Mod, "**": ast.Pow,
    "&": ast.BitAnd, "|": ast.BitOr, "^": ast.BitXor, "<<": ast.LShift, ">>": ast.RShift, "~": ast.Invert,
    "in": ast.In, "not in": ast.NotIn, "is": ast.Is, "==": ast.Eq, "!=": ast.NotEq, "<": ast.Lt, "<=": ast.LtE,
    ">": ast.Gt, ">=": ast.GtE, "and": ast.And, "or": ast.Or, "not": ast.Not,
}
RULE_LABELS = {
    "listcomp": "a list comprehension", "dictcomp": "a dict comprehension", "setcomp": "a set comprehension",
    "genexp": "a generator expression", "comprehension": "a comprehension", "lambda": "a `lambda`", "yield": "`yield`",
    "with": "a `with` block", "try": "`try`/`except`", "raise": "`raise`", "while": "a `while` loop", "for": "a `for` loop",
    "if": "an `if` statement", "class": "a class", "fstring": "an f-string", "walrus": "the walrus operator `:=`",
    "slicing": "slicing", "ternary": "a one-line `x if cond else y`", "nonlocal": "`nonlocal`", "global": "`global`",
    "assert": "`assert`", "del": "`del`", "import": "an import", "augassign": "an augmented assignment like `+=`",
    "unpack": "`*` unpacking", "match": "a `match` statement", "recursion": "recursion (a function that calls itself)", "decorator": "a decorator",
    "break": "`break`", "continue": "`continue`",
}


def rule_label(rule):
    if rule in RULE_LABELS:
        return RULE_LABELS[rule]
    if rule.startswith("op:"):
        return f"the `{rule[3:]}` operator"
    if rule.startswith("."):
        return f"the `{rule}()` method"
    return f"`{rule}`"


def _uses(tree, rule):
    if rule in _SYNTAX:
        return any(isinstance(n, _SYNTAX[rule]) for n in ast.walk(tree))
    if rule.startswith("op:"):
        op = _OPS[rule[3:]]
        return any(isinstance(n, op) for n in ast.walk(tree))
    if rule == "decorator":
        return any(getattr(n, "decorator_list", None) for n in ast.walk(tree))
    if rule == "recursion":
        for fn in ast.walk(tree):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for n in ast.walk(fn):
                    if isinstance(n, ast.Call):
                        f = n.func
                        if (isinstance(f, ast.Name) and f.id == fn.name) or (isinstance(f, ast.Attribute) and f.attr == fn.name):
                            return True
        return False
    if rule.startswith("."):
        return any(isinstance(n, ast.Attribute) and n.attr == rule[1:] for n in ast.walk(tree))
    # A plain name matches `name` or `module.name` (so `math.gcd` counts as using `gcd`).
    return any((isinstance(n, ast.Name) and n.id == rule) or (isinstance(n, ast.Attribute) and n.attr == rule) for n in ast.walk(tree))


def check_rules(code, spec):
    """Raise TaskRuleError if the code skips a required tool or uses a forbidden one."""
    require, forbid = spec.get("require") or [], spec.get("forbid") or []
    if not require and not forbid:
        return
    tree = ast.parse(code)
    for rule in require:
        if not _uses(tree, rule):
            raise TaskRuleError(f"This task is about {rule_label(rule)}. Use it in your solution.")
    for rule in forbid:
        if _uses(tree, rule):
            raise TaskRuleError(f"This task asks you not to use {rule_label(rule)}. Write that part yourself.")


def canon(x, mode):
    if mode == "unordered":
        return sorted(x, key=_key)
    if mode == "unordered_nested":
        return sorted((sorted(i, key=_key) for i in x), key=_key)
    return x


def eq(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-6)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    return type(a) == type(b) and a == b


# ---------------------------------------------------------------- execution
def resolve(ns, name):
    obj = ns.get(name)
    if callable(obj) and not isinstance(obj, type):
        return obj
    sol = ns.get("Solution")
    if isinstance(sol, type) and hasattr(sol, name):
        return getattr(sol(), name)
    raise NameError(f"function `{name}` is not defined (don't rename the starter function)")


def resolve_class(ns, name):
    obj = ns.get(name)
    if isinstance(obj, type):
        return obj
    raise NameError(f"class `{name}` is not defined (don't rename the starter class)")


def _compile_helper(src, fname):
    if not src:
        return None
    env = dict(globals())
    exec(src, env)
    return env[fname]


class Session:
    def __init__(self, code, spec, rules=True):
        self.spec = spec
        self.ns = {"__name__": "__main__", "__builtins__": __builtins__}
        exec(PRELUDE, self.ns)
        self.ns.update(ListNode=ListNode, TreeNode=TreeNode, Node=Node)
        self.driver = _compile_helper(spec.get("driver"), "driver")
        self.checker = _compile_helper(spec.get("checker"), "check")
        linecache.cache[USER_FILE] = (len(code), None, code.splitlines(True), USER_FILE)
        compiled = compile(code, USER_FILE, "exec")
        if rules:
            check_rules(code, spec)
        exec(compiled, self.ns)

    def _invoke(self, fn, args):
        """Call user code, applying the task's output mode (stdout capture, raises)."""
        spec = self.spec
        try:
            if spec.get("out") == "stdout":
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    fn(*args)
                return buf.getvalue()
            return fn(*args)
        except Exception as e:
            if spec.get("raises"):
                return {"raises": type(e).__name__}
            raise

    def _finish(self, result):
        if isinstance(result, dict) and set(result) == {"raises"}:
            return result
        if self.spec.get("compare") == "strict":
            return typed_repr(result)
        return normalize(result)

    def _feed_stdin(self, lines):
        lines = [str(x) for x in lines]

        def fake_input(prompt=""):
            if prompt:
                print(prompt, end="")
            if not lines:
                raise EOFError("EOF when reading a line (the test gave no more input)")
            return lines.pop(0)

        self.ns["input"] = fake_input

    def call(self, args):
        spec, ns = self.spec, self.ns
        args = copy.deepcopy(args)
        if spec.get("stdin"):
            self._feed_stdin(args[0])
            args = args[1:]
        if self.driver:
            return self._finish(self.driver(ns, *args))
        if spec.get("kind") == "class":
            ops, op_args = args
            cls = resolve_class(ns, spec["cls"])
            obj = cls(*op_args[0])
            out = [None]
            for op, a in zip(ops[1:], op_args[1:]):
                method = getattr(obj, op, None)
                if method is None:
                    raise AttributeError(f"{spec['cls']} has no method `{op}`")
                out.append(self._finish(self._invoke(method, a)))
            return out
        fn = resolve(ns, spec["fn"])
        ins = spec.get("in") or []
        conv = [IN_ADAPTERS[ins[i]](a) if i < len(ins) and ins[i] else a for i, a in enumerate(args)]
        result = self._invoke(fn, conv)
        if spec.get("mutate") is not None and not isinstance(result, dict):
            result = conv[spec["mutate"]]
        if spec.get("out") in OUT_ADAPTERS:
            result = OUT_ADAPTERS[spec["out"]](result)
        return self._finish(result)

    def check(self, args, result, expected):
        if self.checker:
            return bool(self.checker(copy.deepcopy(args), result, expected))
        mode = self.spec.get("compare", "exact")
        if mode == "strict" or self.spec.get("out") == "stdout":
            return result == expected
        try:
            return eq(canon(result, mode), canon(expected, mode))
        except Exception:
            return False

    def run(self, args, expected=None, has_expected=True):
        buf = io.StringIO()
        start = time.perf_counter()
        result, error, ok = None, None, False
        try:
            with contextlib.redirect_stdout(buf):
                result = self.call(args)
            if has_expected:
                ok = self.check(args, result, expected)
        except BaseException as e:  # noqa: BLE001 - report everything to the user
            error = format_error(e)
        ms = (time.perf_counter() - start) * 1000
        out = buf.getvalue()
        if len(out) > 4000:
            out = out[:4000] + "\n... (output truncated)"
        return {"ok": ok, "result": result, "error": error, "stdout": out, "ms": round(ms, 2)}


def format_error(e):
    frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == USER_FILE]
    lines = []
    if frames:
        lines.append("Traceback (most recent call last):")
        for f in frames:
            lines.append(f'  Line {f.lineno}, in {f.name}')
            if f.line:
                lines.append(f"    {f.line.strip()}")
    if isinstance(e, TaskRuleError):
        return f"Task rule: {e}"
    if isinstance(e, SyntaxError):
        lines.append(f"SyntaxError: {e.msg} (line {e.lineno})")
        if e.text:
            lines.append(f"    {e.text.rstrip()}")
    else:
        lines.append(f"{type(e).__name__}: {e}")
    return "\n".join(lines)


# ---------------------------------------------------------------- JS bridge (JSON in/out)
_session = None


def js_prepare(code, spec_json):
    global _session
    _session = None
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            _session = Session(code, json.loads(spec_json))
        return json.dumps({"ok": True, "stdout": buf.getvalue()})
    except BaseException as e:  # noqa: BLE001
        return json.dumps({"ok": False, "error": format_error(e), "stdout": buf.getvalue()})


def js_run_one(args_json, expected_json):
    res = _session.run(json.loads(args_json), json.loads(expected_json))
    return json.dumps(res, default=repr)


def js_exec(code):
    """Playground: run a snippet in a fresh namespace and capture stdout."""
    ns = {"__name__": "__main__", "__builtins__": __builtins__}
    buf = io.StringIO()
    error = None
    linecache.cache[USER_FILE] = (len(code), None, code.splitlines(True), USER_FILE)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, USER_FILE, "exec"), ns)
    except BaseException as e:  # noqa: BLE001
        error = format_error(e)
    out = buf.getvalue()
    if len(out) > 10000:
        out = out[:10000] + "\n... (output truncated)"
    return json.dumps({"stdout": out, "error": error})
