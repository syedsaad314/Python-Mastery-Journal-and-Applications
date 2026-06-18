"""
Component: Priority Queue Manager
Description: Thread-safe queue wrapper with integrated Dead-Letter Queue (DLQ) routing.
Author: Syed Saad Bin Irfan
"""

import heapq
import threading
from typing import Optional
from job_model import EnterpriseJob, JobState

class PriorityJobQueueManager:
    """Manages an thread-safe priority task heap with automatic failure routing."""
    
    def __init__(self) -> None:
        self._heap = []
        self._dlq = []
        self._lock = threading.Lock()

    def submit_job(self, job: EnterpriseJob) -> None:
        """Safely pushes a job onto the internal tracking heap structure under lock guards."""
        with self._lock:
            job.state = JobState.QUEUED
            heapq.heappush(self._heap, job)

    def extract_next_job(self) -> Optional[EnterpriseJob]:
        """Pulls the highest-priority job from the heap safely."""
        with self._lock:
            if self._heap:
                job = heapq.heappop(self._heap)
                job.state = JobState.RUNNING
                return job
            return None

    def route_to_dlq(self, job: EnterpriseJob) -> None:
        """Permanently moves a completely failed job out of active circulation into the DLQ."""
        with self._lock:
            job.state = JobState.DLQ
            self._dlq.append(job)

    def get_snapshot_counts(self) -> tuple[int, int]:
        """Returns the current number of pending and dead-lettered jobs."""
        with self._lock:
            return len(self._heap), len(self._dlq)

    def get_dlq_records(self) -> list[EnterpriseJob]:
        with self._lock:
            return list(self._dlq)