"""
Core Topic: Raft Distributed consensus Leader Election Framework
Description: Implements an isolated abstract state machine to manage node execution transitions.
Lead Engineer: Syed Saad Bin Irfan
"""

import random
import time
from typing import Optional

class RaftNodeStateMachine:
    """Models internal state transitions for Raft consensus node lifecycle management."""
    
    def __init__(self, physical_node_id: str) -> None:
        self.node_id: str = physical_node_id
        self.current_role: str = "FOLLOWER"  # FOLLOWER, CANDIDATE, LEADER
        self.current_term: int = 0
        self.voted_for: Optional[str] = None
        self._election_timeout_seconds: float = self._recalculate_randomized_timer()
        self.last_heartbeat_timestamp: float = time.time()

    def _recalculate_randomized_timer(self) -> float:
        """Generates a randomized election timeout value to minimize split-vote deadlocks."""
        return random.uniform(0.15, 0.30)

    def process_heartbeat_tick(self, cluster_leader_id: str, leader_term: int) -> bool:
        """Processes inbound leader heartbeats, resetting state metrics or stepping down if out-of-date."""
        if leader_term >= self.current_term:
            self.current_term = leader_term
            self.current_role = "FOLLOWER"
            self.voted_for = None
            self.last_heartbeat_timestamp = time.time()
            return True
        return False

    def initiate_election_sequence(self) -> Tuple[int, str]: # type: ignore
        """Triggers candidate transformation sequences when local election timers expire."""
        if self.current_role == "LEADER":
            return self.current_term, self.current_role
            
        self.current_role = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id  # Vote for self
        self.last_heartbeat_timestamp = time.time()
        self._election_timeout_seconds = self._recalculate_randomized_timer()
        
        return self.current_term, self.node_id

    def register_vote_request(self, candidate_id: str, candidate_term: int) -> bool:
        """Evaluates vote requests, protecting terms from backward regressions."""
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.current_role = "FOLLOWER"
            self.voted_for = None

        if candidate_term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            self.last_heartbeat_timestamp = time.time()  # Reset timeout on successful vote allocation
            return True
        return False


if __name__ == "__main__":
    print("[RAFT-STATE] Initializing finite state replication machines...")
    node = RaftNodeStateMachine("CLUSTER_NODE_01")
    
    print(f"[RAFT-STATE] Startup role configuration status: {node.current_role} | Term: {node.current_term}")
    term, target = node.initiate_election_sequence()
    print(f"[RAFT-STATE] Post-timeout status transition: Role={node.current_role} | Voted For={node.voted_for}")