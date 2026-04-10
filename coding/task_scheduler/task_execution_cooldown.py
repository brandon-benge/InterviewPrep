from collections import Counter, defaultdict

class Scheduler:
    def __init__(self, tasks: list, k: int):
        self.tasks = tasks
        self.k = k
        self.counter = self.get_order()

    def get_order(self):
        remaining = Counter(task_id for task_id, _timestamp in self.tasks)
        next_available = defaultdict(int)
        time = 0

        while remaining:
            best_task = None
            best_count = 0

            for task_id, count in remaining.items():
                if next_available[task_id] <= time and count > best_count:
                    best_task = task_id
                    best_count = count

            if best_task is None:
                time += 1
                continue

            remaining[best_task] -= 1
            if remaining[best_task] == 0:
                del remaining[best_task]

            next_available[best_task] = time + self.k + 1
            time += 1

        return time

if __name__ == "__main__":
    tasks = [
        ("A", 0),
        ("A", 1),
        ("B", 2),
        ("A", 3),
    ]
    k = 2
    schedule = Scheduler(tasks, k)
    print(schedule.counter)



'''
tasks = [
    ("A", 0),
    ("A", 1),
    ("B", 2),
    ("A", 3)
]

k = 2

One valid execution:

time 0: A  
time 1: B  
time 2: idle  
time 3: A  
time 4: idle  
time 5: A  

Output:

6
'''
