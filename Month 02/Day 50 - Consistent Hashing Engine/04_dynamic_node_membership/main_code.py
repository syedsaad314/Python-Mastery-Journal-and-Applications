# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Dynamic Node Membership
Description: Adds and removes cluster nodes dynamically while ensuring minimal 
             key disruption across the remaining cluster topology.
"""
from typing import List, Tuple

class DynamicNodeMembership:
    def __init__(self) -> None:
        self.ring: List[Tuple[int, str]] = []

    def remove_physical_node(self, node_id: str) -> None:
        # Clear out all tokens associated with the target physical node
        self.ring = [item for item in self.ring if item[1] != node_id]
        print(f"[MEMBERSHIP] Evicted node '{node_id}' from topology ring configurations.")

if __name__ == "__main__":
    membership = DynamicNodeMembership()
    self_ring = membership.ring
    self_ring.append((10, "node_A"))
    self_ring.append((20, "node_B"))
    membership.remove_physical_node("node_A")
    assert len(membership.ring) == 1
    assert membership.ring[0][1] == "node_B"