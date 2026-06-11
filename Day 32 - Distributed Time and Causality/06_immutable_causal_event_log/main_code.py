"""
Core Topic: Immutable Causally Ordered Event Log
Description: Structures transaction streaming frames sorted deterministically by logical clock bounds.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any

class ImmutableCausalLog:
    """Maintains an append-only event stream ordered by logical causality rather than arrival time."""
    
    def __init__(self) -> None:
        self.storage_stream: List[Dict[str, Any]] = []

    def append_event(self, causal_vector: Dict[str, int], payload: str) -> None:
        """Appends a transaction frame to the log stream."""
        event_frame = {
            "vector": dict(causal_vector),
            "payload": payload
        }
        self.storage_stream.append(event_frame)

    def generate_sorted_stream(self) -> List[Dict[str, Any]]:
        """Sorts and returns the log stream based on vector clock causal ordering rules."""
        def sorting_comparator(item):
            # Deterministic sorting function based on vector clock properties
            vec = item["vector"]
            # Use total sum of ticks as a primary sort key, and individual node values to break ties
            return (sum(vec.values()), sorted(vec.items()))
            
        return sorted(self.storage_stream, key=sorting_comparator)


if __name__ == "__main__":
    stream_logger = ImmutableCausalLog()
    
    # Append events as they arrive out of order from the network
    stream_logger.append_event({"node_x": 1, "node_y": 1}, "Render Page UI View Component")
    stream_logger.append_event({"node_x": 1, "node_y": 0}, "Initialize Core Framework Instance")
    
    print("[CAUSAL-STREAM] Re-assembling log stream into exact logical sequence...")
    reconstructed_sequence = stream_logger.generate_sorted_stream()
    
    for rank, entry in enumerate(reconstructed_sequence):
        print(f" -> Position [{rank}]: {entry['payload']} | Vector: {entry['vector']}")