"""
System: Distributed Fault-Tolerant Cluster Coordination Engine
Description: Implements high-availability active lease locking systems using consensus term fences.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Coord-Core) %(message)s')

class DistributedLeaseCoordinator:
    """Manages distributed locks using term-based fencing tokens to prevent race conditions."""
    
    def __init__(self) -> None:
        self.active_lock_resource: Optional[str] = None
        self.current_fencing_token: int = 0
        self.lease_expiration_timestamp: float = 0.0

    def acquire_distributed_lock(self, client_id: str, cluster_term: int, duration_seconds: float = 2.0) -> Tuple[bool, int]: # type: ignore
        """Grants a resource lock if the request comes from a valid, up-to-date term."""
        current_time = time.time()
        
        # Enforce the consensus fence rule: reject requests from older terms
        if cluster_term < self.current_fencing_token:
            logging.warning(f"[LEASE-DENIED] Rejected client '{client_id}' due to outdated term token.")
            return False, self.current_fencing_token

        # Check if the existing lock has expired or is being renewed by the same term
        if self.active_lock_resource is None or current_time > self.lease_expiration_timestamp or cluster_term > self.current_fencing_token:
            self.active_lock_resource = client_id
            self.current_fencing_token = cluster_term
            self.lease_expiration_timestamp = current_time + duration_seconds
            
            logging.info(f"[LEASE-GRANTED] Client '{client_id}' secured lock. Fencing token issued: {self.current_fencing_token}")
            return True, self.current_fencing_token

        return False, self.current_fencing_token


if __name__ == "__main__":
    print("\n=== SYSTEM START: DISTRIBUTED HA COORDINATION ENGINE ===\n")
    coordinator = DistributedLeaseCoordinator()

    # Term 1: Client Alpha successfully acquires the resource lock
    ok_1, token_1 = coordinator.acquire_distributed_lock("client_alpha", cluster_term=1)
    print(f"[RESOURCES] Session 1 Status: {ok_1} | Token assigned: {token_1}")

    # Term 1: Client Beta tries to intercept the lock but is rejected due to active lease constraints
    ok_2, token_2 = coordinator.acquire_distributed_lock("client_beta", cluster_term=1)
    print(f"[RESOURCES] Session 2 Status: {ok_2} | Token assigned: {token_2}")

    # Term 2: A new cluster leader emerges, breaks the old lease, and secures the resource lock cleanly
    ok_3, token_3 = coordinator.acquire_distributed_lock("client_gamma", cluster_term=2)
    print(f"[RESOURCES] Session 3 Status: {ok_3} | Token assigned: {token_3}")
    
    print("\n=== SYSTEM SHUTDOWN: COORDINATION MATRIX TERMINATED ===")