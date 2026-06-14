"""
Core Topic: Local Log Entry Appending
Description: Models how a Raft leader tracks and appends uncommitted instructions to its local log.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Any, List

class RaftLogManager:
    """Manages an ordered, index-tracked sequence of transactional log entries."""
    
    def __init__(self) -> None:
        # Raft logs are 1-indexed by convention; index 0 represents a baseline genesis boundary.
        self.entries: List[Dict[str, Any]] = [{"term": 0, "command": "GENESIS_INIT"}]

    def append_client_command(self, current_term: int, command: str) -> int:
        """Appends a new uncommitted command to the local log array, returning its assigned index."""
        new_index = len(self.entries)
        entry = {
            "term": current_term,
            "command": command
        }
        self.entries.append(entry)
        return new_index

    def get_latest_log_details(self) -> tuple:
        """Returns the (index, term) configuration of the latest entry in the log."""
        last_index = len(self.entries) - 1
        last_term = self.entries[last_index]["term"]
        return last_index, last_term


if __name__ == "__main__":
    log_manager = RaftLogManager()
    
    # Simulate a leader in Term 2 accepting mutations from a client
    idx_1 = log_manager.append_client_command(current_term=2, command="SET user_id=saad_irfan")
    idx_2 = log_manager.append_client_command(current_term=2, command="SET balance=50000")
    
    last_idx, last_trm = log_manager.get_latest_log_details()
    print(f"[RAFT-LOG] Current log payload state: {log_manager.entries}")
    print(f"[RAFT-LOG] Last log index tracked: {last_idx} | Last log term tracked: {last_trm}")