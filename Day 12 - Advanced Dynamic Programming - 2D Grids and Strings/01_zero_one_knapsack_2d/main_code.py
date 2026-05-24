"""
Core Topic: 0/1 Knapsack 2D Bounded Selection
Description: Maximizing output value within a hard weight constraint via a 2D capacity matrix.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class KnapsackOptimizer:
    @staticmethod
    def maximize_value(weights: list[int], values: list[int], max_capacity: int) -> int:
        """Evaluates combination states to find the highest value yield without exceeding max capacity."""
        items_count = len(weights)
        # 2D Grid: Rows = Items, Columns = Weight Capacities from 0 to max_capacity
        dp_matrix = [[0 for _ in range(max_capacity + 1)] for _ in range(items_count + 1)]
        
        for item_idx in range(1, items_count + 1):
            current_weight = weights[item_idx - 1]
            current_value = values[item_idx - 1]
            
            for capacity in range(1, max_capacity + 1):
                if current_weight <= capacity:
                    # Transition: Max of (Skipping Item) vs (Including Item + Remaining Capacity Value)
                    dp_matrix[item_idx][capacity] = max(
                        dp_matrix[item_idx - 1][capacity], 
                        dp_matrix[item_idx - 1][capacity - current_weight] + current_value
                    )
                else:
                    # Item is too heavy, must skip and carry forward previous best
                    dp_matrix[item_idx][capacity] = dp_matrix[item_idx - 1][capacity]
                    
        return dp_matrix[items_count][max_capacity]

if __name__ == "__main__":
    asset_values = [60, 100, 120]
    asset_weights = [10, 20, 30]
    hard_limit = 50
    
    maximized_yield = KnapsackOptimizer.maximize_value(asset_weights, asset_values, hard_limit)
    print(f"Maximized Cargo Value within [{hard_limit}] capacity limit: {maximized_yield}")