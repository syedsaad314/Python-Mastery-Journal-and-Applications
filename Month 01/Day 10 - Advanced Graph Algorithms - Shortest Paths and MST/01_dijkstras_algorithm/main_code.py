"""
Core Topic: Dijkstra's Shortest Path Algorithm
Description: Single-source shortest path calculation on non-negative weighted graphs using a min-heap.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq

class PathOptimizer:
    @staticmethod
    def find_shortest_paths(graph: dict[int, list[tuple[int, int]]], source: int) -> dict[int, float]:
        """Computes minimal cost pathways from a target source node using priority evaluation."""
        # Initialize distances with infinity, source node with zero
        shortest_distances = {node: float('inf') for node in graph}
        shortest_distances[source] = 0.0
        
        # Priority Queue storage scheme: (accumulated_cost, current_node)
        priority_queue = [(0.0, source)]
        
        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)
            
            # Skip evaluation if a more efficient route has already finalized this node
            if current_cost > shortest_distances[current_node]:
                continue
                
            for neighbor, edge_weight in graph.get(current_node, []):
                calculated_route_cost = current_cost + edge_weight
                
                # Relaxation strategy: check if the new path cost is lower than the old known cost
                if calculated_route_cost < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = calculated_route_cost
                    heapq.heappush(priority_queue, (calculated_route_cost, neighbor))
                    
        return shortest_distances

if __name__ == "__main__":
    # Graph schema: { source_node: [(target_node, edge_weight), ...] }
    network_map = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    
    optimized_routes = PathOptimizer.find_shortest_paths(network_map, source=0)
    print(f"Optimized Minimal Path Routing Table from Node [0]: {optimized_routes}")