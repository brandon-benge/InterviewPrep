from collections import defaultdict, deque
from typing import Any

class RateLimiter:
    def __str__(self):
        return (f"limiter_name={self.limiter_name}, "
                f"message={self.message}, threshold={self.threshold}, "
                f"current_time={self.current_time}")
    _ttl = 60
    _hist = defaultdict(deque)
    _events = []  # Store all RateLimiter instances

    def __init__(self, limiter_name : str, message : dict[str, Any], threshold : int, current_time : int):
        self.limiter_name = limiter_name
        self.message = message
        self.threshold = threshold
        self.current_time = current_time

    @classmethod
    def rateLimiter(cls, limiter_name : str, message : dict[str, Any], threshold : int, current_time : int):
        dq = cls._hist[limiter_name]
        cuttoff = current_time - cls._ttl
        while cls._hist[limiter_name] and dq[0] < cuttoff:
            dq.popleft(0)
        if len(dq) >= threshold:
            return False
        else:
            dq.append(current_time)
            cls._events.append(RateLimiter(limiter_name, message, threshold, current_time))
            return True
        return False
    
if __name__ == "__main__":
    messages = [
        ("limiterA", {"first_name": "Zane", "last_name": "Cross", "number": 99}, 3, 10),
        ("limiterA", {"first_name": "Amy", "last_name": "Smith", "number": 42}, 3, 12),
        ("limiterA", {"first_name": "Bob", "last_name": "Lee", "number": 7}, 3, 15),
        ("limiterA", {"first_name": "Eve", "last_name": "Stone", "number": 23}, 3, 18),
        ("limiterB", {"first_name": "John", "last_name": "Doe", "number": 1}, 2, 20),
        ("limiterB", {"first_name": "Jane", "last_name": "Doe", "number": 2}, 2, 22),
        ("limiterB", {"first_name": "Max", "last_name": "Payne", "number": 3}, 2, 25),
        ("limiterC", {"first_name": "Alice", "last_name": "Wonder", "number": 5}, 1, 30),
        ("limiterC", {"first_name": "Charlie", "last_name": "Brown", "number": 6}, 1, 32),
        ("limiterC", {"first_name": "Oscar", "last_name": "Wilde", "number": 8}, 1, 35)
    ]

    for msg in messages:
        allowed = RateLimiter.rateLimiter(*msg)
        print(f"{'Allowed' if allowed else 'Denied'}: {msg}")

    q = deque(RateLimiter._events)
    print("\nProcessing the following messages:")
    while q:
        processing = q.popleft()
        print(processing)