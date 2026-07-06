# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Follower Log Conflict Truncation
Description: Detects and overwrites conflicting log entries to force followers 
             to match the leader's authoritative history.
"""
from typing import NamedTuple, List

class LogEntry(NamedTuple):
    term: int
    index: int

class LogSanitizer:
    @staticmethod
    def align_follower_log(local_log: List[LogEntry], incoming_entries: List[LogEntry]) -> List[LogEntry]:
        for entry in incoming_entries:
            idx_pos = entry.index - 1
            # If our log reaches this far, check for a term conflict
            if idx_pos < len(local_log):
                if local_log[idx_pos].term != entry.term:
                    # Truncate all entries from this conflict point onward
                    local_log = local_log[:idx_pos]
                    local_log.append(entry)
            else:
                local_log.append(entry)
        return local_log

if __name__ == "__main__":
    # Follower has uncommitted logs from an old term 2
    follower_history = [LogEntry(1, 1), LogEntry(2, 2), LogEntry(2, 3)]
    # Leader sends authoritative entries for term 3
    leader_update = [LogEntry(3, 2), LogEntry(3, 3)]
    
    sanitized = LogSanitizer.align_follower_log(follower_history, leader_update)
    assert len(sanitized) == 3
    assert sanitized[1].term == 3 # Conflicting history correctly overwritten