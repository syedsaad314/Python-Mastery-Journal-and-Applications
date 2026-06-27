# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Replication Placement Paths
Description: Locates a primary node on the ring and traces downstream clockwise 
             to find unique secondary replicas for high availability.
"""
from typing import List, Tuple, Set

class ReplicationPlacementEngine:
    @staticmethod
    def identify_replica_nodes(ring: List[Tuple[int, str]], start_index: int, replication_factor: int) -> List[str]:
        replicas: List[str] = []
        seen_nodes: Set[str] = set()
        ring_len = len(ring)
        
        idx = start_index
        while len(replicas) < replication_factor and len(seen_nodes) < len(set(n for _, n in ring)):
            node_id = ring[idx % ring_len][1]
            if node_id not in seen_nodes:
                replicas.append(node_id)
                seen_nodes.add(node_id)
            idx += 1
        return replicas

if __name__ == "__main__":
    mock_ring = [(100, "node_A"), (200, "node_B"), (300, "node_A"), (400, "node_C")]
    engine = ReplicationPlacementEngine()
    targets = engine.identify_replica_nodes(mock_ring, start_index=0, replication_factor=2)
    assert targets == ["node_A", "node_B"]