import time
from typing import Any

class RateLimiter:
    _cache = {}  # class-level cache
    _ttl = 10    # seconds

    def __init__(self, limiter_name : str, message : dict[str, Any], threshold : int, current_time : int):
        self.limiter_name = limiter_name
        self.message = message
        self.threshold = threshold
        self.current_time = current_time

    
    @classmethod
    def rateLimiter(cls, limiter_name : str, message : dict[str, Any], threshold : int, current_time : int):
        key_val = (limiter_name, message["first_name"])
        entry = cls._cache.get(key_val)
        if entry:
            instance, creation_time, message_num = entry
            if message_num > threshold:
                print(f"Blocking due to too many connections: {key_val} ")
                return False
            elif current_time - creation_time < cls._ttl:
                print("Updating cached object and returning")
                cls._cache[key_val] = (instance, creation_time, message_num+1)
                return True
            else:
                print("Cache expired, deleting cached entry and destroying instance")
                del cls._cache[key_val]
                del instance

        print("Creating new object")
        instance = cls(limiter_name, message, threshold, current_time)
        cls._cache[key_val] = (instance, current_time, 1)
        return True
    


if __name__ == "__main__":
    test_inputs = [
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 10 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 12 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Julie", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 13 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Smith", "number": 5 }, "threshold": 1, "current_time": 14 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 4 }, "threshold": 2, "current_time": 15 },
        { "limiter_name": "new_limiter_2", "message": { "first_name": "Nora", "last_name": "Benge", "number": 7 }, "threshold": 1, "current_time": 16 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 20 },
        { "limiter_name": "new_limiter_3", "message": { "first_name": "Eve", "last_name": "Johnson", "number": 3 }, "threshold": 3, "current_time": 22 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 8 }, "threshold": 1, "current_time": 24 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 4 }, "threshold": 5, "current_time": 30 },
        # Additional test cases for broader coverage and TTL expiry
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Brandon", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 45 },
        { "limiter_name": "new_limiter_2", "message": { "first_name": "Julie", "last_name": "Smith", "number": 9 }, "threshold": 2, "current_time": 46 },
        { "limiter_name": "new_limiter_2", "message": { "first_name": "Julie", "last_name": "Smith", "number": 9 }, "threshold": 2, "current_time": 47 },
        { "limiter_name": "new_limiter_2", "message": { "first_name": "Julie", "last_name": "Smith", "number": 9 }, "threshold": 2, "current_time": 48 },
        { "limiter_name": "new_limiter_4", "message": { "first_name": "Alice", "last_name": "Jones", "number": 1 }, "threshold": 3, "current_time": 49 },
        { "limiter_name": "new_limiter_4", "message": { "first_name": "Bob", "last_name": "Martin", "number": 2 }, "threshold": 1, "current_time": 50 },
        { "limiter_name": "new_limiter_4", "message": { "first_name": "Alice", "last_name": "Jones", "number": 1 }, "threshold": 3, "current_time": 55 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Nora", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 60 },
        { "limiter_name": "new_limiter_1", "message": { "first_name": "Nora", "last_name": "Benge", "number": 4 }, "threshold": 1, "current_time": 61 },
        { "limiter_name": "new_limiter_5", "message": { "first_name": "Zane", "last_name": "Cross", "number": 99 }, "threshold": 5, "current_time": 62 }
    ]
    for i in test_inputs:
        if RateLimiter.rateLimiter(i["limiter_name"], i["message"], i["threshold"], i["current_time"]):
            instance, creation_time, message_num =  RateLimiter._cache[i["limiter_name"], i["message"]["first_name"]]
            print("memory location: ",f"{id(instance)}",  )
    

    
