"""
Component: Transaction Atomic Commitment Manager
Description: Directs 2PC execution flows across all participant nodes in the cluster.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List
from transaction import LedgerTransaction
from participant import ParticipantCohortNode

class TransactionCommitCoordinator:
    """Manages atomic transaction commit states across all cluster participant nodes."""
    
    def __init__(self, participants: List[ParticipantCohortNode]) -> None:
        self.participants = participants
        self.coordinator_recovery_log: List[str] = []

    def dispatch_distributed_transaction(self, tx: LedgerTransaction) -> bool:
        """Executes a Two-Phase Commit transaction. Returns True if successfully committed everywhere."""
        self.coordinator_recovery_log.append(f"COORDINATOR_TX_INIT:{tx.tx_id}")
        
        # Phase 1: Collect votes from all participant nodes
        node_votes: List[str] = []
        for node in self.participants:
            vote = node.submit_prepare_vote(tx)
            node_votes.append(vote)

        # Phase 2: Check consensus and execute the final action
        if all(vote == "VOTE_COMMIT" for vote in node_votes):
            self.coordinator_recovery_log.append(f"COORDINATOR_GLOBAL_COMMIT_DECVISION:{tx.tx_id}")
            for node in self.participants:
                node.execute_final_commit(tx)
            return True
        else:
            self.coordinator_recovery_log.append(f"COORDINATOR_GLOBAL_ABORT_DECISION:{tx.tx_id}")
            for node in self.participants:
                node.execute_final_abort(tx)
            return False