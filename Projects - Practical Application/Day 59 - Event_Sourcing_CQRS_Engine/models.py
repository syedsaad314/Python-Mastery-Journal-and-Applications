# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Immutable Domain Event Specifications and Command Definitions
"""
from dataclasses import dataclass, field
import uuid
import time

@dataclass(frozen=True)
class TransactionDomainEvent:
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    aggregate_id: str = "ACC_UNKNOWN"
    version: int = 0
    event_type: str = "BASE_EVENT"
    timestamp: float = field(default_factory=lambda: time.time())
    payload: dict = field(default_factory=dict)

@dataclass(frozen=True)
class AccountCommand:
    aggregate_id: str
    command_type: str
    payload: dict