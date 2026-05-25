"""
Core Topic: Centroid Decomposition Balancing
Description: Divide-and-conquer tree decomposition that isolates structural center points.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import Dict, List, Set

class CentroidDecomposition:
    def __init__(self, num_nodes: int, adjacency_list: Dict[int, List[int]]) -> None:
        self.adj: Dict[int, List[int]] = adjacency_list
        self.subtree_sizes: List[int] = [0] * num_nodes
        self.is_deactivated: Set[int] = set()
        self.parent_links: List[int] = [-1] * num_nodes
        
        # Build balanced tracking matrix structure
        self._decompose_tree(node=0, structural_parent=-1)

    def _calculate_sizes(self, node: int, parent: int) -> int:
        """Computes the size of each subtree recursively, skipping deactivated nodes."""
        self.subtree_sizes[node] = 1
        for neighbor in self.adj.get(node, []):
            if neighbor != parent and neighbor not in self.is_deactivated:
                self.subtree_sizes[node] += self._calculate_sizes(neighbor, node)
        return self.subtree_sizes[node]

    def _find_centroid(self, node: int, parent: int, total_tree_size: int) -> int:
        """Locates the centroid node whose removal splits the tree into balanced components."""
        for neighbor in self.adj.get(node, []):
            if neighbor != parent and neighbor not in self.is_deactivated:
                # If a branch contains more than half the tree's nodes, move down that path
                if self.subtree_sizes[neighbor] > total_tree_size // 2:
                    return self._find_centroid(neighbor, node, total_tree_size)
        return node

    def _decompose_tree(self, node: int, structural_parent: int) -> int:
        """Recursively isolates centroids to construct a balanced tree hierarchy."""
        # Step 1: Calculate current subtree sizes
        current_size = self._calculate_sizes(node, -1)
        # Step 2: Locate the centroid for this component
        centroid = self._find_centroid(node, -1, current_size)
        
        self.parent_links[centroid] = structural_parent
        self.is_deactivated.add(centroid)
        
        # Step 3: Decompose remaining connected components recursively
        for neighbor in self.adj.get(centroid, []):
            if neighbor not in self.is_deactivated:
                self._decompose_tree(neighbor, centroid)
                
        return centroid


if __name__ == "__main__":
    # Linear un-balanced tree structure layout: 0 - 1 - 2 - 3 - 4
    unbalanced_tree = {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3]
    }
    
    decom_engine = CentroidDecomposition(num_nodes=5, adjacency_list=unbalanced_tree)
    print(f"Centroid Tree Parent Links Matrix Map: {decom_engine.parent_links}")