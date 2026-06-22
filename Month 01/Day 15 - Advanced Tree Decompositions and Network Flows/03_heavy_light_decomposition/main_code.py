"""
Core Topic: Heavy-Light Tree Decomposition
Description: Breaks down a tree structure into heavy paths and light edges for logarithmic path queries.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import Dict, List

class HeavyLightDecomposition:
    def __init__(self, num_nodes: int, adjacency_list: Dict[int, List[int]], root: int = 0) -> None:
        self.adj: Dict[int, List[int]] = adjacency_list
        self.parent: List[int] = [-1] * num_nodes
        self.depth: List[int] = [0] * num_nodes
        self.subtree_sizes: List[int] = [0] * num_nodes
        self.heavy_child: List[int] = [-1] * num_nodes
        self.head: List[int] = [i for i in range(num_nodes)]
        self.array_pos: List[int] = [0] * num_nodes
        
        self._cur_pos: int = 0
        
        # Pass 1: Map depths, parents, and identify heavy child paths
        self._dfs_heavy_analysis(root, -1, 0)
        # Pass 2: Connect paths into continuous linear blocks
        self._dfs_path_stitching(root, root)

    def _dfs_heavy_analysis(self, node: int, p: int, d: int) -> int:
        self.parent[node] = p
        self.depth[node] = d
        self.subtree_sizes[node] = 1
        
        max_subtree_size = 0
        for neighbor in self.adj.get(node, []):
            if neighbor != p:
                size_collected = self._dfs_heavy_analysis(neighbor, node, d + 1)
                self.subtree_sizes[node] += size_collected
                # The branch with the largest node count becomes the heavy path child
                if size_collected > max_subtree_size:
                    max_subtree_size = size_collected
                    self.heavy_child[node] = neighbor
                    
        return self.subtree_sizes[node]

    def _dfs_path_stitching(self, node: int, path_head: int) -> None:
        self.head[node] = path_head
        self.array_pos[node] = self._cur_pos
        self._cur_pos += 1
        
        # Follow the heavy path first to keep it continuous within the array
        if self.heavy_child[node] != -1:
            self._dfs_path_stitching(self.heavy_child[node], path_head)
            
        # Stitch light edges as new path heads
        for neighbor in self.adj.get(node, []):
            if neighbor != self.parent[node] and neighbor != self.heavy_child[node]:
                self._dfs_path_stitching(neighbor, neighbor)


if __name__ == "__main__":
    # Structure setup: 0 connected to 1 and 2. 1 connected to 3.
    tree = {
        0: [1, 2],
        1: [0, 3],
        2: [0],
        3: [1]
    }
    
    hld = HeavyLightDecomposition(num_nodes=4, adjacency_list=tree, root=0)
    print(f"Segment array position mapping layout: {hld.array_pos}")
    print(f"Path chain head indicators layout: {hld.head}")