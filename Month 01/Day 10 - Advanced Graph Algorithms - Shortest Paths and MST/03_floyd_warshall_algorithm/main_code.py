"""
Core Topic: Floyd-Warshall All-Pairs Shortest Path
Description: Dynamic programming matrix relaxation tracking pathways between all node pairs.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class AllPairsRoutingSolver:
    @staticmethod
    def compute_all_pairs_shortest_path(matrix_dimension: int, graph_matrix: list[list[float]]) -> list[list[float]]:
        """Computes comprehensive shortest paths between all pairs using dynamic programming grid updates."""
        # Deep-copy the entry matrix map to protect raw input structures
        distance_grid = [list(row) for row in graph_matrix]

        # Core Dynamic Programming loops tracking through intermediate node 'k'
        for k in range(matrix_dimension):
            for i in range(matrix_dimension):
                for j in range(matrix_dimension):
                    # Check if routing from i through k to j lowers the current path cost
                    if distance_grid[i][k] + distance_grid[k][j] < distance_grid[i][j]:
                        distance_grid[i][j] = distance_grid[i][k] + distance_grid[k][j]

        return distance_grid

if __name__ == "__main__":
    INF = float('inf')
    # Direct adjacency grid representation setup
    input_topology = [
        [0.0, 5.0, INF, 10.0],
        [INF, 0.0, 3.0, INF],
        [INF, INF, 0.0, 1.0],
        [INF, INF, INF, 0.0]
    ]
    
    resolved_routing_grid = AllPairsRoutingSolver.compute_all_pairs_shortest_path(4, input_topology)
    print("Resolved All-Pairs Shortest Path Distance Matrix:")
    for routing_row in resolved_routing_grid:
        print(f"  {routing_row}")