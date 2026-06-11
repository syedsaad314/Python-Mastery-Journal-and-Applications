"""
System: Decentralized Dynamo Storage Core
Description: Production grade masterless key-value cluster node engine featuring
             strict quorum reads/writes, version tracking, and active read repairs.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Dynamo-Core) %(message)s')

class StorageReplicaNode:
    """An independent storage engine replica that retains keys alongside their write versions."""
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.partition_store: Dict[str, Tuple[str, int]] = {}

    def put_direct(self, key: str, value: str, version: int) -> None:
        self.partition_store[key] = (value, version)

    def get_direct(self, key: str) -> Optional[Tuple[str, int]]:
        return self.partition_store.get(key, None)


class DynamoClusterCoordinator:
    """Manages data distribution, handles quorum routing, and triggers automatic read repairs."""
    def __init__(self, node_ids: List[str], replication_factor: int = 3) -> None:
        self.n = replication_factor
        self.nodes_map: Dict[str, StorageReplicaNode] = {nid: StorageReplicaNode(nid) for nid in node_ids}

    def write_key(self, key: str, value: str, target_version: int, write_quorum: int) -> bool:
        """Sends data updates to replicas and returns success if the write quorum is met."""
        successful_write_count = 0
        
        # Route writes to all nodes in the replication group
        for node_id, node_instance in self.nodes_map.items():
            try:
                node_instance.put_direct(key, value, target_version)
                successful_write_count += 1
            except Exception:
                logging.error(f"Write transmission failed at replica node reference: {node_id}")

        return successful_write_count >= write_quorum

    def read_key(self, key: str, read_quorum: int) -> Optional[str]:
        """Reads data from replicas, evaluates version counts, and runs read repairs on stale nodes."""
        collected_responses: List[Tuple[StorageReplicaNode, Tuple[str, int]]] = []

        for node_id, node_instance in self.nodes_map.items():
            response = node_instance.get_direct(key)
            if response:
                collected_responses.append((node_instance, response))

        if len(collected_responses) < read_quorum:
            logging.error(f"[QUORUM-FAILURE] Insufficient read responses gathered for key: '{key}'")
            return None

        # Identify the most up-to-date value by looking for the highest version number
        farthest_replica, (newest_value, highest_version) = max(collected_responses, key=lambda item: item[1][1])

        # Synchronously repair any nodes that returned stale data versions
        for node_instance, (val, ver) in collected_responses:
            if ver < highest_version:
                logging.info(f"[READ-REPAIR-TRIGGER] Updating stale node '{node_instance.node_id}' to latest version v{highest_version}")
                node_instance.put_direct(key, newest_value, highest_version)

        return newest_value


if __name__ == "__main__":
    print("\n=== SYSTEM INITIALIZATION: DECENTRALIZED DYNAMO STORAGE CORE ===\n")
    
    node_identities = ["node_us_east", "node_eu_central", "node_sa_east"]
    cluster_manager = DynamoClusterCoordinator(node_identities, replication_factor=3)

    # Execute a strict write requiring a quorum of 2 nodes
    logging.info("Staging initial write operation for app parameters...")
    cluster_manager.write_key("app_mode", "Maintenance", target_version=1, write_quorum=2)

    # Simulate a partial failure: manually update a single node to mimic a newer, split-brain write
    cluster_manager.nodes_map["node_sa_east"].put_direct("app_mode", "LiveProduction", version=2)

    # Perform a quorum read to trigger automatic data repair across out-of-sync nodes
    print("\n[CLIENT-READ] Executing a strict quorum read operation...")
    current_state = cluster_manager.read_key("app_mode", read_quorum=2)
    print(f" -> Current cluster state resolved: '{current_state}'")

    print("\n=== SYSTEM SHUTDOWN: DECENTRALIZED DYNAMO ENGINE EXITED ===")