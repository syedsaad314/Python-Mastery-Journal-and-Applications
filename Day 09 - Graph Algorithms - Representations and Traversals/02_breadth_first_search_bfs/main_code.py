"""
Core Topic: Breadth-First Search Network Traversal
Description: Running queue-driven expansions to calculate unweighted path hops.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque

class NetworkBFS:
    @staticmethod
    def calculate_shortest_hops(graph: dict[int, list[int]], start_node: int) -> dict[int, int]:
        """Calculates minimal node hops from a starting point using a queue layout."""
        # Tracks minimal step distance to each discovered node
        hop_distances = {start_node: 0}
        evaluation_queue = deque([start_node])

        while evaluation_queue:
            current_node = evaluation_queue.popleft()
            current_distance = hop_distances[current_node]

            for neighbor in graph.get(current_node, []):
                if neighbor not in hop_distances:
                    hop_distances[neighbor] = current_distance + 1
                    evaluation_queue.append(neighbor)

        return hop_distances

if __name__ == "__main__":
    # Modeling connected server switches
    network_topology = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 4],
        3: [1],
        4: [1, 2]
    }
    
    hop_map = NetworkBFS.calculate_shortest_hops(network_topology, start_node=0)
    print(f"Calculated Hop Distances from Core Switch Node [0]: {hop_map}")