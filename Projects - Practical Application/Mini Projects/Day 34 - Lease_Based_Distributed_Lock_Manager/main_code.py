"""
System: High-Concurrency Lease-Based Distributed Lock Manager
Description: Implements a distributed mutual exclusion lock system that uses 
             time-expiring leases to automatically free resources if a worker crashes.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Lease-DLM) %(message)s')

class LeaseLockToken:
    """Tracks resource lease data, matching resource keys to owner workers and expiration times."""
    
    def __init__(self, owner_worker_id: str, lease_duration_seconds: float) -> None:
        self.owner_worker_id: str = owner_worker_id
        self.expires_at: float = time.time() + lease_duration_seconds

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class DistributedLeaseLockManager:
    """Manages resource access and prevents deadlocks using time-bound lease agreements."""
    
    def __init__(self) -> None:
        # Maps ResourceKey -> LeaseLockToken
        self.lock_table: Dict[str, LeaseLockToken] = {}

    def acquire_resource_lease(self, resource_key: str, worker_id: str, duration: float) -> bool:
        """Grants a lease lock token if the resource is unassigned, expired, or already owned by the worker."""
        current_lock = self.lock_table.get(resource_key)
        
        if current_lock is None or current_lock.is_expired():
            self.lock_table[resource_key] = LeaseLockToken(worker_id, duration)
            logging.info(f"[DLM-LEASE] Granted lock on resource '{resource_key}' to worker '{worker_id}' for {duration} seconds.")
            return True
            
        if current_lock.owner_worker_id == worker_id:
            # Renew lease duration path
            current_lock.expires_at = time.time() + duration
            logging.info(f"[DLM-LEASE] Renewed lock on resource '{resource_key}' for worker '{worker_id}' for {duration} seconds.")
            return True

        logging.warning(f"[DLM-LEASE] Acquisition Denied: Resource '{resource_key}' is locked by worker '{current_lock.owner_worker_id}'.")
        return False

    def release_resource_lease(self, resource_key: str, worker_id: str) -> bool:
        """Releases the resource lock if the lease is still valid and requested by the active owner."""
        current_lock = self.lock_table.get(resource_key)
        
        if current_lock is None:
            return True
            
        if current_lock.owner_worker_id == worker_id:
            if not current_lock.is_expired():
                del self.lock_table[resource_key]
                logging.info(f"[DLM-LEASE] Released lock on resource '{resource_key}' by worker '{worker_id}'.")
                return True
                
        return False


if __name__ == "__main__":
    print("\n=== STARTING HIGH-CONCURRENCY DISTRIBUTED LEASE LOCK MANAGER ===\n")
    
    manager = DistributedLeaseLockManager()
    
    # Worker 1 acquires an exclusive lease lock for 2 seconds
    manager.acquire_resource_lease("inventory_sku_900", "worker-node-alpha", duration=2.0)
    
    # Worker 2 tries to acquire the same resource concurrently
    print("\n[CONCURRENCY-CHALLENGE] Worker Beta attempts to claim locked inventory resource...")
    manager.acquire_resource_lease("inventory_sku_900", "worker-node-beta", duration=5.0)
    
    # Simulate a worker node crashing by waiting for the lease to expire naturally
    print("\n[NODE-CRASH-SIMULATION] Worker Alpha crashes. Waiting for its lease to expire...")
    time.sleep(2.5) # Wait past the 2 second lease duration limit
    
    # Worker 2 tries to acquire the resource again after the lease expires
    print("\n[AUTOMATIC-DEADLOCK-RESOLUTION] Worker Beta retries acquisition after lease expiration...")
    acquired_success = manager.acquire_resource_lease("inventory_sku_900", "worker-node-beta", duration=4.0)
    
    print(f" -> Worker Beta lock status: {acquired_success}")
    print("\n=== SYSTEM SHUTDOWN: LEASE LOCK MANAGER EXITED ===")