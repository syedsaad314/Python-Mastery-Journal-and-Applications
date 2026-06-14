"""
Core Topic: Quorum Commit Index Computation
Description: Simulates a leader tracking follower indices to find the highest committed entry.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List

class QuorumCommitTracker:
    """Computes the highest log index replicated to a majority of cluster nodes."""
    
    def __init__(self, cluster_node_ids: List[str]) -> None:
        self.node_ids = cluster_node_ids
        # Track the highest log index known to be replicated on each peer node
        self.match_index_table: Dict[str, int] = {nid: 0 for nid in cluster_node_ids}

    def update_peer_match_index(self, node_id: str, verified_index: int) -> None:
        self.match_index_table[node_id] = verified_index

    def compute_highest_majority_commit_index(self, leader_id: str, leader_current_log_index: int) -> int:
        """Finds the maximum index replicated to a cluster majority."""
        self.match_index_table[leader_id] = leader_current_log_index
        
        all_indices = sorted(list(self.match_index_table.values()))
        # In a sorted list of match indices, the median value represents the highest index achieved by a majority quorum
        mid_point = len(all_indices) // 2
        majority_index = all_indices[mid_point]
        
        return majority_index


if __name__ == "__main__":
    # Simulate a 5-node cluster infrastructure
    nodes = ["node-A", "node-B", "node-C", "node-D", "node-E"]
    tracker = QuorumCommitTracker(nodes)
    
    # Leader node-A has logs up to index 5
    # Followers acknowledge successful replication up to various points
    tracker.update_peer_match_index("node-B", 5)
    tracker.update_peer_match_index("node-C", 5)
    tracker.update_peer_match_index("node-D", 2) # Slow or lagging node
    tracker.update_peer_match_index("node-E", 1) # Severely delayed node
    
    committed_idx = tracker.compute_highest_majority_commit_index("node-A", leader_current_log_index=5)
    print(f"[QUORUM-COMMIT] Calculated cluster majority commit index line boundary: {committed_idx}")