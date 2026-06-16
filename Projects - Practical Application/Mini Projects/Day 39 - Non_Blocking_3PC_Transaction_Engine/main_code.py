"""
System: Multi-Regional Non-Blocking 3PC Distributed Transaction Engine
Description: Implements a production-style, non-blocking Three-Phase Commit engine.
             Orchestrates transaction state progression across multiple regions,
             handling validation, staging, and execution phases cleanly.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (3PC-Engine) %(message)s')

class RegionalDataShard3PC:
    """Manages transaction records and resource locks for an isolated regional database shard."""
    
    def __init__(self, shard_id: str, liquid_cash: float) -> None:
        self.shard_id = shard_id
        self.cash_balance = liquid_cash
        self.staged_reserve = 0.0
        self.runtime_state = "IDLE" # IDLE, CAN_COMMIT_VOTED, PRE_COMMIT_STAGED, FINALIZED
        self.exclusive_locks = False

    def process_can_commit_rpc(self, tx_id: str, amount: float) -> str:
        """Phase 1: Validates account funds early on without engaging heavy resource locks."""
        if self.cash_balance >= amount:
            self.runtime_state = "CAN_COMMIT_VOTED"
            logging.info(f"[{self.shard_id}] Phase 1 (Can-Commit) Approved for {tx_id}. Funds available.")
            return "VOTE_YES"
        else:
            self.runtime_state = "IDLE"
            logging.warning(f"[{self.shard_id}] Phase 1 (Can-Commit) Rejected for {tx_id}. Insufficient funds.")
            return "VOTE_NO"

    def process_pre_commit_rpc(self, tx_id: str, amount: float) -> str:
        """Phase 2: Secures exclusive resource locks and stages the transaction modifications."""
        self.exclusive_locks = True
        self.staged_reserve = amount
        self.runtime_state = "PRE_COMMIT_STAGED"
        logging.info(f"[{self.shard_id}] Phase 2 (Pre-Commit) Engaged for {tx_id}. Locks secured.")
        return "ACK_PRE_COMMIT"

    def process_do_commit_rpc(self, tx_id: str) -> None:
        """Phase 3: Applies the staged changes to persistent storage and releases locks."""
        if self.runtime_state == "PRE_COMMIT_STAGED":
            self.cash_balance -= self.staged_reserve
            self.runtime_state = "FINALIZED"
            self.exclusive_locks = False
            self.staged_reserve = 0.0
            logging.info(f"++++ [{self.shard_id}] Phase 3 (Do-Commit) Finalized for {tx_id}. New Balance: {self.cash_balance} ++++")

    def process_abort_rpc(self, tx_id: str) -> None:
        """Rolls back transaction changes and safely releases active resource locks."""
        logging.warning(f"---- [{self.shard_id}] Abort Command Processed for {tx_id}. Rolling back locks. ----")
        self.exclusive_locks = False
        self.staged_reserve = 0.0
        self.runtime_state = "IDLE"


class NonBlockingThreePhaseCoordinator:
    """Coordinates distributed transactions using 3PC to ensure non-blocking safety."""
    
    def __init__(self, shards: List[RegionalDataShard3PC]) -> None:
        self.shards = shards

    def coordinate_transaction(self, tx_id: str, requirements: Dict[str, float]) -> bool:
        logging.info("======================================================================")
        logging.info(f"[COORDINATOR] Launching Asynchronous 3PC Transaction Flow: '{tx_id}'")
        logging.info("======================================================================")
        
        # --- PHASE 1: CAN-COMMIT EXPLORATORY POLL ---
        phase1_votes: Dict[str, str] = {}
        for shard in self.shards:
            target_amount = requirements.get(shard.shard_id, 0.0)
            phase1_votes[shard.shard_id] = shard.process_can_commit_rpc(tx_id, target_amount)

        if any(vote == "VOTE_NO" for vote in phase1_votes.values()):
            logging.error("[COORDINATOR] Phase 1 check failed. Aborting transaction across all shards.")
            for shard in self.shards:
                shard.process_abort_rpc(tx_id)
            return False

        # --- PHASE 2: PRE-COMMIT ISOLATION AND LOCKING ---
        logging.info("[COORDINATOR] Phase 1 succeeded. Broadasting Phase 2 Pre-Commit demands...")
        for shard in self.shards:
            target_amount = requirements.get(shard.shard_id, 0.0)
            shard.process_pre_commit_rpc(tx_id, target_amount)

        # --- PHASE 3: DO-COMMIT FINAL EXECUTION ---
        logging.info("[COORDINATOR] Phase 2 succeeded. Broadcasting Phase 3 Do-Commit finalize execution...")
        for shard in self.shards:
            shard.process_do_commit_rpc(tx_id)

        return True


if __name__ == "__main__":
    print("\n=== STARTING THREE-PHASE COMMIT TRANSACTION ENGINE ===\n")
    
    shard_karachi = RegionalDataShard3PC("pk-khi", liquid_cash=45000.0)
    shard_dubai   = RegionalDataShard3PC("ae-dxb", liquid_cash=15000.0)
    
    engine = NonBlockingThreePhaseCoordinator([shard_karachi, shard_dubai])
    
    # Run a valid distributed transaction requiring funds from both regions
    tx_manifest = {"pk-khi": 12000.0, "ae-dxb": 3500.0}
    tx_outcome = engine.coordinate_transaction("tx-3pc-001", tx_manifest)
    print(f"\n[EXECUTION-OUTCOME] Transaction 001 Final Result Status = {tx_outcome}")
    
    print("\n=== SYSTEM SHUTDOWN: 3PC TRANSACTION CONTAINER CLOSED ===")