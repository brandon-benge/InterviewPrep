# The threading.Lock() object in Python, also known as a mutex (mutual exclusion), is a 
# synchronization primitive used to prevent race conditions when multiple threads access 
# shared resources. It ensures that only one thread can execute a critical section of 
# code at a time, protecting shared data from being corrupted by concurrent modifications.

import threading
import time

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        self.lock.acquire()
        temp = self.value 
        time.sleep(0.0001)  # 1 microsecond delay
        self.value = temp +1 
        self.lock.release() 

def worker(counter, iterations):
    for _ in range(iterations):
        counter.increment()

if __name__ == "__main__":
    counter = Counter()
    threads = []

    for i in range(10):
        t = threading.Thread(target=worker, args=(counter, 100))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print(f"Expected: 1000, Actual: {counter.value}")
        