# Addepar-Style Coding Problem: Temporal Aggregation & Expiring State

## Problem

You are given a stream of events representing updates to user portfolios.

Each event is a tuple:

(user_id: str, timestamp: int, value: int, ttl: int)

- timestamp may be out of order
- value is a delta to the user’s balance
- ttl (time-to-live) defines how long the event is valid

## Task

Implement:

def compute_balances(events, query_time):
    pass

Return the final balance per user at query_time.

### Rules

1. Only include events where:
   timestamp <= query_time < timestamp + ttl

2. If multiple events have the same (user_id, timestamp),
   keep ONLY the last one (input order wins)

3. Events must be processed in timestamp order per user

4. Ignore expired events

---

## Example

events = [
    ("A", 10, 100, 10),
    ("A", 12, -20, 5),
    ("A", 10, 200, 10),
    ("B", 11, 50, 10),
    ("A", 20, 30, 5)
]

query_time = 15

Output:
{
    "A": 180,
    "B": 50
}

---

## What This Tests

- Hashmap grouping
- Sorting by timestamp
- Deduplication
- TTL filtering
- Edge case handling
