# Time-Based Key-Value Store

# Problem Statement:
# Design a time-based key-value data structure that can store multiple values for the same key at different timestamps and retrieve the key's value at a certain timestamp.

# Examples:
# 1. `set("foo", "bar", 1); get("foo", 1);` → `"bar"`
# 2. `get("foo", 3);` → `"bar"`
# 3. `set("foo", "bar2", 4); get("foo", 4); get("foo", 5);` → `"bar2"`, `"bar2"`
from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list) # list so that we can loop through it

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        
        # Binary search for the largest timestamp <= requested timestamp
        timestamps_values = self.store[key]
        
        # Extract just timestamps for binary search
        timestamps = [tv[0] for tv in timestamps_values]
        
        # Find insertion point
        idx = bisect.bisect_right(timestamps, timestamp)
        
        # If idx is 0, no timestamp <= requested timestamp exists
        if idx == 0:
            return ""
        
        # Return the value at the largest timestamp <= requested timestamp
        return timestamps_values[idx - 1][1]

    def set(self, key: str, val: str, timestamp: int) -> str:
        bisect.insort(self.store[key], (timestamp, val))
        return self.store[key]



if __name__ == "__main__":
    timemap = TimeMap()
    timemap.set("foo", "bar", 1)
    print(timemap.get("foo", 1))
    print(timemap.get("foo", 3))
    timemap.set("foo", "bar2", 4)
    print(timemap.get("foo", 4))
    print(timemap.get("foo", 5))