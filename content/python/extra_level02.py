# Extra rep questions for Learn Python level 2 (Strings). See extra_level03.py for the format.
from _helpers import Q

EXTRA = {
    "indexing": dict(reps=[
        Q("What does this print?", "p n", "p o", "y n", "error", code="s = 'python'\nprint(s[0], s[-1])", predict=True,
          why="Position 0 is the first character; -1 counts from the end."),
        Q("What does this print?", "IndexError", "''", "None", "n", code="s = 'hi'\ntry:\n    print(s[5])\nexcept IndexError:\n    print('IndexError')", predict=True,
          why="Reading a single position past the end raises an error (slices don't)."),
        Q("What does this print?", "6", "5", "7", "0", code="print(len('banana'))", predict=True, why="`len` counts every character."),
    ]),
    "slicing": dict(reps=[
        Q("What does this print?", "pyt", "pyth", "yth", "p", code="print('python'[:3])", predict=True, why="`[:3]` takes positions 0, 1 and 2."),
        Q("What does this print?", "hon", "thon", "on", "python", code="print('python'[3:])", predict=True, why="`[3:]` takes everything from position 3 to the end."),
        Q("What does this print?", "python", "", "p", "nohtyp", code="print('python'[:])", predict=True, why="`[:]` with nothing on either side is a copy of the whole thing."),
        Q("What does this print?", "nohtyp", "python", "n", "error", code="print('python'[::-1])", predict=True, why="A step of -1 walks backwards."),
        Q("What does this print?", "pto", "yhn", "pyt", "ptn", code="print('python'[::2])", predict=True, why="A step of 2 takes every other character from position 0."),
        Q("What does this print?", "on", "o", "hon", "n", code="print('python'[-2:])", predict=True, why="`-2` means two from the end, so the slice takes the last two characters."),
        Q("What does this print?", "''", "error", "'hi'", "None", code="print(repr('hi'[5:9]))", predict=True,
          why="Slices past the end don't crash; they just come back empty."),
    ]),
    "string-methods": dict(reps=[
        Q("What does this print?", "HI hi", "HI HI", "Hi hi", "error", code="s = 'hi'\nprint(s.upper(), s)", predict=True,
          why="String methods return a new string; the original never changes."),
        Q("What does this print?", "'a b'", "'a b '", "' a b'", "'ab'", code="print(repr('  a b '.strip()))", predict=True,
          why="`strip` removes whitespace from both ends only."),
        Q("What does this print?", "a-b-c", "a b c", "a-b c", "-a-b-c", code="print('a b c'.replace(' ', '-'))", predict=True, why="`replace` changes every match."),
    ]),
    "searching": dict(reps=[
        Q("What does this print?", "2 -1", "2 None", "3 -1", "error", code="s = 'hello'\nprint(s.find('l'), s.find('z'))", predict=True,
          why="`find` gives the first index, or -1 when it's missing."),
        Q("What does this print?", "True", "False", "1", "error", code="print('cat' in 'concatenate')", predict=True, why="`in` checks for the text anywhere inside."),
        Q("What does this print?", "2", "1", "3", "0", code="print('banana'.count('na'))", predict=True, why="`count` counts non-overlapping matches."),
    ]),
    "split-join": dict(reps=[
        Q("What does this print?", "['a', 'b', 'c']", "['a b c']", "'abc'", "['a', ' ', 'b']", code="print('a  b c'.split())", predict=True,
          why="`split()` with no argument splits on any run of spaces."),
        Q("What does this print?", "['a', '', 'b']", "['a', 'b']", "['a,,b']", "error", code="print('a,,b'.split(','))", predict=True,
          why="Splitting on a specific character keeps empty pieces."),
        Q("What does this print?", "x-y-z", "xyz", "x y z", "['x', 'y', 'z']", code="print('-'.join(['x', 'y', 'z']))", predict=True,
          why="The separator comes first, then `.join(list)`."),
    ]),
    "formatting": dict(reps=[
        Q("What does this print?", "3.14", "3.14159", "3.1", "3", code="print(f'{3.14159:.2f}')", predict=True, why="`.2f` rounds to two decimal places."),
        Q("What does this print?", "007", "7", "  7", "700", code="print(f'{7:03d}')", predict=True, why="`03d` pads with zeros to width 3."),
        Q("What does this print?", "Ada is 36", "{name} is {age}", "Ada is age", "error", code="name, age = 'Ada', 36\nprint(f'{name} is {age}')", predict=True,
          why="An f-string puts each value into its braces."),
    ]),
}
