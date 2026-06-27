# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Bounded Load Consistent Hashing
Description: Caps the maximum allocation load per node to prevent hot-spotting 
             when keys cluster within a specific token range.
"""
from typing import Dict, List

class BoundedLoadBalancer:
    def __init__(self, capacity_ceiling: int) -> None:
        self.capacity_ceiling = capacity_ceiling
        self.node_loads: Dict[str, int] = {}

    def accommodate_key(self, target_node: str, fallback_nodes: List[str]) -> str:
        # Check if the primary node has available capacity
        current_load = self.node_loads.get(target_node, 0)
        if current_load < self.capacity_ceiling:
            self.node_loads[target_node] = current_load + 1
            return target_node
            
        # Fall back to the next available node along the ring path
        for fallback in fallback_nodes:
            f_load = self.node_loads.get(fallback, 0)
            if f_load < self.capacity_ceiling:
                self.node_loads[fallback] = f_load + 1
                return fallback
        return "CLUSTER_OVERLOADED"

if __name__ == "__main__":
    balancer = BoundedLoadBalancer(capacity_ceiling=1)
    balancer.node_loads["node_A"] = 1
    allocated = balancer.accommodate_key("node_A", ["node_B"])
    assert allocated == "node_B"