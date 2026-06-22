"""
Core Topic: Gossip Protocol Failure Detection
Description: Simulates cluster nodes exchanging health statuses to discover failures.
Lead Engineer: Syed Saad Bin Irfan
"""

import random
from typing import Dict, List

class GossipClusterNode:
    """Represents a node that gossips with random peers to spread cluster membership health states."""
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        # Tracks internal version counters for all known nodes in the cluster
        self.membership_heartbeats: Dict[str, int] = {node_id: 0}

    def increment_local_heartbeat(self) -> None:
        self.membership_heartbeats[self.node_id] += 1

    def send_gossip_packet(self, target_peer: 'GossipClusterNode') -> None:
        """Shares local heartbeat tracking states with a random peer node."""
        target_peer.receive_gossip_packet(self.membership_heartbeats)

    def receive_gossip_packet(self, incoming_state: Dict[str, int]) -> None:
        """Merges incoming states by adopting the highest known heartbeat counter for each node."""
        for node_id, heartbeat in incoming_state.items():
            self.membership_heartbeats[node_id] = max(self.membership_heartbeats.get(node_id, 0), heartbeat)


if __name__ == "__main__":
    cluster = [GossipClusterNode(f"node_instance_{i}") for i in range(4)]
    
    print("[GOSSIP] Simulating cluster background health exchanges...")
    # Node 0 ticks its heartbeat and gossips with Node 1
    cluster[0].increment_local_heartbeat()
    cluster[0].send_gossip_packet(cluster[1])
    
    # Node 1 gossips with Node 2, spreading Node 0's updated status down the chain
    cluster[1].send_gossip_packet(cluster[2])
    
    print(f" -> Node 2 updated membership view: {cluster[2].membership_heartbeats}")