"""
Component: Job Model Definition
Description: Defines the structure, states, and comparison invariants for scheduled tasks.
Author: Syed Saad Bin Irfan
"""

import uuid
from enum import Enum, auto

class JobState(Enum):
    QUEUED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    DLQ = auto()

class Priority(Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1  # Lower value equals higher priority in heap queues

class EnterpriseJob:
    """Represents an isolated background compute task with strict priority and execution metrics."""
    
    def __init__(self, name: str, priority: Priority, task_action: callable, max_retries: int = 2) -> None:
        self.job_id = str(uuid.uuid4())[:8]
        self.name = name
        self.priority = priority
        self.task_action = task_action
        self.max_retries = max_retries
        self.retry_count = 0
        self.state = JobState.QUEUED
        self.execution_error = None

    def __lt__(self, other: 'EnterpriseJob') -> bool:
        """Enforces deterministic priority order for heap-based priority sorting algorithms."""
        return self.priority.value < other.priority.value