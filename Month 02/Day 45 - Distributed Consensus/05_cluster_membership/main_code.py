"""
Core Topic: Dynamic Cluster Membership Tracking
Description: Tracks cluster node configurations dynamically to support membership updates safely.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Set

class ClusterMembershipRegistry:
    def __init__(self, initial_members: Set[str]) -> None:
        self.active_member_pool = initial_members

    def add_node_to_cluster(self, new_node_id: str) -> None:
        self.active_member_pool.add(new_node_id)
        print(f"[MEMBERSHIP] Registered new node identity '{new_node_id}' into consensus configuration.")

    def calculate_majority_quorum_limit(self) -> int:
        return (len(self.active_member_pool) // 2) + 1


if __name__ == "__main__":
    registry = ClusterMembershipRegistry({"node_a", "node_b", "node_c"})
    assert registry.calculate_majority_quorum_limit() == 2
    
    registry.add_node_to_cluster("node_d") # Scale cluster size up dynamically
    assert registry.calculate_majority_quorum_limit() == 3