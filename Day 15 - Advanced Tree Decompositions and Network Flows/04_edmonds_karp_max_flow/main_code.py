"""
Core Topic: Edmonds-Karp Maximum Flow
Description: Computes maximum network flow using Breadth-First Search (BFS) to find augmenting paths.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque
from typing import List

class EdmondsKarp:
    def __init__(self, capacity_matrix: List[List[int]]) -> None:
        # Expects a square capacity grid mapping node-to-node constraints
        self.residual_graph: List[List[int]] = [row[:] for row in capacity_matrix]
        self.num_nodes: int = len(capacity_matrix)

    def _bfs_find_path(self, source: int, sink: int, parent_map: List[int]) -> bool:
        """Searches for an available path with remaining capacity from source to sink."""
        visited = [False] * self.num_nodes
        queue: deque[int] = deque([source])
        visited[source] = True
        
        while queue:
            current = queue.popleft()
            
            for neighbor in range(self.num_nodes):
                # If the neighbor hasn't been visited and has available capacity
                if not visited[neighbor] and self.residual_graph[current][neighbor] > 0:
                    parent_map[neighbor] = current
                    if neighbor == sink:
                        return True
                    queue.append(neighbor)
                    visited[neighbor] = True
                    
        return False

    def calculate_max_flow(self, source: int, sink: int) -> int:
        """Calculates the maximum flow through the network using augmenting paths."""
        parent_map = [-1] * self.num_nodes
        total_flow = 0
        
        # Keep finding augmenting paths using BFS
        while self._bfs_find_path(source, sink, parent_map):
            # Step 1: Find the bottleneck capacity along the discovered path
            bottleneck_capacity = float('inf')
            current_node = sink
            while current_node != source:
                p = parent_map[current_node]
                bottleneck_capacity = min(bottleneck_capacity, self.residual_graph[p][current_node])
                current_node = p
                
            # Step 2: Update residual capacities along the path
            current_node = sink
            while current_node != source:
                p = parent_map[current_node]
                self.residual_graph[p][current_node] -= bottleneck_capacity
                self.residual_graph[current_node][p] += bottleneck_capacity
                current_node = p
                
            total_flow += bottleneck_capacity
            
        return total_flow


if __name__ == "__main__":
    # Capacity matrix details:
    # 0 -> Source node, 3 -> Sink node destination
    graph_capacities = [
        [0, 10, 10, 0],
        [0, 0, 4, 8],
        [0, 0, 0, 9],
        [0, 0, 0, 0]
    ]
    
    flow_engine = EdmondsKarp(graph_capacities)
    max_network_capacity = flow_engine.calculate_max_flow(source=0, sink=3)
    print(f"Maximum calculated network capacity throughput: {max_network_capacity}")