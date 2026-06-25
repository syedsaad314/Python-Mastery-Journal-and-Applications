# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Linearizable Fallback Mechanics
Description: Automatically downgrades to a full quorum consensus verification check 
             if local lease timers expire or look suspect.
"""
import time

class LinearizableReadEngineFallback:
    def __init__(self) -> None:
        self.lease_expires_at = 0.0

    def determine_read_strategy(self, current_time: float) -> str:
        if current_time < self.lease_expires_at:
            print("[STRATEGY] Lease is active. Executing local high-speed memory read optimization.")
            return "LOCAL_LEASE_READ"
        else:
            print("[WARN] Lease expired or suspect. Falling back to full ReadIndex quorum verification.")
            return "QUORUM_READ_INDEX_FALLBACK"

if __name__ == "__main__":
    engine = LinearizableReadEngineFallback()
    
    # Test fallback branch activation
    assert engine.determine_read_strategy(time.time()) == "QUORUM_READ_INDEX_FALLBACK"
    
    # Test valid lease path activation
    engine.lease_expires_at = time.time() + 10.0
    assert engine.determine_read_strategy(time.time()) == "LOCAL_LEASE_READ"