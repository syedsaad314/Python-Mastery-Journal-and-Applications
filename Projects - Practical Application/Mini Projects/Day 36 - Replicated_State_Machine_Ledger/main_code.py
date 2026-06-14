"""
System: Fully Replicated State Machine Ledger Store
Description: Implements a distributed key-value ledger store driven by a replicated log pipeline,
             demonstrates parsing committed entries and executing mutations safely.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (StateLedger) %(message)s')

class ReplicatedLedgerEngine:
    """Manages an isolated database ledger driven by verified, committed log entries."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.ledger_balances: Dict[str, float] = {}
        self.last_applied_index: int = 0

    def execute_state_machine_loop(self, shared_log: List[dict], current_cluster_commit_index: int) -> None:
        """Parses and executes committed log entries sequentially up to the cluster commit line."""
        while self.last_applied_index < current_cluster_commit_index:
            self.last_applied_index += 1
            log_entry = shared_log[self.last_applied_index]
            command: str = log_entry["command"]
            
            logging.info(f"[{self.node_id}-StateMachine] Processing entry at index {self.last_applied_index}: '{command}'")
            
            # Parse financial ledger mutation commands
            if command.startswith("INIT_ACC "):
                parts = command[9:].split("=")
                if len(parts) == 2:
                    self.ledger_balances[parts[0].strip()] = float(parts[1].strip())
                    
            elif command.startswith("TRANSFER "):
                # Expected format: TRANSFER from_acc -> to_acc : amt
                payload = command[9:]
                try:
                    meta_parts = payload.split(":")
                    amt = float(meta_parts[1].strip())
                    acc_parts = meta_parts[0].split("->")
                    src = acc_parts[0].strip()
                    dst = acc_parts[1].strip()
                    
                    if self.ledger_balances.get(src, 0) >= amt:
                        self.ledger_balances[src] -= amt
                        self.ledger_balances[dst] = self.ledger_balances.get(dst, 0) + amt
                except Exception as ex:
                    logging.error(f"[{self.node_id}] Failed to parse transaction payload execution: {ex}")


if __name__ == "__main__":
    print("\n=== STARTING REPLICATED STATE MACHINE LEDGER INSTANCES ===\n")
    
    # Simulate a consensus cluster log array containing committed entries
    consolidated_cluster_log = [
        {"term": 0, "command": "GENESIS"},
        {"term": 1, "command": "INIT_ACC saad_irfan = 25000.0"},
        {"term": 1, "command": "INIT_ACC fabha_iqbal = 10000.0"},
        {"term": 2, "command": "TRANSFER saad_irfan -> fabha_iqbal : 5000.0"},
        {"term": 2, "command": "TRANSFER fabha_iqbal -> saad_irfan : 1200.0"} # Not yet committed
    ]
    
    # Initialize separate ledger instances for different regional nodes
    node_karachi = ReplicatedLedgerEngine("node-pk-khi")
    node_dubai   = ReplicatedLedgerEngine("node-ae-dxb")
    
    # Consensus moves the commit line up to index 3 (first three mutations are safely committed)
    safe_commit_line = 3
    
    print("[REPLICATION-LOOP] Synchronizing Karachi data center instance...")
    node_karachi.execute_state_machine_loop(consolidated_cluster_log, current_cluster_commit_index=safe_commit_line)
    
    print("\n[REPLICATION-LOOP] Synchronizing Dubai data center instance...")
    node_dubai.execute_state_machine_loop(consolidated_cluster_log, current_cluster_commit_index=safe_commit_line)
    
    print("\n=== VERIFYING COHERENT RUNTIME BALANCES ===")
    print(f" -> Karachi Ledger States: {node_karachi.ledger_balances}")
    print(f" -> Dubai Ledger States:   {node_dubai.ledger_balances}")
    
    assert node_karachi.ledger_balances["saad_irfan"] == 20000.0
    assert node_dubai.ledger_balances["fabha_iqbal"] == 15000.0
    print("\n[CONSISTENCY-CHECK] Success: Balances match exactly across nodes.")
    
    print("\n=== SYSTEM SHUTDOWN: REPLICATED LEDGER INSTANCES CLOSED ===")