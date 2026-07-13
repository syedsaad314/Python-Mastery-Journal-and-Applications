# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Saga State Machine Models
Description: Implements core domain structures, execution contexts, and status 
             token tracking for an orchestration-driven Saga workflow.
"""
from enum import Enum
from typing import Dict, Any, NamedTuple
import uuid

class SagaStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESSFUL = "SUCCESSFUL"
    COMPENSATING = "COMPENSATING"
    FAILED = "FAILED"

class SagaContext(NamedTuple):
    saga_id: uuid.UUID
    status: SagaStatus
    payload: Dict[str, Any]
    steps_executed: list[str]

if __name__ == "__main__":
    tx_id = uuid.uuid4()
    context = SagaContext(
        saga_id=tx_id,
        status=SagaStatus.PENDING,
        payload={"user_id": "usr_404", "charge_amount": 250},
        steps_executed=[]
    )
    assert context.status == SagaStatus.PENDING
    assert context.payload["user_id"] == "usr_404"