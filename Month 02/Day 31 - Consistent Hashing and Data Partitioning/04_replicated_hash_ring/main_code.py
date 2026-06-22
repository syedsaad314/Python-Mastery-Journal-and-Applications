"""
Core Topic: Replicated Consistent Hash Ring
Description: Routes data keys to primary nodes and returns the next N distinct nodes for replication.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
import bisect
from typing import List, Optional

class ReplicatedHashRing:
    """Tracks and returns a chain of unique physical nodes to handle replicated data writes."""
    
    def __init__(self, physical_nodes: List[str], vnode_count: int = 50) -> None:
        self.vnode_count = vnode_count
        self.ring_positions: List[int] = []
        self.position_to_node_map: dict[int, str] = {}
        
        for node in physical_nodes:
            self.add_node(node)

    def _compute_hash(self, key: str) -> int:
        return int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16) & 0xFFFFFFFF

    def add_node(self, node: str) -> None:
        for i in range(self.vnode_count):
            position = self._compute_hash(f"{node}-vnode-{i}")
            if position not in self.position_to_node_map:
                bisect.insort(self.ring_positions, position)
                self.position_to_node_map[position] = node

    def get_replication_chain(self, key: str, replication_factor: int) -> List[str]:
        """Returns the first N distinct physical nodes found by walking clockwise from the key's hash position."""
        if not self.ring_positions:
            return []
            
        key_hash = self._compute_hash(key)
        start_idx = bisect.bisect_right(self.ring_positions, key_hash)
        
        replication_chain: List[str] = []
        current_idx = start_idx
        
        # Walk clockwise around the ring until we find enough distinct physical nodes
        while len(replication_chain) < replication_factor:
            if current_idx >= len(self.ring_positions):
                current_idx = 0 # Wrap around to the start of the ring
                
            target_node = self.position_to_node_map[self.ring_positions[current_idx]]
            if target_node not in replication_chain:
                replication_chain.append(target_node)
                
            current_idx += 1
            # Break if we've inspected the entire ring to avoid infinite loops
            if current_idx == start_idx and len(replication_chain) < replication_factor:
                break
                
        return replication_chain


if __name__ == "__main__":
    cluster = ["west_dc_0", "east_dc_1", "asia_dc_2", "eu_dc_3"]
    r_ring = ReplicatedHashRing(cluster, vnode_count=50)
    
    target_key = "user_profile_data_payload_101"
    # Find a primary node and 2 backup nodes
    chain = r_ring.get_replication_chain(target_key, replication_factor=3)
    print(f"[REPLICATED-RING] Target Key: '{target_key}'")
    print(f" -> Preference List Replication Chain: {chain}")