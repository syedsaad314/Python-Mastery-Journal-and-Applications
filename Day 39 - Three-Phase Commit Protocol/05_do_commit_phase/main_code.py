"""
Core Topic: 3PC Phase 3 - Do-Commit Final Execution Pipeline
Description: Signals prepared nodes to release locks and finalize their data writes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class PersistentStorageNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.allocation_state = "PRE_COMMIT"
        self.locks_engaged = True

    def execute_final_commit(self) -> None:
        """Applies data updates to persistent storage and releases resource locks."""
        self.allocation_state = "COMMITTED"
        self.locks_engaged = False


class DoCommitPhaseOrchestrator:
    """Coordinates Phase 3, executing the final data writes across the cluster."""
    
    def __init__(self, storage_units: List[PersistentStorageNode]) -> None:
        self.storage_units = storage_units

    def execute_global_finalize(self) -> str:
        for unit in self.storage_units:
            unit.execute_final_commit()
        return "GLOBAL_DO_COMMIT_COMPLETED"


if __name__ == "__main__":
    shards = [PersistentStorageNode("shard-01"), PersistentStorageNode("shard-02")]
    orchestrator = DoCommitPhaseOrchestrator(shards)
    
    result = orchestrator.execute_global_finalize()
    print(f"[3PC-PHASE-3] Phase 3 completion status code: {result}")
    print(f"[3PC-PHASE-3] Shard 1 state: {shards[0].allocation_state} | Active Lock status: {shards[0].locks_engaged}")