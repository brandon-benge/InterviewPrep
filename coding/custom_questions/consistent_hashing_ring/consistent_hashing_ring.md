# Consistent Hashing Ring

Problem Statement:
Build a consistent hashing ring with **virtual nodes** supporting server add/remove and `get_server(key)`.

Examples:
1. add A,B; `get_server('user:1')`, `get_server('user:2')` → deterministically A or B
2. add C; `get_server('user:1')` → possibly C; **most keys remain on prior server**
3. remove B; `get_server('user:2')` → A or C, keys remap clockwise

```python
class ConsistentHashRing:
    def __init__(self, vnodes: int = 100):
        ...

    def get_server(self, key: str) -> str | None:
        ...
```