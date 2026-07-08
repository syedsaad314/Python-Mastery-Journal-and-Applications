# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Dynamic Memory Reclamation
Description: Slices log arrays during compaction to ensure discarded memory 
             is garbage collected and freed.
"""
import sys
from typing import List, NamedTuple

class LogEntry(NamedTuple):
    index: int
    payload: str

def compact_and_reclaim(raw_log: List[LogEntry], compact_up_to_idx: int) -> List[LogEntry]:
    # Retain only entries positioned strictly after our compaction point
    return [entry for entry in raw_log if entry.index > compact_up_to_idx]

if __name__ == "__main__":
    large_log = [LogEntry(i, "heavy_payload_string_data_bytes") for i in range(1, 101)]
    assert len(large_log) == 100
    
    # Compact up to index 70
    compacted_log = compact_and_reclaim(large_log, compact_up_to_idx=70)
    assert len(compacted_log) == 30
    assert compacted_log[0].index == 71