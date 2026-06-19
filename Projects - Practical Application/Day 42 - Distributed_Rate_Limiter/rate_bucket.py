"""
Component: Token Bucket Controller
Description: High-performance mathematical implementation of the token bucket throttling algorithm.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import threading

class TokenBucketLimiter:
    """Calculates request compliance using mathematical token refills over time."""
    
    def __init__(self, capacity: int, refill_rate_per_sec: float) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_update_timestamp = time.time()
        self._lock = threading.Lock()

    def evaluate_request(self, cost: int = 1) -> bool:
        """Calculates current token counts and consumes tokens if available."""
        with self._lock:
            now = time.time()
            elapsed_time = now - self.last_update_timestamp
            self.last_update_timestamp = now

            # Formula: New_Tokens = Min(Capacity, Current_Tokens + Elapsed_Time * Refill_Rate)
            self.tokens = min(float(self.capacity), self.tokens + (elapsed_time * self.refill_rate))

            if self.tokens >= cost:
                self.tokens -= cost
                return True
            return False

    def synchronize_tokens(self, network_sync_count: float) -> None:
        """Synchronizes token levels with updates received from the central cluster state."""
        with self._lock:
            self.tokens = min(float(self.capacity), network_sync_count)