# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Quorum Heartbeat Verification
Description: Forces a leader node to successfully communicate with a majority quorum 
             before responding to linearizable read operations.
"""
from typing import List

class QuorumHeartbeatVerifier:
    def __init__(self, cluster_nodes: List[str]) -> None:
        self.cluster_nodes = cluster_nodes
        self.quorum_size = (len(cluster_nodes) // 2) + 1

    def verify_leadership_quorum(self, successful_responses: List[str]) -> bool:
        # Evaluate if the active responses cross the strict majority threshold line
        valid_acks = [node for node in successful_responses if node in self.cluster_nodes]
        has_quorum = len(valid_acks) >= self.quorum_size
        print(f"[QUORUM] Acks gathered: {len(valid_acks)}/{len(self.cluster_nodes)}. Quorum met: {has_quorum}")
        return has_quorum

if __name__ == "__main__":
    nodes = ["node_A", "node_B", "node_C", "node_D", "node_E"]
    verifier = QuorumHeartbeatVerifier(nodes)
    
    # Assert successful quorum validation pass
    assert verifier.verify_leadership_quorum(["node_A", "node_B", "node_C"]) == True
    # Assert failure when isolated via partition gaps
    assert verifier.verify_leadership_quorum(["node_A", "node_B"]) == False