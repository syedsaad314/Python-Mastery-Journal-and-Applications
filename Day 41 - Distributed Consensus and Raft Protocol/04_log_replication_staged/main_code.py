"""
Core Topic: Staged Log Replication Entry
Description: Models appending log entries to a local ledger before global quorum consensus is verified.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List

class RaftLogEntry:
    def __init__(self, index: int, term: int, command: str) -> None:
        self.index = index
        self.term = term
        self.command = command

class LocalRaftLedger:
    """Tracks local log entries before they are finalized across the cluster."""
    
    def __init__(self) -> None:
        self.log_history: List[RaftLogEntry] = []

    def stage_entry(self, term: int, command: str) -> int:
        """Appends a new uncommitted command to the local log sequence."""
        next_index = len(self.log_history) + 1
        entry = RaftLogEntry(next_index, term, command)
        self.log_history.append(entry)
        return next_index


if __name__ == "__main__":
    ledger = LocalRaftLedger()
    idx = ledger.stage_entry(term=2, command="SET balance = 5000")
    print(f"[LOG-REPLICATION] Staged command at entry index: {idx} | Local Log Count: {len(ledger.log_history)}")