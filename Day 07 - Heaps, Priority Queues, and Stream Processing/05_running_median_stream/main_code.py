"""
Core Topic: Continuous Rolling Median Tracking
Description: Balancing items between a Max-Heap and Min-Heap to extract live mid-points.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq

class ContinuousMedianTracker:
    def __init__(self):
        # Max-Heap tracks the lower, smaller half of incoming elements (inverted values for heapq)
        self.lower_max_heap = []
        # Min-Heap tracks the upper, larger half of incoming elements
        self.upper_min_heap = []

    def ingest_stream_metric(self, metric: float) -> None:
        """Adds a new performance metric into balanced heap storage partitions."""
        # Always insert into lower heap first, then balance to upper heap
        if not self.lower_max_heap or metric <= -self.lower_max_heap[0]:
            heapq.heappush(self.lower_max_heap, -metric)
        else:
            heapq.heappush(self.upper_min_heap, metric)

        # Enforce the structural balance rule: size difference must not exceed 1
        if len(self.lower_max_heap) > len(self.upper_min_heap) + 1:
            moved_val = -heapq.heappop(self.lower_max_heap)
            heapq.heappush(self.upper_min_heap, moved_val)
        elif len(self.upper_min_heap) > len(self.lower_max_heap):
            moved_val = heapq.heappop(self.upper_min_heap)
            heapq.heappush(self.lower_max_heap, -moved_val)

    def extract_current_median(self) -> float:
        """Returns the calculated live midpoint value across all processed metrics."""
        if len(self.lower_max_heap) == len(self.upper_min_heap):
            # Even item count: calculate the average of both roots
            return (-self.lower_max_heap[0] + self.upper_min_heap[0]) / 2.0
        else:
            # Odd item count: the root of the lower max-heap holds the true midpoint
            return float(-self.lower_max_heap[0])

if __name__ == "__main__":
    tracker = ContinuousMedianTracker()
    simulated_latency_stream = [12.5, 40.2, 5.0, 18.9, 22.1]
    
    for ping in simulated_latency_stream:
        tracker.ingest_stream_metric(ping)
        print(f"Ingested Request Latency: {ping:4} -> Running Median Assessment: {tracker.extract_current_median()}")