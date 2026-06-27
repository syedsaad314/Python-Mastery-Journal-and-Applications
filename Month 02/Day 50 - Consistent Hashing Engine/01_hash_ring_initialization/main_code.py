# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Hash Ring Initialization
Description: Builds a basic token ring topology mapping 32-bit integer spaces 
             to locate node coordinates using md5 hashing.
"""
import hashlib
from typing import List, Tuple

class HashRingInitializer:
    def __init__(self) -> None:
        self.ring: List[Tuple[int, str]] = []

    def _compute_hash(self, key: str) -> int:
        # Generate stable 32-bit unsigned integers from md5 strings
        digest = hashlib.md5(key.encode('utf-8')).hexdigest()
        return int(digest[:8], 16)

    def register_physical_node(self, node_id: str) -> int:
        token = self._compute_hash(node_id)
        self.ring.append((token, node_id))
        self.ring.sort() # Ensure sorted ring token structures
        print(f"[RING-INIT] Node '{node_id}' placed at token index: {token}")
        return token

if __name__ == "__main__":
    initializer = HashRingInitializer()
    t1 = initializer.register_physical_node("node_asia")
    t2 = initializer.register_physical_node("node_europe")
    assert len(initializer.ring) == 2
    assert initializer.ring[0][0] <= initializer.ring[1][0]