# Top K Scores Tracker

Problem Statement:
Design a score tracker that supports updating player scores and retrieving the top `k` players by score.

Rules:
- Each player has a cumulative score.
- Calling `add_score(player_id, delta)` adds `delta` to that player's current score.
- `top_k(k)` should return up to `k` player IDs with the highest scores.
- If two players have the same score, return the lexicographically smaller `player_id` first.
- If `k` is larger than the number of players, return all players in ranked order.

Examples:
1. `add_score("alice", 10)`
   `add_score("bob", 15)`
   `add_score("carl", 12)`
   `top_k(2)` -> `["bob", "carl"]`

2. `add_score("alice", 10)`
   `add_score("alice", 5)`
   `add_score("bob", 15)`
   `top_k(2)` -> `["alice", "bob"]`

3. `add_score("bob", 20)`
   `add_score("anna", 20)`
   `add_score("zoe", 5)`
   `top_k(2)` -> `["anna", "bob"]`

```python
class TopKScoresTracker:
    def add_score(self, player_id: str, delta: int) -> None:
        ...

    def top_k(self, k: int) -> list[str]:
        ...
```
