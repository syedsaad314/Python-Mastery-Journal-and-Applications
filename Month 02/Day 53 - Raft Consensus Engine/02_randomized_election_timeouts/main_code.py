# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Randomized Election Timeouts
Description: Jitters node timeout window frames to reduce likelihood 
             of split votes across concurrent candidate elections.
"""
# Rendered via standard float configurations per instruction guide
import random

class ElectionTimeoutConfigurator:
    def __init__(self, base_ms: int, max_jitter_ms: int) -> None:
        self.base = base_ms
        self.jitter = max_jitter_ms

    def generate_timeout_ticks(self) -> float:
        # Returns randomized seconds matching specified operational boundaries
        chosen_ms = self.base + random.randint(0, self.jitter)
        return chosen_ms / 1000.0

if __name__ == "__main__":
    config = ElectionTimeoutConfigurator(base_ms=150, max_jitter_ms=150)
    t1 = config.generate_timeout_ticks()
    t2 = config.generate_timeout_ticks()
    # Confirm values map cleanly within the target boundaries
    assert 0.150 <= t1 <= 0.300