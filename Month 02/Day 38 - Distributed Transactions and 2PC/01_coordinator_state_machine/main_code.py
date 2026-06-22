"""
Core Topic: Coordinator Transaction State Tracking
Description: Models the internal states of a central 2PC transaction coordinator.
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto
from typing import Dict, Any

class CoordinatorState(Enum):
    INIT = auto()
    PREPARING = auto()
    COMMITTED = auto()
    ABORTED = auto()

class TransactionCoordinatorTracker:
    """Tracks the lifecycle of a distributed transaction from initialization to global outcome."""
    
    def __init__(self, tx_id: str) -> None:
        self.tx_id: str = tx_id
        self.state: CoordinatorState = CoordinatorState.INIT
        self.participants: Dict[str, str] = {} # node_id -> current_vote

    def transition_to(self, target_state: CoordinatorState) -> None:
        """Enforces clean, unidirectional state transitions for the coordinator."""
        valid_transitions = {
            CoordinatorState.INIT: [CoordinatorState.PREPARING],
            CoordinatorState.PREPARING: [CoordinatorState.COMMITTED, CoordinatorState.ABORTED],
            CoordinatorState.COMMITTED: [],
            CoordinatorState.ABORTED: []
        }
        
        if target_state in valid_transitions[self.state]:
            self.state = target_state
        else:
            raise ValueError(f"Invalid state transition: {self.state.name} -> {target_state.name}")


if __name__ == "__main__":
    tracker = TransactionCoordinatorTracker(tx_id="tx-9901-khi")
    print(f"[COORDINATOR-STATE] Initial transaction tracking state: {tracker.state.name}")
    
    tracker.transition_to(CoordinatorState.PREPARING)
    print(f"[COORDINATOR-STATE] Transitioned tracking state: {tracker.state.name}")