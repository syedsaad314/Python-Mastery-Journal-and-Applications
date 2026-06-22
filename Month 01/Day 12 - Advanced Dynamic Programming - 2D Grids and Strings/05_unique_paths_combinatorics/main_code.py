"""
Core Topic: Unique Paths Combinatorial Tracking
Description: Calculating total structural routing combinations across open constraints.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class CombinatoricsEngine:
    @staticmethod
    def calculate_total_pathways(rows: int, cols: int) -> int:
        """Accumulates all possible valid directional routes to the target destination."""
        # Initialize an accumulation grid filled with 1s
        # (Edges default to 1 since there's only one straight line path down or right)
        path_matrix = [[1 for _ in range(cols)] for _ in range(rows)]
        
        for r in range(1, rows):
            for c in range(1, cols):
                # Transition rule: Total paths = routes from above + routes from the left
                path_matrix[r][c] = path_matrix[r - 1][c] + path_matrix[r][c - 1]
                
        return path_matrix[rows - 1][cols - 1]

if __name__ == "__main__":
    grid_rows = 3
    grid_cols = 7
    
    pathway_volume = CombinatoricsEngine.calculate_total_pathways(grid_rows, grid_cols)
    print(f"Total Unique Routing Configurations for a [{grid_rows}x{grid_cols}] space: {pathway_volume}")