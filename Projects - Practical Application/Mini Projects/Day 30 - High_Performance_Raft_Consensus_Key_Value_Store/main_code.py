"""
System: Distributed Fault-Tolerant Raft Consensus Key-Value Storage Engine
Description: A functional, single-process multi-node simulation of Raft Consensus State Machines,
             handling leader election, log replication, and key-value state execution.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import random
import logging
from typing import List, Dict, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (RaftKV-Hub) %(message)s')

class SimulatedRaftNode:
    """Simulates a single Raft node running inside a cluster network configuration."""
    
    def __init__(self, node_id: str, peers: List[str]) -> None:
        self.node_id: str = node_id
        self.peers: List[str] = peers
        
        # State indicators
        self.role: str = "FOLLOWER" # FOLLOWER, CANDIDATE, LEADER
        self.current_term: int = 0
        self.voted_for: Optional[str] = None
        
        # Log management structures: tracking elements as (term, command)
        self.log_history: List[Tuple[int, str]] = [(0, "NO_OP")]
        self.commit_index: int = 0
        self.last_applied: int = 0
        self.state_machine: Dict[str, str] = {}
        
        # Track follower log updates (used exclusively by the leader)
        self.next_index_map: Dict[str, int] = {}
        self.match_index_map: Dict[str, int] = {}

    def process_heartbeat(self, leader_id: str, term: int, leader_commit: int) -> bool:
        """Processes an incoming keep-alive signal from the leader."""
        if term >= self.current_term:
            self.current_term = term
            self.role = "FOLLOWER"
            self.voted_for = None
            
            if leader_commit > self.commit_index:
                self.commit_index = min(leader_commit, len(self.log_history) - 1)
                self._apply_committed_logs()
            return True
        return False

    def solicit_votes(self) -> bool:
        """Triggers an election phase, gathering votes from available peers."""
        self.role = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1 # Vote for self
        
        logging.info(f"Node '{self.node_id}' initiated election for Term {self.current_term}.")
        return votes >= (len(self.peers) + 1) // 2 + 1

    def append_entries_replication(self, term: int, prev_idx: int, prev_term: int, entries: List[Tuple[int, str]]) -> bool:
        """Validates and replicates data entries sent by the leader."""
        if term < self.current_term:
            return False
            
        if prev_idx >= len(self.log_history) or self.log_history[prev_idx][0] != prev_term:
            return False

        # Clear out conflicts and append new entries safely
        self.log_history = self.log_history[:prev_idx + 1] + entries
        return True

    def configure_as_leader(self) -> None:
        """Initializes tracking maps when this node wins the election and becomes the leader."""
        self.role = "LEADER"
        for peer in self.peers:
            self.next_index_map[peer] = len(self.log_history)
            self.match_index_map[peer] = 0
        logging.info(f"Node '{self.node_id}' secured consensus. State upgraded to cluster LEADER.")

    def _apply_committed_logs(self) -> None:
        """Applies committed log entries to the local key-value state machine."""
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            cmd = self.log_history[self.last_applied][1]
            if cmd.startswith("SET "):
                k, v = cmd[4:].split("=")
                self.state_machine[k.strip()] = v.strip()


class LocalClusterCoordinator:
    """Coordinates message routing and node actions within the simulated cluster environment."""
    
    def __init__(self) -> None:
        self.nodes_map: Dict[str, SimulatedRaftNode] = {}
        names = ["alpha", "beta", "gamma"]
        
        for name in names:
            peers_list = [p for p in names if p != name]
            self.nodes_map[name] = SimulatedRaftNode(name, peers_list)

    def execute_cluster_write(self, client_command: str) -> bool:
        """Routes write requests to the leader node, which replicates updates across the cluster."""
        # Locate the active cluster leader node
        leader_node = next((n for n in self.nodes_map.values() if n.role == "LEADER"), None)
        if not leader_node:
            logging.error("Write failed: No active leader found in the cluster.")
            return False

        logging.info(f"Leader received command: '{client_command}'. Replicating entries across followers...")
        new_entry = (leader_node.current_term, client_command)
        prev_idx = len(leader_node.log_history) - 1
        prev_term = leader_node.log_history[prev_idx][0]
        
        leader_node.log_history.append(new_entry)
        match_count = 1 # Count the leader's local append

        # Replicate entries to follower nodes
        for peer_id in leader_node.peers:
            follower = self.nodes_map[peer_id]
            if follower.append_entries_replication(leader_node.current_term, prev_idx, prev_term, [new_entry]):
                match_count += 1
                leader_node.match_index_map[peer_id] = len(leader_node.log_history) - 1

        # Commit changes once a majority of nodes have replicated the entry
        if match_count >= (len(self.nodes_map) // 2) + 1:
            leader_node.commit_index = len(leader_node.log_history) - 1
            leader_node._apply_committed_logs()
            
            # Update follower commit indexes via a heartbeat broadcast pass
            for peer_id in leader_node.peers:
                self.nodes_map[peer_id].process_heartbeat(leader_node.node_id, leader_node.current_term, leader_node.commit_index)
            return True
            
        return False


if __name__ == "__main__":
    print("\n=== SYSTEM START: HIGH-PERFORMANCE RAFT STORAGE SIMULATION ===\n")
    orchestrator = LocalClusterCoordinator()

    # Simulate an election where 'alpha' assumes cluster leadership
    node_alpha = orchestrator.nodes_map["alpha"]
    if node_alpha.solicit_votes():
        node_alpha.configure_as_leader()

    # Execute a write transaction through the cluster manager
    success = orchestrator.execute_cluster_write("SET developer_token = saad_se_2026")
    print(f"\n[WRITE COMPLETE] Consensus confirmation status flag: {success}")
    print(f" -> Leader (alpha) State Store: {orchestrator.nodes_map['alpha'].state_machine}")
    print(f" -> Follower (beta) State Store: {orchestrator.nodes_map['beta'].state_machine}")
    print("\n=== SYSTEM SHUTDOWN: RAFT STORE WORKSPACE TERMINATED ===")