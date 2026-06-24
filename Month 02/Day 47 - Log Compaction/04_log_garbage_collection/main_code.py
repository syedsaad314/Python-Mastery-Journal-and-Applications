# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Garbage Collection & Truncation
Description: Safely discards historical write-ahead log elements up to the snapshot index limit.
"""
from typing import List, Dict

class LogGarbageCollector:
    @staticmethod
    def prune_historical_indices(active_log: List[Dict[str, any]], snapshot_ceiling_index: int) -> List[Dict[str, any]]:
        print(f"[GC] Scanning log array. Pruning everything up to index: {snapshot_ceiling_index}")
        # Retain only operations running strictly beyond the checkpoint index marker
        return [entry for entry in active_log if entry["index"] > snapshot_ceiling_index]

if __name__ == "__main__":
    managed_log = [
        {"index": 0, "term": 1},
        {"index": 1, "term": 1},
        {"index": 2, "term": 2},
        {"index": 3, "term": 2}
    ]
    
    cleaned_log = LogGarbageCollector.prune_historical_indices(managed_log, 1)
    assert len(cleaned_log) == 2
    assert cleaned_log[0]["index"] == 2