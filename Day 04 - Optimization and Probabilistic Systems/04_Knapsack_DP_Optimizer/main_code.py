"""
CORE CONCEPT: Dynamic Programming Resource Allocation (0/1 Knapsack Engine)
Implementing a discrete knapsack optimization engine using tabular memoization.
Eliminates redundant calculations by converting exponential combinations 
into highly efficient linear space checks.
"""

class KnapsackDPOptimizer:
    @staticmethod
    def maximize_resource_allocation(weights: list[int], values: list[int], max_capacity: int) -> tuple[int, list[int]]:
        """Calculates optimal item selections to maximize value within weight constraints."""
        item_count = len(weights)
        # Create dynamic programming lookup matrix table initialized to zero bounds
        dp_table = [[0] * (max_capacity + 1) for _ in range(item_count + 1)]

        # Construct lookup table records row by row
        for i in range(1, item_count + 1):
            for w in range(max_capacity + 1):
                # Check if current item weight fits in the current capacity sub-boundary
                if weights[i-1] <= w:
                    dp_table[i][w] = max(
                        values[i-1] + dp_table[i-1][w - weights[i-1]], 
                        dp_table[i-1][w]
                    )
                else:
                    dp_table[i][w] = dp_table[i-1][w]

        # Trace backward through table layers to find the exact items selected
        max_value_achieved = dp_table[item_count][max_capacity]
        selected_indices = []
        remaining_capacity = max_capacity

        for i in range(item_count, 0, -1):
            if dp_table[i][remaining_capacity] != dp_table[i-1][remaining_capacity]:
                selected_indices.append(i - 1)
                remaining_capacity -= weights[i - 1]

        return max_value_achieved, selected_indices[::-1]


if __name__ == "__main__":
    # Context setup: Resource weight footprints alongside matching processing utility values
    mock_weights = [1, 3, 4, 5]
    mock_values = [1, 4, 5, 7]
    target_capacity = 7

    optimizer = KnapsackDPOptimizer()
    highest_val, items = optimizer.maximize_resource_allocation(mock_weights, mock_values, target_capacity)
    print(f"Maximized Allocation Return Metric: {highest_val} (Selected Resource Item Array: {items})")