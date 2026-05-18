"""
CORE CONCEPT: Network Adjacency Mapping and Interative Graph Traversal 
Building an object-oriented graph manager using adjacency sets. Implements iterative 
Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms to scan network nodes.
"""

from collections import deque

class NetworkGraphEngine:
    def __init__(self):
        # Master mapping mapping structural node integers to isolated tracking sets
        self.adjacency_map: dict[int, set[int]] = {}

    def register_node(self, node: int) -> None:
        """Registers a unique node identifier into the internal mapping schema space."""
        if node not in self.adjacency_map:
            self.adjacency_map[node] = set()

    def connect_undirected_edge(self, node_a: int, node_b: int) -> None:
        """Binds two nodes together using reciprocal reference channels."""
        self.register_node(node_a)
        self.register_node(node_b)
        self.adjacency_map[node_a].add(node_b)
        self.adjacency_map[node_b].add(node_a)

    def execute_iterative_bfs(self, starting_node: int) -> list[int]:
        """Traverses the network graph level-by-level using an iterative queue pattern."""
        if starting_node not in self.adjacency_map:
            return []
            
        visited_registry = set([starting_node])
        traversal_queue = deque([starting_node])
        traversal_path = []

        while traversal_queue:
            current_node = traversal_queue.popleft()
            traversal_path.append(current_node)

            for neighbor in sorted(self.adjacency_map[current_node]):
                if neighbor not in visited_registry:
                    visited_registry.add(neighbor)
                    traversal_queue.append(neighbor)

        return traversal_path

    def execute_iterative_dfs(self, starting_node: int) -> list[int]:
        """Traverses the network graph by diving deep into branches using a stack pattern."""
        if starting_node not in self.adjacency_map:
            return []

        visited_registry = set()
        traversal_stack = [starting_node]
        traversal_path = []

        while traversal_stack:
            current_node = traversal_stack.pop()
            
            if current_node not in visited_registry:
                visited_registry.add(current_node)
                traversal_path.append(current_node)
                
                # Push elements in reverse order to maintain consistent evaluation sweeps
                for neighbor in sorted(self.adjacency_map[current_node], reverse=True):
                    if neighbor not in visited_registry:
                        traversal_stack.append(neighbor)

        return traversal_path


if __name__ == "__main__":
    graph = NetworkGraphEngine()
    graph.connect_undirected_edge(1, 2)
    graph.connect_undirected_edge(1, 3)
    graph.connect_undirected_edge(2, 4)
    graph.connect_undirected_edge(3, 4)

    print(f"BFS Matrix Traversal Output Vector: {graph.execute_iterative_bfs(starting_node=1)}")
    print(f"DFS Matrix Traversal Output Vector: {graph.execute_iterative_dfs(starting_node=1)}")