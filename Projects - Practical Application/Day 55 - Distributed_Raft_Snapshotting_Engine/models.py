# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Raft Snapshotting Core Model Payloads
"""
from typing import NamedTuple, Any, List, Dict

class LogEntry(NamedTuple):
    term: int
    index: int
    command: Dict[str, Any]

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

class InstallSnapshotRequest(NamedTuple):
    term: int
    leader_id: str
    last_included_index: int
    last_included_term: int
    data: Dict[str, Any]

class InstallSnapshotResponse(NamedTuple):
    term: int
    responder_id: str
    success: bool