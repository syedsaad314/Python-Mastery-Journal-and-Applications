"""
Core Topic: Cluster Heartbeat RPC Coordinator
Description: Simulates the leader node's heartbeat broadcast loops to maintain authority over followers.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import List, Dict

class ClusterHeartbeatCoordinator:
    """Simulates a leader node sending routine heartbeats to prevent followers from starting elections."""
    
    def __init__(self, leader_id: str, cluster_nodes: List[str]) -> None:
        self.leader_id: str = leader_id
        self.peers: List[str] = [p for p in cluster_nodes if p != leader_id]
        self.current_term: int = 1
        # Track follower statuses using a dictionary
        self.follower_lease_map: Dict[str, float] = {peer: time.time() for peer in self.peers}

    def broadcast_heartbeats(self) -> int:
        """Dispatches empty AppendEntries packets to reset follower election timeouts."""
        successful_delivery_count = 0
        current_time = time.time()
        
        print(f"[HEARTBEAT] Leader '{self.leader_id}' broadcasting keep-alive frames for Term {self.current_term}...")
        for peer in self.peers:
            # Simulating network transit path delivery checks
            network_drop_simulated = False
            if not network_drop_simulated:
                self.follower_lease_map[peer] = current_time
                successful_delivery_count += 1
                
        return successful_delivery_count


if __name__ == "__main__":
    cluster_layout = ["node_0", "node_1", "node_2"]
    coordinator = ClusterHeartbeatCoordinator("node_0", cluster_layout)
    
    delivered = coordinator.broadcast_heartbeats()
    print(f"[HEARTBEAT] Keep-alive frames successfully received by {delivered}/{len(coordinator.peers)} followers.")