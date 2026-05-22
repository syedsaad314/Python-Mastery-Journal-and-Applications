"""
Core Topic: Bellman-Ford Routing Engine
Description: Calculating paths with negative edge weights while catching negative loop anomalies.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class RobustNetworkRouter:
    @staticmethod
    def calculate_routes(total_nodes: int, edge_list: list[tuple[int, int, int]], source: int) -> list[float]:
        """Calculates single-source shortest paths while explicitly scanning for cyclic negative weight traps."""
        distances = [float('inf')] * total_nodes
        distances[source] = 0.0

        # Pass 1 to (V - 1): Standard structural relaxation cycle execution
        for _ in range(total_nodes - 1):
            for u, v, weight in edge_list:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

        # Pass V: Final edge verification loop to catch negative-weight cycles
        for u, v, weight in edge_list:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                raise ValueError("Critical Anomaly: Infinite negative cycle trap detected within network graph.")

        return distances

if __name__ == "__main__":
    # Node count and edge array layout: (source, target, weight)
    nodes_count = 4
    network_edges = [
        (0, 1, 4),
        (0, 2, 3),
        (1, 2, -2),
        (2, 3, 2)
    ]
    
    try:
        calculated_costs = RobustNetworkRouter.calculate_routes(nodes_count, network_edges, source=0)
        print(f"Calculated Path Routing Matrix (With Negative Edges Support): {calculated_costs}")
    except ValueError as error_message:
        print(error_message)