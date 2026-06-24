# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Volatile Memory Monitor & Compaction Policy
"""
import sys
from typing import Any, List, Dict

class SystemCompactionPolicy:
    def __init__(self, max_allowed_bytes: int) -> None:
        self.max_allowed_bytes = max_allowed_bytes

    def is_compaction_required(self, live_wal_log: List[Dict[str, Any]]) -> bool:
        # Check if the memory footprint of the logs exceeds our policy limits
        allocated_bytes = sys.getsizeof(str(live_wal_log))
        return allocated_bytes >= self.max_allowed_bytes