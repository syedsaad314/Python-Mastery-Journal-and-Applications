# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Matching Property Verification
Description: Asserts whether a node's local historical entries align perfectly 
             with the metadata provided by incoming update payloads.
"""
from typing import NamedTuple, Optional

class LogEntry(NamedTuple):
    term: int
    index: int

class LogMatcher:
    @staticmethod
    def verify_log_continuity(local_entries: list[LogEntry], prev_log_index: int, prev_log_term: int) -> bool:
        # Base case: if it is the first index entry, it matches by default
        if prev_log_index == 0:
            return True
        
        # Reject if the node does not have a log entry at the expected position
        if len(local_entries) < prev_log_index:
            return False
            
        # Verify if the term checks out at the given index boundary
        target_entry = local_entries[prev_log_index - 1]
        return target_entry.term == prev_log_term

if __name__ == "__main__":
    mock_log = [LogEntry(term=1, index=1), LogEntry(term=1, index=2)]
    # Perfect alignment match
    assert LogMatcher.verify_log_continuity(mock_log, prev_log_index=2, prev_log_term=1) == True
    # Mismatched term configuration
    assert LogMatcher.verify_log_continuity(mock_log, prev_log_index=2, prev_log_term=2) == False