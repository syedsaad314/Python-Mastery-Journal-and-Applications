"""
Core Topic: 3PC Phase 2 - Pre-Commit Isolation Phase
Description: Advances nodes to the Pre-Commit state, locking resources after a successful Phase 1 poll.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class LockableExecutionNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.phase_state = "IDLE"
        self.locks_engaged = False

    def process_pre_commit(self) -> str:
        """Secures local locks, promising to complete the transaction unless a failure occurs."""
        self.phase_state = "PRE_COMMIT"
        self.locks_engaged = True
        return "ACK_PRE_COMMIT"

class PreCommitPhaseOrchestrator:
    """Orchestrates Phase 2, ensuring nodes lock resources before final execution."""
    
    def __init__(self, nodes: List[LockableExecutionNode]) -> None:
        self.nodes = nodes

    def broadcast_pre_commit_demands(self) -> Dict[str, str]:
        """Moves all participants into the secure Pre-Commit state."""
        acknowledgments: Dict[str, str] = {}
        for node in self.nodes:
            acknowledgments[node.node_id] = node.process_pre_commit()
        return acknowledgments


if __name__ == "__main__":
    cluster_nodes = [LockableExecutionNode("node-01"), LockableExecutionNode("node-02")]
    orchestrator = PreCommitPhaseOrchestrator(cluster_nodes)
    
    acks = orchestrator.broadcast_pre_commit_demands()
    print(f"[3PC-PHASE-2] Pre-Commit Phase acknowledgments received: {acks}")
    print(f"[3PC-PHASE-2] Verification: Node 1 State = {cluster_nodes[0].phase_state} | Locks = {cluster_nodes[0].locks_engaged}")