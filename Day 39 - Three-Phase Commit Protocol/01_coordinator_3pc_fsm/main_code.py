"""
Core Topic: 3PC Coordinator Finite State Machine
Description: Models the non-blocking state progression transitions of a 3PC coordinator.
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto

class State3PC(Enum):
    INIT = auto()
    CAN_COMMIT = auto()
    PRE_COMMIT = auto()
    COMMITTED = auto()
    ABORTED = auto()

class ThreePhaseCoordinatorFSM:
    """Tracks state progressions required by 3PC to eliminate blocking vulnerabilities."""
    
    def __init__(self, tx_id: str) -> None:
        self.tx_id = tx_id
        self.current_state = State3PC.INIT

    def transition_to(self, target_state: State3PC) -> None:
        """Enforces legal 3PC lifecycle pathways to maintain state machine safety invariants."""
        allowed_transitions = {
            State3PC.INIT: [State3PC.CAN_COMMIT, State3PC.ABORTED],
            State3PC.CAN_COMMIT: [State3PC.PRE_COMMIT, State3PC.ABORTED],
            State3PC.PRE_COMMIT: [State3PC.COMMITTED, State3PC.ABORTED],
            State3PC.COMMITTED: [],
            State3PC.ABORTED: []
        }
        
        if target_state in allowed_transitions[self.current_state]:
            self.current_state = target_state
        else:
            raise ValueError(f"[FSM-ERROR] Prohibited transition: {self.current_state.name} -> {target_state.name}")


if __name__ == "__main__":
    fsm = ThreePhaseCoordinatorFSM("tx-3pc-101")
    print(f"[3PC-FSM] Initialized State: {fsm.current_state.name}")
    
    fsm.transition_to(State3PC.CAN_COMMIT)
    fsm.transition_to(State3PC.PRE_COMMIT)
    print(f"[3PC-FSM] Advanced Non-Blocking Milestone State: {fsm.current_state.name}")