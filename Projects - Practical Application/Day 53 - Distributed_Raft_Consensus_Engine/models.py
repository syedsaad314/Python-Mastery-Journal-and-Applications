# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Raft Protocol Data Payload Schemas
"""
from typing import NamedTuple, Optional, List

class VoteRequest(NamedTuple):
    term: int
    candidate_id: str

class VoteResponse(NamedTuple):
    term: int
    vote_granted: bool
    responder_id: str

class AppendEntriesHeartbeat(NamedTuple):
    term: int
    leader_id: str