# Data Structures & Collections

## Overview
Essential Python data structures and collections for efficient data manipulation, storage, and retrieval.

---

## Core Data Structures

```python
# Set
s = set(); s.add(1); s.remove(1)  # What: Unordered collection of unique elements. Why: Fast membership tests, removing duplicates.

# Dict
d = {'a': 1}; d['b'] = 2; value = d.get('a')  # What: Key-value pairs, fast lookups. Why: Store and retrieve data by key efficiently.

# List
l = [1, 2]; l.append(3); l.remove(2); l[0] = 10; last = l[-1]; popped = l.pop()  # What: Ordered, mutable sequence. Why: Store collections, easy to modify, can use pop like a queue. Hazard: single-threaded

# Tuple
t = (1, 2, 3)  # What: Ordered, immutable sequence. Why: Fixed data, hashable, can be dict keys.
```

---

## Advanced Collections

```python
from collections import Counter, defaultdict, deque, OrderedDict

# Counter - count frequencies, find most common elements
freq = Counter("hello"); most_common = freq.most_common(2); freq['x'] += 1  # What: Counts hashable objects. Why: Frequency analysis, safe incrementing.
print(most_common)  # [('l', 2), ('h', 1)] - Returns list of (element, count) tuples in descending frequency order

# defaultdict - automatically create default values for missing keys
g = defaultdict(list); g['key'].append('value')  # What: Dict with factory function for missing keys. Why: Avoid KeyError, great for grouping.
print(g['nonexistent'])  # [] - Creates empty list automatically using factory function
print(g)  # defaultdict(<class 'list'>, {'key': ['value'], 'nonexistent': []}) - Shows factory function and all created keys

# deque - double-ended queue with fast O(1) operations on both ends
q = deque([1, 2], maxlen=3); q.extend([5, 6, 8]); q.append(9); q.appendleft(0)  # What: Double-ended queue. Why: Fast operations on both ends, Breadth-First Search(graph/tree traversal), sliding window.
print(q)  # deque([0, 6, 8], maxlen=3) - Fixed-size circular buffer auto-discards oldest when full
print(q.pop())  # 8 - Removes and returns rightmost element, q becomes deque([0, 6], maxlen=3)
print(f"maxlen: {q.maxlen}")  # maxlen: 3 - Shows the maximum size limit

# OrderedDict - maintains insertion order with O(1) move_to_end
od = OrderedDict([('a', 1)]); od['b'] = 2; od.move_to_end('a'); oldest = od.popitem(last=False)  # What: Dict that remembers insertion order. Why: LRU cache, ordered operations.
print(list(od.keys()))  # ['b'] - Maintains order after move_to_end and popitem operations
print(oldest)  # ('a', 1) - The key-value tuple that was removed by popitem(last=False)
print(list(od.items()))  # [('b', 2)] - Shows remaining key-value pairs in order
```

---

## Queue Operations

#### queue.Queue (put/get)
**Use when:** Thread-safe operations, producer/consumer patterns
```python
import queue
q = queue.Queue(maxsize=10); q.put('item'); item = q.get(); q.task_done()  # What: Thread-safe FIFO queue. Why: Producer/consumer patterns, multi-threading.
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
fifo_q = queue.Queue() # FIFO Queue (First In, First Out)
lifo_q = queue.LifoQueue() # LIFO Queue (Last In, First Out) - Stack
pq = queue.PriorityQueue() # Priority Queue (lowest priority first)
pq.put((priority, item))  # Lower numbers = higher priority
```

---