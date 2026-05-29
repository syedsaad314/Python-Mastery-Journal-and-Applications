"""
Core Topic: Mutex (Mutual Exclusion) Lock Synchronization
Description: Enforces absolute memory consistency across threads utilizing threading.Lock.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
import time

class SynchronizedStateCounter:
    def __init__(self) -> None:
        self.value: int = 0
        self.mutex: threading.Lock = threading.Lock()

    def safe_increment(self) -> None:
        """Secures exclusive atomic lock control to guarantee consistent memory operations."""
        # Using context management protocol safely handles acquisition and release phases
        with self.mutex:
            current_state = self.value
            time.sleep(0.0001)
            self.value = current_state + 1

if __name__ == "__main__":
    counter = SynchronizedStateCounter()
    worker_pool = []

    print("[CORE THREAD] Spawning 50 synchronized mutation threads...")
    for _ in range(50):
        t = threading.Thread(target=counter.safe_increment)
        worker_pool.append(t)
        t.start()

    for t in worker_pool:
        t.join()

    print(f"[CORE THREAD] Synchronized Run Finished. Guaranteed Consistent Value: {counter.value}")