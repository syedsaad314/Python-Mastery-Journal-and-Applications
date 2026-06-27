# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Virtual Node Distribution
Description: Allocates multiple virtual positions (VNodes) per physical host 
             to achieve an even distribution of data across the ring.
"""
import hashlib
from typing import List, Tuple

class VNodeDistributionEngine:
    def __init__(self, vnodes_per_node: int = 3) -> None:
        self.vnodes_per_node = vnodes_per_node
        self.ring: List[Tuple[int, str]] = []

    def add_node(self, node_id: str) -> None:
        for i in range(self.vnodes_per_node):
            vnode_key = f"{node_id}-vnode-{i}"
            digest = hashlib.md5(vnode_key.encode('utf-8')).hexdigest()
            token = int(digest[:8], 16)
            self.ring.append((token, node_id))
        self.ring.sort()

if __name__ == "__main__":
    engine = VNodeDistributionEngine(vnodes_per_node=4)
    engine.add_node("node_A")
    assert len(engine.ring) == 4