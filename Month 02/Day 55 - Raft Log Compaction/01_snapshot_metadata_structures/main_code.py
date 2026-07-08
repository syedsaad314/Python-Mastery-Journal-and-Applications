# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Snapshot Metadata Structures
Description: Defines the immutable structural parameters that capture 
             a log compaction state boundary.
"""
from typing import NamedTuple, Dict, Any

class SnapshotMetadata(NamedTuple):
    last_included_index: int
    last_included_term: int
    state_data: Dict[str, Any]

if __name__ == "__main__":
    meta = SnapshotMetadata(
        last_included_index=45,
        last_included_term=2,
        state_data={"user_101": "active", "balance": 5000}
    )
    assert meta.last_included_index == 45
    assert meta.state_data["balance"] == 5000