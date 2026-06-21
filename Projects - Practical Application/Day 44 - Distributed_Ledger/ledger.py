"""
Component: Ledger Local Balancing Space
Description: Manages account balances, write-ahead logs, and uncommitted transaction staging fields.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List
from transaction import LedgerTransaction

class LocalLedgerAccountSpace:
    """Manages individual node account databases, handling write-ahead logging and local changes."""
    
    def __init__(self, node_identity: str) -> None:
        self.node_identity = node_identity
        self.account_balances: Dict[str, float] = {}
        self.write_ahead_log: List[str] = []
        self.staged_buffer: Dict[str, float] = {}

    def configure_balance_profile(self, account_id: str, balance: float) -> None:
        self.account_balances[account_id] = balance

    def evaluate_prepare_phase(self, tx: LedgerTransaction) -> bool:
        """Validates balances and logs the transaction preparation state before committing changes."""
        self.write_ahead_log.append(f"PREPARE_START:{tx.tx_id}")
        
        # Check if the node needs to validate sufficient funds for a sender
        if tx.sender in self.account_balances:
            available_funds = self.account_balances[tx.sender]
            if available_funds < tx.token_amount:
                self.write_ahead_log.append(f"PREPARE_VOTE_ABORT:{tx.tx_id}")
                return False

        self.write_ahead_log.append(f"PREPARE_VOTE_COMMIT:{tx.tx_id}")
        return True

    def commit_staged_changes(self, tx: LedgerTransaction) -> None:
        """Saves staged transaction changes permanently to the account database balances."""
        if tx.sender in self.account_balances:
            self.account_balances[tx.sender] -= tx.token_amount
        if tx.receiver in self.account_balances:
            self.account_balances[tx.receiver] += tx.token_amount
            
        self.write_ahead_log.append(f"GLOBAL_COMMIT_EXECUTE:{tx.tx_id}")

    def abort_staged_changes(self, tx: LedgerTransaction) -> None:
        """Discards transaction changes and logs the rollback action to persistent storage."""
        self.write_ahead_log.append(f"GLOBAL_ABORT_EXECUTE:{tx.tx_id}")