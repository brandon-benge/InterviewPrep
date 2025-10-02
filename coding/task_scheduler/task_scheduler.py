# Task Scheduler with Retries & Exponential Backoff

# Problem Statement:
# Design a scheduler that accepts tasks with an earliest-execute time and executes them in order. If a task fails, it is retried with exponential backoff and **full jitter** up to `max_retries`.
# APIs to support conceptually (no need to implement now): `schedule(task_id, run_at, fn, max_retries)` and `tick(now)`.

# Examples:
# 1. `schedule("A", 1000, ok)`; `tick(999)`; `tick(1000)` → `[]`, then `[('A','success')]`
# 2. `schedule("B", 1000, fail, max_retries=1)` with base=100, jitter=0; `tick(1000)`; `tick(1099)`; `tick(1100)` → `[]`, `[]`, `[('B','failed')]`
# 3. `schedule("C", 1000, flaky)` (fail, fail, succeed), base=50, jitter=0; `tick(1000)`; `tick(1050)`; `tick(1150)` → `[]` (or success), `[]` (or success), `[]` (or success)`


import random
import bisect
from collections import defaultdict
import threading
import time

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

class Job:
    def __init__(self, task_id, fn, primary_key, args=(), kwargs=None):
        self.task_id = task_id
        self.fn = fn
        self.retry_count = 0
        self.max_retries = kwargs.get('max_retries', 0)
        self.primary_key = primary_key
        self.args = args
        self.kwargs = kwargs or {}

class TaskScheduler:
    def __init__(self, base_backoff_ms: int = 100):
        self.base_backoff_ms = base_backoff_ms
        self.jitter = None
        self.now_ms = 0
        self.dictionary = defaultdict(list)
        self.sorted_time = []
        self.primarykey = {}
        self.counter = Counter()
        
    def tick(self, now_ms: int) -> list[tuple[str, str]]:
        responses = []
        old_time = self.now_ms
        self.now_ms = now_ms

        # Process all tasks that should run between old_time and now_ms
        times_to_remove = []
        for run_at in self.sorted_time:
            if run_at > old_time and run_at <= now_ms:
                # Process all jobs at this time
                for primary_key in sorted(self.dictionary[run_at]):
                    job = self.primarykey[primary_key]
                    result = self._execute_job(job)
                    if result:  # Only add if job completed (success or final failure)
                        responses.append(result)
                        del self.primarykey[primary_key]  # Clean up
                times_to_remove.append(run_at)
            elif run_at > now_ms:
                break

        # Clean up processed times
        for time_to_remove in times_to_remove:
            self.sorted_time.remove(time_to_remove)
            del self.dictionary[time_to_remove]

        return responses

    def schedule(self, task_id, run_at, fn: callable, *args, **kwargs):
        job = Job(task_id, fn, self.counter.increment(), args, kwargs)

        if run_at in self.dictionary:
            self.dictionary[run_at].append(job.primary_key)
        else:
            bisect.insort(self.sorted_time, run_at)
            self.dictionary[run_at] = [job.primary_key]

        self.primarykey[job.primary_key] = job


    def _execute_job(self, job):
        try:
            # Execute the job
            job.fn(job.task_id)
            return (job.task_id, "success")
        except Exception as e:
            print(f"Job {job.task_id} failed (attempt {job.retry_count + 1}): {e}")
            
            if job.retry_count < job.max_retries:
                base_delay = self.base_backoff_ms * (2 ** job.retry_count)
            
                if self.jitter == 0:
                    jitter_delay = base_delay  # No jitter - use exact delay
                elif self.jitter is None:
                    jitter_delay = random.uniform(0, base_delay)  # Full jitter (default)
                else:
                    jitter_delay = random.uniform(0, min(self.jitter, base_delay))  # Limited jitter
                
                retry_time = self.now_ms + int(jitter_delay)
                job.retry_count += 1
                
                print(f"Scheduling retry at {retry_time}")
                
                # Reschedule the job
                if retry_time not in self.dictionary:
                    bisect.insort(self.sorted_time, retry_time)
                    self.dictionary[retry_time] = []  # Initialize empty list
                
                self.dictionary[retry_time].append(job.primary_key)
                return None  # Don't return result yet - job will retry
            else:
                return (job.task_id, "failed")

def ok(name):
    return ""

def fail(name):
    raise Exception(f"Job {name} failed!")


def flaky(name):
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception(f"Job {name} failed!")

if __name__ == "__main__":
    print("=== Test 1: Simple success case ===")
    taskscheduler = TaskScheduler()
    taskscheduler.schedule("A", 1000, ok)
    result1 = taskscheduler.tick(999)
    print(f"tick(999): {result1}")
    result2 = taskscheduler.tick(1000)
    print(f"tick(1000): {result2}")
    print()
    
    print("=== Test 2: Retry with failure ===")
    taskscheduler.schedule("B", 2000, fail, max_retries=1)  # Use different time
    taskscheduler.base_backoff_ms = 100
    taskscheduler.jitter = 0
    result3 = taskscheduler.tick(2000)
    print(f"tick(2000): {result3}")
    result4 = taskscheduler.tick(2099)
    print(f"tick(2099): {result4}")
    result5 = taskscheduler.tick(2100)
    print(f"tick(2100): {result5}")
    print()
    
    print("=== Test 3: Flaky job ===")
    taskscheduler.schedule("C", 3000, flaky)  # Use different time
    taskscheduler.base_backoff_ms = 50
    taskscheduler.jitter = 0
    result6 = taskscheduler.tick(3000)
    print(f"tick(3000): {result6}")
    result7 = taskscheduler.tick(3050)
    print(f"tick(3050): {result7}")
    result8 = taskscheduler.tick(3150)
    print(f"tick(3150): {result8}")


