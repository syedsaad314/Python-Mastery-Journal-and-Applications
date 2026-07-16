# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Core Data Models and Strongly-Typed Event Structures
"""
import uuid
import datetime
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(frozen=True)
class ChoreographyEvent:
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    event_type: str = "BASE"
    sender: str = "SYSTEM"
    payload: Dict[str, Any] = field(default_factory=dict)