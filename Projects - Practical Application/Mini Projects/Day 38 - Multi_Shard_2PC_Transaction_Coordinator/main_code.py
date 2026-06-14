"""
System: Multi-Shard Resilient 2PC Distributed Transaction Coordinator
Description: A high-fidelity production-grade emulator of a Two-Phase Commit transaction engine.
             Orchestrates atomic financial mutations across multi-regional database shards,
             handling voting loops, global decision broadcasts, and network edge cases.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (2PC-Coordinator) %(message)s')

class ProductionDatabaseShard:
    """An isolated database shard that locks funds and registers votes for transactions."""
    
    def __init__(self, shard_id: str, current_balance: float) -> None:
        self.shard_id: str = shard_id
        self.balance: float = current_balance
        self.lock_active: bool = False
        self.reserved_amount: float = 0.0

    def process_prepare(self, tx_id: str, amount_to_debit: float) -> str:
        """Phase 1: Validates account funds, locks resources, and returns a vote choice."""
        if self.lock_active:
            logging.warning(f"[{self.shard_id}] Prepare Rejected for {tx_id}: Shard resource already locked.")
            return "VOTE_ABORT"
            
        if self.balance >= amount_to_debit:
            self.lock_active = True
            self.reserved_amount = amount_to_debit
            logging.info(f"[{self.shard_id}] Prepare Successful for {tx_id}: Locked {amount_to_debit} units.")
            return "VOTE_COMMIT"
        else:
            logging.warning(f"[{self.shard_id}] Prepare Rejected for {tx_id}: Insufficient balance.")
            return "VOTE_ABORT"

    def process_global_decision(self, tx_id: str, decision: str) -> None:
        """Phase 2: Executes the final global commit or abort decision across the shard."""
        if not self.lock_active:
            return

        if decision == "GLOBAL_COMMIT":
            self.balance -= self.reserved_amount
            logging.info(f"++++ [{self.shard_id}] Transaction {tx_id} COMMITTED. Balance updated to: {self.balance} ++++")
        else:
            logging.info(f"---- [{self.shard_id}] Transaction {tx_id} ABORTED. Resource lock rolled back cleanly. ----")
            
        # Release the resource lock
        self.lock_active = False
        self.reserved_amount = 0.0


class CoreDistributedTransactionCoordinator:
    """Coordinates multi-shard transactions, ensuring all-or-nothing atomic execution."""
    
    def __init__(self, shards: List[ProductionDatabaseShard]) -> None:
        self.registered_shards = shards

    def execute_distributed_transaction(self, tx_id: str, multi_shard_demands: Dict[str, float]) -> bool:
        """Orchestrates the complete two-phase commit protocol across all shards."""
        logging.info(f"======================================================================")
        logging.info(f"[COORDINATOR] Starting Distributed Transaction: '{tx_id}'")
        logging.info(f"======================================================================")
        
        collected_votes: Dict[str, str] = {}

        # PHASE 1: Broadcast Prepare requests and collect votes
        for shard in self.registered_shards:
            demand_amount = multi_shard_demands.get(shard.shard_id, 0.0)
            # Fetch the shard's vote
            vote = shard.process_prepare(tx_id, demand_amount)
            collected_votes[shard.shard_id] = vote

        # PHASE 2: Evaluate votes and determine the global outcome
        if any(v == "VOTE_ABORT" for v in collected_votes.values()):
            global_decision = "GLOBAL_ABORT"
            transaction_success = False
            logging.error(f"[COORDINATOR] Abort detected in voting patterns. Issuing GLOBAL_ABORT decision.")
        else:
            global_decision = "GLOBAL_COMMIT"
            transaction_success = True
            logging.info(f"[COORDINATOR] All shards voted YES. Issuing GLOBAL_COMMIT decision.")

        # Broadcast the final decision to all shards
        for shard in self.registered_shards:
            shard.process_global_decision(tx_id, global_decision)

        return transaction_success


if __name__ == "__main__":
    # Set up isolated regional database shards
    shard_karachi = ProductionDatabaseShard("shard-khi", current_balance=50000.0)
    shard_dubai   = ProductionDatabaseShard("shard-dxb", current_balance=12000.0)
    
    coordinator = CoreDistributedTransactionCoordinator([shard_karachi, shard_dubai])

    # Scenario A: A valid cross-border transaction where both shards have sufficient funds
    tx_demands_valid = {"shard-khi": 15000.0, "shard-dxb": 4000.0}
    success_a = coordinator.execute_distributed_transaction("tx-global-001", tx_demands_valid)
    print(f"Transaction 001 Final Result Status: {success_a}\n")

    # Scenario B: An invalid transaction that fails because a shard has insufficient funds
    tx_demands_invalid = {"shard-khi": 2000.0, "shard-dxb": 95000.0} # Shard Dubai will reject this
    success_b = coordinator.execute_distributed_transaction("tx-global-002", tx_demands_invalid)
    print(f"Transaction 002 Final Result Status: {success_b}")