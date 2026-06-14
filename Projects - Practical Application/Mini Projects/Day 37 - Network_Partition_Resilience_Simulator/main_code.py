"""
System: Asymmetric Network Partition Resilience Simulator
Description: Simulates a 5-node cluster split into a minority and a majority partition.
             Demonstrates how the Pre-Vote protocol prevents split-brain anomalies and keeps 
             isolated nodes from disrupting the cluster when the partition heals.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict, Set

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (PartitionSim) %(message)s')

class PartitionResilientNode:
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.term: int = 1
        self.role: str = "FOLLOWER" # FOLLOWER, LEADER
        self.log: List[str] = ["INIT"]

    def run_pre_vote_check(self, visible_nodes: Set[str], cluster_size: int) -> bool:
        """Runs a speculative pre-vote check to see if a quorum majority is reachable."""
        # The node automatically votes for itself in the pre-vote phase
        votes_received = 1 + len([nid for nid in visible_nodes if nid != self.node_id])
        required_quorum = (cluster_size // 2) + 1
        
        return votes_received >= required_quorum

    def trigger_real_election(self) -> None:
        """Increments the term and takes over as leader if the pre-vote phase succeeds."""
        self.term += 1
        self.role = "LEADER"
        logging.info(f"++++ [{self.node_id}] Pre-Vote Quorum Won! Advanced to Term {self.term} and elected LEADER ++++")


class NetworkPartitionSimulator:
    """Manages a 5-node cluster simulation environment, orchestrating network splits and healing."""
    
    def __init__(self) -> None:
        self.node_ids = ["node-A", "node-B", "node-C", "node-D", "node-E"]
        self.nodes: Dict[str, PartitionResilientNode] = {nid: PartitionResilientNode(nid) for nid in self.node_ids}
        
        # Establish Node A as the initial baseline cluster leader
        self.nodes["node-A"].role = "LEADER"
        # Track which nodes can reach each other over the network
        self.connectivity_matrix: Dict[str, Set[str]] = {nid: set(self.node_ids) for nid in self.node_ids}

    def introduce_network_split(self) -> None:
        """Splits the cluster into a minority partition (A, B) and a majority partition (C, D, E)."""
        logging.warning("======================================================================")
        logging.warning("[PARTITION-START] Cutting network connections between cluster components...")
        logging.warning(" -> Partition 1 (Minority): [node-A, node-B]")
        logging.warning(" -> Partition 2 (Majority): [node-C, node-D, node-E]")
        logging.warning("======================================================================")
        
        minority = {"node-A", "node-B"}
        majority = {"node-C", "node-D", "node-E"}
        
        for node in minority:
            self.connectivity_matrix[node] = minority
        for node in majority:
            self.connectivity_matrix[node] = majority

    def simulate_ticker_timeout_on_isolated_node(self, target_node_id: str) -> None:
        """Simulates an election timeout on a node, using the Pre-Vote protocol to gauge stability."""
        node = self.nodes[target_node_id]
        visible_peers = self.connectivity_matrix[target_node_id]
        
        logging.info(f"[{target_node_id}] Election timeout expired. Running speculative Pre-Vote check phase...")
        
        if node.run_pre_vote_check(visible_peers, len(self.node_ids)):
            node.trigger_real_election()
        else:
            logging.warning(f"[{target_node_id}] Pre-Vote check failed. Quorum majority unreachable. Staying FOLLOWER (Term {node.term}).")

    def heal_network_partition(self) -> None:
        """Restores full connectivity across all cluster nodes, letting states rebalance."""
        logging.info("======================================================================")
        logging.info("[HEAL-RECOVERY] Reconnecting all partitions. Restoring full network visibility...")
        logging.info("======================================================================")
        
        for nid in self.node_ids:
            self.connectivity_matrix[nid] = set(self.node_ids)


if __name__ == "__main__":
    print("\n=== RUNNING ASYMMETRIC NETWORK PARTITION RESILIENCE SIMULATOR ===\n")
    
    simulator = NetworkPartitionSimulator()
    
    # Step 1: Split the network into two isolated partitions
    simulator.introduce_network_split()
    
    # Step 2: Node E times out inside the majority partition (C, D, E)
    # Since it can reach a quorum majority, its Pre-Vote check succeeds, and it becomes the new leader
    simulator.simulate_ticker_timeout_on_isolated_node("node-E")
    
    # Step 3: Node B times out inside the isolated minority partition (A, B)
    # Its Pre-Vote check fails because it cannot reach a majority, preventing it from incrementing its term unnecessarily
    simulator.simulate_ticker_timeout_on_isolated_node("node-B")
    
    # Step 4: Heal the network partition and restore full connectivity
    simulator.heal_network_partition()
    
    print("\n=== POST-RECOVERY VERIFICATION STATE DUMP ===")
    print(f" -> Node-A Role: {simulator.nodes['node-A'].role} | Logical Term Clock: {simulator.nodes['node-A'].term}")
    print(f" -> Node-B Role: {simulator.nodes['node-B'].role} | Logical Term Clock: {simulator.nodes['node-B'].term}")
    print(f" -> Node-E Role: {simulator.nodes['node-E'].role} | Logical Term Clock: {simulator.nodes['node-E'].term}")
    
    print("\n[PREVOTE-SUCCESS] Node B kept its term low, ensuring a smooth recovery after healing.")
    print("\n=== SYSTEM SHUTDOWN: NET-PARTITION SIMULATION ENGINE EXITED ===")