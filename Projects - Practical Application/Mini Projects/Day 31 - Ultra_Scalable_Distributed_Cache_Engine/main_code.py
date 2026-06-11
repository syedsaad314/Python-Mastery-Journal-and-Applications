"""
System: Ultra-Scalable Distributed Cache Engine with Hotspot Mitigation
Description: A complete production-grade sharded cache simulation featuring virtual node hash rings, 
             unbalanced load protection, metrics auditing, and automatic failover handling.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
import bisect
import logging
from typing import List, Dict, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (ShardedCache-Core) %(message)s')

class ShardedCacheServerNode:
    """Represents an independent cache storage server containing a bounded memory partition map."""
    
    def __init__(self, node_id: str, request_threshold: int = 400) -> None:
        self.node_id: str = node_id
        self.memory_store: Dict[str, str] = {}
        self.request_threshold: int = request_threshold
        self.metrics_request_counter: int = 0

    def set_cached_value(self, key: str, value: str) -> bool:
        """Saves a key-value pair to this node's cache partition, tracking the write request volume."""
        self.metrics_request_counter += 1
        if self.metrics_request_counter > self.request_threshold:
            logging.warning(f"[HOTSPOT-ALARM] Node '{self.node_id}' exceeded its safe request threshold!")
        self.memory_store[key] = value
        return True

    def get_cached_value(self, key: str) -> Optional[str]:
        """Retrieves a cached value from this node, incrementing its request metrics counter."""
        self.metrics_request_counter += 1
        return self.memory_store.get(key, None)

    def clear_metrics(self) -> None:
        self.metrics_request_counter = 0


class ClusterConsistentHashRing:
    """Manages virtual node mappings to cleanly distribute keys across a cluster of cache servers."""
    
    def __init__(self, vnode_count: int = 100) -> None:
        self.vnode_count = vnode_count
        self.ring_positions: List[int] = []
        self.position_to_node_map: Dict[int, str] = {}

    def _hash(self, text: str) -> int:
        return int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) & 0xFFFFFFFF

    def register_physical_server(self, node_id: str) -> None:
        """Maps a new server's virtual nodes across the hash ring."""
        for i in range(self.vnode_count):
            pos = self._hash(f"{node_id}-vnode-{i}")
            if pos not in self.position_to_node_map:
                bisect.insort(self.ring_positions, pos)
                self.position_to_node_map[pos] = node_id

    def unregister_physical_server(self, node_id: str) -> None:
        """Removes all virtual node points for a server when it leaves the cluster."""
        targets = [pos for pos, name in self.position_to_node_map.items() if name == node_id]
        for pos in targets:
            self.ring_positions.remove(pos)
            del self.position_to_node_map[pos]

    def resolve_target_server(self, key: str) -> Optional[str]:
        """Finds the correct server node for a key by searching clockwise along the ring."""
        if not self.ring_positions:
            return None
        pos = self._hash(key)
        idx = bisect.bisect_right(self.ring_positions, pos)
        if idx == len(self.ring_positions):
            idx = 0
        return self.position_to_node_map[self.ring_positions[idx]]


class DistributedCacheOrchestrator:
    """Manages the distributed caching layer, routing requests and mitigating traffic hotspots."""
    
    def __init__(self, initial_node_ids: List[str]) -> None:
        self.ring_manager = ClusterConsistentHashRing(vnode_count=120)
        self.cluster_nodes_map: Dict[str, ShardedCacheServerNode] = {}
        
        for name in initial_node_ids:
            self.cluster_nodes_map[name] = ShardedCacheServerNode(name)
            self.ring_manager.register_physical_server(name)

    def write_cache(self, key: str, value: str) -> str:
        """Routes a write request to the appropriate cache server."""
        target_node = self.ring_manager.resolve_target_server(key)
        if target_node and target_node in self.cluster_nodes_map:
            self.cluster_nodes_map[target_node].set_cached_value(key, value)
            return target_node
        return "ERROR_ROUTING"

    def read_cache(self, key: str) -> Tuple[Optional[str], str]:
        """Reads a value from the cache ring. If a server is running hot, it sheds load to a backup node."""
        target_node = self.ring_manager.resolve_target_server(key)
        if not target_node or target_node not in self.cluster_nodes_map:
            return None, "ROUTING_MISS"

        server = self.cluster_nodes_map[target_node]
        # Hotspot mitigation: if a server is overloaded, route the request to a backup server
        if server.metrics_request_counter > server.request_threshold:
            logging.info(f"[LOAD-SHEDDING] Server '{target_node}' is hot! Falling back to backup server paths.")
            # Resolve backup node by modifying key string slightly to simulate a fallback path
            backup_node = self.ring_manager.resolve_target_server(f"{key}-fallback-replica")
            if backup_node and backup_node in self.cluster_nodes_map:
                return self.cluster_nodes_map[backup_node].get_cached_value(key), backup_node

        return server.get_cached_value(key), target_node


if __name__ == "__main__":
    print("\n=== SYSTEM START: SHARDED CACHE WITH HOTSPOT MITIGATION ===\n")
    
    # Initialize a cluster with 3 cache instances
    cluster_setup = ["cache_instance_us_east", "cache_instance_eu_central", "cache_instance_asia_pac"]
    orchestrator = DistributedCacheOrchestrator(cluster_setup)

    # Populate the cache cluster with test entries
    for index in range(500):
        orchestrator.write_cache(f"session_token_key_{index}", f"metadata_payload_string_index_{index}")

    # Simulate a sudden traffic spike on a single key to test load shedding
    print("\n[TRAFFIC-SPIKE] Simulating a high-volume traffic burst on a hot key...")
    for _ in range(450):
        val, served_by = orchestrator.read_cache("session_token_key_12")

    print(f"\n[METRICS-AUDIT] Final Cache Metrics Summary:")
    for name, node_instance in orchestrator.cluster_nodes_map.items():
        print(f" -> Server Instance '{name}' processed: {node_instance.metrics_request_counter} operations.")

    print("\n=== SYSTEM SHUTDOWN: DISTRIBUTED CACHE CORE EXITED ===")