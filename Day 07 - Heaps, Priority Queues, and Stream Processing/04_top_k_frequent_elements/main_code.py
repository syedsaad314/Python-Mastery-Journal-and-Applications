"""
Core Topic: Real-Time Stream Analytics (Top-K Items)
Description: Tracking high-frequency network elements using a size-bounded minimum heap.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq
from collections import Counter

class NetworkStreamAnalyzer:
    @staticmethod
    def identify_top_elements(packet_stream: list[str], target_k: int) -> list[str]:
        """Filters incoming traffic streams to locate the top K most common entries."""
        # Step 1: Calculate structural item counts in linear time
        frequency_map = Counter(packet_stream)
        min_heap = []

        # Step 2: Maintain a min-heap capped at size K to preserve the highest frequencies
        for item, count in frequency_map.items():
            heapq.heappush(min_heap, (count, item))
            if len(min_heap) > target_k:
                heapq.heappop(min_heap)  # Discard the item with the lowest frequency count

        # Step 3: Extract remaining elements from the heap
        return [element_id for count, element_id in sorted(min_heap, reverse=True)]

if __name__ == "__main__":
    ingested_ip_stream = [
        "192.168.1.1", "10.0.0.5", "192.168.1.1", "172.16.0.4",
        "10.0.0.5", "192.168.1.1", "10.0.0.5", "8.8.8.8"
    ]
    
    volume_limit = 2
    hot_targets = NetworkStreamAnalyzer.identify_top_elements(ingested_ip_stream, volume_limit)
    print(f"Top {volume_limit} Most Active System Traffic Connections: {hot_targets}")