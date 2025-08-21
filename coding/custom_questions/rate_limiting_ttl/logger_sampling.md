# Logger with Sampling & Severity Levels

Problem Statement:
Create a logger with levels `DEBUG < INFO < WARN < ERROR`. Support a per-key sampler (events per sliding minute) and return True when an event is emitted.

Examples:
1. level=INFO; `log(DEBUG,'k','x',0)` → `False`
2. sampler INFO=2/min for `user_login`; calls at t=0,10,20 → `[True, True, False]`
3. new minute (t=70); `log(INFO,'user_login','ok',70)` → `True`

```python
class Logger:
    def __init__(self, level: str = "INFO"):
        ...

    def log(self, level: str, message_key: str, message: str, timestamp_sec: int) -> bool:
        ...
```