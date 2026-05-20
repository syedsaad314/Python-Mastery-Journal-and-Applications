"""
Core Topic: Breadth-First Search (BFS) in Unweighted Graph Networks
Description: Implementing an adjacency list-based graph to execute layer-by-layer state space search.
Lead Engineer: Syed Saad Bin Irfan
"""

from collections import deque

def bfs_shortest_path(graph: dict, start: str, target: str) -> list:
    """Finds the shortest path between two nodes using a queue."""
    if start not in graph or target not in graph:
        return []

    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target:
            return path

        for adjacent in graph.get(node, []):
            if adjacent not in visited:
                visited.add(adjacent)
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)

    return []

if __name__ == "__main__":
    # Simulating a basic server network or state-space map
    network = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    print(f"Optimal Path A -> F: {bfs_shortest_path(network, 'A', 'F')}")