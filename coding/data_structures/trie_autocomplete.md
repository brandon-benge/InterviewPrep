# Trie / Autocomplete

Problem Statement:
Implement an autocomplete supporting `insert(word)` and `top_k(prefix, k)` that returns up to `k` most frequent completions (ties broken lexicographically). Frequency increments on repeated inserts.

Examples:
1. inserts `[apple, app, app, apex, apply, apple]`; `top_k('ap', 3)` → ["apple", "app", "apply"]
2. after above, `top_k('app', 2)` → ["app", "apple"]
3. `top_k('b', 5)` → []

```python
class Autocomplete:
    def __init__(self):
        ...

    def insert(self, word: str) -> None:
        ...

    def top_k(self, prefix: str, k: int) -> list[str]:
        ...