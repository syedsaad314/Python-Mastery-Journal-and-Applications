"""
Core Topic: Raft Leader Election and Term State Machine
Description: Implements the standardized three-state consensus transitions with randomized election timers.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import random
from typing import List, Dict, Optional

class RaftNodeElectionCore:
    """Manages the internal state transitions and term voting tracking of a single cluster node."""
    
    def __init__(self, node_id: str, cluster_nodes: List[str]) -> None:
        self.node_id: str = node_id
        self.peers: List[str] = [p for p in cluster_nodes if p != node_id]
        
        # Core consensus state fields
        self.current_term: int = 0
        self.voted_for: Optional[str] = None
        self.node_state: str = "FOLLOWER" # States: FOLLOWER, CANDIDATE, LEADER
        
        # Timing configurations (simulated in milliseconds)
        self.election_timeout: float = random.uniform(150.0, 300.0)
        self.last_heartbeat_timestamp: float = time.time() * 1000.0

    def check_election_timeout(self) -> bool:
        """Verifies if the node's follower timeout window has closed, forcing a transition to Candidate."""
        current_now = time.time() * 1000.0
        if self.node_state != "LEADER" and (current_now - self.last_heartbeat_timestamp) > self.election_timeout:
            self._transition_to_candidate()
            return True
        return False

    def _transition_to_candidate(self) -> None:
        """Increments the term and switches state to Candidate, voting for itself immediately."""
        self.node_state = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        self.election_timeout = random.uniform(150.0, 300.0) # Reset jitter to prevent split votes
        self.last_heartbeat_timestamp = time.time() * 1000.0
        print(f"[ELECTION-CORE] Node {self.node_id} turned CANDIDATE. Initiating Term {self.current_term}.")

    def handle_request_vote_rpc(self, candidate_id: str, candidate_term: int) -> bool:
        """Processes incoming vote requests, granting a vote if the incoming term is greater."""
        # Rule 1: Reject votes if the candidate's term is older than our local term
        if candidate_term < self.current_term:
            return False
            
        # Rule 2: If the term is strictly greater, step down to a follower state immediately
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.node_state = "FOLLOWER"
            self.voted_for = None

        # Rule 3: Grant the vote if we haven't voted for anyone else in this term yet
        if self.voted_for is None or self.voted_for == candidate_id:
            self.voted_for = candidate_id
            self.last_heartbeat_timestamp = time.time() * 1000.0 # Reset election timer on vote grant
            return True
            
        return False

    def achieve_leadership(self) -> None:
        """Transitions the node to the Leader state upon winning a majority vote."""
        if self.node_state == "CANDIDATE":
            self.node_state = "LEADER"
            print(f"[ELECTION-CORE] Node {self.node_id} successfully secured majority. Cluster LEADER for Term {self.current_term}.")


if __name__ == "__main__":
    cluster = ["node_alpha", "node_beta", "node_gamma"]
    print("[ELECTION-CORE] Spinning up cluster nodes and initializing randomized election intervals...")
    node = RaftNodeElectionCore("node_alpha", cluster)
    
    # Simulate a network timeout event
    time.sleep(0.3)
    if node.check_election_timeout():
        # Mock voting simulation: solicit votes from peer nodes
        votes_received = 1 # Self vote
        for peer in node.peers:
            # Simulate peer granting a vote for the current term
            if random.choice([True, False]):
                votes_received += 1
                
        print(f"[ELECTION-CORE] Votes gathered: {votes_received}/{len(cluster)}")
        if votes_received >= (len(cluster) // 2) + 1:
            node.achieve_leadership()