"""
Core Topic: Lowest Common Ancestor (LCA) via Binary Lifting
Description: Precomputes parent jump paths to isolate common ancestors in tree structures.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import math
from typing import Dict, List

class TreeLCA:
    def __init__(self, num_nodes: int, adjacency_list: Dict[int, List[int]], root: int = 0) -> None:
        self.n: int = num_nodes
        self.adj: Dict[int, List[int]] = adjacency_list
        
        # Max power depth step limit log2(N)
        self.log_max: int = int(math.log2(self.n)) + 1 if self.n > 0 else 1
        
        self.depths: List[int] = [0] * self.n
        # Allocate lifting matrix: up[node][power]
        self.up: List[List[int]] = [[root] * self.log_max for _ in range(self.n)]
        
        # Run initial tree traversal pass to map depth layers
        self._dfs(root, root, 0)

    def _dfs(self, node: int, parent: int, d: int) -> None:
        """Traverses the tree to map depths and precalculate immediate parent connections."""
        self.depths[node] = d
        self.up[node][0] = parent
        
        # Populate the jump table entries using power-of-two parent references
        for j in range(1, self.log_max):
            mid_parent = self.up[node][j - 1]
            self.up[node][j] = self.up[mid_parent][j - 1]
            
        for neighbor in self.adj.get(node, []):
            if neighbor != parent:
                self._dfs(neighbor, node, d + 1)

    def query_lca(self, u: int, v: int) -> int:
        """Finds the lowest common ancestor of two nodes in logarithmic O(log N) time."""
        # 1. Ensure node 'u' is positioned deeper than node 'v'
        if self.depths[u] < self.depths[v]:
            u, v = v, u
            
        # 2. Lift node 'u' upward until it matches the depth layer of node 'v'
        depth_diff = self.depths[u] - self.depths[v]
        for j in range(self.log_max - 1, -1, -1):
            if (depth_diff >> j) & 1:
                u = self.up[u][j]
                
        # Return early if node 'v' is an ancestor of node 'u'
        if u == v:
            return u
            
        # 3. Lift both nodes upward together until they are just below their common ancestor
        for j in range(self.log_max - 1, -1, -1):
            if self.up[u][j] != self.up[v][j]:
                u = self.up[u][j]
                v = self.up[v][j]
                
        # The immediate parent is the lowest common ancestor
        return self.up[u][0]


if __name__ == "__main__":
    # Construct a sample tree structure layout:
    #        0
    #       / \
    #      1   2
    #     / \
    #    3   4
    tree = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0],
        3: [1],
        4: [1]
    }
    
    lca_engine = TreeLCA(num_nodes=5, adjacency_list=tree, root=0)
    
    print(f"LCA of node 3 and node 4: {lca_engine.query_lca(3, 4)}")  # Should return parent node 1
    print(f"LCA of node 3 and node 2: {lca_engine.query_lca(3, 2)}")  # Should return root node 0
    print(f"LCA of node 1 and node 4: {lca_engine.query_lca(1, 4)}")  # Should return node 1