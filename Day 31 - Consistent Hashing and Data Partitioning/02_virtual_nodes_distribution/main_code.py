"""
Core Topic: Virtual Nodes (VNodes) Distribution
Description: Extends the hash ring with virtual nodes to ensure keys are evenly distributed across servers.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
import bisect
from typing import List, Dict, Optional

class VirtualNodeHashRing:
    """Implements consistent hashing with virtual nodes to balance cluster workloads."""
    
    def __init__(self, physical_nodes: Optional[List[str]] = None, vnode_count: int = 100) -> None:
        self.vnode_count: int = vnode_count
        self.ring_positions: List[int] = []
        self.position_to_node_map: Dict[int, str] = {}
        
        if physical_nodes:
            for node in physical_nodes:
                self.add_node(node)

    def _compute_hash(self, key: str) -> int:
        digest = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return int(digest, 16) & 0xFFFFFFFF

    def add_node(self, physical_node: str) -> None:
        """Generates multiple virtual positions for a single physical node to distribute it across the ring."""
        for i in range(self.vnode_count):
            vnode_token = f"{physical_node}-vnode-{i}"
            position = self._compute_hash(vnode_token)
            
            if position not in self.position_to_node_map:
                bisect.insort(self.ring_positions, position)
                self.position_to_node_map[position] = physical_node

    def remove_node(self, physical_node: str) -> None:
        """Removes all virtual nodes associated with a physical server from the ring."""
        for i in range(self.vnode_count):
            vnode_token = f"{physical_node}-vnode-{i}"
            position = self._compute_hash(vnode_token)
            if position in self.position_to_node_map:
                self.ring_positions.remove(position)
                del self.position_to_node_map[position]

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring_positions:
            return None
            
        key_hash = self._compute_hash(key)
        idx = bisect.bisect_right(self.ring_positions, key_hash)
        if idx == len(self.ring_positions):
            idx = 0
        return self.position_to_node_map[self.ring_positions[idx]]


if __name__ == "__main__":
    servers = ["node_alpha", "node_beta"]
    # Initialize with 150 vnodes per physical server
    vring = VirtualNodeHashRing(servers, vnode_count=150)
    
    # Track distribution metrics across a pool of test keys
    distribution_audit: Dict[str, int] = {"node_alpha": 0, "node_beta": 0}
    for item_id in range(1000):
        target_node = vring.get_node(f"item_payload_key_{item_id}")
        if target_node:
            distribution_audit[target_node] += 1
            
    print(f"[VNODE-RING] Allocation metrics across 1000 items: {distribution_audit}")