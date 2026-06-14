"""
Core Topic: Write-Ahead Logging (WAL) for Transactions
Description: Simulates an append-only transaction ledger used to guarantee durability across restarts.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import List, Dict, Any

class WriteAheadLedger:
    """An append-only log that persists state modifications before they are applied to memory."""
    
    def __init__(self) -> None:
        self.storage_log: List[Dict[str, Any]] = []

    def log_state_change(self, tx_id: str, state_marker: str) -> None:
        """Appends a new state entry to the persistent log."""
        log_entry = {
            "timestamp": time.time(),
            "tx_id": tx_id,
            "state": state_marker
        }
        self.storage_log.append(log_entry)
        # In production, this step forces a physical disk flush operation (fsync)

    def read_all_records(self) -> List[Dict[str, Any]]:
        return list(self.storage_log)


if __name__ == "__main__":
    wal = WriteAheadLedger()
    
    # Log key transaction lifecycle milestones
    wal.log_state_change(tx_id="tx-101", state_marker="COORDINATOR_PREPARE_START")
    wal.log_state_change(tx_id="tx-101", state_marker="COORDINATOR_GLOBAL_COMMIT")
    
    print(f"[WAL-LOG] Persistent Write-Ahead Log entries:")
    for record in wal.read_all_records():
        print(f" -> Tx: {record['tx_id']} | Step Marked: {record['state']}")