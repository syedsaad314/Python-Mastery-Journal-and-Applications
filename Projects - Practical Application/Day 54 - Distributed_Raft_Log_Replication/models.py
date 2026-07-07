# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Raft Protocol Network Struct Models
"""
from typing import NamedTuple, Any, List

class LogEntry(NamedTuple):
    term: int
    index: int
    command: Any

class AppendEntriesRequest(NamedTuple):
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit: int

class AppendEntriesResponse(NamedTuple):
    term: int
    success: bool
    match_index: int
    responder_id: str