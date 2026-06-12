"""
Core Topic: Two-Phase Commit (2PC) Execution Engine
Description: A full multi-node execution loop tracking formal preparation, global decisions, and rollbacks.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class ResourceShard:
    """Manages transactional state changes, supporting dry-run locks and atomic commitments."""
    
    def __init__(self, shard_id: str) -> None:
        self.shard_id: str = shard_id
        self.staged_data: Dict[str, str] = {}
        self.committed_data: Dict[str, str] = {}

    def prepare(self, key: str, value: str) -> bool:
        """Stage the update locally and lock the resource key."""
        self.staged_data[key] = value
        return True # Assumes safe stage for this core baseline engine

    def commit(self, key: str) -> None:
        """Move data from staged buffers to true storage."""
        if key in self.staged_data:
            self.committed_data[key] = self.staged_data.pop(key)

    def abort(self, key: str) -> None:
        """Clear out staged mutations and release resource boundaries."""
        if key in self.staged_data:
            del self.staged_data[key]


class TwoPhaseCommitEngine:
    """Coordinates atomic execution loops across isolated data partitions."""
    
    def __init__(self, shards: List[ResourceShard]) -> None:
        self.shards: List[ResourceShard] = shards

    def execute_transaction(self, key: str, value: str) -> str:
        """Runs the explicit two-phase protocol: Phase 1 (Prepare) and Phase 2 (Commit/Abort)."""
        # Phase 1: Prepare Phase
        prepare_success = True
        for shard in self.shards:
            if not shard.prepare(key, value):
                prepare_success = False
                break

        # Phase 2: Decision Phase
        if prepare_success:
            for shard in self.shards:
                shard.commit(key)
            return "GLOBAL_COMMIT_SUCCESS"
        else:
            for shard in self.shards:
                shard.abort(key)
            return "GLOBAL_ABORT_EXECUTED"


if __name__ == "__main__":
    partition_a = ResourceShard("partition-us")
    partition_b = ResourceShard("partition-eu")
    
    engine = TwoPhaseCommitEngine([partition_a, partition_b])
    status = engine.execute_transaction("user_99", "RegionRoutingUpdated")
    
    print(f"[2PC-ENGINE] Transaction execution result status: {status}")
    print(f" -> Target storage evaluation (partition-us): {partition_a.committed_data}")