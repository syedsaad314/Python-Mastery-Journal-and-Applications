"""
Core Topic: Greedy Best-First Search
Description: Introducing heuristics (educated guesses) to prioritize state exploration.
Lead Engineer: Syed Saad Bin Irfan
"""

import heapq

def greedy_search(graph: dict, start: str, target: str, heuristics: dict) -> list:
    """Navigates to the target strictly by choosing the node that 'looks' closest."""
    priority_queue = [(heuristics[start], start)]
    visited = set([start])
    came_from = {start: None}

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current == target:
            # Reconstruct the path backwards
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                # Rank priority purely by how close the neighbor claims to be to target
                heapq.heappush(priority_queue, (heuristics[neighbor], neighbor))

    return []

if __name__ == "__main__":
    # Graph layout
    map_graph = {'Start': ['A', 'B'], 'A': ['Target'], 'B': ['Target'], 'Target': []}
    # Heuristic: Estimated distance to target from each node
    estimated_distance = {'Start': 10, 'A': 4, 'B': 2, 'Target': 0}
    
    path = greedy_search(map_graph, 'Start', 'Target', estimated_distance)
    print(f"Greedy Path Chosen: {path}")