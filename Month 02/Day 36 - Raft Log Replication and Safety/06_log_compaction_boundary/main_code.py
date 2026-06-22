"""
Core Topic: Log Compaction Checkpoint Baseline
Description: Simulates truncating historical log entries using baseline memory snapshots.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any

class CompactableLogEngine:
    """Simulates log truncation via state checkpointing to manage disk storage growth."""
    
    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = [
            {"term": 0, "command": "INIT"},
            {"term": 1, "command": "SET x=1"},
            {"term": 1, "command": "SET x=2"},
            {"term": 2, "command": "SET y=5"}
        ]
        self.snapshot_metadata: Dict[str, Any] = {"last_included_index": 0, "last_included_term": 0}

    def generate_snapshot_checkpoint(self, state_snapshot: dict, snapshot_index: int) -> None:
        """Truncates logs up to the snapshot index and saves the latest state metadata."""
        if snapshot_index >= len(self.entries):
            return
            
        self.snapshot_metadata["last_included_index"] = snapshot_index
        self.snapshot_metadata["last_included_term"] = self.entries[snapshot_index]["term"]
        
        # Truncate the log: remove entries up to snapshot_index
        # We retain a placeholder index at 0 to hold the snapshot metadata context boundary
        self.entries = [self.entries[0]] + self.entries[snapshot_index + 1:]
        print(f"[COMPACTION] Snapshotted through index {snapshot_index}. Current active log size: {len(self.entries)}")


if __name__ == "__main__":
    engine = CompactableLogEngine()
    print(f"[COMPACTION] Pre-compaction log entries total: {len(engine.entries)}")
    
    # Checkpoint state values up through index 2
    mock_computed_state = {"x": "2"}
    engine.generate_snapshot_checkpoint(mock_computed_state, snapshot_index=2)
    
    print(f"[COMPACTION] Post-compaction log array dump: {engine.entries}")
    print(f"[COMPACTION] Saved boundary marker context attributes: {engine.snapshot_metadata}")