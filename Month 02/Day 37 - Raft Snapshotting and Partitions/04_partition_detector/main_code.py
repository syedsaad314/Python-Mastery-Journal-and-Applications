"""
Core Topic: Network Partition Connectivity Matrix
Description: Models an asymmetric cluster network topology, tracking connection cuts between components.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List, Set

class NetworkPartitionMatrix:
    """Manages connection routing rules across cluster nodes to simulate network splits."""
    
    def __init__(self, nodes: List[str]) -> None:
        self.all_nodes = nodes
        # Maps each node to the set of peers it can actively reach over the network
        self.reachability_registry: Dict[str, Set[str]] = {nid: set(nodes) for nid in nodes}

    def introduce_asymmetric_split(self, minority_partition: List[str], majority_partition: List[str]) -> None:
        """Cuts network connections between two groups of nodes, creating a partition."""
        for m_node in minority_partition:
            self.reachability_registry[m_node] = set(minority_partition)
        for maj_node in majority_partition:
            self.reachability_registry[maj_node] = set(majority_partition)

    def verify_direct_reachability(self, sender: str, receiver: str) -> bool:
        """Checks if a network packet can travel directly between two nodes."""
        return receiver in self.reachability_registry[sender]


if __name__ == "__main__":
    cluster_nodes = ["node-A", "node-B", "node-C", "node-D", "node-E"]
    network = NetworkPartitionMatrix(cluster_nodes)
    
    # Isolate node-A and node-B into a minority partition
    network.introduce_asymmetric_split(minority_partition=["node-A", "node-B"], majority_partition=["node-C", "node-D", "node-E"])
    
    can_a_reach_b = network.verify_direct_reachability("node-A", "node-B")
    can_a_reach_c = network.verify_direct_reachability("node-A", "node-C")
    
    print(f"[PARTITION] Can Node A talk to Node B inside its partition? {can_a_reach_b}")
    print(f"[PARTITION] Can Node A talk to Node C across the network split? {can_a_reach_c}")