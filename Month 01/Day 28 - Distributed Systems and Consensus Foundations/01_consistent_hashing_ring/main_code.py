"""
Core Topic: Consistent Hashing Ring with Virtual Nodes
Description: Implements load distribution rings to bound key remapping overhead under node mutation churn.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
from typing import List, Dict, Optional, Tuple

class ConsistentHashRing:
    """Balances transactional key distribution paths across an array of logical backing nodes."""
    
    def __init__(self, replicas_count: int = 3) -> None:
        self.replicas: int = replicas_count
        # Maps absolute ring hash positions to physical node descriptor strings
        self.ring_positions: List[int] = []
        self.hash_to_node_map: Dict[int, str] = {}

    def _compute_md5_hash_integer(self, key_string: str) -> int:
        """Generates a uniform 32-bit integer coordinate projection over the hashing circle."""
        digest = hashlib.md5(key_string.encode('utf-8')).hexdigest()
        return int(digest, 16) & 0xFFFFFFFF

    def add_node(self, physical_node_id: str) -> None:
        """Injects a physical node alongside its configured virtual replication slots into the ring."""
        for i in range(self.replicas):
            virtual_key = f"{physical_node_id}-replica-{i}"
            position_hash = self._compute_md5_hash_integer(virtual_key)
            
            self.hash_to_node_map[position_hash] = physical_node_id
            self.ring_positions.append(position_hash)
            
        self.ring_positions.sort() # Keep hash rings systematically ordered for quick binary lookups

    def remove_node(self, physical_node_id: str) -> None:
        """Purges a cluster node configuration entirely from the dynamic hashing perimeter."""
        for i in range(self.replicas):
            virtual_key = f"{physical_node_id}-replica-{i}"
            position_hash = self._compute_md5_hash_integer(virtual_key)
            
            if position_hash in self.hash_to_node_map:
                del self.hash_to_node_map[position_hash]
                self.ring_positions.remove(position_hash)
                
        self.ring_positions.sort()

    def route_key_to_node(self, operational_key: str) -> Optional[str]:
        """Maps a payload lookup key to its closest clockwise node neighbor along the hash ring."""
        if not self.ring_positions:
            return None
            
        key_hash = self._compute_md5_hash_integer(operational_key)
        
        # Binary search (bisect left mechanics) to find the insertion point coordinates
        low_idx, high_idx = 0, len(self.ring_positions) - 1
        target_index = 0
        
        while low_idx <= high_idx:
            mid_idx = (low_idx + high_idx) // 2
            if self.ring_positions[mid_idx] >= key_hash:
                target_index = mid_idx
                high_idx = mid_idx - 1
            else:
                low_idx = mid_idx + 1
                
        # If the key hash falls past the highest node value, wrap around to the first node position
        if low_idx > len(self.ring_positions) - 1:
            target_index = 0
            
        return self.hash_to_node_map[self.ring_positions[target_index]]


if __name__ == "__main__":
    print("[HASH-RING] Initializing consistent distribution clusters...")
    cluster_ring = ConsistentHashRing(replicas_count=4)
    
    cluster_ring.add_node("BACKEND_NODE_ALPHA")
    cluster_ring.add_node("BACKEND_NODE_BETA")
    
    user_session_token = "saad_session_99412_token"
    assigned_node = cluster_ring.route_key_to_node(user_session_token)
    print(f"[HASH-RING] Key '{user_session_token}' dynamically mapped to: {assigned_node}")
    
    # Scale clustering out dynamically
    cluster_ring.add_node("BACKEND_NODE_GAMMA")
    new_assignment = cluster_ring.route_key_to_node(user_session_token)
    print(f"[HASH-RING] Key mapping verification post-scale mutation: {new_assignment}")