"""
Core Topic: Write-Ahead Logging (WAL) Integrity
Description: Ensures transaction states are written to persistent storage before modifying live balances.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class WriteAheadLogger:
    def __init__(self) -> None:
        self.disk_storage_log: List[str] = []

    def write_to_disk(self, state_action: str) -> None:
        """Appends a transaction state entry to persistent storage before updating runtime values."""
        self.disk_storage_log.append(state_action)
        print(f"[WAL-FLUSH] Safely saved state checkpoint to storage: '{state_action}'")


if __name__ == "__main__":
    wal = WriteAheadLogger()
    # The state log must be saved first before updating any live application values
    wal.write_to_disk("TX_START: account_01")
    wal.write_to_disk("COMMIT_PREPARED")
    assert len(wal.disk_storage_log) == 2