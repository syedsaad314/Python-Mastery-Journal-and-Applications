"""
Core Topic: Raft Node State Machine
Description: Models fundamental role states and transition validations for a consensus node.
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto

class RaftRole(Enum):
    FOLLOWER = auto()
    CANDIDATE = auto()
    LEADER = auto()

class RaftStateEngine:
    """Enforces strict state transitions rules according to the Raft specification."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.current_role: RaftRole = RaftRole.FOLLOWER

    def transition_to_candidate(self) -> None:
        """Triggers when local election timeouts expire without receiving a heartbeat."""
        if self.current_role in (RaftRole.FOLLOWER, RaftRole.CANDIDATE):
            self.current_role = RaftRole.CANDIDATE
        else:
            raise ValueError(f"Invalid transition from state {self.current_role} to CANDIDATE.")

    def transition_to_leader(self) -> None:
        """Triggers when a candidate successfully wins a cluster quorum majority vote."""
        if self.current_role == RaftRole.CANDIDATE:
            self.current_role = RaftRole.LEADER
        else:
            raise ValueError(f"Invalid transition from state {self.current_role} to LEADER.")

    def transition_to_follower(self) -> None:
        """Triggers immediately if a higher term or valid leader heartbeat is discovered."""
        self.current_role = RaftRole.FOLLOWER


if __name__ == "__main__":
    node = RaftStateEngine("node-alpha")
    print(f"[RAFT-STATE] Initial baseline operational role: {node.current_role.name}")
    
    node.transition_to_candidate()
    print(f"[RAFT-STATE] Role after election timeout trigger: {node.current_role.name}")
    
    node.transition_to_leader()
    print(f"[RAFT-STATE] Role following successful quorum vote collection: {node.current_role.name}")