"""
CORE CONCEPT: A* Grid Pathfinding Optimizer
Implementing a heuristic-driven pathfinding engine over a 2D coordinate grid. 
Leverages Manhattan distance calculations and a priority queue to find 
optimal paths around obstacles.
"""

import heapq

class AStarGridOptimizer:
    def __init__(self, coordinate_grid: list[list[int]]):
        self.grid = coordinate_grid
        self.rows = len(coordinate_grid)
        self.cols = len(coordinate_grid[0]) if self.rows > 0 else 0

    def _calculate_manhattan_heuristic(self, current: tuple[int, int], target: tuple[int, int]) -> float:
        """Computes structural distance estimations between current coordinates and destination."""
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

    def resolve_shortest_path(self, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """Calculates path paths over grid systems, tracking cost boundaries."""
        # Elements inside min-heap priority queue format: (f_score, cost_so_far, current_coord)
        open_priority_queue = [(0.0, 0.0, start)]
        
        origin_parent_tracker = {}
        g_cost_score = {start: 0.0}

        while open_priority_queue:
            _, current_cost, current_node = heapq.heappop(open_priority_queue)

            if current_node == goal:
                # Reconstruct path by tracing parents backward
                reconstructed_path = []
                while current_node in origin_parent_tracker:
                    reconstructed_path.append(current_node)
                    current_node = origin_parent_tracker[current_node]
                reconstructed_path.append(start)
                return reconstructed_path[::-1]

            # Evaluate 4 directional neighbor movements (Up, Down, Left, Right)
            for delta_r, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current_node[0] + delta_r, current_node[1] + delta_c)

                # Validate grid boundaries and obstacle avoidance states (1 = Obstacle)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                    if self.grid[neighbor[0]][neighbor[1]] == 1:
                        continue

                    tentative_g_score = current_cost + 1.0

                    if neighbor not in g_cost_score or tentative_g_score < g_cost_score[neighbor]:
                        g_cost_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self._calculate_manhattan_heuristic(neighbor, goal)
                        origin_parent_tracker[neighbor] = current_node
                        heapq.heappush(open_priority_queue, (f_score, tentative_g_score, neighbor))

        return []  # Return empty if path is blocked


if __name__ == "__main__":
    # 0 = Open path coordinate, 1 = Solid obstacle boundary barrier
    test_matrix = [
        [0, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 0, 0],
        [0, 1, 1, 0]
    ]

    pathfinder = AStarGridOptimizer(test_matrix)
    resolved_route = pathfinder.resolve_shortest_path(start=(0, 0), goal=(3, 3))
    print(f"Optimal A* Coordinate Navigation Pathway: {resolved_route}")