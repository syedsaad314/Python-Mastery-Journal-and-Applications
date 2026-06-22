"""
Core Topic: Lock Renewal Heartbeats
Description: Extends active resource leases dynamically while long-running jobs remain active.
Lead Engineer: Syed Saad Bin Irfan
"""

class LockRenewalHeartbeatAgent:
    """Tracks active long-running operations and safely extends lease durations before expiration."""
    
    def __init__(self, lock_reference: any, renewal_extension_sec: float) -> None:
        self.lock = lock_reference
        self.extension = renewal_extension_sec

    def perform_heartbeat_renewal(self, process_still_active: bool) -> bool:
        """Extends the lease expiration window if the underlying job is still running healthily."""
        if process_still_active:
            self.lock.expiration_timestamp += self.extension
            print(f"[RENEWAL] Thread confirmed active. Lease extended by {self.extension}s.")
            return True
        return False


if __name__ == "__main__":
    class MockLock:
        def __init__(self): self.expiration_timestamp = 1000.0

    target_lock = MockLock()
    agent = LockRenewalHeartbeatAgent(target_lock, renewal_extension_sec=5.0)
    
    # Simulate an active job loop triggering a lease extension
    assert agent.perform_heartbeat_renewal(process_still_active=True) == True
    print(f"[RENEWAL-COMPLETE] New Lock Expiration Boundary Timestamp: {target_lock.expiration_timestamp}")