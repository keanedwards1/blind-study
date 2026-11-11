CATEGORY = "Intervals"

PROBLEMS = [
    dict(
        slug="insert-interval",
        title="Insert Interval",
        difficulty="Medium",
        sig="def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:",
        desc="""
`intervals` is a list of non-overlapping `[start, end]` pairs sorted by start. Insert `new_interval`, merging any intervals it overlaps, and return the resulting sorted, non-overlapping list.

**Constraints**
- `0 <= len(intervals) <= 10^4`
- `0 <= start <= end <= 10^5`
""",
        hints=["Work in three phases: copy the intervals that end before the new one starts, merge every interval that overlaps it, then copy the rest."],
        solution="""
def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    result = []
    start, end = new_interval
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    result.extend(intervals[i:])
    return result
""",
        explanation="""
Because the input is sorted, a single scan works. Intervals ending before `start` come first unchanged. Intervals that start at or before `end` overlap and get absorbed into the new interval. The rest follow unchanged.

- **Time:** O(n)
- **Space:** O(n) for the output
""",
        examples=[([[[1, 3], [6, 9]], [2, 5]], [[1, 5], [6, 9]]), ([[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]], [[1, 2], [3, 10], [12, 16]])],
        tests=[[[], [5, 7]], [[[1, 5]], [2, 3]], [[[1, 5]], [6, 8]], [[[3, 5]], [1, 2]], [[[1, 5]], [5, 7]]],
    ),
    dict(
        slug="merge-intervals",
        title="Merge Intervals",
        difficulty="Medium",
        sig="def merge(intervals: List[List[int]]) -> List[List[int]]:",
        desc="""
Given a list of `[start, end]` intervals, merge every pair that overlaps (intervals that share an endpoint count as overlapping). Return the merged intervals **sorted by start**.

**Constraints**
- `1 <= len(intervals) <= 10^4`
""",
        hints=["Sort the intervals by start. Then each interval either extends the last merged interval or starts a new one."],
        solution="""
def merge(intervals: List[List[int]]) -> List[List[int]]:
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
""",
        explanation="""
After sorting by start, overlaps can only happen between an interval and the most recently merged one. Extend that one's end, or start a new interval.

- **Time:** O(n log n)
- **Space:** O(n)
""",
        examples=[([[[1, 3], [2, 6], [8, 10], [15, 18]]], [[1, 6], [8, 10], [15, 18]]), ([[[1, 4], [4, 5]]], [[1, 5]])],
        tests=[[[[1, 4], [0, 4]]], [[[1, 4], [2, 3]]], [[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]], [[[5, 6]]]],
    ),
    dict(
        slug="non-overlapping-intervals",
        title="Non-overlapping Intervals",
        difficulty="Medium",
        sig="def erase_overlap_intervals(intervals: List[List[int]]) -> int:",
        desc="""
Return the **minimum number of intervals to remove** so that the remaining intervals don't overlap. Intervals that only touch at an endpoint (like `[1,2]` and `[2,3]`) do not overlap.

**Constraints**
- `1 <= len(intervals) <= 10^5`
""",
        hints=["Keep as many intervals as possible. Greedily keep the interval that ends earliest, since it leaves the most room."],
        solution="""
def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    removed = 0
    prev_end = float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= prev_end:
            prev_end = end
        else:
            removed += 1
    return removed
""",
        explanation="""
This is the classic activity-selection problem. Sort by end time and keep each interval that starts at or after the last kept end; every other interval must be removed. Picking the earliest end always leaves the most room for the rest.

- **Time:** O(n log n)
- **Space:** O(1) beyond sorting
""",
        examples=[([[[1, 2], [2, 3], [3, 4], [1, 3]]], 1), ([[[1, 2], [1, 2], [1, 2]]], 2), ([[[1, 2], [2, 3]]], 0)],
        tests=[[[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]]], [[[-52, 31], [-73, -26], [82, 97], [-65, -11], [-62, -49], [95, 99], [58, 95], [-31, 49], [66, 98], [-63, 2], [30, 47], [-40, -26]]], [[[1, 100], [11, 22], [1, 11], [2, 12]]]],
    ),
    dict(
        slug="meeting-rooms",
        title="Meeting Rooms",
        difficulty="Easy",
        sig="def can_attend_meetings(intervals: List[List[int]]) -> bool:",
        desc="""
Given meeting time intervals `[start, end]`, return `True` if one person could attend all of them, meaning no two meetings overlap. A meeting ending at time `t` doesn't conflict with one starting at `t`.

**Constraints**
- `0 <= len(intervals) <= 10^4`
""",
        hints=["Sort by start time and check each meeting against the previous one."],
        solution="""
def can_attend_meetings(intervals: List[List[int]]) -> bool:
    intervals = sorted(intervals)
    return all(intervals[i][0] >= intervals[i - 1][1] for i in range(1, len(intervals)))
""",
        explanation="""
After sorting by start time, a conflict can only occur between neighbours: each meeting must start no earlier than the previous one ends.

- **Time:** O(n log n)
- **Space:** O(n) for the sorted copy
""",
        examples=[([[[0, 30], [5, 10], [15, 20]]], False), ([[[7, 10], [2, 4]]], True)],
        tests=[[[]], [[[5, 8], [8, 9]]], [[[1, 5], [2, 3]]], [[[9, 10], [1, 2], [4, 9]]]],
    ),
    dict(
        slug="meeting-rooms-ii",
        title="Meeting Rooms II",
        difficulty="Medium",
        sig="def min_meeting_rooms(intervals: List[List[int]]) -> int:",
        desc="""
Given meeting time intervals `[start, end]`, return the minimum number of rooms needed so every meeting gets a room. A room freed at time `t` can be reused by a meeting starting at `t`.

**Constraints**
- `0 <= len(intervals) <= 10^4`
""",
        hints=["Sort by start time. Keep a min-heap of end times for rooms in use.", "If the earliest-ending room is free by the time the next meeting starts, reuse it (pop); then push this meeting's end."],
        solution="""
def min_meeting_rooms(intervals: List[List[int]]) -> int:
    ends = []
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heappop(ends)
        heappush(ends, end)
    return len(ends)
""",
        explanation="""
Process meetings by start time with a min-heap of end times. If the room that frees up soonest is already free, reuse it; otherwise open another room. The heap's final size is the peak number of rooms used at once.

- **Time:** O(n log n)
- **Space:** O(n)

Alternative: sort starts and ends separately and sweep with two pointers.
""",
        examples=[([[[0, 30], [5, 10], [15, 20]]], 2), ([[[7, 10], [2, 4]]], 1)],
        tests=[[[]], [[[1, 5], [5, 10]]], [[[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]]], [[[1, 2], [1, 2], [1, 2]]]],
    ),
]
