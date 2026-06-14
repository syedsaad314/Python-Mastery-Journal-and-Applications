"""
Core Topic: State Machine Snapshot Serialization
Description: Serializes the live memory state of a key-value database along with Raft lifecycle boundaries.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
from typing import Dict, Any

class RaftSnapshotSerializer:
    """Manages compilation and parsing of state machine memory blocks to minimize disk footprint."""
    
    @staticmethod
    def serialize_checkpoint(state_data: Dict[str, Any], last_idx: int, last_trm: int) -> bytes:
        """Encapsulates raw state store maps alongside physical log compaction markers."""
        payload = {
            "metadata": {
                "last_included_index": last_idx,
                "last_included_term": last_trm
            },
            "data_store_state": state_data
        }
        return json.dumps(payload).encode('utf-8')

    @staticmethod
    def deserialize_checkpoint(raw_bytes: bytes) -> Dict[str, Any]:
        """Reconstructs structured maps directly out of raw network snapshot streams."""
        return json.loads(raw_bytes.decode('utf-8'))


if __name__ == "__main__":
    # Live data representing memory states up to log index 45
    live_memory_kv = {"user_session": "authenticated", "access_level": "root"}
    
    raw_block = RaftSnapshotSerializer.serialize_checkpoint(
        state_data=live_memory_kv, last_idx=45, last_trm=3
    )
    print(f"[SERIALIZATION] Raw encoded binary snapshot frame: {raw_block[:60]}...")
    
    reconstructed = RaftSnapshotSerializer.deserialize_checkpoint(raw_block)
    print(f"[SERIALIZATION] Reconstructed metadata layout: {reconstructed['metadata']}")