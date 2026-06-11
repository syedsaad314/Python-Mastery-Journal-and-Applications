"""
Core Topic: Synchronous Read Repair Mechanism
Description: Detects data version mismatches during read operations and repairs stale nodes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Tuple, Optional

class MockReplicaNode:
    """Represents a storage node holding a key value pair alongside a numeric version vector."""
    def __init__(self, node_name: str) -> None:
        self.node_name: str = node_name
        self.store: Dict[str, Tuple[str, int]] = {} # Maps Key -> (Value, Version)

    def write(self, key: str, value: str, version: int) -> None:
        self.store[key] = (value, version)

    def read(self, key: str) -> Optional[Tuple[str, int]]:
        return self.store.get(key, None)


class ReadRepairCoordinator:
    """Coordinates quorum reads across replicas and applies repairs to nodes with stale data versions."""
    def __init__(self, replicas: List[MockReplicaNode]) -> None:
        self.replicas = replicas

    def execute_quorum_read(self, key: str) -> Optional[str]:
        """Reads from all nodes, identifies the newest version, and updates any stale replicas found."""
        read_responses: List[Tuple[MockReplicaNode, Tuple[str, int]]] = []
        
        for node in self.replicas:
            data = node.read(key)
            if data:
                read_responses.append((node, data))

        if not read_responses:
            return None

        # Find the node containing the highest version number
        farthest_node, (newest_value, highest_version) = max(read_responses, key=lambda item: item[1][1])
        
        # Repair any replica that returned an older version number
        for node, (val, ver) in read_responses:
            if ver < highest_version:
                print(f"[READ-REPAIR] Node '{node.node_name}' has stale data (v{ver}). Repairing to v{highest_version}...")
                node.write(key, newest_value, highest_version)

        return newest_value


if __name__ == "__main__":
    n1 = MockReplicaNode("replica-us-east")
    n2 = MockReplicaNode("replica-eu-west")
    n3 = MockReplicaNode("replica-asia-pacific")
    
    # Establish a baseline version across nodes
    n1.write("config_param", "Timeout=30", version=1)
    n2.write("config_param", "Timeout=30", version=1)
    
    # Simulate a network drop where a newer write only hits node 3
    n3.write("config_param", "Timeout=60", version=2)
    
    coordinator = ReadRepairCoordinator([n1, n2, n3])
    print("[COORDINATOR] Launching read repair verification sweep...")
    resolved_value = coordinator.execute_quorum_read("config_param")
    print(f" -> Quorum output value resolved: '{resolved_value}'")