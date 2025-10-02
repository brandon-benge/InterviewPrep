## TTL Cache

# **Problem Statement:**

# Implement a cache with time-to-live (TTL) functionality. 
# The cache should store key-value pairs and return the value only if it has not expired. 
# If the cached value has expired or does not exist, return `None`. 
# The TTL duration is fixed for all entries.

# **Examples:**

# - Assume TTL is 1000 milliseconds:
#   - `get("foo", now_ms=5000)` -> `None` (key not set)
#   - After setting `foo` at time 4000 ms with value "bar":
#     - `get("foo", now_ms=4500)` -> `"bar"` (not expired)
#     - `get("foo", now_ms=5100)` -> `None` (expired)

# - Multiple keys with different insertion times:
#   - Set `a` at 1000 ms, `b` at 1500 ms
#   - `get("a", now_ms=1800)` -> value if not expired
#   - `get("b", now_ms=2600)` -> `None` if expired

# - Without specifying `now_ms`, `get` should use current system time to determine expiration.

import time


class TTLCache:
    def __init__(self):
      self.now_ms = 0
      self.ttl = 1000
      self.cache = {}

    def set(self, key: str, value: str, now_ms: int | None = None):
      if now_ms is None:
        now_ms = time.time() * 1000
      self.cache[key] = (value, now_ms)
        
    def get(self, key: str, now_ms: int | None = None) -> object | None:
      if now_ms is None:
        now_ms = time.time() * 1000
      if key not in self.cache:
          return None
      
      value, timestamp = self.cache[key]  
      
      if timestamp < now_ms - self.ttl or timestamp > now_ms:
        return None

      return self.cache[key]  
        
  

if __name__ == "__main__":
    ttlcache = TTLCache()
    print(ttlcache.get("foo", now_ms=5000))
    ttlcache.set("foo", "bar", now_ms=4000)
    print(ttlcache.get("foo", now_ms=4500))
    print(ttlcache.get("foo", now_ms=5100))
    ttlcache.set("a", "value_a", now_ms=1000)
    ttlcache.set("b", "value_b", now_ms=1500)
    print(ttlcache.get("a", now_ms=1800))
    print(ttlcache.get("b", now_ms=2600))



