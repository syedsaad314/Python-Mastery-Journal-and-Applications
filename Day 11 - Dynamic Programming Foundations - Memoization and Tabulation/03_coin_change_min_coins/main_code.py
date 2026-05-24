"""
Core Topic: Unbounded Combination Optimization
Description: Using an iterative optimization table to calculate the minimal elements needed to hit a target.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class CombinatoricsOptimizer:
    @staticmethod
    def find_min_elements(elements_pool: list[int], target_sum: int) -> int:
        """Builds a minimization table to track the fewest elements needed to reach the target sum."""
        # Initialize table slots with infinity, baseline slot zero with zero
        optimization_grid = [float('inf')] * (target_sum + 1)
        optimization_grid[0] = 0
        
        # Outer loop evaluates target sum thresholds progressively
        for current_amount in range(1, target_sum + 1):
            for element in elements_pool:
                if current_amount - element >= 0:
                    # Transition rule: minimize current vs path containing the active element item
                    optimization_grid[current_amount] = min(
                        optimization_grid[current_amount],
                        optimization_grid[current_amount - element] + 1
                    )
                    
        return int(optimization_grid[target_sum]) if optimization_grid[target_sum] != float('inf') else -1

if __name__ == "__main__":
    available_coins = [1, 2, 5]
    required_target = 11
    
    fewest_coins = CombinatoricsOptimizer.find_min_elements(available_coins, required_target)
    print(f"Minimal Count Requirements to hit Target Sum [{required_target}]: {fewest_coins}")