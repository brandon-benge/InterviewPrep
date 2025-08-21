# Least Recently Used (LRU) Cache

Problem Statement:
Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following operations: `get` and `put`.
- `get(key)` - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
- `put(key, value)` - Set or insert the value if the key is not already present. When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.

Examples:
1. `LRUCache cache = new LRUCache(2);`
2. `cache.put(1, 1); cache.put(2, 2); cache.get(1);` → returns `1`
3. `cache.put(3, 3); cache.get(2);` → returns `-1` (not found)

```python
class LRUCache:
    def __init__(self, capacity: int):
        ...

    def get(self, key: int) -> int:
        ...
```
