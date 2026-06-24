# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Historical Log Garbage Collectors
"""
from typing import List, Dict, Any

class AdvancedLogTruncator:
    @staticmethod
    def purge_below_boundary(wal_history: List[Dict[str, Any]], checkpoint_index: int) -> List[Dict[str, Any]]:
        # Slice away memory logs that are already committed and safely backed up in the snapshot
        return [entry for entry in wal_history if entry.get("index", -1) > checkpoint_index]