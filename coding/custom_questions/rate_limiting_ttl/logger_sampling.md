# Logger with Sampling & Severity Levels

Problem Statement:
Create a logger with levels `DEBUG < INFO < WARN < ERROR`. Support a per-key sampler (events per sliding minute) and return True when an event is emitted.

Inputs & Outputs:
- **Inputs**:
  - `level` (str): The severity level of the event (`DEBUG`, `INFO`, `WARN`, `ERROR`).
  - `message_key` (str): Identifier for the type of message (e.g., `"user_login"`, `"payment_attempt"`).
  - `message` (str): The content of the log message.
  - `timestamp_sec` (int): The time in seconds when the log event occurs.

- **Outputs**:
  - Returns a boolean:
    - `True` if the event should be emitted (based on severity and sampling rules).
    - `False` if the event should be suppressed (below severity threshold or over the sampling limit).

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