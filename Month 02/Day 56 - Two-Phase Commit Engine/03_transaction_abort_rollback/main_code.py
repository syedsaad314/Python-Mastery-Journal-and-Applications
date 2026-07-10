# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Transaction Abort & Rollback Logic
Description: Triggers rollback procedures to undo partial changes across all 
             participants when a transaction fails validation.
"""
from typing import Dict, List, Any

class RollbackEngine:
    def __init__(self) -> None:
        self.rollback_log: List[str] = []

    def execute_global_abort(self, participants: List[str], database_states: Dict[str, Any], tx_id: str) -> None:
        for peer in participants:
            if tx_id in database_states.get(peer, {}):
                # Purge uncommitted transactional workspaces
                database_states[peer].pop(tx_id, None)
                self.rollback_log.append(f"ROLLBACK_SUCCESS:{peer}")

if __name__ == "__main__":
    mock_cluster_state = {
        "shard_1": {"tx_alpha": "pending_payload"},
        "shard_2": {"tx_alpha": "pending_payload"}
    }
    
    engine = RollbackEngine()
    engine.execute_global_abort(["shard_1", "shard_2"], mock_cluster_state, "tx_alpha")
    
    assert "tx_alpha" not in mock_cluster_state["shard_1"]
    assert len(engine.rollback_log) == 2