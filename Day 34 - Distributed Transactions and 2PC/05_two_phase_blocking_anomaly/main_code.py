"""
Core Topic: Two-Phase Commit Blocking Anomaly Simulator
Description: Showcases how a coordinator crash during Phase 2 leaves participant nodes locked and blocking.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List, Optional

class BlockableParticipant:
    """A participant node that locks up indefinitely if the coordinator crashes during execution."""
    
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.transaction_state: Optional[str] = None # None, PREPARED, COMMITTED
        self.resource_locked: bool = False

    def receive_prepare(self) -> str:
        self.transaction_state = "PREPARED"
        self.resource_locked = True
        return "VOTE_COMMIT"

    def handle_coordinator_timeout(self) -> str:
        """Triggers if the coordinator goes offline after the prepare phase."""
        if self.transaction_state == "PREPARED":
            # The node cannot safely abort or commit on its own because it doesn't know what other nodes voted
            return "BLOCKED_WAITING_FOR_COORDINATOR"
        return "SAFE_LOCAL_ABORT"


if __name__ == "__main__":
    node_a = BlockableParticipant("node-region-1")
    
    # Step 1: Node processes a prepare request, locks its resources, and votes to commit
    node_a.receive_prepare()
    print(f"[BLOCKING-SIM] Node current execution state: {node_a.transaction_state} | Lock Active: {node_a.resource_locked}")
    
    # Step 2: The coordinator crashes before sending the final decision, causing a timeout
    resolution_status = node_a.handle_coordinator_timeout()
    print(f"[BLOCKING-SIM] Timeout resolution status: {resolution_status}")