"""
Core Topic: Time-Bound Lease Management
Description: Implements a time-expiring lock lease preventing indefinite deadlocks on node drops.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import Optional

class DistributedLockLease:
    """Manages an ephemeral lock lease that auto-expires if the holding node crashes."""
    
    def __init__(self, resource_key: str, lease_duration_sec: float) -> None:
        self.resource_key = resource_key
        self.lease_duration = lease_duration_sec
        self.current_holder: Optional[str] = None
        self.expiration_timestamp: float = 0.0

    def acquire_lease(self, client_id: str) -> bool:
        """Grabs the lease if unheld or if the previous lease has naturally expired."""
        now = time.time()
        if self.current_holder is None or now > self.expiration_timestamp:
            self.current_holder = client_id
            self.expiration_timestamp = now + self.lease_duration
            print(f"[LEASE] Granted lock on '{self.resource_key}' to '{client_id}' for {self.lease_duration}s.")
            return True
        return False


if __name__ == "__main__":
    lock = DistributedLockLease("db_user_row_77", lease_duration_sec=0.5)
    assert lock.acquire_lease("gateway-node-A") == True
    assert lock.acquire_lease("gateway-node-B") == False # Blocked
    time.sleep(0.6) # Wait out the lease expiration window
    assert lock.acquire_lease("gateway-node-B") == True # Successfully acquires expired lock