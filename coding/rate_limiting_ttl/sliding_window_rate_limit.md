# Sliding Window Rate Limit (Per-User)

## Problem

You are building a rate limiter.

Each request is:
(user_id: str, timestamp: int)

Each user is allowed at most **N requests within a rolling window of W seconds**.

---

## Task

Implement:

def allow_requests(requests, N, W):
    pass

Return a list of booleans indicating whether each request is allowed.

---

## Example

requests = [
    ("A", 1),
    ("A", 2),
    ("A", 3),
    ("A", 5)
]

N = 2
W = 3

Output:
[True, True, False, True]

---

## Explanation

For user A:
- At time 1 → allowed
- At time 2 → allowed
- At time 3 → window [1,3] has 3 requests → reject
- At time 5 → window [2,5] has 2 → allowed

---

## Constraints

- 1 ≤ len(requests) ≤ 10^5
- timestamps are non-decreasing
- multiple users

---

## What This Tests

- Sliding window logic
- Queue / deque usage
- Per-user state tracking
- Edge case handling

---

## Hints

- Use a hashmap: user → queue of timestamps
- Remove timestamps outside the window
- Check size before inserting

---

## Follow-Ups

1. How would you make this thread-safe?
2. How would you distribute this across services?
