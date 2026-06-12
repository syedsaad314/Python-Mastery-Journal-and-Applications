"""
Core Topic: Write-Ahead Log (WAL) Recovery Architecture
Description: Parses transaction log states to rebuild system memory models after a crash.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class CrashRecoverableSystem:
    """Simulates a cluster node that uses an append-only log to rebuild its state after a crash."""
    
    def __init__(self) -> None:
        self.volatile_memory: Dict[str, str] = {}
        self.append_only_wal: List[str] = []

    def log_and_execute(self, action: str, key: str, value: str) -> None:
        """Appends an operational step to the log before modifying volatile memory namespaces."""
        log_entry = f"{action}:{key}:{value}"
        self.append_only_wal.append(log_entry)
        if action == "COMMIT":
            self.volatile_memory[key] = value

    def simulate_hard_crash(self) -> None:
        """Clears out the volatile memory space while preserving the append-only log."""
        self.volatile_memory.clear()

    def play_wal_recovery(self) -> None:
        """Parses the append-only log entries sequentially to rebuild the volatile memory state."""
        for entry in self.append_only_wal:
            action, key, value = entry.split(":")
            if action == "COMMIT":
                self.volatile_memory[key] = value


if __name__ == "__main__":
    node = CrashRecoverableSystem()
    node.log_and_execute("COMMIT", "ledger_id_101", "Balance=5000-PKR")
    node.log_and_execute("COMMIT", "ledger_id_102", "Balance=7500-PKR")
    
    print(f"[WAL-RECOVERY] Pre-crash system memory snapshot: {node.volatile_memory}")
    
    # Trigger a simulated power loss crash
    node.simulate_hard_crash()
    print(f"[WAL-RECOVERY] Post-crash memory snapshot (Expecting Empty): {node.volatile_memory}")
    
    # Parse the log to restore the data state
    node.play_wal_recovery()
    print(f"[WAL-RECOVERY] Rebuilt system memory state after parsing log: {node.volatile_memory}")