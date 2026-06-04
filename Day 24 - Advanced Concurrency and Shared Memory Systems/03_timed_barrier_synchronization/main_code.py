"""
Core Topic: Heavy Resource Parallel Synchronization Barriers
Description: Orchestrates multiple sub-processes to wait at an execution gate before continuing.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import time
import random

def coordinated_cluster_worker(worker_id: int, synchronization_gate: multiprocessing.Barrier) -> None: # pyright: ignore[reportInvalidTypeForm]
    """Simulates localized resource alignment before breaching global operational steps."""
    startup_delay = random.uniform(0.1, 0.4)
    time.sleep(startup_delay)
    print(f"[WORKER-{worker_id}] Pre-flight database integrity checks passed in {startup_delay:.2f}s. Holding at gate...")
    
    try:
        # Block until all registered processes reach this exact checkpoint
        gate_index = synchronization_gate.wait(timeout=2.0)
        print(f"[WORKER-{worker_id}] Gate released! Released with barrier rank identity: {gate_index}")
    except multiprocessing.BrokenBarrierError:
        print(f"[WORKER-{worker_id}] Synchronization failure encountered. Aborting step routines.")

if __name__ == "__main__":
    # Define a barrier that unlocks only when 3 unique processes check in
    cluster_gate = multiprocessing.Barrier(parties=3)
    worker_pool = []

    print("[ORCHESTRATOR] Initializing clustered multi-stage parallel synchronization sequences...")
    for i in range(3):
        p = multiprocessing.Process(target=coordinated_cluster_worker, args=(i, cluster_gate))
        worker_pool.append(p)
        p.start()

    for p in worker_pool:
        p.join()
    print("[ORCHESTRATOR] All nodes successfully passed synchronization boundaries.")