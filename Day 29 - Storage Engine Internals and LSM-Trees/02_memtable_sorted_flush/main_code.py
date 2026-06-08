"""
Core Topic: In-Memory MemTable Sorted Buffering and SSTable Flushing
Description: Manages a volatile write buffer that flushes to immutable disk tables when full.
Lead Engineer: Syed Saad Bin Irfan
"""

import os
from typing import Dict, List, Tuple

class VolatileMemTable:
    """Buffers writes in a sorted memory array, triggering disk flushes when capacity thresholds are breached."""
    
    def __init__(self, capacity_limit_bytes: int = 128) -> None:
        self.capacity_limit: int = capacity_limit_bytes
        self.current_size_bytes: int = 0
        # Emulating sorted trees utilizing a standard dictionary sorted on modification cycles
        self.memory_store: Dict[str, str] = {}

    def put(self, key: str, value: str) -> bool:
        """Inserts mutations into the memory buffer, tracking layout size changes closely."""
        entry_footprint = len(key.encode('utf-8')) + len(value.encode('utf-8'))
        self.memory_store[key] = value
        self.current_size_bytes += entry_footprint
        
        # Returns True if memory usage breaches the configured capacity threshold limit
        return self.current_size_bytes >= self.capacity_limit

    def extract_sorted_entries(self) -> List[Tuple[str, str]]:
        """Extracts and sorts memory buffer entries, mimicking tree structure traversals."""
        return sorted(self.memory_store.items(), key=lambda x: x[0])

    def flush_to_sstable(self, sstable_destination_path: str) -> None:
        """Flushes sorted items to an immutable, disk-backed storage file."""
        sorted_data = self.extract_sorted_entries()
        with open(sstable_destination_path, "wb") as f:
            for key, val in sorted_data:
                k_bytes = key.encode('utf-8')
                v_bytes = val.encode('utf-8')
                # Format: 2 bytes for key length, 2 bytes for value length, followed by data bytes
                f.write(len(k_bytes).to_bytes(2, byteorder='big'))
                f.write(len(v_bytes).to_bytes(2, byteorder='big'))
                f.write(k_bytes + v_bytes)
                
        self.memory_store.clear()
        self.current_size_bytes = 0


if __name__ == "__main__":
    print("[MEMTABLE] Initializing active sorted write buffer tracking arrays...")
    memtable = VolatileMemTable(capacity_limit_bytes=40)
    
    # Insert updates to trigger a boundary flush signal
    memtable.put("user_a", "active")
    breach_signal = memtable.put("user_b", "restricted_profile_tier_status")
    print(f"[MEMTABLE] Boundary capacity breach detected status flag: {breach_signal}")

    if breach_signal:
        target_file = "generation_0_data.sst"
        memtable.flush_to_sstable(target_file)
        print(f"[MEMTABLE] Sorted items flushed to immutable disk storage file: '{target_file}'")
        if os.path.exists(target_file): os.remove(target_file)