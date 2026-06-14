"""
Core Topic: Raft Pre-Vote Safety Phase
Description: Implements a Pre-Vote check phase to keep isolated nodes from increasing terms.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class PreVoteConsensusNode:
    """Runs a pre-vote check before an election to verify if it can reach a cluster majority."""
    
    def __init__(self, node_id: str, total_cluster_size: int) -> None:
        self.node_id = node_id
        self.current_term = 1
        self.cluster_size = total_cluster_size

    def evaluate_pre_vote_feasibility(self, active_reachable_peers: List[str]) -> bool:
        """Determines if the node can collect enough pre-votes to safely start a real election."""
        # The node automatically votes for itself in the pre-vote phase
        pre_votes_secured = 1 + len([p for p in active_reachable_peers if p != self.node_id])
        quorum_needed = (self.cluster_size // 2) + 1
        
        if pre_votes_secured >= quorum_needed:
            print(f"[PRE-VOTE] Node '{self.node_id}' reached quorum. Safe to trigger a real election and increment term.")
            return True
        
        print(f"[PRE-VOTE] Node '{self.node_id}' failed quorum check ({pre_votes_secured}/{quorum_needed}). Staying follower.")
        return False


if __name__ == "__main__":
    # Simulate an isolated node cut off in a minority partition of a 5-node cluster
    isolated_node = PreVoteConsensusNode("node-isolated-E", total_cluster_size=5)
    
    # Node E can only see itself due to the partition
    safe_to_elect = isolated_node.evaluate_pre_vote_feasibility(active_reachable_peers=[])
    print(f" -> Resulting execution path decision state: Trigger Election = {safe_to_elect}")