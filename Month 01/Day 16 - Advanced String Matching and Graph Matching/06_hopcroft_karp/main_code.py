"""
Core Topic: Bipartite Graph Cardinality Matching (Hopcroft-Karp)
Description: Optimizes maximum assignment distributions across bipartite networks using BFS/DFS layers.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque
from typing import Dict, List

class HopcroftKarp:
    def __init__(self, left_side_nodes: List[int], bipartite_edges: Dict[int, List[int]]) -> None:
        self.left_nodes: List[int] = left_side_nodes
        self.adj: Dict[int, List[int]] = bipartite_edges
        
        # Track active matching assignments (0 indicates unassigned/dummy state)
        self.match_left: Dict[int, int] = {u: 0 for u in left_side_nodes}
        self.match_right: Dict[int, int] = {}
        
        # Depth layer metrics used during BFS passes
        self.distances: Dict[int, int] = {}

    def _bfs_layer_generation(self) -> bool:
        """Builds a layered structure over unmatched nodes using BFS."""
        queue: deque[int] = deque()
        self.distances[0] = float('inf')  # Dummy node serves as the target sink

        for u in self.left_nodes:
            if self.match_left[u] == 0:
                self.distances[u] = 0
                queue.append(u)
            else:
                self.distances[u] = float('inf')

        # Continue scanning layers as long as unassigned nodes exist
        while queue:
            u = queue.popleft()
            
            if self.distances[u] < self.distances[0]:
                for v in self.adj.get(u, []):
                    assigned_left = self.match_right.get(v, 0)
                    
                    if self.distances[assigned_left] == float('inf'):
                        self.distances[assigned_left] = self.distances[u] + 1
                        queue.append(assigned_left)

        return self.distances[0] != float('inf')

    def _dfs_augment_path(self, u: int) -> bool:
        """Finds disjoint augmenting paths using DFS to increase maximum matching cardality."""
        if u != 0:
            for v in self.adj.get(u, []):
                assigned_left = self.match_right.get(v, 0)
                
                # Verify if the node aligns with the next sequential layer depth
                if self.distances[assigned_left] == self.distances[u] + 1:
                    if self._dfs_augment_path(assigned_left):
                        # Secure the new link assignment
                        self.match_left[u] = v
                        self.match_right[v] = u
                        return True
                        
            self.distances[u] = float('inf')
            return False
        return True

    def compute_max_matching(self) -> int:
        """Calculates the absolute maximum cardinality matching count across the graph."""
        max_matching_count = 0
        # Continue optimization cycles as long as valid augmenting paths are found
        while self._bfs_layer_generation():
            for u in self.left_nodes:
                if self.match_left[u] == 0 and self._dfs_augment_path(u):
                    max_matching_count += 1
        return max_matching_count


if __name__ == "__main__":
    # Graph structure mapping Left Node IDs to matching Right Node destination lists
    bipartite_graph = {
        1: [10, 11],
        2: [10],
        3: [11, 12]
    }
    left_side = [1, 2, 3]
    
    matcher = HopcroftKarp(left_side, bipartite_graph)
    total_assignments = matcher.compute_max_matching()
    
    print(f"Maximum calculated matching cardinality: {total_assignments}")
    print(f"Final Left-to-Right layout matches: {matcher.match_left}")