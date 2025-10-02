# KV Store with Nested Transactions

Problem Statement:
Implement a KV store with `set/get/delete` and `begin/commit/rollback` supporting **nested transactions**.

Examples:
1. `set('a',1)`; `begin()`; `set('a',2)`; `get('a')` → `2`
2. `begin()`; `set('a',3)`; `rollback()`; `get('a')` → `2`
3. `commit()`; `get('a')` → `2`

```python
class TxnKV:
    def __init__(self):
        ...

    def get(self, key: str) -> object | None:
        ...
```
