"""
Core Topic: Redlock Algorithm Quorum Logic
Description: Simulates multi-node consensus-based lock validation across independent nodes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class RedlockNodeInstance:
    def __init__(self, name: str, online: bool = True) -> None:
        self.name = name
        self.online = online

    def request_lock_grant(self) -> bool:
        return self.online


class RedlockQuorumValidator:
    """Coordinates lock allocation by verifying validation agreements across a node quorum."""
    
    def __init__(self, node_pool: List[RedlockNodeInstance]) -> None:
        self.pool = node_pool
        self.quorum_threshold = (len(node_pool) // 2) + 1

    def evaluate_global_lock_consensus(self) -> bool:
        """Requires successful lock acquisition from a clear majority of independent nodes."""
        successful_grants = 0
        for node in self.pool:
            if node.request_lock_grant():
                successful_grants += 1
                
        has_consensus = successful_grants >= self.quorum_threshold
        print(f"[REDLOCK-QUORUM] Node Grants: {successful_grants}/{len(self.pool)} | Quorum Met? -> {has_consensus}")
        return has_consensus


if __name__ == "__main__":
    cluster_nodes = [
        RedlockNodeInstance("redis-01", online=True),
        RedlockNodeInstance("redis-02", online=True),
        RedlockNodeInstance("redis-03", online=False), # Simulating an isolated server node
    ]
    validator = RedlockQuorumValidator(cluster_nodes)
    assert validator.evaluate_global_lock_consensus() == True # 2 out of 3 online meets majority quorum