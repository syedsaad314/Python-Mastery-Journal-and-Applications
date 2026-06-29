# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vector Clock Pruning Mechanics
Description: Removes stale or ancient node IDs from vector maps to prevent 
             unbounded metadata growth as nodes leave the cluster.
"""
from typing import Dict, List

class VectorClockGarbageCollector:
    @staticmethod
    def prune_dead_nodes(clock: Dict[str, int], active_nodes: List[str]) -> Dict[str, int]:
        # Drop historical records belonging to nodes that are no longer part of the topology
        pruned_clock = {k: v for k, v in clock.items() if k in active_nodes}
        return pruned_clock

if __name__ == "__main__":
    gc = VectorClockGarbageCollector()
    bloated_clock = {"node_A": 12, "old_dead_node": 99, "node_B": 4}
    cleaned = gc.prune_dead_nodes(bloated_clock, ["node_A", "node_B"])
    assert "old_dead_node" not in cleaned
    assert len(cleaned) == 2