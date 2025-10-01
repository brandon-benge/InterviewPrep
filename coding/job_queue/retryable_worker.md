# Retryable Job Queue with Exponential Backoff

Problem Statement:
Implement a job queue where failed jobs are retried with exponential backoff. Use worker threads to process jobs in parallel.

Requirements:
- Use `queue.Queue` and `threading.Thread`
- Add retry attempts and backoff
- Mark jobs failed after max retries

```python
class RetryableJobQueue:
    def __init__(self, num_workers: int, max_retries: int):
        ...

    def enqueue(self, job_callable: callable) -> None:
        ...