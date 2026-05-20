"""
Core Topic: Dijkstra's Algorithm for Weighted Routing
Description: Utilizing a priority queue (Min-Heap) to find the lowest-cost path in a weighted graph.
Lead Engineer: Syed Saad Bin Irfan
"""

import heapq

def optimize_route(graph: dict, start: str) -> dict:
    """Calculates the lowest cost to reach all nodes from the starting node."""
    # Track the minimum cost to reach each node (initialize to infinity)
    costs = {node: float('inf') for node in graph}
    costs[start] = 0
    
    # Priority queue stores tuples of (accumulated_cost, current_node)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        
        # Optimization: Ignore outdated, higher-cost entries in the heap
        if current_cost > costs[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            cost_to_neighbor = current_cost + weight
            
            # If we found a cheaper route to the neighbor, update it
            if cost_to_neighbor < costs[neighbor]:
                costs[neighbor] = cost_to_neighbor
                heapq.heappush(priority_queue, (cost_to_neighbor, neighbor))
                
    return costs

if __name__ == "__main__":
    # Graph edges now carry a "cost" or "weight"
    logistics_network = {
        'Warehouse': {'Hub_A': 5, 'Hub_B': 2},
        'Hub_A': {'Store_1': 3, 'Store_2': 7},
        'Hub_B': {'Hub_A': 1, 'Store_2': 8},
        'Store_1': {}, 'Store_2': {}
    }
    print(f"Optimized routing costs: {optimize_route(logistics_network, 'Warehouse')}")