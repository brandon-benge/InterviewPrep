# Rate Limiter & TTL Cache

**Problem Statement:**

Design a rate limiter that restricts the number of actions allowed per unique key within a sliding one-minute window. The limiter should accept a maximum number of allowed actions per minute, and for each request, determine if the action is allowed based on the history of requests for that key.

**Examples:**

```json
{
  "limiter_name": "new_limiter_1",
  "message": { "first_name": "Rachel", "last_name": "Court", "number": 4 },
  "threshold": 1,
  "current_time": 60
}
```
Expected Output: memory location (e.g., `"0x7f8a12bc"`).

```json
{
  "limiter_name": "orders_write_limiter",
  "message": { "order_id": "A123", "user_id": 42 },
  "threshold": 2,
  "current_time": 161
}
```
Expected Output: memory location (e.g., `"0x7f92c01d"`).

```json
{
  "limiter_name": "orders_write_limiter",
  "message": { "order_id": "A124", "user_id": 42 },
  "threshold": 2,
  "current_time": 180
}
```
Expected Output: memory location (e.g., `"0x7f92c8de"`).

**Inputs:**

- `limiter_name` (str)
- `message` (object with arbitrary fields)
- `threshold` (int)
- `current_time` (int, seconds)

**Outputs:**

Returns the **memory location** (string) where the message is stored for this limiter instance.

```python
class RateLimiter:
    def __init__(self, limiter_name : str, message : dict[str, Any], threshold : int, current_time : int):
        ...

    def rateLimiter(cls, limiter_name : str, message : dict[str, Any], threshold : int, current_time : int):
        ...
```
