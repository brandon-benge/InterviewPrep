from collections import defaultdict, deque


class RateLimiter:
    def allow_requests(self, requests, N, W):
        user_requests = defaultdict(deque)
        response = []

        for user_id, timestamp in requests:
            q = user_requests[user_id]

            # Remove requests outside the rolling window
            while q and q[0] <= timestamp - W:
                q.popleft()

            if len(q) >= N:
                response.append(False)
            else:
                q.append(timestamp)
                response.append(True)

        return response

if __name__ == "__main__":
    ratelimiter=RateLimiter()
    requests = [
        ("A", 1),
        ("A", 2),
        ("A", 3),
        ("A", 5)
    ]
    
    N = 2
    W = 3

    print(ratelimiter.allow_requests(requests, N, W))



'''
Each user is allowed at most **N requests within a rolling window of W seconds**.

Output:
[True, True, False, True]
'''