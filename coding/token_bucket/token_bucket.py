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

# - Automatic time tracking: getToken() automatically updates tokens based on elapsed real time
#   Time is measured from when the bucket was created (start_time)

# Example:
# - Bucket capacity: 5
# - Refill rate: 1 (add 1 token every 1 second)
# - Initially 5 tokens; 5 requests allowed immediately
# - After 5 seconds, 5 new tokens are available (if bucket was empty)
# - Tokens automatically refill based on real elapsed time

# Token Refill Calculation:
# tokens_to_add = floor((current_time - last_refill_time) / refill_rate)
# Example: If 3.7 seconds elapsed with refill_rate=1, you get floor(3.7/1) = 3 tokens


import math
import threading
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.current_count = capacity
        self.refill_time = 0
        self.lock = threading.Lock()
        self.start_time = time.time()

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
        with self.lock:
            time_elapsed_sec = now_sec - self.refill_time 
            tokens_to_add = min(math.floor(time_elapsed_sec / self.refill_rate), (self.capacity - self.current_count))
            self.refill_time = self.refill_time + (self.refill_rate * tokens_to_add)
            # Instead of calling change_transaction(), directly update:
            self.current_count += tokens_to_add

    def getToken(self):
        self.tick(time.time() - self.start_time)
        if self.allow_request():
            print("Success: you got a token")
            return True
        else:
            print("Warning: wait for a token")
            return False
        
    
if __name__ == "__main__":
    print("=== Token Bucket Rate Limiter Tests ===\n")
    
    # Test 1: Using initial tokens
    print("Test 1: Using initial tokens")
    tokenbucket = TokenBucketRateLimiter(5, 1)
    print(f"Initial tokens: {tokenbucket.current_count}")
    
    for i in range(6):  # Try 6 requests with 5 capacity
        result = tokenbucket.getToken()
        print(f"After request {i+1}: tokens = {tokenbucket.current_count}")
    print()
    
    # Test 2: Wait for refill (automatic with real time)
    print("Test 2: Waiting for automatic refill...")
    time.sleep(2)  # Wait 2 seconds for tokens to refill
    print("After waiting 2 seconds:")
    for i in range(3):
        result = tokenbucket.getToken()
        print(f"Request {i+1}: tokens = {tokenbucket.current_count}")
    print()
    
    # Test 3: Fresh bucket test
    print("Test 3: Fresh bucket with immediate requests")
    tokenbucket = TokenBucketRateLimiter(3, 1)  # 3 capacity, 1 token/sec
    
    # Use all tokens immediately
    for i in range(4):  # Try 4 requests with 3 capacity
        result = tokenbucket.getToken()
        print(f"Request {i+1}: tokens = {tokenbucket.current_count}")
    print()
    
    # Test 4: Capacity limits
    print("Test 4: Testing capacity limits")
    tokenbucket = TokenBucketRateLimiter(2, 1)  # 2 capacity
    tokenbucket.getToken()  # Use 1 token
    print(f"After using 1 token: {tokenbucket.current_count}")
    
    print("Waiting 5 seconds (should cap at capacity 2)...")
    time.sleep(5)
    tokenbucket.getToken()  # This will trigger refill
    print(f"After waiting: {tokenbucket.current_count} (should be capped at 2)")