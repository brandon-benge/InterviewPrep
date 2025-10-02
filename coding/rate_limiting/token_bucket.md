# Token Bucket Rate Limiter

Problem Statement:
Implement a token bucket rate limiter. Tokens refill at a constant rate. A request is allowed only if at least 1 token is available.

Key Concepts:
- refill_rate: Time interval (in seconds) between adding each token
  Example: refill_rate = 1 means "add 1 token every 1 second"
  Example: refill_rate = 2 means "add 1 token every 2 seconds" 
  Example: refill_rate = 0.5 means "add 1 token every 0.5 seconds"

- refill_time: Tracks the last time (in seconds since start) when tokens were added
  Used to calculate elapsed time: current_time - refill_time

- tick(now_sec): Manual time advancement where now_sec = seconds since system start
  This simulates the passage of time for testing purposes

- Time tracking: All times are relative to a "time 0" baseline
  tick(5) means "5 seconds have passed since start"
  tick(10) means "10 seconds have passed since start"

Example:
- Bucket capacity: 5
- Refill rate: 1 (add 1 token every 1 second)
- Initially 5 tokens; 5 requests allowed immediately
- After tick(5), 5 new tokens are available (if bucket was empty)
- After tick(7), only 2 more tokens added since last refill at tick(5)

Token Refill Calculation:
tokens_to_add = floor((current_time - last_refill_time) / refill_rate)
Example: If 3.7 seconds elapsed with refill_rate=1, you get floor(3.7/1) = 3 tokens

```python
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        ...

    def allow_request(self) -> bool:
        ...