"""
Core Topic: Bounded Semaphore Throttling
Description: Restricts concurrent access to limited pool resources using an internal counter.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
import time
import random

class ResourcePoolGatekeeper:
    def __init__(self, max_concurrent_slots: int = 3) -> None:
        # BoundedSemaphore raises an error if code flaws cause excess releases
        self.pool_semaphore = threading.BoundedSemaphore(max_concurrent_slots)

    def access_limited_service(self, client_id: int) -> None:
        print(f"[CLIENT-{client_id}] Awaiting an open resource slot...")
        with self.pool_semaphore:
            print(f"[CLIENT-{client_id}] Entered pool gateway slot successfully.")
            # Simulate processing time inside the protected resource pool
            time.sleep(random.uniform(0.2, 0.5))
            print(f"[CLIENT-{client_id}] Leaving pool slot.")

if __name__ == "__main__":
    gatekeeper = ResourcePoolGatekeeper(max_concurrent_slots=2)
    clients = []

    for i in range(5):
        t = threading.Thread(target=gatekeeper.access_limited_service, args=(i,))
        clients.append(t)
        t.start()

    for t in clients:
        t.join()