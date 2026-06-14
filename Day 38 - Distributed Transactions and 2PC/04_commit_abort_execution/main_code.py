"""
Core Topic: Two-Phase Commit - Phase 2: Global Decision Execution
Description: Evaluates collected votes and broadcasts the final global commit or abort decision.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List

class ExecutingShardNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.status = "PREPARED"

    def finalize_transaction(self, global_decision: str) -> None:
        self.status = "COMMITTED" if global_decision == "GLOBAL_COMMIT" else "ABORTED"

class DecisionEvaluatorEngine:
    """Evaluates cluster voting patterns and broadcasts final execution decisions."""
    
    @staticmethod
    def evaluate_and_broadcast(votes: Dict[str, str], participants: List[ExecutingShardNode]) -> str:
        """Enforces atomicity: executes a global commit only if every vote is VOTE_COMMIT."""
        # Atomic Guard: Any single abort vote forces a global abort decision
        if any(vote == "VOTE_ABORT" for vote in votes.values()):
            global_decision = "GLOBAL_ABORT"
        else:
            global_decision = "GLOBAL_COMMIT"

        # Broadcast the decision to all participant nodes
        for node in participants:
            node.finalize_transaction(global_decision)
            
        return global_decision


if __name__ == "__main__":
    nodes = [ExecutingShardNode("shard-A"), ExecutingShardNode("shard-B")]
    
    # Scenario: One shard votes to commit, but the other aborts
    mock_votes = {"shard-A": "VOTE_COMMIT", "shard-B": "VOTE_ABORT"}
    
    final_action = DecisionEvaluatorEngine.evaluate_and_broadcast(mock_votes, nodes)
    print(f"[DECISION-EXECUTION] Coordinator consensus evaluation: {final_action}")
    print(f"[DECISION-EXECUTION] Shard A final status: {nodes[0].status} | Shard B final status: {nodes[1].status}")