# Account Balance Aggregator

Problem Statement:
You are given a stream of transaction events. Each event contains a unique `txn_id`, an `account_id`, an `amount`, and a `timestamp`.

Build a component that ingests these events and returns a summary per account.

Rules:
- Multiple events may belong to the same account.
- Duplicate events with the same `txn_id` should only be applied once.
- Transactions may arrive out of order, but balances must reflect timestamp order.
- If two transactions for the same account have the same timestamp, preserve their original arrival order.

For each account, return:
- final balance
- number of unique applied transactions
- latest processed timestamp

Examples:
1. events:
   - `("t1", "A", 100, 10)`
   - `("t2", "A", -20, 12)`
   - `("t3", "B", 50, 11)`
   summary:
   - `"A"` -> `(80, 2, 12)`
   - `"B"` -> `(50, 1, 11)`

2. events:
   - `("t1", "A", 100, 10)`
   - `("t1", "A", 100, 10)`
   - `("t2", "A", -30, 9)`
   summary for `"A"` -> `(70, 2, 10)`

3. events:
   - `("t1", "A", 40, 5)`
   - `("t2", "A", -10, 5)`
   - `("t3", "A", 15, 6)`
   summary for `"A"` -> `(45, 3, 6)`

```python
class AccountBalanceAggregator:
    def add_transaction(self, txn_id: str, account_id: str, amount: int, timestamp: int) -> None:
        ...

    def get_summary(self) -> dict[str, tuple[int, int, int]]:
        ...
```
