"""
Core Topic: Raft Cluster Node State Machine
Description: Models the three distinct states of a Raft node (Follower, Candidate, Leader).
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto

class RaftRole(Enum):
    FOLLOWER = auto()
    CANDIDATE = auto()
    LEADER = auto()

class RaftNodeStateFSM:
    """Manages role transitions for a single cluster node under strict consensus invariants."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.role = RaftRole.FOLLOWER
        self.current_term = 0

    def transition_to(self, new_role: RaftRole, term: int) -> None:
        """Enforces legal state progression pathways according to Raft specifications."""
        if term < self.current_term:
            raise ValueError("[Raft-Error] Cannot transition to a stale term.")
            
        self.current_term = term
        old_role = self.role
        self.role = new_role
        print(f"[RAFT-FSM] Node {self.node_id}: {old_role.name} -> {self.role.name} (Term: {self.current_term})")


if __name__ == "__main__":
    node = RaftNodeStateFSM("srv-node-01")
    # Simulate discovering that a leader has timed out
    node.transition_to(RaftRole.CANDIDATE, term=1)
    # Simulate winning the cluster majority quorum vote
    node.transition_to(RaftRole.LEADER, term=1)