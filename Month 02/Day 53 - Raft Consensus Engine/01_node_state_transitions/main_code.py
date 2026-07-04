# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Node State Transitions
Description: Implements the baseline enumerated states and transition rules 
             governing a consensus host lifecycle.
"""
from enum import Enum

class RaftState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class ConsensusStateNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.state: RaftState = RaftState.FOLLOWER

    def transition_to(self, target_state: RaftState) -> None:
        print(f"[STATE-TRANSITION] Node '{self.node_id}' changing from {self.state.name} -> {target_state.name}")
        self.state = target_state

if __name__ == "__main__":
    node = ConsensusStateNode("replica_01")
    assert node.state == RaftState.FOLLOWER
    node.transition_to(RaftState.CANDIDATE)
    assert node.state == RaftState.CANDIDATE