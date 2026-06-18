"""
Component: Concurrent Worker Pool Engine
Description: Spawns background worker threads that consume tasks from the priority queue.
Author: Syed Saad Bin Irfan
"""

import threading
import time
from queue_manager import PriorityJobQueueManager
from job_model import JobState

class ConcurrentWorkerPool:
    """Spawns and monitors background worker threads consuming tasks from the priority queue."""
    
    def __init__(self, queue_manager: PriorityJobQueueManager, worker_count: int = 3) -> None:
        self.manager = queue_manager
        self.worker_count = worker_count
        self.workers: list[threading.Thread] = []
        self.is_running = False
        self.active_worker_status = {}

    def start_pool(self) -> None:
        self.is_running = True
        for i in range(self.worker_count):
            w_id = f"worker-{i+1}"
            self.active_worker_status[w_id] = "IDLE"
            t = threading.Thread(target=self._worker_loop, args=(w_id,), daemon=True)
            self.workers.append(t)
            t.start()

    def _worker_loop(self, worker_id: str) -> None:
        while self.is_running:
            job = self.manager.extract_next_job()
            if job:
                self.active_worker_status[worker_id] = f"RUNNING: {job.name}"
                try:
                    # Execute the functional payload assigned to the job
                    job.task_action()
                    job.state = JobState.COMPLETED
                except Exception as ex:
                    job.execution_error = str(ex)
                    if job.retry_count < job.max_retries:
                        job.retry_count += 1
                        time.sleep(0.2) # Base retry backing delay delay
                        self.manager.submit_job(job)
                    else:
                        self.manager.route_to_dlq(job)
                self.active_worker_status[worker_id] = "IDLE"
            else:
                self.active_worker_status[worker_id] = "IDLE"
                time.sleep(0.3) # Avoid high cpu polling burn loops

    def stop_pool(self) -> None:
        self.is_running = False