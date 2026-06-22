"""
Core Topic: Coordinator-Participant Handshake Model
Description: Simulates Phase 1 (Voting Phase) of the Two-Phase Commit protocol.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class ParticipantNode:
    """Represents a database node or shard responding to coordinator preparation requests."""
    
    def __init__(self, node_id: str, lock_available: bool = True) -> None:
        self.node_id: str = node_id
        self.lock_available: bool = lock_available

    def prepare_vote(self, tx_id: str) -> str:
        """Evaluates internal state to cast a VOTE_COMMIT or VOTE_ABORT."""
        if self.lock_available:
            return "VOTE_COMMIT"
        return "VOTE_ABORT"


class TransactionCoordinator:
    """Orchestrates Phase 1 voting procedures across multiple cluster shards."""
    
    def __init__(self, participants: List[ParticipantNode]) -> None:
        self.participants: List[ParticipantNode] = participants

    def collect_votes(self, tx_id: str) -> Dict[str, str]:
        """Polls all participants to determine if a transaction can safely proceed."""
        votes: Dict[str, str] = {}
        for node in self.participants:
            votes[node.node_id] = node.prepare_vote(tx_id)
        return votes


if __name__ == "__main__":
    shard_1 = ParticipantNode("shard-alpha", lock_available=True)
    shard_2 = ParticipantNode("shard-beta", lock_available=False) # Simulates a resource lock conflict
    
    coordinator = TransactionCoordinator([shard_1, shard_2])
    vote_matrix = coordinator.collect_votes("TX-9001")
    
    print(f"[2PC-HANDSHAKE] Voting phase matrix results: {vote_matrix}")
    can_commit = all(vote == "VOTE_COMMIT" for vote in vote_matrix.values())
    print(f" -> Decision result: {'PROCEED TO COMMIT' if can_commit else 'TRIGGER GLOBAL ABORT'}")