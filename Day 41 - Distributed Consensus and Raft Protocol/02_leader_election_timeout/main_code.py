"""
Core Topic: Randomized Election Timeouts
Description: Implements randomized timeouts to minimize split-vote scenarios during candidate elections.
Lead Engineer: Syed Saad Bin Irfan
"""

import random
import time

class RaftElectionTimer:
    """Manages randomized heartbeat monitoring thresholds to optimize cluster stability."""
    
    def __init__(self, node_id: str, lower_bound_ms: int = 150, upper_bound_ms: int = 300) -> None:
        self.node_id = node_id
        self.lower_bound = lower_bound_ms
        self.upper_bound = upper_bound_ms
        self.active_timeout_ms = 0
        self.reset_timer()

    def reset_timer(self) -> None:
        """Randomizes the timeout window to ensure nodes don't start elections simultaneously."""
        self.active_timeout_ms = random.randint(self.lower_bound, self.upper_bound)

    def check_if_timeout_exceeded(self, elapsed_ms: int) -> bool:
        return elapsed_ms >= self.active_timeout_ms


if __name__ == "__main__":
    timer_a = RaftElectionTimer("node-A")
    timer_b = RaftElectionTimer("node-B")
    
    print(f"[RAFT-TIMER] Node A Timeout Threshold: {timer_a.active_timeout_ms}ms")
    print(f"[RAFT-TIMER] Node B Timeout Threshold: {timer_b.active_timeout_ms}ms")