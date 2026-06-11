"""
System: Peer-to-Peer Anti-Entropy Sync Engine
Description: Implements background synchronization between replicas using Merkle Trees 
             to pinpoint and fix data differences with minimal network overhead.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
import logging
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (AntiEntropy-Sync) %(message)s')

class SyncMerkleNode:
    """Represents a node in a binary Merkle tree, tracking data hashes and key ranges."""
    def __init__(self, hash_string: str, bound_range: Optional[Tuple[int, int]] = None) -> None:
        self.hash_string: str = hash_string
        self.bound_range = bound_range
        self.left: Optional[SyncMerkleNode] = None
        self.right: Optional[SyncMerkleNode] = None


class DistributedStorageReplica:
    """A cluster replica that builds Merkle trees over its data partitions to handle background sync."""
    def __init__(self, name: str, data_partition: Dict[int, str]) -> None:
        self.name: str = name
        self.data_partition: Dict[int, str] = dict(data_partition)

    def generate_merkle_tree(self) -> Optional[SyncMerkleNode]:
        return self._recursive_build(sorted(list(self.data_partition.keys())))

    def _recursive_build(self, sorted_keys: List[int]) -> Optional[SyncMerkleNode]:
        if not sorted_keys:
            return None
        if len(sorted_keys) == 1:
            k = sorted_keys[0]
            leaf_hash = hashlib.sha256(f"{k}:{self.data_partition[k]}".encode('utf-8')).hexdigest()
            return SyncMerkleNode(leaf_hash, (k, k))

        mid = len(sorted_keys) // 2
        left_child = self._recursive_build(sorted_keys[:mid])
        right_child = self._recursive_build(sorted_keys[mid:])
        
        combined_hash = hashlib.sha256(
            ((left_child.hash_string if left_child else "") + 
             (right_child.hash_string if right_child else "")).encode('utf-8')
        ).hexdigest()
        
        low_bound = left_child.bound_range[0] if left_child else 0
        high_bound = right_child.bound_range[1] if right_child else 0
        
        parent = SyncMerkleNode(combined_hash, (low_bound, high_bound))
        parent.left = left_child
        parent.right = right_child
        return parent


class AntiEntropyEngineOrchestrator:
    """Compares Merkle trees from different replicas to find and sync mismatched data ranges."""
    
    def reconcile_nodes(self, replica_a: DistributedStorageReplica, replica_b: DistributedStorageReplica) -> None:
        """Finds out-of-sync keys between two replicas and applies targeted updates to fix them."""
        tree_a = replica_a.generate_merkle_tree()
        tree_b = replica_b.generate_merkle_tree()
        
        mismatched_ranges = self._extract_mismatched_ranges(tree_a, tree_b)
        
        if not mismatched_ranges:
            logging.info(f"Replicas '{replica_a.name}' and '{replica_b.name}' are completely in sync.")
            return

        for low, high in mismatched_ranges:
            # Sync data in the mismatched range from Replica A to Replica B
            for key in range(low, high + 1):
                if key in replica_a.data_partition:
                    correct_value = replica_a.data_partition[key]
                    if replica_b.data_partition.get(key) != correct_value:
                        logging.info(f"[SYNC-REPAIR] Copying key {key} from '{replica_a.name}' to '{replica_b.name}'")
                        replica_b.data_partition[key] = correct_value

    def _extract_mismatched_ranges(self, node_a: Optional[SyncMerkleNode], node_b: Optional[SyncMerkleNode]) -> List[Tuple[int, int]]:
        if not node_a and not node_b:
            return []
        if (not node_a or not node_b) or (node_a.hash_string != node_b.hash_string):
            if node_a and not node_a.left and not node_a.right:
                return [node_a.bound_range]
            if node_b and not node_b.left and not node_b.right:
                return [node_b.bound_range]
                
            deltas = []
            deltas.extend(self._extract_mismatched_ranges(node_a.left if node_a else None, node_b.left if node_b else None))
            deltas.extend(self._extract_mismatched_ranges(node_a.right if node_a else None, node_b.right if node_b else None))
            return deltas
        return []


if __name__ == "__main__":
    print("\n=== SYSTEM START: PEER-TO-PEER ANTI-ENTROPY SYNC ENGINE ===\n")
    
    # Define primary datasets with a drift at key ID index 500
    base_data_a = {100: "DataVersionA", 300: "DataVersionB", 500: "TargetValueAlpha"}
    base_data_b = {100: "DataVersionA", 300: "DataVersionB", 500: "TargetValueBeta"}
    
    server_east = DistributedStorageReplica("Datacenter-East", base_data_a)
    server_west = DistributedStorageReplica("Datacenter-West", base_data_b)
    
    sync_engine = AntiEntropyEngineOrchestrator()
    
    logging.info("Starting background synchronization pass between datacenters...")
    sync_engine.reconcile_nodes(server_east, server_west)
    
    print(f"\n[POST-SYNC] Verification Check: Server West Key 500 value = '{server_west.data_partition[500]}'")
    print("\n=== SYSTEM SHUTDOWN: ANTI-ENTROPY ENGINE COMPLETED ===")