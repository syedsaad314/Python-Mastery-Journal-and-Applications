"""
Core Topic: Optimizing Memory Footprints with Slots
Description: Drops the standard __dict__ map using class-level slots to optimize memory allocation.
Lead Engineer: Syed Saad Bin Irfan
"""

import sys
from typing import List

class DynamicStandardNode:
    """Standard node configuration using default dynamic dictionary storage spaces."""
    def __init__(self, key: int, payload: str) -> None:
        self.key = key
        self.payload = payload

class OptimizedSlottedNode:
    """Optimized node leveraging slots to lock attributes and eliminate dynamic dictionaries."""
    __slots__ = ["key", "payload"]
    def __init__(self, key: int, payload: str) -> None:
        self.key = key
        self.payload = payload

if __name__ == "__main__":
    node_count = 50000
    
    # Build uniform instance loops to compare memory allocation patterns
    standard_pool: List[DynamicStandardNode] = [DynamicStandardNode(i, "DATA") for i in range(node_count)]
    slotted_pool: List[OptimizedSlottedNode] = [OptimizedSlottedNode(i, "DATA") for i in range(node_count)]
    
    # Sample individual elements to calculate individual base memory costs
    std_elem = standard_pool[0]
    slot_elem = slotted_pool[0]
    
    print("[MEMORY METRICS] Calculating base instance object allocations...")
    print(f" Standard Dynamic Node Object : {sys.getsizeof(std_elem) + sys.getsizeof(std_elem.__dict__)} Bytes")
    print(f" Optimized Slotted Node Object: {sys.getsizeof(slot_elem)} Bytes")
    print(f"[REDUCTION EFFECT] Slotted optimization significantly reduces individual node memory consumption.")