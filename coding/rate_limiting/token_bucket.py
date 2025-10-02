# Token Bucket Rate Limiter

# Problem Statement:
# Implement a token bucket rate limiter. Tokens refill at a constant rate. A request is allowed only if at least 1 token is available.

# Key Concepts:
# - refill_rate: Time interval (in seconds) between adding each token
#   Example: refill_rate = 1 means "add 1 token every 1 second"
#   Example: refill_rate = 2 means "add 1 token every 2 seconds" 
#   Example: refill_rate = 0.5 means "add 1 token every 0.5 seconds"

# - refill_time: Tracks the last time (in seconds since start) when tokens were added
#   Used to calculate elapsed time: current_time - refill_time

# - tick(now_sec): Manual time advancement where now_sec = seconds since system start
#   This simulates the passage of time for testing purposes

# - Time tracking: All times are relative to a "time 0" baseline
#   tick(5) means "5 seconds have passed since start"
#   tick(10) means "10 seconds have passed since start"

# Example:
# - Bucket capacity: 5
# - Refill rate: 1 (add 1 token every 1 second)
# - Initially 5 tokens; 5 requests allowed immediately
# - After tick(5), 5 new tokens are available (if bucket was empty)
# - After tick(7), only 2 more tokens added since last refill at tick(5)

# Token Refill Calculation:
# tokens_to_add = floor((current_time - last_refill_time) / refill_rate)
# Example: If 3.7 seconds elapsed with refill_rate=1, you get floor(3.7/1) = 3 tokens

import math
import threading

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.current_count = capacity
        self.refill_time = 0
        self.lock = threading.Lock()

    def change_transaction(self, int_change):
        with self.lock:
            self.current_count += int_change
            return self.current_count
    

    def allow_request(self) -> bool:
        token = self.change_transaction(-1)
        if token >= 0:
            return True
        else:
            self.change_transaction(1)
            return False

    
    def tick(self, now_sec: int):
        time_elapsed_sec = now_sec - self.refill_time 
        tokens_to_add = min(math.floor(time_elapsed_sec / self.refill_rate), (self.capacity - self.current_count))
        self.refill_time = self.refill_time + (self.refill_rate * tokens_to_add)
        self.change_transaction(tokens_to_add)

    def getToken(self):
        if self.allow_request():
            print("Success: you got a token")
            return True
        else:
            print("Warning: wait for a token")
            return False
        
    
if __name__ == "__main__":
    print("=== Token Bucket Rate Limiter Tests ===\n")
    
    # Test 1: Initial token usage
    print("Test 1: Using initial tokens")
    tokenbucket = TokenBucketRateLimiter(5, 1)
    print(f"Initial tokens: {tokenbucket.current_count}")
    
    for i in range(6):  # Try 6 requests with 5 capacity
        result = tokenbucket.getToken()
        print(f"After request {i+1}: tokens = {tokenbucket.current_count}")
    print()
    
    # Test 2: Manual refill with tick
    print("Test 2: Refill after 5 seconds")
    print(f"Before tick(5): tokens = {tokenbucket.current_count}")
    tokenbucket.tick(5)
    print(f"After tick(5): tokens = {tokenbucket.current_count}")
    
    # Try getting tokens after refill
    print("Trying to get tokens after refill:")
    for i in range(3):
        result = tokenbucket.getToken()
        print(f"Request {i+1}: tokens = {tokenbucket.current_count}")
    print()
    
    # Test 3: Partial refill
    print("Test 3: Partial refill")
    tokenbucket = TokenBucketRateLimiter(3, 1)  # 3 capacity, 1 token/sec
    
    # Use all tokens
    for i in range(3):
        tokenbucket.getToken()
    print(f"After using all tokens: {tokenbucket.current_count}")
    
    # Refill with 2 seconds (should get 2 tokens)
    tokenbucket.tick(2)
    print(f"After tick(2): {tokenbucket.current_count}")
    
    # Test 4: Overflow protection
    print("\nTest 4: Overflow protection")
    tokenbucket = TokenBucketRateLimiter(2, 1)  # 2 capacity
    tokenbucket.getToken()  # Use 1 token
    print(f"After using 1 token: {tokenbucket.current_count}")
    
    tokenbucket.tick(10)  # 10 seconds - should cap at capacity
    print(f"After tick(10): {tokenbucket.current_count} (should be capped at 2)")



