"""
Core Topic: Follower Log Consistency Verification
Description: Simulates a follower validating incoming logs and rolling back conflicting histories.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any, Tuple

class ValidatingFollowerNode:
    """Verifies incoming log entries against local history, resolving conflicts cleanly."""
    
    def __init__(self, node_id: str, initial_entries: List[Dict[str, Any]]) -> None:
        self.node_id = node_id
        self.local_log: List[Dict[str, Any]] = list(initial_entries)

    def process_append_entries(self, prev_log_index: int, prev_log_term: int, new_entries: List[Dict[str, Any]]) -> Tuple[bool, int]:
        """Validates log consistency. Overwrites conflicts and appends new entries if match succeeds."""
        # Step 1: Out-of-bounds check
        if prev_log_index >= len(self.local_log):
            return False, len(self.local_log)

        # Step 2: Term mismatch check at prev_log_index
        if self.local_log[prev_log_index]["term"] != prev_log_term:
            # Force optimization: delete conflicting log and everything after it
            self.local_log = self.local_log[:prev_log_index]
            return False, len(self.local_log)

        # Step 3: Append new entries, overwriting any existing conflicts at overlapping indices
        for i, entry in enumerate(new_entries):
            target_index = prev_log_index + 1 + i
            if target_index < len(self.local_log):
                if self.local_log[target_index]["term"] != entry["term"]:
                    self.local_log = self.local_log[:target_index] # Truncate mismatched history
                    self.local_log.append(entry)
            else:
                self.local_log.append(entry)
                
        return True, len(self.local_log)


if __name__ == "__main__":
    # Simulate a follower that has a stale or conflicting entry at index 2 from an old term
    follower_history = [
        {"term": 0, "command": "GENESIS"},
        {"term": 1, "command": "OP-1"},
        {"term": 1, "command": "OLD-STALE-DATA"} # Conflict target index 2
    ]
    
    follower = ValidatingFollowerNode("node-02", follower_history)
    
    # Leader issues an RPC matching up through index 1, but providing clean data for index 2
    success, current_length = follower.process_append_entries(
        prev_log_index=1,
        prev_log_term=1,
        new_entries=[{"term": 2, "command": "NEW-VALID-DATA"}]
    )
    
    print(f"[CONSISTENCY] AppendEntries request status: {success}")
    print(f"[CONSISTENCY] Post-validation follower local log: {follower.local_log}")