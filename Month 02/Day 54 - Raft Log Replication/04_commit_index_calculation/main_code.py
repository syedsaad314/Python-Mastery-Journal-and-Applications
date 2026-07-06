# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Commit Index Consensus Calculus
Description: Determines whether a log entry has been successfully replicated 
             across a majority of cluster nodes to update the commit threshold.
"""
from typing import Dict

class CommitCalculator:
    @staticmethod
    def calculate_new_commit_index(match_indices: Dict[str, int], current_commit: int, total_nodes: int) -> int:
        # Extract and sort all matching index values across the cluster
        all_indices = sorted(list(match_indices.values()))
        majority_idx = total_nodes // 2
        
        # The index at this boundary represents the highest value agreed upon by a majority
        median_replicated = all_indices[majority_idx]
        
        if median_replicated > current_commit:
            return median_replicated
        return current_commit

if __name__ == "__main__":
    # Cluster of 3 nodes: Leader is node_1 at index 3. Peers are at index 3 and index 1.
    peer_matches = {"node_1": 3, "node_2": 3, "node_3": 1}
    new_commit = CommitCalculator.calculate_new_commit_index(peer_matches, current_commit=1, total_nodes=3)
    assert new_commit == 3