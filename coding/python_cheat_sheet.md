# Python Cheat Sheet: Concepts, Syntax & Reminders

## Overview

> This cheat sheet summarizes essential Python concepts, syntax, and practical reminders for interviews and daily coding. Each section covers what, why, and how to use core Python features.

---

## Quick Coding Interview Flow (2–5 min)

> A tight checklist to stay structured under pressure.

1) **Clarify & Restate (≤30s)**  
   Restate the goal, inputs/outputs, and corner cases. Ask about constraints (n, ranges, duplicates, ordering, streaming, memory limits).

2) **Work Small Examples (≤30s)**  
   One happy path + one edge case (empty, size 1, ties, negatives, unicode, etc.).

3) **Baseline > Better (≤60s)**  
   Describe a brute force in 1–2 sentences → estimate time/space → propose an improved approach and why it’s better. Confirm trade‑offs.

4) **Outline Before Code (≤30s)**  
   Verbal pseudocode in bullets (inputs → data structures → key loops/conditions → outputs).

5) **Code Cleanly (3–8 min)**  
   Name things well, handle edges early, keep helpers small.

6) **Test Aloud (≤60s)**  
   Dry‑run the examples; call out indices, counters, heap/top, set/dict contents at each key step.

7) **Complexity & Extensions (≤30s)**  
   State time/space, discuss alternative trade‑offs or follow‑ups (streaming, parallelism, distributed, larger alphabet, stability, stability of sort, etc.).

### Talk‑Track Template
```text
Goal: <problem>  
Input/Output: <types, ranges, order, duplicates?>  
Constraints: n≈?, time target?, memory?, in‑place?

Baseline: <very short> → O(...).  
Better idea: <DS/algorithm> because <property>.  
Plan: <steps 1‑2‑3>  
Edge cases: <list>
```

### Scratchpad Template
```python
from typing import List, Optional

def solve(...):
    # Guard / edge cases
    # Build / choose DS
    # Main loop / logic
    # Return result

# Quick tests (speak through these)
# print(solve(...))  # expect ...
# print(solve(...))  # edge ...
```

### Common Prompts to Ask
- Can I sort / mutate the input?  
- Are values bounded / integers only?  
- Is streaming required or can I store O(n)?  
- What should happen on ties / duplicates / empty input?  
- Do we need stable ordering or original indices?

### Time & Space Complexity Cheats
- `list`: index O(1), append amortized O(1), insert/delete middle O(n)
- `dict` / `set`: average O(1) get/put, worst O(n)
- `heapq`: push/pop O(log n)

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
my_list.remove(4)
my_list[0] = 10
value = my_list.pop(1)
last_item = my_list[-1]  # Access the last element
if not my_list[-1]:
    print("Last item is falsy!")  # True if last item is 0, '', None, False, etc.
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
# With enumerate:
for idx, item in enumerate(my_list):
    print(f"Index {idx}: {item}")
```

**Tuple:**
```python
my_tuple = (1, 2, 3)
for item in my_tuple:
    print(item)
# With enumerate:
for idx, item in enumerate(my_tuple):
    print(f"Index {idx}: {item}")
```

**Set:**
```python
my_set = {1, 2, 3}
for item in my_set:
    print(item)
# With enumerate:
for idx, item in enumerate(my_set):
    print(f"Index {idx}: {item}")
```

**Dictionary (keys):**
```python
my_dict = {'a': 1, 'b': 2}
for key in my_dict:
    print(key)
# With enumerate:
for idx, key in enumerate(my_dict):
    print(f"Index {idx}: {key}")
```

**Dictionary (values):**
```python
for value in my_dict.values():
    print(value)
# With enumerate:
for idx, value in enumerate(my_dict.values()):
    print(f"Index {idx}: {value}")
```

**Dictionary (key-value pairs):**
```python
for key, value in my_dict.items():
    print(f"{key}: {value}")
# With enumerate:
for idx, (key, value) in enumerate(my_dict.items()):
    print(f"Index {idx}: {key}: {value}")
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
def test_subtract():
    assert (5 - 2) == 3
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


## Interview Must‑Haves (Python)

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
q.pop()      # Removes (right end)
x = q.popleft()    # remove from left
```

**heapq** — Implements a min-heap for efficient priority queue operations.
```python
import heapq

nums = [3, 1, 4, 2, 5, 6]

# 3 largest elements
largest_three = heapq.nlargest(3, nums)

# 3 smallest elements
smallest_three = heapq.nsmallest(3, nums)

print("Largest three:", largest_three)    # Output: [6, 5, 4]
print("Smallest three:", smallest_three)  # Output: [1, 2, 3]
```


### Sorting Tricks
**Sorting Tricks** — Quickly sort lists and custom objects.
```python
# By first element only (ascending)
sorted_by_first = sorted(pairs, key=lambda x: x[0])
# By first, then second (both ascending)
sorted_by_first_second_asc = sorted(pairs, key=lambda p: (p[0], p[1]))
# By first ascending, second descending (common interview pattern)
sorted_by_first_asc_second_desc = sorted(pairs, key=lambda p: (p[0], -p[1]))
# All keys descending (global reverse)
sorted_all_desc = sorted(pairs, key=lambda p: (p[0], p[1]), reverse=True)

sorted_nums = sorted(nums)  # sort a list in ascending order
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


## Binary Trees

### Class and Build Function
```python
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(nodes):
    """Helper to build a binary tree from a list (level-order)."""
    if not nodes:
        return None
    root = TreeNode(nodes[0])
    queue = [root]
    i = 1
    while queue and i < len(nodes):
        node = queue.pop(0)
        if i < len(nodes) and nodes[i] is not None:
            node.left = TreeNode(nodes[i])
            queue.append(node.left)
        i += 1
        if i < len(nodes) and nodes[i] is not None:
            node.right = TreeNode(nodes[i])
            queue.append(node.right)
        i += 1
    return root
```

### InvertTree
```python
def invertTree(self, root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    self.invertTree(root.left)
    self.invertTree(root.right)
    return root
```

### LevelOrder
```python
def levelOrder(self, root):
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.pop(0)
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)
    return result
```

### DiameterOfBinaryTree
```python
def diameterOfBinaryTree(self, root):
    def depth(node):
        if not node:
            return 0
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        self.diameter = max(self.diameter, left_depth + right_depth)
        return max(left_depth, right_depth) + 1
    self.diameter = 0
    depth(root)
    return self.diameter
```

## Recursion
```python
    def generateParenthesis(self, n):
        result=[]
        length=2*n

        def recursive_string(string_var, open_left, open_right):
            if length == len(string_var):
                result.append(string_var)
                return

            if open_left < n:
                recursive_string(string_var+"(", open_left+1, open_right)
            if open_right < open_left:
                recursive_string(string_var+")", open_left, open_right+1)

        recursive_string("", 0, 0)
        return result
```

## Permutations
```python
    def permute(self, nums):
        results=[]
        def backtrack(front, back):
            if not back:
                results.append(front[:])
                return
            for i in range(len(back)):
                choice = back[i]
                front.append(choice)
                next_remaining = back[:i] + back[i+1:]
                backtrack(front, next_remaining)
                front.pop()
        backtrack([],nums)
        return results
```