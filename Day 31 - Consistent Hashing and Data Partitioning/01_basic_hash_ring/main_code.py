"""
Core Topic: Basic Consistent Hashing Ring
Description: Implements a straightforward hash ring using MD5 to map keys to physical nodes.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
import bisect
from typing import List, Optional

class BasicHashRing:
    """Manages a collection of physical servers mapped onto a continuous 32-bit hash space ring."""
    
    def __init__(self, physical_nodes: Optional[List[str]] = None) -> None:
        self.ring_positions: List[int] = []
        self.position_to_node_map: dict[int, str] = {}
        
        if physical_nodes:
            for node in physical_nodes:
                self.add_node(node)

    def _compute_hash(self, key: str) -> int:
        """Generates an integer hash value in the range [0, 2^32 - 1] using MD5."""
        digest = hashlib.md5(key.encode('utf-8')).hexdigest()
        return int(digest, 16) & 0xFFFFFFFF

    def add_node(self, node: str) -> None:
        """Hashes a physical node ID and inserts it into its designated position on the ring."""
        position = self._compute_hash(node)
        if position not in self.position_to_node_map:
            bisect.insort(self.ring_positions, position)
            self.position_to_node_map[position] = node

    def remove_node(self, node: str) -> None:
        """Removes a physical node from the cluster ring topology."""
        position = self._compute_hash(node)
        if position in self.position_to_node_map:
            self.ring_positions.remove(position)
            del self.position_to_node_map[position]

    def get_node(self, key: str) -> Optional[str]:
        """Routes a lookup key to the nearest clockwise server node on the ring."""
        if not self.ring_positions:
            return None
            
        key_hash = self._compute_hash(key)
        # Binary search to locate the first node position >= key_hash
        idx = bisect.bisect_right(self.ring_positions, key_hash)
        
        # If the hash falls past the last node, wrap around to the first node (index 0)
        if idx == len(self.ring_positions):
            idx = 0
            
        return self.position_to_node_map[self.ring_positions[idx]]


if __name__ == "__main__":
    cluster_nodes = ["server_node_1", "server_node_2", "server_node_3"]
    ring = BasicHashRing(cluster_nodes)
    
    test_keys = ["user_session_9921", "image_blob_uuid", "telemetry_metrics_payload"]
    print("[BASIC-RING] Routing client data keys across available cluster topology...")
    for k in test_keys:
        target = ring.get_node(k)
        print(f" -> Key '{k}' hashes to node: {target}")