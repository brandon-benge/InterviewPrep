from queue import Queue
import threading
import time
import random

class Job:
    def __init__(self, func, args=(), kwargs=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.retry_count = 0

class RetryableJobQueue:
    def __init__(self, num_workers: int, max_retries: int):
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.queue = Queue()  # Instance variable
        self.workers = []
        self.running = True
        
        # Start worker threads
        for _ in range(num_workers):
            worker = threading.Thread(target=self._worker)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    def enqueue(self, job_callable: callable, *args, **kwargs) -> None:
        job = Job(job_callable, args, kwargs)
        self.queue.put(job)

    def _worker(self):
        while self.running:
            try:
                job = self.queue.get(timeout=1)
                self._execute_job(job)
                self.queue.task_done()
            except:
                continue  # Timeout or queue empty

    def _execute_job(self, job):
        try:
            # Execute the job
            job.func(*job.args, **job.kwargs)
            print(f"Job completed successfully")
        except Exception as e:
            print(f"Job failed (attempt {job.retry_count + 1}): {e}")
            
            if job.retry_count < self.max_retries:
                # Exponential backoff: 1s, 2s, 4s, 8s...
                delay = 2 ** job.retry_count
                job.retry_count += 1
                
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                
                # Re-enqueue the job
                self.queue.put(job)
            else:
                print(f"Job failed permanently after {self.max_retries + 1} attempts")

# Example job that sometimes fails
def unreliable_job(name):
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception(f"Job {name} failed!")
    print(f"Job {name} succeeded!")

if __name__ == "__main__":
    queue = RetryableJobQueue(3, 2)
    
    # Enqueue some jobs
    queue.enqueue(unreliable_job, "job1")
    queue.enqueue(unreliable_job, "job2")
    queue.enqueue(unreliable_job, "job3")
    
    # Wait for jobs to complete
    time.sleep(10)

# # DAEMON PROCESS VERSION - Run forever and accept interactive input
# if __name__ == "__main__":
#     import signal
#     import sys
    
#     # Create the queue
#     queue = RetryableJobQueue(3, 2)
    
#     # Signal handler for graceful shutdown
#     def signal_handler(sig, frame):
#         print("\nShutting down daemon...")
#         queue.running = False
#         sys.exit(0)
    
#     signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
#     signal.signal(signal.SIGTERM, signal_handler)  # Handle termination
    
#     print("Job Queue Daemon started. Type 'help' for commands.")
#     print("Commands: add <job_name>, status, quit")
    
#     try:
#         while True:
#             try:
#                 user_input = input("queue> ").strip().lower()
                
#                 if user_input == "quit" or user_input == "exit":
#                     print("Shutting down...")
#                     queue.running = False
#                     break
                
#                 elif user_input == "help":
#                     print("Available commands:")
#                     print("  add <job_name>  - Add a new unreliable job")
#                     print("  status          - Show queue status")
#                     print("  quit/exit       - Shutdown daemon")
                
#                 elif user_input == "status":
#                     print(f"Queue size: {queue.queue.qsize()}")
#                     print(f"Active workers: {queue.num_workers}")
#                     print(f"Running: {queue.running}")
                
#                 elif user_input.startswith("add "):
#                     job_name = user_input[4:].strip()
#                     if job_name:
#                         queue.enqueue(unreliable_job, job_name)
#                         print(f"Added job: {job_name}")
#                     else:
#                         print("Please provide a job name: add <job_name>")
                
#                 else:
#                     print("Unknown command. Type 'help' for available commands.")
                    
#             except EOFError:
#                 # Handle Ctrl+D
#                 print("\nShutting down...")
#                 break
                
#     except KeyboardInterrupt:
#         print("\nShutting down...")
#     finally:
#         queue.running = False
#         print("Daemon stopped.")

# # ALTERNATIVE: Run as system daemon (background process)
# # To run as daemon: python retryable_worker.py &
# # To make it a proper system service, create a systemd service file:
# #
# # /etc/systemd/system/job-queue.service:
# # [Unit]
# # Description=Retryable Job Queue Service
# # After=network.target
# #
# # [Service]
# # Type=simple
# # User=your_user
# # WorkingDirectory=/path/to/your/script
# # ExecStart=/usr/bin/python3 /path/to/retryable_worker.py
# # Restart=always
# # RestartSec=10
# #
# # [Install]
# # WantedBy=multi-user.target
# #
# # Commands:
# # sudo systemctl enable job-queue.service
# # sudo systemctl start job-queue.service
# # sudo systemctl status job-queue.service