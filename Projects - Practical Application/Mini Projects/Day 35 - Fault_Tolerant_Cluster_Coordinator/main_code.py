"""
System: Fault-Tolerant Raft Cluster Coordinator
Description: Simulates an active 5-node cluster, demonstrating how the system 
             handles a leader crash and uses consensus quorums to recover safely.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (ClusterCoord) %(message)s')

class MockRaftPeer:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.term = 1
        self.is_alive = True

    def vote_rpc(self, candidate_id: str, candidate_term: int) -> bool:
        if not self.is_alive or candidate_term <= self.term:
            return False
        self.term = candidate_term
        return True


class FaultTolerantClusterCoordinator:
    """Simulates cluster behavior, managing node failures and tracking election recovery."""
    
    def __init__(self, node_list: List[str]) -> None:
        self.nodes: Dict[str, MockRaftPeer] = {nid: MockRaftPeer(nid) for nid in node_list}
        self.active_leader: str = "node-A"
        logging.info(f"Cluster initialized. Active Leader: '{self.active_leader}' across 5 nodes.")

    def simulate_leader_crash(self) -> None:
        """Simulates a hard crash on the active leader node."""
        logging.warning(f"[CRASH-SIMULATION] Active leader node '{self.active_leader}' has crashed!")
        self.nodes[self.active_leader].is_alive = False
        self.active_leader = "NONE"

    def orchestrate_emergency_election(self, candidate_id: str) -> bool:
        """Triggers an emergency election to replace a crashed leader."""
        logging.info(f"[RECOVERY-LOOP] Node '{candidate_id}' detected heartbeat timeout. Starting emergency election...")
        
        candidate_node = self.nodes[candidate_id]
        candidate_node.term += 1 # Increment term count for the new election
        
        votes_received = 1 # Candidate votes for itself
        cluster_size = len(self.nodes)
        quorum_target = (cluster_size // 2) + 1
        
        for nid, peer_node in self.nodes.items():
            if nid != candidate_id:
                if peer_node.vote_rpc(candidate_id, candidate_node.term):
                    votes_received += 1

        logging.info(f"[RECOVERY-LOOP] Election completed. Votes collected: {votes_received}/{cluster_size}")
        
        if votes_received >= quorum_target:
            self.active_leader = candidate_id
            logging.info(f"[CONSENSUS-SUCCESS] New leader successfully elected: '{self.active_leader}' (Term {candidate_node.term})")
            return True
            
        logging.error("[CONSENSUS-FAILURE] Election failed to secure a quorum majority.")
        return False


if __name__ == "__main__":
    print("\n=== SYSTEM START: FAULT-TOLERANT CLUSTER COORDINATOR ===\n")
    
    # Set up a standard 5-node production cluster layout
    production_nodes = ["node-A", "node-B", "node-C", "node-D", "node-E"]
    cluster = FaultTolerantClusterCoordinator(production_nodes)
    
    # Step 1: Simulate a leader crash scenario
    cluster.simulate_leader_crash()
    
    # Step 2: Node B times out first and tries to run an emergency election
    election_outcome = cluster.orchestrate_emergency_election(candidate_id="node-B")
    
    print(f"\n[POST-RECOVERY] Verification Check: Current Cluster Leader = '{cluster.active_leader}'")
    print("\n=== SYSTEM SHUTDOWN: CLUSTER SIMULATION WORKLOAD EXITED ===")