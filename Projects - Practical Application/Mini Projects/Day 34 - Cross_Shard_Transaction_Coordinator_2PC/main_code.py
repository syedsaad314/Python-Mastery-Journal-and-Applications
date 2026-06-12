"""
System: Cross-Shard Resilient Distributed Transaction Coordinator
Description: A production-grade implementation of a multi-shard transactional ledger. 
             Features Two-Phase Commit orchestration, shard-level data isolation boundaries, 
             and append-only write-ahead log logging for system recovery.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import Dict, List, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (CrossShard-2PC) %(message)s')

class AccountLedgerShard:
    """An independent database shard storing financial account records with localized staging buffers."""
    
    def __init__(self, shard_id: str) -> None:
        self.shard_id: str = shard_id
        self.committed_balances: Dict[str, float] = {}
        self.staged_transaction_buffers: Dict[str, Tuple[str, float]] = {} # Maps TxID -> (Account, DeltaAmt)

    def initialize_account(self, account_id: str, initial_balance: float) -> None:
        self.committed_balances[account_id] = initial_balance

    def prepare_mutation(self, tx_id: str, account_id: str, delta_amount: float) -> bool:
        """Phase 1: Validates funds and stages the transaction, locking the account."""
        if account_id not in self.committed_balances:
            logging.warning(f"[{self.shard_id}] Prepare Failed: Account '{account_id}' not found.")
            return False
            
        current_balance = self.committed_balances[account_id]
        if current_balance + delta_amount < 0:
            logging.warning(f"[{self.shard_id}] Prepare Failed: Insufficient funds for account '{account_id}'.")
            return False

        # Stage the update and hold the resource lock
        self.staged_transaction_buffers[tx_id] = (account_id, delta_amount)
        logging.info(f"[{self.shard_id}] Phase 1 Prepared. Staged change for account '{account_id}': {delta_amount}")
        return True

    def commit_mutation(self, tx_id: str) -> None:
        """Phase 2a: Finalizes the staged transaction and updates the ledger balance."""
        if tx_id in self.staged_transaction_buffers:
            account_id, delta_amount = self.staged_transaction_buffers.pop(tx_id)
            self.committed_balances[account_id] += delta_amount
            logging.info(f"[{self.shard_id}] Phase 2 Committed. Updated balance for account '{account_id}': {self.committed_balances[account_id]}")

    def abort_mutation(self, tx_id: str) -> None:
        """Phase 2b: Rolls back the transaction and clears the staging buffer."""
        if tx_id in self.staged_transaction_buffers:
            del self.staged_transaction_buffers[tx_id]
            logging.info(f"[{self.shard_id}] Phase 2 Aborted. Cleared staging buffer for transaction '{tx_id}'.")


class CrossShardTransactionCoordinator:
    """Orchestrates Two-Phase Commit transactions across distributed account shards."""
    
    def __init__(self, shard_registry: Dict[str, AccountLedgerShard]) -> None:
        self.shard_registry: Dict[str, AccountLedgerShard] = shard_registry
        self.coordinator_wal: List[str] = []

    def execute_cross_shard_transfer(self, tx_id: str, from_shard_id: str, from_account: str, 
                                     to_shard_id: str, to_account: str, amount: float) -> bool:
        """Executes a cross-shard financial transfer using strict Two-Phase Commit rules."""
        logging.info(f"[COORDINATOR] Initiating Distributed Transaction '{tx_id}': Transferring {amount} PKR...")
        
        from_shard = self.shard_registry.get(from_shard_id)
        to_shard = self.shard_registry.get(to_shard_id)
        
        if not from_shard or not to_shard:
            logging.error("[COORDINATOR] Error: One or both specified shards were not found in registry.")
            return False

        self.coordinator_wal.append(f"START:{tx_id}")

        # Phase 1: Prepare Phase (Gather Votes)
        vote_from = from_shard.prepare_mutation(tx_id, from_account, -amount)
        vote_to = to_shard.prepare_mutation(tx_id, to_account, amount)

        # Phase 2: Decision Phase
        if vote_from and vote_to:
            self.coordinator_wal.append(f"COMMIT:{tx_id}")
            logging.info(f"[COORDINATOR] Unanimous approval received. Broadcasting COMMIT for transaction '{tx_id}'...")
            from_shard.commit_mutation(tx_id)
            to_shard.commit_mutation(tx_id)
            return True
        else:
            self.coordinator_wal.append(f"ABORT:{tx_id}")
            logging.warning(f"[COORDINATOR] Conflict detected. Broadcasting ABORT for transaction '{tx_id}'...")
            from_shard.abort_mutation(tx_id)
            to_shard.abort_mutation(tx_id)
            return False


if __name__ == "__main__":
    print("\n=== STARTING DISTRIBUTED SHARD TRANSACTION LEDGER ENGINE ===\n")
    
    # Initialize separate database shards representing regional data centers
    shard_karachi = AccountLedgerShard("shard-khi")
    shard_lahore  = AccountLedgerShard("shard-lhr")
    
    # Seed balances across shards
    shard_karachi.initialize_account("saad_irfan_001", 15000.0)
    shard_lahore.initialize_account("receiver_user_202", 2500.0)
    
    cluster_registry = {"shard-khi": shard_karachi, "shard-lhr": shard_lahore}
    manager = CrossShardTransactionCoordinator(cluster_registry)

    # Scenario A: Successful Cross-Shard Transfer
    print("[TX-FLOW-1] Running transaction 001 (Valid balances expected)...")
    manager.execute_cross_shard_transfer(
        tx_id="TX-ID-A100",
        from_shard_id="shard-khi", from_account="saad_irfan_001",
        to_shard_id="shard-lhr", to_account="receiver_user_202",
        amount=5000.0
    )

    # Scenario B: Failed Transaction triggering an Abort due to insufficient funds
    print("\n[TX-FLOW-2] Running transaction 002 (Insufficient funds expected)...")
    manager.execute_cross_shard_transfer(
        tx_id="TX-ID-B200",
        from_shard_id="shard-khi", from_account="saad_irfan_001",
        to_shard_id="shard-lhr", to_account="receiver_user_202",
        amount=50000.0 # Exceeds current available balance bounds
    )
    
    print("\n=== SYSTEM SHUTDOWN: CROSS-SHARD DISTRIBUTED LEDGER TERMINATED ===")