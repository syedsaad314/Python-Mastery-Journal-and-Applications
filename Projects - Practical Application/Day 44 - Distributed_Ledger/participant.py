"""
Component: Transaction Cohort Network Participant Node
Description: Connects coordinator commands to local account spaces and processes commit steps.
Lead Engineer: Syed Saad Bin Irfan
"""

from ledger import LocalLedgerAccountSpace
from transaction import LedgerTransaction

class ParticipantCohortNode:
    """Coordinates transaction requests with the node's local database spaces."""
    
    def __init__(self, node_identity: str, ledger_space: LocalLedgerAccountSpace) -> None:
        self.node_identity = node_identity
        self.ledger_space = ledger_space

    def submit_prepare_vote(self, tx: LedgerTransaction) -> str:
        """Evaluates local state limits and returns a prepare vote response."""
        is_ready = self.ledger_space.evaluate_prepare_phase(tx)
        return "VOTE_COMMIT" if is_ready else "VOTE_ABORT"

    def execute_final_commit(self, tx: LedgerTransaction) -> None:
        self.ledger_space.commit_staged_changes(tx)

    def execute_final_abort(self, tx: LedgerTransaction) -> None:
        self.ledger_space.abort_staged_changes(tx)