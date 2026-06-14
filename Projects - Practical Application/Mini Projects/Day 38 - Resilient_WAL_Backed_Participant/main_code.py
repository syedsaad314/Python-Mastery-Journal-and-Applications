"""
System: Fault-Tolerant WAL-Backed Storage Participant Engine
Description: Emulates a database shard node reinforced with an active Write-Ahead Log.
             Logs state milestones to a persistent file structure before responding to network
             requests, allowing the shard to safely recover its exact status after sudden crashes.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (WAL-Participant) %(message)s')

class FaultTolerantWALParticipant:
    """A database node that uses an append-only log to survive crashes mid-transaction."""
    
    def __init__(self, node_id: str, balance: float) -> None:
        self.node_id: str = node_id
        self.balance: float = balance
        self.lock_active: bool = False
        self.staged_debit: float = 0.0
        
        # Simulated write-ahead log storage array
        self.wal_file_stream: List[Dict[str, Any]] = []

    def _write_to_wal(self, tx_id: str, action_marker: str) -> None:
        """Appends a new state change record to the write-ahead log before changing state."""
        log_record = {"tx_id": tx_id, "action": action_marker}
        self.wal_file_stream.append(log_record)
        logging.info(f"[{self.node_id}-WAL-WRITE] Flushed record to disk stream: {log_record}")

    def handle_prepare_rpc(self, tx_id: str, amount: float) -> str:
        """Saves the prepare step to the log and locks resources if funds are available."""
        if self.balance >= amount:
            # Enforce Write-Ahead discipline: log the step before modifying memory states
            self._write_to_wal(tx_id, "VOTED_PREPARE_COMMIT")
            
            self.lock_active = True
            self.staged_debit = amount
            return "VOTE_COMMIT"
        else:
            self._write_to_wal(tx_id, "VOTED_PREPARE_ABORT")
            return "VOTE_ABORT"

    def handle_commit_rpc(self, tx_id: str) -> None:
        """Logs the final commit state change and updates the database balance."""
        if self.lock_active:
            self._write_to_wal(tx_id, "FINAL_COMMIT_EXECUTED")
            self.balance -= self.staged_debit
            self.lock_active = False
            self.staged_debit = 0.0
            logging.info(f"[{self.node_id}] Account data updated successfully in memory.")

    def simulate_sudden_power_crash(self) -> None:
        """Simulates an unexpected crash that wipes out all volatile RAM memory tracking attributes."""
        logging.warning("🚨 [CRASH-EVENT] Unexpected hardware crash occurred! Wiping RAM contents... 🚨")
        self.lock_active = False
        self.staged_debit = 0.0

    def run_startup_recovery_loop(self) -> None:
        """Scans the write-ahead log on startup to rebuild the node's state after a crash."""
        logging.info(f"[{self.node_id}-STARTUP] Running crash recovery loop from log stream...")
        
        tx_states: Dict[str, str] = {}
        for entry in self.wal_file_stream:
            tx_states[entry["tx_id"]] = entry["action"]

        # Restore memory locks and states based on the log entries
        for tx_id, last_action in tx_states.items():
            if last_action == "VOTED_PREPARE_COMMIT":
                logging.warning(f" -> [RECOVERED-LOCK] Tx '{tx_id}' was left in the PREPARED state. Re-acquiring locks!")
                self.lock_active = True
            elif last_action == "FINAL_COMMIT_EXECUTED":
                logging.info(f" -> [RECOVERED-OK] Tx '{tx_id}' was completed successfully. No action needed.")


if __name__ == "__main__":
    print("\n=== STARTING FAULT-TOLERANT WAL-BACKED STORAGE ENGINE ===\n")
    
    node = FaultTolerantWALParticipant("shard-khi-01", balance=30000.0)
    
    # Step 1: Process an incoming transaction request normally
    print("[RUN] Processing transaction request...")
    node.handle_prepare_rpc(tx_id="tx-8809", amount=5000.0)
    
    # Step 2: Simulate a crash while the transaction is still in the prepared state
    node.simulate_sudden_power_crash()
    print(f" -> Post-Crash Memory status: Lock Active = {node.lock_active}\n")
    
    # Step 3: Reboot the node and run the recovery loop to restore the lost locks
    node.run_startup_recovery_loop()
    print(f" -> Post-Recovery Memory status: Lock Active = {node.lock_active}")
    
    print("\n=== SYSTEM SHUTDOWN: FAULT-TOLERANT STORAGE ENGINE CONTAINER CLOSED ===")