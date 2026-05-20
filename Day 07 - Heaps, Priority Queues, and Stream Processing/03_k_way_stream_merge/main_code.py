"""
Core Topic: K-Way Stream Log Merge Engine
Description: Merging sorted telemetry logs into a single timeline with bounded memory usage.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq

class DistributedStreamMerger:
    @staticmethod
    def merge_telemetry_channels(streams: list[list[int]]) -> list[int]:
        """Combines multiple pre-sorted data channels into a single timeline."""
        min_heap = []
        consolidated_output = []

        # Step 1: Seed the heap with the initial element from each active channel
        for channel_idx, channel_data in enumerate(streams):
            if channel_data:
                # Structure: (current_value, channel_index, next_element_pointer)
                heapq.heappush(min_heap, (channel_data[0], channel_idx, 0))

        # Step 2: Extract the minimum value and pull the next item from that specific channel
        while min_heap:
            value, channel_idx, element_idx = heapq.heappop(min_heap)
            consolidated_output.append(value)
            
            next_element_idx = element_idx + 1
            if next_element_idx < len(streams[channel_idx]):
                next_val = streams[channel_idx][next_element_idx]
                heapq.heappush(min_heap, (next_val, channel_idx, next_element_idx))

        return consolidated_output

if __name__ == "__main__":
    # Simulated pre-sorted logs coming from 3 isolated cluster nodes
    server_node_alpha = [10, 15, 30]
    server_node_beta  = [5, 20, 25]
    server_node_gamma = [12, 14, 99]
    
    cluster_matrix = [server_node_alpha, server_node_beta, server_node_gamma]
    
    timeline = DistributedStreamMerger.merge_telemetry_channels(cluster_matrix)
    print(f"Consolidated Global Telemetry Timeline: {timeline}")