# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Two-Phase Commit Network Data Schemas
"""
from typing import NamedTuple, Any, Dict
from enum import Enum

class TransactionCommand(Enum):
    PREPARE = "PREPARE"
    COMMIT = "COMMIT"
    ABORT = "ABORT"

class ParticipantVote(Enum):
    VOTE_COMMIT = "VOTE_COMMIT"
    VOTE_ABORT = "VOTE_ABORT"
    TIMEOUT = "TIMEOUT"

class TransactionPayload(NamedTuple):
    tx_id: str
    command: TransactionCommand
    payload_data: Dict[str, Any]