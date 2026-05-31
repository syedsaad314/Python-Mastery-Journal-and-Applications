"""
Core Topic: Process Lifecycles and Absolute Memory Isolation
Description: Proves the structural divergence of memory state across isolated OS processes.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import os
import time
from typing import List

# Shared state visualization target
system_registry: List[str] = ["INITIAL_STATE"]

def worker_target_routine(payload_item: str) -> None:
    """Executes inside an entirely independent OS process memory segment."""
    global system_registry
    print(f"[CHILD WORKER PID: {os.getpid()}] Modifying local system_registry copy...")
    system_registry.append(payload_item)
    print(f"[CHILD WORKER PID: {os.getpid()}] Local State internal map: {system_registry}")

if __name__ == "__main__":
    print(f"[PARENT ENGINE PID: {os.getpid()}] Global baseline status: {system_registry}")
    
    # Instantiate child process allocation
    child_process = multiprocessing.Process(
        target=worker_target_routine, 
        args=("CORE_NODE_MUTATION",),
        name="Worker-Isolation-Node"
    )
    
    child_process.start()
    child_process.join()  # Hold parent thread until child worker pipeline concludes safely
    
    print(f"[PARENT ENGINE PID: {os.getpid()}] Evaluation post-child exit: {system_registry}")
    print("[PARENT ENGINE] Structural proof: Global memory modifications did not bleed across process boundaries.")