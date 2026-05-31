"""
Core Topic: Shared Memory Proxies via Managers
Description: Bypasses serialization overhead using shared memory Value primitives and SyncManagers.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
from multiprocessing import Lock
from multiprocessing.sharedctypes import Synchronized
import ctypes
import time
from typing import Any

def metrics_mutator(shared_balance: Any, shared_lock: Lock) -> None: # type: ignore
    """Safely updates shared memory primitive allocations using synchronization locks.

    shared_balance is a multiprocessing.Value (a synchronized ctypes object).
    """
    for _ in range(100):
        time.sleep(0.001)
        # Shared memory values must be explicitly synchronized to prevent corruption
        with shared_lock:
            shared_balance.value += 1.5

if __name__ == "__main__":
    # Allocate a double-precision float value ('d') initialized to zero in shared memory
    global_telemetry_value = multiprocessing.Value(ctypes.c_double, 0.0)
    coordination_lock = multiprocessing.Lock()
    
    p1 = multiprocessing.Process(target=metrics_mutator, args=(global_telemetry_value, coordination_lock))
    p2 = multiprocessing.Process(target=metrics_mutator, args=(global_telemetry_value, coordination_lock))

    print("[MAIN] Launching twin parallel processes over shared memory primitives...")
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print(f"[MAIN] Final synchronized calculation output value: {global_telemetry_value.value}")