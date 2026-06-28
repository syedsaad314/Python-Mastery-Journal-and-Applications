# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Consistent Hash Ring Core Topology Manager
"""
import hashlib
import bisect
from typing import List, Tuple, Dict, Set
from models import NodeConfig, RingLookupResult

class ConsistentHashRing:
    def __init__(self) -> None:
        self.ring: List[Tuple[int, str]] = [] # Sorted list of (token, node_id)
        self.nodes_manifest: Dict[str, NodeConfig] = {}
        self.node_current_loads: Dict[str, int] = {}

    def _generate_token(self, input_string: str) -> int:
        digest = hashlib.md5(input_string.encode('utf-8')).hexdigest()
        return int(digest[:8], 16)

    def register_node(self, config: NodeConfig) -> None:
        self.nodes_manifest[config.node_id] = config
        self.node_current_loads[config.node_id] = 0
        
        # Distribute virtual nodes across the ring
        for i in range(config.vnode_count):
            vnode_label = f"{config.node_id}-vnode-{i}"
            token = self._generate_token(vnode_label)
            self.ring.append((token, config.node_id))
            
        self.ring.sort()
        print(f"[RING-ENGINE] Node '{config.node_id}' online with {config.vnode_count} VNodes.")

    def remove_node(self, node_id: str) -> None:
        if node_id in self.nodes_manifest:
            self.nodes_manifest.pop(node_id)
            self.node_current_loads.pop(node_id, None)
            self.ring = [entry for entry in self.ring if entry[1] != node_id]
            print(f"[RING-ENGINE] Evicted node '{node_id}' and all associated VNodes from token configuration ranges.")

    def resolve_key_placement(self, key: str, replication_factor: int) -> RingLookupResult:
        if not self.ring:
            raise RuntimeError("Cannot resolve key: Hash ring is empty.")

        key_token = self._generate_token(key)
        
        # Find position on the ring using binary search
        idx = bisect.bisect_right(self.ring, (key_token, ""))
        if idx == len(self.ring):
            idx = 0

        target_node = self.ring[idx][1]
        strategy = "STANDARD_ROUTING"

        # Apply Bounded Load balancing rules
        config = self.nodes_manifest[target_node]
        if self.node_current_loads[target_node] >= config.max_capacity_weight:
            strategy = "BOUNDED_LOAD_REALLOCATION"
            # Trace the ring to find the next available fallback node
            fallback_found = False
            search_idx = (idx + 1) % len(self.ring)
            
            while search_idx != idx:
                possible_node = self.ring[search_idx][1]
                p_config = self.nodes_manifest[possible_node]
                if self.node_current_loads[possible_node] < p_config.max_capacity_weight:
                    target_node = possible_node
                    fallback_found = True
                    break
                search_idx = (search_idx + 1) % len(self.ring)
                
            if not fallback_found:
                strategy = "CLUSTER_OVERLOAD_FALLBACK"

        # Increment target node load counter
        self.node_current_loads[target_node] += 1

        # Trace replication placement paths clockwise along the ring
        replica_list: List[str] = []
        seen_replicas: Set[str] = {target_node}
        scan_idx = (idx + 1) % len(self.ring)

        while len(replica_list) < replication_factor and len(seen_replicas) < len(self.nodes_manifest):
            node_candidate = self.ring[scan_idx][1]
            if node_candidate not in seen_replicas:
                replica_list.append(node_candidate)
                seen_replicas.add(node_candidate)
            scan_idx = (scan_idx + 1) % len(self.ring)

        return RingLookupResult(
            key=key,
            primary_node=target_node,
            replica_nodes=replica_list,
            routing_strategy=strategy
        )