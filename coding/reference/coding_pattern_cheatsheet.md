# Coding Pattern Cheat Sheet

## 1. Grouping → HashMap

```python
from collections import defaultdict

transactions = [("A", 10), ("B", 5), ("A", 3)]
balances = defaultdict(int)

for user, amount in transactions:
    balances[user] += amount

print(dict(balances))

```

---

## 2. Time-Based → Sort / Binary Search / Deque

```python
# Sort
events = [(10, "A"), (5, "B"), (8, "C")]
events.sort()
print(events)

# Binary Search
import bisect
timestamps = [5, 8, 10, 15]
target = 9
i = bisect.bisect_right(timestamps, target)
print(timestamps[i])
timestamps.insert(i, target)
print(timestamps)

# Deque
from collections import deque

window = deque()
events = [(1, 100), (2, 200), (4, 300), (7, 400)]  # (timestamp, value)
window_size = 3

for timestamp, value in events:
    window.append((timestamp, value))
    while window and timestamp - window[0][0] > window_size:
        window.popleft()
    print(list(window))
```

---

## 3. Ranking → Heap(priority queue)

```python
import heapq
from collections import Counter

nums = [1,1,1,2,2,3]
count = Counter(nums)

top_k = heapq.nlargest(2, count.keys(), key=lambda x: count[x])
print(top_k)

tasks = [
    ("A", 0),
    ("A", 1),
    ("B", 2),
    ("A", 3),
]
remaining = Counter(task_id for task_id, _timestamp in tasks)
top_k = heapq.nlargest(1, remaining.keys(), key=lambda x: remaining[x])
print(top_k)

# if you need a cache use `OrderedDict`
```

---

## 4. Intervals → Merge Logic

```python
intervals = [[1,3],[2,6],[8,10]]
intervals.sort()

merged = []
for start, end in intervals:
    if not merged or merged[-1][1] < start:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)

print(merged)
```

---


## Mental Model

- Grouping → hashmap  
- Time-based → sort / binary search / deque  
- Ranking → heap  
- Intervals → merge logic
