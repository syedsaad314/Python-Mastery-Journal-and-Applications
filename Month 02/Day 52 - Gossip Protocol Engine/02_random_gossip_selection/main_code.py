# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Random Gossip Target Selection
Description: Implements a non-deterministic routing selector that handles picking random 
             active targets from the member registry list.
"""
import random
from typing import List, Optional

class GossipTargetSelector:
    @staticmethod
    def select_gossip_peer(current_node: str, all_known_nodes: List[str]) -> Optional[str]:
        eligible_peers = [node for node in all_known_nodes if node != current_node]
        if not eligible_peers:
            return None
        return random.choice(eligible_peers)

if __name__ == "__main__":
    selector = GossipTargetSelector()
    nodes = ["node_A", "node_B", "node_C"]
    target = selector.select_gossip_peer("node_A", nodes)
    assert target in ["node_B", "node_C"]