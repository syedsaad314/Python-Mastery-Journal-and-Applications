"""
System: Raft Leader Election Core Engine
Description: A production-grade implementation of the Raft leader election state machine.
             Features role transitions, term validation, randomized election timers, 
             and strict quorum verification to prevent concurrent leaders.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import random
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Raft-Core) %(message)s')

class RaftClusterNode:
    """An independent Raft consensus node managing terms, state transitions, and timers."""
    
    def __init__(self, node_id: str, all_node_ids: List[str]) -> None:
        self.node_id: str = node_id
        self.cluster_members: List[str] = all_node_ids
        self.current_term: int = 0
        self.voted_for: Optional[str] = None
        self.role: str = "FOLLOWER" # FOLLOWER, CANDIDATE, LEADER
        
        # Configuration for randomized election timeouts (150ms to 300ms)
        self.min_timeout_ms: int = 150
        self.max_timeout_ms: int = 300
        self.election_timeout: float = self._reset_election_timer()
        self.last_heartbeat_time: float = time.time()

    def _reset_election_timer(self) -> float:
        """Generates a new randomized timeout value in seconds."""
        return random.randint(self.min_timeout_ms, self.max_timeout_ms) / 1000.0

    def step_down_to_follower(self, term: int) -> None:
        """Reverts the node back to a follower state if a higher term is discovered."""
        self.role = "FOLLOWER"
        self.current_term = term
        self.voted_for = None
        self.last_heartbeat_time = time.time()

    def handle_heartbeat(self, leader_id: str, leader_term: int) -> bool:
        """Processes an incoming heartbeat from the leader."""
        if leader_term < self.current_term:
            logging.warning(f"[{self.node_id}] Rejected heartbeat from stale leader '{leader_id}' (Term {leader_term} < Local {self.current_term})")
            return False

        if leader_term > self.current_term:
            logging.info(f"[{self.node_id}] Discovered higher term from leader '{leader_id}'. Updating term count.")
            self.step_down_to_follower(leader_term)
            
        self.last_heartbeat_time = time.time()
        if self.role != "FOLLOWER":
            self.role = "FOLLOWER"
            self.voted_for = None
            
        return True

    def handle_request_vote(self, candidate_id: str, candidate_term: int) -> bool:
        """Evaluates whether to grant a vote to a candidate."""
        if candidate_term < self.current_term:
            return False

        if candidate_term > self.current_term:
            self.step_down_to_follower(candidate_term)

        # Grant the vote if the node hasn't voted yet or has already voted for this candidate
        if self.voted_for is None or self.voted_for == candidate_id:
            self.voted_for = candidate_id
            self.last_heartbeat_time = time.time() # Reset election timer on vote grant
            logging.info(f"[{self.node_id}] Granted vote to candidate '{candidate_id}' for Term {candidate_term}")
            return True

        return False

    def initiate_election(self) -> Dict[str, Any]: # type: ignore
        """Transitions the node to a candidate and sets up election parameters."""
        self.role = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id # Vote for self
        self.last_heartbeat_time = time.time()
        self.election_timeout = self._reset_election_timer()
        
        logging.info(f"====== [{self.node_id}] Initiated Election Loop for Term {self.current_term} ======")
        return {
            "candidate_id": self.node_id,
            "term": self.current_term
        }


if __name__ == "__main__":
    print("\n=== INITIALIZING RAFT LEADER ELECTION STATE ENGINE ===\n")
    
    cluster_layout = ["node_1", "node_2", "node_3"]
    
    # Initialize separate node instances
    node1 = RaftClusterNode("node_1", cluster_layout)
    node2 = RaftClusterNode("node_2", cluster_layout)
    node3 = RaftClusterNode("node_3", cluster_layout)
    
    # Simulate node 1 timing out first due to its randomized timer
    election_rpc = node1.initiate_election()
    
    # Send vote requests to peer nodes
    vote_granted_n2 = node2.handle_request_vote(election_rpc["candidate_id"], election_rpc["term"])
    vote_granted_n3 = node3.handle_request_vote(election_rpc["candidate_id"], election_rpc["term"])
    
    # Collect and count votes
    total_votes = 1 # Starts with 1 because node 1 voted for itself
    if vote_granted_n2: total_votes += 1
    if vote_granted_n3: total_votes += 1
    
    quorum_limit = (len(cluster_layout) // 2) + 1
    logging.info(f"[ELECTION-POOL] Votes collected: {total_votes}/{len(cluster_layout)} (Quorum required: {quorum_limit})")
    
    if total_votes >= quorum_limit:
        node1.role = "LEADER"
        logging.info(f"[{node1.node_id}] Successfully elected as cluster leader for Term {node1.current_term}.")
        
        # Leader begins broadcasting heartbeats to maintain authority
        print("\n[LEADER-HEARTBEAT] Broadcasting heartbeats to followers...")
        node2.handle_heartbeat(node1.node_id, node1.current_term)
        node3.handle_heartbeat(node1.node_id, node1.current_term)
        
    print("\n=== SYSTEM SHUTDOWN: RAFT ENGINE CONTAINER EXITED ===")