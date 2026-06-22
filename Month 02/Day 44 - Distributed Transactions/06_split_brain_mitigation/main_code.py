"""
Core Topic: Network Partition Split-Brain Mitigation
Description: Validates active node consensus requirements before approving transaction scopes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class NetworkClusterPartition:
    def __init__(self, node_count: int) -> None:
        self.node_count = node_count
        self.minimum_quorum = (node_count // 2) + 1

    def validate_quorum_slice(self, visible_nodes: int) -> bool:
        """Blocks network operations if the active node group drops below the majority quorum."""
        is_valid = visible_nodes >= self.minimum_quorum
        print(f"[QUORUM-CHECK] Visible Nodes: {visible_nodes}/{self.node_count} | Allowed to run? -> {is_valid}")
        return is_valid


if __name__ == "__main__":
    cluster = NetworkClusterPartition(node_count=5) # Quorum majority required = 3
    assert cluster.validate_quorum_slice(visible_nodes=4) == True
    assert cluster.validate_quorum_slice(visible_nodes=2) == False # Isolate split segments