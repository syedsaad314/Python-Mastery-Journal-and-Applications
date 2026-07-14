# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Architecture Models for the Asynchronous Saga Pattern
"""
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Callable, Coroutine

class SagaStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESSFUL = "SUCCESSFUL"
    COMPENSATING = "COMPENSATING"
    FAILED = "FAILED"

@dataclass
class SagaContext:
    saga_id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: SagaStatus = SagaStatus.PENDING
    payload: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)
    errors: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SagaStepDefinition:
    name: str
    action_coro: Callable[[SagaContext], Coroutine[Any, Any, None]]
    compensate_coro: Callable[[SagaContext], Coroutine[Any, Any, None]]