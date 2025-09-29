# LRU Cache

Problem Statement:
Design a data structure that implements an LRU (Least Recently Used) cache with O(1) `get()` and `put()` operations using a fixed capacity.

Example:
lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
lru.get(1)       → 1
lru.put(3, 3)    → evicts key 2
lru.get(2)       → -1 (not found)

```python
class LRUCache:
    def __init__(self, capacity: int):
        ...
        
    def get(self, key: int) -> int:
        ...

    def put(self, key: int, value: int) -> None:
        ...