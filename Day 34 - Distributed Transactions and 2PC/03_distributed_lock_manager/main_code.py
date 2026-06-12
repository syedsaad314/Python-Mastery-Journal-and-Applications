"""
Core Topic: Distributed Lock Manager (DLM) Basics
Description: Implements a token locking registry mechanism protecting distributed resources.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import Dict, Optional

class CentralLockRegistry:
    """Manages mutually exclusive resource token grants across multiple cluster workers."""
    
    def __init__(self) -> None:
        # Maps ResourceKey -> OwnerWorkerID
        self.active_locks: Dict[str, str] = {}

    def acquire_lock(self, resource_key: str, worker_id: str) -> bool:
        """Grants exclusive access if the resource is currently unassigned."""
        if resource_key not in self.active_locks:
            self.active_locks[resource_key] = worker_id
            return True
        return self.active_locks[resource_key] == worker_id

    def release_lock(self, resource_key: str, worker_id: str) -> bool:
        """Removes the assignment if the requesting worker matches the active token owner."""
        if self.active_locks.get(resource_key) == worker_id:
            del self.active_locks[resource_key]
            return True
        return False


if __name__ == "__main__":
    dlm = CentralLockRegistry()
    
    # Worker 1 claims exclusive access to a resource
    lock_granted_w1 = dlm.acquire_lock("db_record_balance", "worker-thread-01")
    # Worker 2 tries to claim the same resource concurrently
    lock_granted_w2 = dlm.acquire_lock("db_record_balance", "worker-thread-02")
    
    print(f"[DLM-REGISTRY] Worker 1 acquisition status: {lock_granted_w1}")
    print(f"[DLM-REGISTRY] Worker 2 acquisition status (Expecting False): {lock_granted_w2}")
    
    # Release the lock to free the resource
    dlm.release_lock("db_record_balance", "worker-thread-01")
    lock_granted_w3 = dlm.acquire_lock("db_record_balance", "worker-thread-02")
    print(f"[DLM-REGISTRY] Worker 2 acquisition status after release: {lock_granted_w3}")