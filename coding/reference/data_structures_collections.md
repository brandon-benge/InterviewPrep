# Data Structures & Collections

## Overview
Essential Python data structures and collections for efficient data manipulation, storage, and retrieval.

---

## Core Data Structures

```python
# Set
s = set(); s.add(1); s.remove(1); is_empty = not s  # What: Unordered collection of unique elements. Why: Fast membership tests, removing duplicates.

# Dict
d = {'a': 1}; d['b'] = 2; value = d.get('a'); is_empty = not d  # What: Key-value pairs, fast lookups. Why: Store and retrieve data by key efficiently.
maybe_a = d.get('A')  # None if 'A' is missing
has_a = 'A' in d  # True only if key exists
a_is_none = has_a and d['A'] is None  # Distinguishes missing key vs present key with None value
missing_or_none = d.get('A') is None  # True when key is missing OR value is None

# List
l = [1, 2]; l.append(3); l.remove(2); l[0] = 10; last = l[-1]; popped = l.pop(); is_empty = not l  # What: Ordered, mutable sequence. Why: Store collections, easy to modify, can use pop like a queue. Hazard: single-threaded

# Tuple
t = (1, 2, 3); is_empty = not t  # What: Ordered, immutable sequence. Why: Fixed data, hashable, can be dict keys.
```

---

## Advanced Collections

```python
from collections import Counter, defaultdict, deque, OrderedDict

# Counter - count frequencies, find most common elements
freq = Counter("hello"); most_common = freq.most_common(2); freq['x'] += 1; is_empty = not freq  # What: Counts hashable objects. Why: Frequency analysis, safe incrementing.
print(most_common)  # [('l', 2), ('h', 1)] - Returns list of (element, count) tuples in descending frequency order

# defaultdict - automatically create default values for missing keys
g = defaultdict(list); g['key'].append('value'); is_empty = not g  # What: Dict with factory function for missing keys. Why: Avoid KeyError, great for grouping.
print(g['nonexistent'])  # [] - Creates empty list automatically using factory function
print(g)  # defaultdict(<class 'list'>, {'key': ['value'], 'nonexistent': []}) - Shows factory function and all created keys

# deque - double-ended queue with fast O(1) operations on both ends
q = deque([1, 2], maxlen=3); q.extend([5, 6, 8]); q.append(9); q.appendleft(0); is_empty = not q  # What: Double-ended queue. Why: Fast operations on both ends, Breadth-First Search(graph/tree traversal), sliding window.
print(q)  # deque([0, 6, 8], maxlen=3) - Fixed-size circular buffer auto-discards oldest when full
print(q.pop())  # 8 - Removes and returns rightmost element, q becomes deque([0, 6], maxlen=3)
print(f"maxlen: {q.maxlen}")  # maxlen: 3 - Shows the maximum size limit

# OrderedDict - maintains insertion order with O(1) move_to_end
od = OrderedDict([('a', 1)]); od['b'] = 2; od.move_to_end('a'); oldest = od.popitem(last=False); is_empty = not od  # What: Dict that remembers insertion order. Why: LRU cache, ordered operations.
print(list(od.keys()))  # ['b'] - Maintains order after move_to_end and popitem operations
print(oldest)  # ('a', 1) - The key-value tuple that was removed by popitem(last=False)
print(list(od.items()))  # [('b', 2)] - Shows remaining key-value pairs in order


# bisect - binary search helpers for sorted lists
from bisect import bisect_left, insort, bisect_right
scores = [10, 20, 20, 40]; new_score = 20  # scores stays a sorted list; new_score is the value you want to place
left_idx = bisect_left(scores, new_score); right_idx = bisect_right(scores, new_score)  # left_idx=1, right_idx=3 for this example
insort(scores, new_score)  # scores becomes [10, 20, 20, 20, 40]; What: insert into sorted order. Why: keep list sorted without calling sorted() again.
scores.insert(left_idx, new_score)   # insert before existing duplicates
scores.insert(right_idx, new_score)  # insert after existing duplicates
before_dupes = scores[:left_idx] # list before 20
is_empty = not scores  # Sorted list empty check
```

### `heapq` Heap Operations
```python
import heapq

# heapq - heap utilities that maintain a min-heap inside a regular list
h = [5, 1, 8, 3]
heapq.heapify(h)  # What: transforms list into min-heap in O(n). Why: start heap operations efficiently.
smallest = h[0]  # Peek smallest item without removing it
heapq.heappush(h, 2)  # Push new item while preserving heap property
next_smallest = heapq.heappop(h)  # Pop smallest item
smallest = heapq.heappushpop(h, 4)  # Push then pop smallest; useful for fixed-size top-k heaps
smallest = heapq.heapreplace(h, 6)  # Pop smallest then push; assumes heap is non-empty
largest_two = heapq.nlargest(2, h)  # Largest k elements without fully sorting descending
smallest_two = heapq.nsmallest(2, h)  # Smallest k elements without fully sorting ascending
is_empty = not h  # Heap is just a list under the hood

# Max-heap pattern in Python: negate numeric values
max_heap = []
heapq.heappush(max_heap, -10); heapq.heappush(max_heap, -3)
largest = -heapq.heappop(max_heap)
```

**Use when:** Repeatedly need the smallest/largest item, top-k problems, scheduling, streaming medians, merge-k-sorted-lists.

**Common operations:**
- `heapq.heapify(nums)` converts a list into a min-heap in `O(n)`.
- `heapq.heappush(heap, x)` inserts an item in `O(log n)`.
- `heapq.heappop(heap)` removes the smallest item in `O(log n)`.
- `heapq.heappushpop(heap, x)` is efficient when maintaining a fixed-size heap.
- `heapq.heapreplace(heap, x)` replaces the smallest item; heap must be non-empty.
- `heapq.nlargest(k, iterable, key=...)` gets top `k` largest items.
- `heapq.nsmallest(k, iterable, key=...)` gets top `k` smallest items.

---

## Queue Operations

#### queue.Queue (put/get)
**Use when:** Thread-safe operations, producer/consumer patterns
```python
import queue
q = queue.Queue(maxsize=10); q.put('item'); item = q.get(); q.task_done(); is_empty = q.empty()  # What: Thread-safe FIFO queue. Why: Producer/consumer patterns, multi-threading.
print(f"Queue size: {q.qsize()}")  # 0 - Shows current number of items in queue after get operation

try: # Non-blocking variants
    q.put(item, block=False)  # Raises queue.Full if full
    item = q.get(block=False) # Raises queue.Empty if empty
except (queue.Full, queue.Empty):
    pass
```

### Queue Types Comparison
```python
import queue
fifo_q = queue.Queue(); fifo_empty = fifo_q.empty() # FIFO Queue (First In, First Out)
lifo_q = queue.LifoQueue(); lifo_empty = lifo_q.empty() # LIFO Queue (Last In, First Out) - Stack
pq = queue.PriorityQueue(); pq_empty = pq.empty() # Priority Queue (lowest priority first)
pq.put((priority, item))  # Lower numbers = higher priority
```

---
