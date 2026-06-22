"""
Core Topic: Dinic's Maximum Flow Optimization
Description: High-performance max-flow engine utilizing layered networks and blocking flows.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque
from typing import List

class DinicsAlgorithm:
    def __init__(self, capacity_matrix: List[List[int]]) -> None:
        self.residual_graph: List[List[int]] = [row[:] for row in capacity_matrix]
        self.num_nodes: int = len(capacity_matrix)
        self.levels: List[int] = [-1] * self.num_nodes

    def _bfs_build_layered_network(self, source: int, sink: int) -> bool:
        """Builds a layered network by assigning level depths to nodes using BFS."""
        self.levels = [-1] * self.num_nodes
        self.levels[source] = 0
        queue: deque[int] = deque([source])
        
        while queue:
            current = queue.popleft()
            for neighbor in range(self.num_nodes):
                if self.levels[neighbor] < 0 and self.residual_graph[current][neighbor] > 0:
                    self.levels[neighbor] = self.levels[current] + 1
                    queue.append(neighbor)
                    
        return self.levels[sink] >= 0

    def _dfs_push_blocking_flow(self, node: int, sink: int, current_flow: int, edge_ptr: List[int]) -> int:
        """Pushes blocking flows along paths in the layered network using DFS."""
        if node == sink or current_flow == 0:
            return current_flow
            
        # Start searching from the last evaluated edge pointer to avoid redundant checks
        for neighbor in range(edge_ptr[node], self.num_nodes):
            edge_ptr[node] = neighbor
            
            # Ensure the neighbor is in the next layer and has available capacity
            if self.levels[neighbor] == self.levels[node] + 1 and self.residual_graph[node][neighbor] > 0:
                pushed_capacity = self._dfs_push_blocking_flow(
                    neighbor, sink, min(current_flow, self.residual_graph[node][neighbor]), edge_ptr
                )
                
                if pushed_capacity > 0:
                    # Update edge capacities along the path
                    self.residual_graph[node][neighbor] -= pushed_capacity
                    self.residual_graph[neighbor][node] += pushed_capacity
                    return pushed_capacity
                    
        return 0

    def calculate_max_flow(self, source: int, sink: int) -> int:
        total_flow = 0
        # Rebuild the layered network as long as the sink remains reachable
        while self._bfs_build_layered_network(source, sink):
            # Track the next edge to process for each node to optimize the DFS pass
            edge_ptr = [0] * self.num_nodes
            while True:
                pushed = self._dfs_push_blocking_flow(source, sink, float('inf'), edge_ptr)
                if pushed == 0:
                    break
                total_flow += pushed
        return total_flow


if __name__ == "__main__":
    graph_capacities = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    
    flow_engine = DinicsAlgorithm(graph_capacities)
    print(f"Dinic's calculated max flow total: {flow_engine.calculate_max_flow(source=0, sink=5)}")