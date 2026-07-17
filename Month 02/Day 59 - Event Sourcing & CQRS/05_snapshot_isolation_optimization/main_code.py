# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Snapshot Isolation Optimization
Description: Saves checkpoints at specific event versions to avoid processing 
             massive logs from scratch during state restoration.
"""
from typing import Dict, List, Tuple

class SnapshotOptimizedEngine:
    def __init__(self) -> None:
        self.snapshot_store: Dict[str, Tuple[int, dict]] = {} # Map containing (version, state_snapshot)

    def save_checkpoint(self, aggregate_id: str, current_version: int, state_data: dict) -> None:
        self.snapshot_store[aggregate_id] = (current_version, state_data.copy())

    def fetch_latest_checkpoint(self, aggregate_id: str) -> Tuple[int, dict]:
        return self.snapshot_store.get(aggregate_id, (0, {"balance": 0, "status": "NEW"}))

if __name__ == "__main__":
    optimizer = SnapshotOptimizedEngine()
    optimizer.save_checkpoint("acc_55", 5000, {"balance": 25000, "status": "ACTIVE"})
    
    ver, state = optimizer.fetch_latest_checkpoint("acc_55")
    assert ver == 5000
    assert state["balance"] == 25000
    print(f"[SNAPSHOT HIT] Checkpoint recovered successfully. Fast-forwarding state from version: {ver}")