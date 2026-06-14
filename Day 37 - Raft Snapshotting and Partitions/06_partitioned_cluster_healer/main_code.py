"""
Core Topic: Partitioned Cluster Recovery Loops
Description: Simulates a network partition healing and demonstrates how cluster logs converge.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class HealableClusterSimulator:
    """Tracks cluster log convergence before and after a network partition heals."""
    
    def __init__(self) -> None:
        # Node-A represents the valid leader of the healthy majority partition
        self.majority_leader_log = ["GENESIS", "SET x=1", "SET y=2"]
        # Node-E represents an isolated stale follower that missed updates during the split
        self.isolated_follower_log = ["GENESIS"]

    def heal_network_partition(self) -> None:
        """Simulates healing the partition and reconciling logs across recovered nodes."""
        print("[HEALER] Network partition has cleared. Reconciling logs...")
        
        # Stale nodes detect the higher term or log length and pull missing entries from the leader
        if len(self.isolated_follower_log) < len(self.majority_leader_log):
            missing_entries = self.majority_leader_log[len(self.isolated_follower_log):]
            self.isolated_follower_log.extend(missing_entries)
        print("[HEALER] Rebalancing complete. Cluster logs are fully aligned.")


if __name__ == "__main__":
    simulator = HealableClusterSimulator()
    print(f"[HEALER] Split logs -> Majority Leader: {simulator.majority_leader_log}")
    print(f"[HEALER] Split logs -> Isolated Follower: {simulator.isolated_follower_log}")
    
    # Heal the network split and let logs converge
    simulator.heal_network_partition()
    print(f"[HEALER] Aligned logs -> Isolated Follower: {simulator.isolated_follower_log}")