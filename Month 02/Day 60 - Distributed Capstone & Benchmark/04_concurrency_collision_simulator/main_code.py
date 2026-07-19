# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Concurrency Collision Simulator
Description: Simulates simultaneous write requests hitting the same event stream version 
             to test Optimistic Concurrency Control (OCC) guard rails.
"""
from typing import List

class ConcurrencyCollisionSimulator:
    def __init__(self) -> None:
        self.stream_version = 10
        self.append_log: List[str] = []

    def attempt_concurrent_write(self, client_expected_version: int, change_data: str) -> bool:
        # Enforce strict Optimistic Concurrency Control (OCC) checks
        if client_expected_version != self.stream_version:
            return False # Collision detected, request rejected safely
            
        self.append_log.append(change_data)
        self.stream_version += 1
        return True

if __name__ == "__main__":
    sim = ConcurrencyCollisionSimulator()
    
    # Simulate two clients fetching version 10 simultaneously and attempting to write back
    success_user = sim.attempt_concurrent_write(10, "Client A Update")
    collided_user = sim.attempt_concurrent_write(10, "Client B Update")
    
    assert success_user is True
    assert collided_user is False
    assert sim.stream_version == 11
    print(f"[OCC CAUGHT EFFECTIVELY] Collision blocked. Final safe state version: {sim.stream_version}")