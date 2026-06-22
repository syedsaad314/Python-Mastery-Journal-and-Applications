"""
Core Topic: Randomized Election Timeout Ticker
Description: Calculates randomized election timeouts to mitigate split-vote issues.
Lead Engineer: Syed Saad Bin Irfan
"""

import random
import time
from typing import Tuple

class ElectionTimeoutTicker:
    """Computes randomized election timeouts to keep cluster nodes out of lockstep."""
    
    def __init__(self, min_timeout_ms: int = 150, max_timeout_ms: int = 300) -> None:
        self.min_bounds = min_timeout_ms
        self.max_bounds = max_timeout_ms

    def generate_randomized_timeout(self) -> float:
        """Generates a randomized duration converted directly into fractional seconds."""
        ms_duration = random.randint(self.min_bounds, self.max_bounds)
        return ms_duration / 1000.0


if __name__ == "__main__":
    ticker = ElectionTimeoutTicker()
    
    # Simulate three distinct nodes generating timers concurrently
    node_1_timer = ticker.generate_randomized_timeout()
    node_2_timer = ticker.generate_randomized_timeout()
    node_3_timer = ticker.generate_randomized_timeout()
    
    print(f"[TICKER] Node 1 calculated election timeout duration: {node_1_timer}s")
    print(f"[TICKER] Node 2 calculated election timeout duration: {node_2_timer}s")
    print(f"[TICKER] Node 3 calculated election timeout duration: {node_3_timer}s")