# Thread-Safe Shared Counter

Problem Statement:
Create a thread-safe counter class to be safely used by multiple threads incrementing a shared variable.

Tasks:
- Simulate race condition (without Lock)
- Fix it using `threading.Lock`

```python
class Counter:
    def __init__(self):
        self.value = 0
        ...

    def increment(self):
        ...