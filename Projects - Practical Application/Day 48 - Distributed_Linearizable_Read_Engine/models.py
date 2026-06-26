# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Invariant Structural Data Models
"""
import time
from typing import NamedTuple, Any

class ClientRequest(NamedTuple):
    client_id: str
    sequence_id: int
    payload: str

class ReadQuery(NamedTuple):
    query_key: str
    timestamp: float

class LeasePacket:
    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.granted_at = 0.0

    def renew(self) -> None:
        self.granted_at = time.time()

    def is_valid_with_drift(self, check_time: float, drift_buffer: float) -> bool:
        # Subtract the drift safety buffer from the lease window to stay safe
        effective_duration = self.duration - drift_buffer
        return (check_time - self.granted_at) < effective_duration