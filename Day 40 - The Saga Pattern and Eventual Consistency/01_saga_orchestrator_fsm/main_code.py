"""
Core Topic: Saga Orchestrator State Tracking
Description: Models a centralized Saga Orchestrator FSM executing serial, sequential local tasks.
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto
from typing import List, Dict

class SagaStatus(Enum):
    SUCCESS = auto()
    PROCESSING = auto()
    COMPENSATING = auto()
    FAILED = auto()

class CentralSagaOrchestrator:
    """Central manager coordinating a series of distributed micro-steps step-by-step."""
    
    def __init__(self, saga_id: str, forward_steps: List[str]) -> None:
        self.saga_id = saga_id
        self.steps = forward_steps
        self.current_step_index = 0
        self.status = SagaStatus.PROCESSING

    def advance_step(self) -> str:
        """Moves the Saga forward to the next micro-service execution milestone."""
        if self.status != SagaStatus.PROCESSING:
            return "NON_PROCESSING_STATE"
            
        if self.current_step_index < len(self.steps):
            active_task = self.steps[self.current_step_index]
            self.current_step_index += 1
            if self.current_step_index == len(self.steps):
                self.status = SagaStatus.SUCCESS
            return active_task
        return "ALREADY_COMPLETED"

    def initiate_compensation(self) -> None:
        """Flips the state machine backward to handle backward recovery loops."""
        self.status = SagaStatus.COMPENSATING


if __name__ == "__main__":
    workflow = ["PROCESS_PAYMENT", "RESERVE_INVENTORY", "BOOK_SHIPPING"]
    saga = CentralSagaOrchestrator(saga_id="saga-order-9902", forward_steps=workflow)
    
    print(f"[ORCHESTRATOR-INIT] Saga {saga.saga_id} Status: {saga.status.name}")
    task_1 = saga.advance_step()
    print(f" -> Executing Forward step: {task_1} | Next Target Step Index: {saga.current_step_index}")