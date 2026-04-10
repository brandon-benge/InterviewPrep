
class AccountBalance:
    def compute_balances(self, events, query_time):
        latest_by_user_and_timestamp = {}

        for user_id, timestamp, value, ttl in events:
            if timestamp <= query_time < timestamp + ttl:
                latest_by_user_and_timestamp[(user_id, timestamp)] = value

        balances = {}

        for (user_id, _timestamp), value in latest_by_user_and_timestamp.items():
            balances[user_id] = balances.get(user_id, 0) + value

        return balances

if __name__ == "__main__":
    balance=AccountBalance()
    events = [
        ("A", 10, 100, 10),
        ("A", 12, -20, 5),
        ("A", 10, 200, 10),
        ("B", 11, 50, 10),
        ("A", 20, 30, 5)
    ]
    query_time = 15
    print(balance.compute_balances(events, query_time) == {"A": 180,"B": 50})

'''
(user_id: str, timestamp: int, value: int, ttl: int)
events = [
    ("A", 10, 100, 10),
    ("A", 12, -20, 5),
    ("A", 10, 200, 10),
    ("B", 11, 50, 10),
    ("A", 20, 30, 5)
]

query_time = 15

Output:
{
    "A": 180,
    "B": 50
}
'''