"""
Core Topic: Minimum Path Sum Spatial Routing
Description: Geographic 2D DP calculating the absolute cheapest path through weighted terrain.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class SpatialRouter:
    @staticmethod
    def calculate_cheapest_route(grid: list[list[int]]) -> int:
        """Scans a 2D weighted matrix to isolate the optimal path from top-left to bottom-right."""
        rows, cols = len(grid), len(grid[0])
        
        # Deep copy to maintain clean functional parameters
        cost_matrix = [list(row) for row in grid]
        
        # Initialize top row boundary (can only arrive from the left)
        for c in range(1, cols):
            cost_matrix[0][c] += cost_matrix[0][c - 1]
            
        # Initialize left column boundary (can only arrive from above)
        for r in range(1, rows):
            cost_matrix[r][0] += cost_matrix[r - 1][0]
            
        # Standard Grid Evaluation
        for r in range(1, rows):
            for c in range(1, cols):
                # Transition: The current cell cost + the cheaper of the two possible inbound paths
                cost_matrix[r][c] += min(cost_matrix[r - 1][c], cost_matrix[r][c - 1])
                
        return cost_matrix[rows - 1][cols - 1]

if __name__ == "__main__":
    terrain_weights = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]
    
    optimal_cost = SpatialRouter.calculate_cheapest_route(terrain_weights)
    print(f"Optimal Grid Traversal Cost: {optimal_cost}")