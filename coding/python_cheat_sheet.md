# Python Cheat Sheet: Concepts, Syntax & Reminders

## Overview

> This cheat sheet summarizes essential Python concepts, syntax, and practical reminders for interviews and daily coding. Each section covers what, why, and how to use core Python features.

---

## Data Structures

### Sets
**What:** Unordered collection of unique elements.
**Why:** Fast membership tests, removing duplicates.
**How:**
```python
my_set = {1, 2, 3}
my_set.add(4)
my_set.remove(2)
```

### Dictionaries
**What:** Key-value pairs, fast lookups.
**Why:** Store and retrieve data by key efficiently.
**How:**
```python
my_dict = {'a': 1, 'b': 2}
my_dict['c'] = 3
value = my_dict.get('a')
```

### Lists
**What:** Ordered, mutable sequence.
**Why:** Store collections, easy to modify.
**How:**
```python
my_list = [1, 2, 3]
my_list.append(4)
my_list[0] = 10
```

### Tuples
**What:** Ordered, immutable sequence.
**Why:** Fixed data, hashable, can be dict keys.
**How:**
```python
my_tuple = (1, 2, 3)
```

---

## Dataclasses
**What:** Classes for storing structured data with less boilerplate.
**Why:** Auto-generates `__init__`, `__repr__`, `__eq__`, and more, making code cleaner and easier to maintain.
**How:**
```python
from dataclasses import dataclass

# 1. Define a dataclass
@dataclass
class Point:
    x: int
    y: int

# 2. Create instances
p1 = Point(1, 2)
p2 = Point(x=3, y=4)

# 3. Access fields
print(p1.x)  # 1
print(p2.y)  # 4

# 4. Comparison and representation
print(p1)         # Point(x=1, y=2)
print(p1 == Point(1, 2))  # True

# 5. Default values
@dataclass
class User:
    name: str
    active: bool = True

u = User("Alice")
print(u)  # User(name='Alice', active=True)

# 6. Type hints and optional fields
from typing import Optional

@dataclass
class Book:
    title: str
    author: Optional[str] = None

b = Book("Python 101")
print(b)  # Book(title='Python 101', author=None)
```

**Summary:**
- Use `@dataclass` above a class definition.
- Define fields with type hints.
- Instantiation is simple: `obj = ClassName(field1, field2)`.
- Fields can have default values and type hints.
- Dataclasses provide readable string representations and easy comparisons.
```

---

## Loops
### For loop
```python
for i in range(5):
    print(i)
```

**While loop:**
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

---

### Looping Through Data Structures

**List:**
```python
my_list = [1, 2, 3]
for item in my_list:
    print(item)
```

**Tuple:**
```python
my_tuple = (1, 2, 3)
for item in my_tuple:
    print(item)
```

**Set:**
```python
my_set = {1, 2, 3}
for item in my_set:
    print(item)
```

**Dictionary (keys):**
```python
my_dict = {'a': 1, 'b': 2}
for key in my_dict:
    print(key)
```

**Dictionary (values):**
```python
for value in my_dict.values():
    print(value)
```

**Dictionary (key-value pairs):**
```python
for key, value in my_dict.items():
    print(f"{key}: {value}")
```

---

## Functions & Testing
**Define a function:**
```python
def add(a, b):
    return a + b
```

### Simple Assertion Test
```python
def test_add():
    assert add(2, 3) == 5

# Call the test directly by invoking the function:
test_add()  # If assertion fails, you'll get an AssertionError

# You can call this in a script, notebook, or interactive shell:
#
# >>> test_add()
# (No output if the test passes)
# >>> test_add()
# Traceback (most recent call last):
#   ...
# AssertionError

# You can also call multiple test functions in a row:
def test_subtract():
    assert (5 - 2) == 3

test_add()
test_subtract()
```

---

## Exception Handling
**Try/Except:**
```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

---


## Quick Reference
- Use `set()` for unique items
- Use `dict()` for key-value storage
- Use `list()` for ordered, mutable data
- Use `tuple()` for ordered, immutable data
- Use `@dataclass` for simple data containers
- Use `for` and `while` for iteration
- Use `def` to define functions
- Use `assert` for simple tests
- Use `try/except` for error handling

---

## Interview Must‑Haves (Python)

### Time & Space Complexity Cheats
- `list`: index O(1), append amortized O(1), insert/delete middle O(n)
- `dict` / `set`: average O(1) get/put, worst O(n)
- `heapq`: push/pop O(log n)

### Core Libraries & Idioms
**collections** — Useful for counting, grouping, and efficient queue operations.
```python
from collections import Counter, defaultdict, deque
# Counter: Count frequencies, find most common elements
freq = Counter(s)  # freq['a'] gives count of 'a' in s

# defaultdict: Automatically create default values for missing keys (great for grouping)
g = defaultdict(list)
for u, v in edges:
    g[u].append(v)  # builds adjacency list for a graph

# deque: Fast O(1) pops from both ends (useful for BFS, sliding window)
q = deque([start])
q.append(x)        # add to right
x = q.popleft()    # remove from left
```

**heapq** — Implements a min-heap for efficient priority queue operations.
```python
import heapq
h = []
heapq.heappush(h, x)  # add x to heap
x = heapq.heappop(h)  # remove and return smallest item
# For max-heap, push negative values: heappush(h, -x)
```

**bisect** — Binary search utilities for sorted lists (find insertion points).
```python
import bisect
i = bisect.bisect_left(a, target)   # first index with a[i] >= target
j = bisect.bisect_right(a, target)  # first index with a[j] > target
# Useful for fast lookups and insertions in sorted lists
```

**itertools** — Tools for combinatorics, iteration, and grouping.
```python
from itertools import combinations, product, accumulate, groupby
pairs = list(combinations(nums, 2))  # all pairs from nums
# product: cartesian product, accumulate: running totals, groupby: group consecutive items
```

**functools** — Functional programming helpers (memoization, custom sorting).
```python
from functools import lru_cache, cmp_to_key
@lru_cache(None)
def dp(i, j):
    ...  # memoized recursive function
# cmp_to_key: convert old-style comparison to key function for sorting
```

**math** — Math functions and constants.
```python
from math import gcd, inf
lcm = a // gcd(a, b) * b  # least common multiple
# inf: positive infinity, useful for initial values in algorithms
```

### Sorting Tricks
**Sorting Tricks** — Quickly sort lists and custom objects.
```python
sorted_nums = sorted(nums)  # sort a list in ascending order
sorted_pairs = sorted(pairs, key=lambda p: (p[0], -p[1]))  # sort by first element, then descending second
```

### Slicing, Comprehensions, Built‑ins
**Slicing, Comprehensions, Built-ins** — Powerful ways to manipulate and create lists and sequences.
```python
rev = s[::-1]  # reverse a string or list
arr2 = [f(x) for x in arr if cond(x)]  # list comprehension with condition
pairs = list(zip(a, b))  # pair up elements from two lists
for i, x in enumerate(arr):  # get index and value while looping
    ...
```

---

## Reusable Templates

### Sliding Window (variable length)
**Sliding Window (variable length)** — Efficiently find subarrays or substrings that meet a condition.
```python
def longest_subarray_at_most_k_distinct(nums, k):
    from collections import Counter
    cnt, left, best = Counter(), 0, 0
    for right, x in enumerate(nums):
        cnt[x] += 1
        while len(cnt) > k:
            cnt[nums[left]] -= 1
            if cnt[nums[left]] == 0:
                cnt.pop(nums[left])
            left += 1
        best = max(best, right - left + 1)
    return best
```

### Binary Search on Answer (monotonic predicate)
**Binary Search on Answer (monotonic predicate)** — Find the smallest/largest value that satisfies a condition.
```python
def bs(lo, hi, ok):
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### DFS / Backtracking
**DFS / Backtracking** — Explore all possible solutions, often used for permutations, combinations, and puzzles.
```python
def backtrack(path, i):
    if done(path):
        ans.append(path[:])
        return
    for choice in choices(i, path):
        path.append(choice)
        backtrack(path, i + 1)
        path.pop()
```

### BFS (graph / grid)
**BFS (graph / grid)** — Breadth-first search for shortest paths and level-order traversal.
```python
from collections import deque
def bfs(start):
    q = deque([start]); seen = {start}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
```

### Topological Sort (Kahn’s)
**Topological Sort (Kahn’s)** — Order tasks with dependencies, detect cycles in directed graphs.
```python
from collections import deque, defaultdict
def topo(n, edges):
    g = defaultdict(list); indeg = [0] * n
    for u, v in edges:
        g[u].append(v); indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0]); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []  # cycle if empty
```

### Dijkstra (non‑negative weights)
**Dijkstra (non‑negative weights)** — Find shortest paths from a source node in a weighted graph.
```python
import heapq
def dijkstra(n, g, src):
    dist = [float('inf')] * n; dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
```

### Union‑Find (Disjoint Set Union)
**Union‑Find (Disjoint Set Union)** — Track connected components, useful for Kruskal’s MST and cycle detection.
```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n)); self.r = [0] * n
    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True
```

### Prefix Sums / 2D Prefix
**Prefix Sums / 2D Prefix** — Quickly compute sums over ranges in arrays and grids.
```python
pref = [0]
for x in nums:
    pref.append(pref[-1] + x)
rng = pref[r] - pref[l]  # sum of nums[l..r-1]

# 2D prefix: sum of submatrices in a grid
P = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    row = 0
    for j in range(1, m + 1):
        row += grid[i - 1][j - 1]
        P[i][j] = P[i - 1][j] + row
def rect_sum(x1, y1, x2, y2):
    return P[x2 + 1][y2 + 1] - P[x1][y2 + 1] - P[x2 + 1][y1] + P[x1][y1]
```

---

## Graph & String Helpers
**Graph & String Helpers** — Common patterns for grids, graphs, and string manipulation.
- Grid directions: `DIRS = [(1,0),(-1,0),(0,1),(0,-1)]` — for moving up/down/left/right in a grid.
- Build adjacency: `from collections import defaultdict; g = defaultdict(list)` — create adjacency lists for graphs.

**Strings & hashing** — Useful for grouping, deduplication, and state tracking.
```python
sig = tuple(sorted(s))  # anagram signature for grouping anagrams
seen = set()            # track substrings or visited states
```

**Bit tricks** (subset DP) — Efficiently iterate over all subsets of a bitmask.
```python
sub = mask
while sub:
    # use sub
    sub = (sub - 1) & mask
```

**Defensive patterns** — Write robust code that handles edge cases and avoids common pitfalls.
- Check edge cases early (empty input, single element, duplicates)
- Use `float('inf')` / `-float('inf')` for bounds
- Avoid quadratic string concatenation in loops; collect and `''.join(parts)`
