from collections import defaultdict
"""Top K Scores Tracker starter file."""


class TopKScoresTracker:
    def __init__(self):
        self.kv = defaultdict()

    def add_score(self, player_id: str, delta: int) -> None:
        if player_id not in self.kv:
            self.kv[player_id] = delta
            return
        self.kv[player_id] = self.kv[player_id]+delta
        return

    def top_k(self, k: int) -> list[str]:
        print(self.kv)
        sorted_by_second_first_asc = sorted(self.kv, key=lambda player: ( -self.kv[player], player ))
        print(sorted_by_second_first_asc)
        return sorted_by_second_first_asc[:k]

if __name__ == "__main__":
    ts = TopKScoresTracker()
    ts.add_score("alice", 10)
    ts.add_score("bob", 15)
    ts.add_score("carl", 12)
    print(ts.top_k(2) == ["bob", "carl"])

    ts = TopKScoresTracker()
    ts.add_score("alice", 10)
    ts.add_score("alice", 5)
    ts.add_score("bob", 15)
    print(ts.top_k(2) == ["alice", "bob"])

    ts = TopKScoresTracker()
    ts.add_score("bob", 20)
    ts.add_score("anna", 20)
    ts.add_score("zoe", 5)
    print(ts.top_k(2) == ["anna", "bob"])