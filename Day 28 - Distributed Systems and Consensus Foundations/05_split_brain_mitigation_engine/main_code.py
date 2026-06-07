"""
Core Topic: Network Partition Split-Brain Mitigation
Description: Enforces strict self-demotion policies on leaders if quorum connectivity drops.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import Set, List

class SplitBrainMitigationEngine:
    """Monitors connectivity state and runs self-demotion rules if a node loses quorum."""
    
    def __init__(self, node_id: str, cluster_membership_pool: Set[str]) -> None:
        self.node_id: str = node_id
        self.membership_pool: Set[str] = cluster_membership_pool
        self.majority_quorum_threshold: int = (len(cluster_membership_pool) // 2) + 1
        self.current_role: str = "LEADER"

    def evaluate_heartbeat_acknowledgments(self, active_responsive_peers: List[str]) -> str:
        """Validates alive feedback loops, forcing leader demotion if quorum connectivity is lost."""
        if self.current_role != "LEADER":
            return self.current_role

        # Build an active reachability pool including self
        reachable_nodes = set(active_responsive_peers)
        reachable_nodes.add(self.node_id)
        
        actual_active_connections_count = len(reachable_nodes.intersection(self.membership_pool))
        
        print(f"[MITIGATION] Connected nodes count: {actual_active_connections_count}/{len(self.membership_pool)} (Req: {self.majority_quorum_threshold})")
        
        # Self-demotion rule: if connectivity drops below the majority threshold, step down immediately
        if actual_active_connections_count < self.majority_quorum_threshold:
            print(f"[⚠️ DEMOTION ALERT] Node '{self.node_id}' lost majority quorum connectivity. Stepping down to FOLLOWER.")
            self.current_role = "FOLLOWER"
            
        return self.current_role


if __name__ == "__main__":
    cluster_nodes = {"NODE_A", "NODE_B", "NODE_C", "NODE_D", "NODE_E"} # Total: 5, Majority Quorum Threshold: 3
    engine = SplitBrainMitigationEngine("NODE_A", cluster_nodes)
    
    # Test case 1: Healthy cluster connectivity conditions match
    status = engine.evaluate_heartbeat_acknowledgments(["NODE_B", "NODE_C"])
    print(f"[TEST-1] Engine operational status outcome: {status}")

    # Test case 2: Network partition splits node into minority zone cluster segment
    print("\n--- Network Partition Severing Link Interface ---")
    status_post_fault = engine.evaluate_heartbeat_acknowledgments(["NODE_B"])
    print(f"[TEST-2] Post-fault engine role status: {status_post_fault}")