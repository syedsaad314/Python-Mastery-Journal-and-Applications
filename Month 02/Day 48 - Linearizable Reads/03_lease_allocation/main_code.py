# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Leader Lease Allocation
Description: Tracks a localized time-bounded window where a leader can safely 
             serve local reads without hitting network consensus.
"""
import time
from typing import Dict

class LeaderLeaseAllocator:
    def __init__(self, lease_duration_seconds: float) -> None:
        self.lease_duration = lease_duration_seconds
        self.lease_granted_at = 0.0

    def renew_lease(self) -> None:
        self.lease_granted_at = time.time()
        print(f"[LEASE] Renewable lock confirmed at timestamp: {self.lease_granted_at}")

    def is_lease_valid(self, current_time: float) -> bool:
        # Check if the elapsed time falls inside the strict lease window bounds
        return (current_time - self.lease_granted_at) < self.lease_duration

if __name__ == "__main__":
    allocator = LeaderLeaseAllocator(lease_duration_seconds=2.0)
    allocator.renew_lease()
    
    # Check immediate valid assertion windows
    assert allocator.is_lease_valid(time.time()) == True
    # Check simulated elapsed time expiration
    assert allocator.is_lease_valid(time.time() + 5.0) == False