"""
Core Topic: 3PC Participant State-Aware Timeout Fallbacks
Description: Implements state-aware timeout rules to prevent nodes from hanging indefinitely.
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto

class ParticipantState3PC(Enum):
    INIT = auto()
    CAN_COMMIT_RECEIVED = auto()
    PRE_COMMIT_RECEIVED = auto()
    COMMITTED = auto()
    ABORTED = auto()

class TimeoutHandlingParticipant:
    """A 3PC participant shard that applies timeout rules based on its current state."""
    
    def __init__(self, shard_id: str) -> None:
        self.shard_id = shard_id
        self.state = ParticipantState3PC.INIT

    def handle_coordinator_timeout(self) -> str:
        """Applies 3PC timeout rules to resolve transactions when the coordinator drops offline."""
        if self.state in [ParticipantState3PC.INIT, ParticipantState3PC.CAN_COMMIT_RECEIVED]:
            # Rule 1: If we haven't reached the pre-commit phase yet, safe to abort-by-default
            self.state = ParticipantState3PC.ABORTED
            return "TIMEOUT_FALLBACK_ABORT"
        elif self.state == ParticipantState3PC.PRE_COMMIT_RECEIVED:
            # Rule 2: If we are already in pre-commit, every node voted yes; auto-commit to prevent blocking
            self.state = ParticipantState3PC.COMMITTED
            return "TIMEOUT_FALLBACK_COMMIT"
        return "NO_ACTION_REQUIRED"


if __name__ == "__main__":
    node_a = TimeoutHandlingParticipant("shard-khi-01")
    node_a.state = ParticipantState3PC.CAN_COMMIT_RECEIVED
    
    node_b = TimeoutHandlingParticipant("shard-dxb-02")
    node_b.state = ParticipantState3PC.PRE_COMMIT_RECEIVED
    
    print(f"[TIMEOUT-HANDLER] Node A fallback action: {node_a.handle_coordinator_timeout()} -> State: {node_a.state.name}")
    print(f"[TIMEOUT-HANDLER] Node B fallback action: {node_b.handle_coordinator_timeout()} -> State: {node_b.state.name}")