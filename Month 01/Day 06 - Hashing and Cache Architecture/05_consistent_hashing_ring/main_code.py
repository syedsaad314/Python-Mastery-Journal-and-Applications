"""
Core Topic: Consistent Hashing Distribution Ring
Description: Mapping storage nodes onto a circular virtual ring layout to maintain mapping stability under scale variations.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import hashlib
import bisect

class ConsistentHashingRing:
    def __init__(self, virtual_node_count: int = 3):
        self.virtual_node_count = virtual_node_count
        # Dynamic tracking arrays mapping structural position keys
        self.ring_positions = []
        self.position_to_node_map = {}

    def _hash_position(self, input_string: str) -> int:
        """Maps an item value down into an integer space integer boundary point."""
        hash_bytes = hashlib.md5(input_string.encode('utf-8')).digest()
        # Extract the initial 4 bytes to form a stable integer value
        return int.from_bytes(hash_bytes[:4], byteorder='big')

    def add_storage_node(self, node: str) -> None:
        """Places multiple virtual node tokens across the circular ring framework."""
        for i in range(self.virtual_node_count):
            virtual_key = f"{node}-replica-{i}"
            position = self._hash_position(virtual_key)
            
            # Binary search positioning insert step to keep ring arrays sorted
            bisect.insort(self.ring_positions, position)
            self.position_to_node_map[position] = node

    def remove_storage_node(self, node: str) -> None:
        """Purges all associated node replicas from the active configuration layout."""
        for i in range(self.virtual_node_count):
            virtual_key = f"{node}-replica-{i}"
            position = self._hash_position(virtual_key)
            
            if position in self.ring_positions:
                self.ring_positions.remove(position)
                del self.position_to_node_map[position]

    def fetch_assigned_node(self, data_key: str) -> str:
        """Finds the closest node on the ring by traveling clockwise from the data key's position."""
        if not self.ring_positions:
            return None
            
        position = self._hash_position(data_key)
        # Locate insertion point matching clockwise rotation direction logic
        idx = bisect.bisect_right(self.ring_positions, position)
        
        # If position exceeds the last node on the ring, wrap around to index 0
        if idx == len(self.ring_positions):
            idx = 0
            
        return self.position_to_node_map[self.ring_positions[idx]]

if __name__ == "__main__":
    cluster_ring = ConsistentHashingRing(virtual_node_count=3)
    cluster_ring.add_storage_node("datastore_node_alpha")
    cluster_ring.add_storage_node("datastore_node_beta")
    
    user_record_key = "user_profile_session_94820"
    target_node = cluster_ring.fetch_assigned_node(user_record_key)
    print(f"Initial Key Assignment Mapping Destination: {target_node}")
    
    # Introduce an active secondary scaling node into the cluster ring topology
    cluster_ring.add_storage_node("datastore_node_gamma")
    new_target_node = cluster_ring.fetch_assigned_node(user_record_key)
    print(f"Post-Scaling Key Assignment Mapping Destination: {new_target_node}")