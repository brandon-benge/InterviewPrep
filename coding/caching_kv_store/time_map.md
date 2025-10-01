# Time-Based Key-Value Store

Problem Statement:
Design a time-based key-value data structure that can store multiple values for the same key at different timestamps and retrieve the key's value at a certain timestamp.

Examples:
1. `set("foo", "bar", 1); get("foo", 1);` → `"bar"`
2. `get("foo", 3);` → `"bar"`
3. `set("foo", "bar2", 4); get("foo", 4); get("foo", 5);` → `"bar2"`, `"bar2"`

```python
class TimeMap:
    def __init__(self):
        ...

    def get(self, key: str, timestamp: int) -> str:
        ...
```
