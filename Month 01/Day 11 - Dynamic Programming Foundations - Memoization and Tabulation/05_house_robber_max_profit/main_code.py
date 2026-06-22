"""
Core Topic: Non-Consecutive Linear Optimizations
Description: A state machine tracking sequential choice constraints (Include vs Exclude decisions).
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class StateChoiceEngine:
    @staticmethod
    def optimize_returns(asset_values: list[int]) -> int:
        """Determines the maximum profit possible when adjacent choices are restricted."""
        if not asset_values:
            return 0
        if len(asset_values) <= 2:
            return max(asset_values)
            
        # Initialize the baseline choices for our sliding window
        skip_past_node_max = asset_values[0]
        include_past_node_max = max(asset_values[0], asset_values[1])
        
        for current_asset in asset_values[2:]:
            # Transition choice rule: skip this asset entirely OR grab it along with the history from two steps back
            max_current_payout = max(include_past_node_max, skip_past_node_max + current_asset)
            
            # Slide window registers forward
            skip_past_node_max = include_past_node_max
            include_past_node_max = max_current_payout
            
        return include_past_node_max

if __name__ == "__main__":
    neighborhood_vaults = [2, 7, 9, 3, 1]
    optimal_yield = StateChoiceEngine.optimize_returns(neighborhood_vaults)
    print(f"Calculated Maximum Yield under Adjacency Constraints: {optimal_yield}")