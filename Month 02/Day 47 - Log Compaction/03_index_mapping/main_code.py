# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Compacted Index Boundary Mapping
Description: Tracks baseline offset counters representing the historical ceiling of a compaction sequence.
"""
from typing import Dict

class CompactedBoundaryMap:
    def __init__(self, last_included_index: int, last_included_term: int) -> None:
        self.last_included_index = last_included_index
        self.last_included_term = last_included_term

    def pack_metadata(self) -> Dict[str, int]:
        return {
            "last_included_index": self.last_included_index,
            "last_included_term": self.last_included_term,
        }


if __name__ == "__main__":
    boundary = CompactedBoundaryMap(last_included_index=146, last_included_term=2)
    meta_packet = boundary.pack_metadata()

    assert meta_packet["last_included_index"] == 146
    assert meta_packet["last_included_term"] == 2