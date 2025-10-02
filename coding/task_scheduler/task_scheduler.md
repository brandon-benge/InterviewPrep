# Task Scheduler with Retries & Exponential Backoff

Problem Statement:
Design a scheduler that accepts tasks with an earliest-execute time and executes them in order. If a task fails, it is retried with exponential backoff and **full jitter** up to `max_retries`.
APIs to support conceptually (no need to implement now): `schedule(task_id, run_at, fn, max_retries)` and `tick(now)`.

Examples:
1. `schedule("A", 1000, ok)`; `tick(999)`; `tick(1000)` → `[]`, then `[('A','success')]`
2. `schedule("B", 1000, fail, max_retries=1)` with base=100, jitter=0; `tick(1000)`; `tick(1099)`; `tick(1100)` → `[]`, `[]`, `[('B','failed')]`
3. `schedule("C", 1000, flaky)` (fail, fail, succeed), base=50, jitter=0; `tick(1000)`; `tick(1050)`; `tick(1150)` → `[]` (or success), `[]` (or success), `[]` (or success)`

```python
class TaskScheduler:
    def __init__(self, base_backoff_ms: int = 100):
        ...

    def tick(self, now_ms: int) -> list[tuple[str, str]]:
        ...
```