"""
Core Topic: Merkle Tree Anti-Entropy Sync
Description: Builds a binary Merkle tree to efficiently compare and sync datasets between replicas.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
from typing import Dict, List, Optional, Tuple

class MerkleNode:
    """Represents a node inside a binary Merkle tree structure."""
    def __init__(self, hash_val: str, key_range: Optional[Tuple[int, int]] = None) -> None:
        self.hash_val: str = hash_val
        self.key_range = key_range # Tracks the sub-range of data keys this hash covers
        self.left: Optional[MerkleNode] = None
        self.right: Optional[MerkleNode] = None


class ReplicaMerkleTree:
    """Builds a Merkle tree over a local data store to quickly identify dataset differences."""
    def __init__(self, local_data: Dict[int, str]) -> None:
        self.local_data = local_data
        self.root = self._build_tree(sorted(list(local_data.keys())))

    def _hash_string(self, text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _build_tree(self, sorted_keys: List[int]) -> Optional[MerkleNode]:
        if not sorted_keys:
            return None
        if len(sorted_keys) == 1:
            k = sorted_keys[0]
            leaf_hash = self._hash_string(f"{k}:{self.local_data[k]}")
            return MerkleNode(leaf_hash, (k, k))

        mid = len(sorted_keys) // 2
        left_child = self._build_tree(sorted_keys[:mid])
        right_child = self._build_tree(sorted_keys[mid:])
        
        combined_hash = self._hash_string((left_child.hash_val if left_child else "") + 
                                          (right_child.hash_val if right_child else ""))
        
        low_bound = left_child.key_range[0] if left_child else 0
        high_bound = right_child.key_range[1] if right_child else 0
        
        parent = MerkleNode(combined_hash, (low_bound, high_bound))
        parent.left = left_child
        parent.right = right_child
        return parent

    @staticmethod
    def detect_deltas(node_a: Optional[MerkleNode], node_b: Optional[MerkleNode]) -> List[Tuple[int, int]]:
        """Traverses two Merkle trees side by side to find the specific key ranges where data differs."""
        if not node_a and not node_b:
            return []
        
        # If one node is missing or hashes don't match, we found a mismatch
        if (not node_a or not node_b) or (node_a.hash_val != node_b.hash_val):
            # If we reached a leaf node, return its exact range
            if node_a and not node_a.left and not node_a.right:
                return [node_a.key_range]
            if node_b and not node_b.left and not node_b.right:
                return [node_b.key_range]
                
            # Otherwise, traverse deeper down the tree to isolate the mismatch
            deltas = []
            deltas.extend(ReplicaMerkleTree.detect_deltas(node_a.left if node_a else None, node_b.left if node_b else None))
            deltas.extend(ReplicaMerkleTree.detect_deltas(node_a.right if node_a else None, node_b.right if node_b else None))
            return deltas
            
        return []


if __name__ == "__main__":
    # Define dataset states with a single mismatch at key 400
    dataset_alpha = {100: "PayloadA", 200: "PayloadB", 400: "PayloadC"}
    dataset_beta  = {100: "PayloadA", 200: "PayloadB", 400: "PayloadModified"}
    
    tree_a = ReplicaMerkleTree(dataset_alpha)
    tree_b = ReplicaMerkleTree(dataset_beta)
    
    mismatched_ranges = ReplicaMerkleTree.detect_deltas(tree_a.root, tree_b.root)
    print(f"[ANTI-ENTROPY] Extracted mismatched range targets: {mismatched_ranges}")