"""
Core Topic: Partitioned Append-Only Commit Logs
Description: Models horizontal log scaling across segmented topic partitions.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List

class SegmentedPartitionLog:
    """Represents an isolated, sequential append-only record commit log partition."""
    
    def __init__(self, partition_id: int) -> None:
        self.partition_id = partition_id
        self.storage_ledger: List[str] = []

    def append_record(self, payload: str) -> int:
        """Appends an immutable event message to the end of the log and returns its assigned offset."""
        assigned_offset = len(self.storage_ledger)
        self.storage_ledger.append(payload)
        print(f"[LOG-APPEND] Partition {self.partition_id}: Saved offset {assigned_offset} -> '{payload}'")
        return assigned_offset


if __name__ == "__main__":
    partition = SegmentedPartitionLog(partition_id=0)
    assert partition.append_record("TX_PAYMENT_INITIATED") == 0
    assert partition.append_record("TX_PAYMENT_SUCCESS") == 1