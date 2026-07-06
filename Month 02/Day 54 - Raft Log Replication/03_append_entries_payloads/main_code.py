# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: AppendEntries Replication Payloads
Description: Builds full replication message payloads containing log data 
             and consensus metadata.
"""
from typing import NamedTuple, Any, List

class LogEntry(NamedTuple):
    term: int
    index: int
    command: Any

class AppendEntriesRPC(NamedTuple):
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit: int

def compile_replication_message(term: int, leader_id: str, current_log: List[LogEntry], next_index_for_peer: int, leader_commit: int) -> AppendEntriesRPC:
    prev_idx = next_index_for_peer - 1
    prev_term = current_log[prev_idx - 1].term if prev_idx > 0 else 0
    payload_entries = current_log[prev_idx:]
    
    return AppendEntriesRPC(
        term=term,
        leader_id=leader_id,
        prev_log_index=prev_idx,
        prev_log_term=prev_term,
        entries=payload_entries,
        leader_commit=leader_commit
    )

if __name__ == "__main__":
    local_history = [LogEntry(1, 1, "cmd1"), LogEntry(1, 2, "cmd2")]
    rpc = compile_replication_message(term=1, leader_id="leader_01", current_log=local_history, next_index_for_peer=2, leader_commit=1)
    assert rpc.prev_log_index == 1
    assert len(rpc.entries) == 1