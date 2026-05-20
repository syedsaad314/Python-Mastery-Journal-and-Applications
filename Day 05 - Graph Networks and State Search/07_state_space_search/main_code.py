"""
CORE CONCEPT: Graph Networks & State Space Search
Implementing an adjacency list-based graph to represent states and actions.
Utilizing Breadth-First Search (BFS) to guarantee the shortest path in an 
unweighted state space—a fundamental algorithm for AI pathfinding and network analysis.

Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque

class GraphNetwork:
    def __init__(self):
        # Using a dictionary as an adjacency list for O(1) node lookups
        self.graph = {}

    def add_connection(self, node: str, neighbor: str):
        """Creates an undirected connection between two state nodes."""
        if node not in self.graph:
            self.graph[node] = []
        if neighbor not in self.graph:
            self.graph[neighbor] = []
            
        self.graph[node].append(neighbor)
        self.graph[neighbor].append(node)

class StateSearch:
    @staticmethod
    def find_shortest_path(network: dict, start_state: str, target_state: str) -> list[str]:
        """
        Executes a Breadth-First Search (BFS) to find the optimal path.
        BFS ensures the first time we hit the target, it is the shortest route.
        """
        if start_state not in network or target_state not in network:
            return []

        # Queue stores tuples of (current_node, path_taken_to_get_here)
        search_queue = deque([(start_state, [start_state])])
        visited_nodes = set([start_state])

        while search_queue:
            current_node, current_path = search_queue.popleft()

            # Target identified; return the exact path taken
            if current_node == target_state:
                return current_path

            # Explore all connected states
            for neighbor in network.get(current_node, []):
                if neighbor not in visited_nodes:
                    visited_nodes.add(neighbor)
                    search_queue.append((neighbor, current_path + [neighbor]))

        # Target is unreachable from the start state
        return []

if __name__ == "__main__":
    # Context setup: Representing a simple server network or physical map
    system_graph = GraphNetwork()
    connections = [
        ("Server_A", "Server_B"),
        ("Server_A", "Server_C"),
        ("Server_B", "Server_D"),
        ("Server_C", "Server_E"),
        ("Server_D", "Server_F"),
        ("Server_E", "Server_F")
    ]

    for node1, node2 in connections:
        system_graph.add_connection(node1, node2)

    start_point = "Server_A"
    end_point = "Server_F"
    
    optimal_path = StateSearch.find_shortest_path(system_graph.graph, start_point, end_point)
    
    print(f"--- State Space Search Results ---")
    print(f"Start Node: {start_point}")
    print(f"Target Node: {end_point}")
    if optimal_path:
        print(f"Optimal Path Discovered: {' -> '.join(optimal_path)}")
        print(f"Total Hops: {len(optimal_path) - 1}")
    else:
        print("Error: Target is unreachable.")