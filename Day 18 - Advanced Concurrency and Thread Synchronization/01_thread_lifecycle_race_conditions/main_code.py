"""
Core Topic: Thread Lifecycles and Shared State Race Conditions
Description: Demonstrates multi-threaded state corruption on un-synchronized variables.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
import time

class SharedStateCounter:
    def __init__(self) -> None:
        self.value: int = 0

    def unsafe_increment(self) -> None:
        """Simulates non-atomic execution context switches to trigger memory context race conditions."""
        current_state = self.value
        # Force the OS scheduler to pause execution and context switch threads
        time.sleep(0.0001)
        self.value = current_state + 1

if __name__ == "__main__":
    counter = SharedStateCounter()
    worker_pool = []

    print("[CORE THREAD] Spawning 50 un-synchronized concurrent worker mutation threads...")
    for _ in range(50):
        t = threading.Thread(target=counter.unsafe_increment)
        worker_pool.append(t)
        t.start()

    for t in worker_pool:
        t.join()

    # If execution was atomic, expected value would be exactly 50
    print(f"[CORE THREAD] Mutation Execution Finished. Final Contaminated Value: {counter.value}")