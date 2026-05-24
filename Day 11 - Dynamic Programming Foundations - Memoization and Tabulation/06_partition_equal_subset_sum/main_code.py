"""
Core Topic: 0/1 Knapsack Boolean State Mapping
Description: Tracking dynamic boolean match flags across localized space-optimized target sets.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class BalancedPartitionValidator:
    @staticmethod
    def verify_split_feasibility(value_pool: list[int]) -> bool:
        """Determines if a pool of numbers can be split into two subsets with identical sums."""
        total_sum = sum(value_pool)
        
        # If the grand total is odd, it's impossible to split it into two equal whole numbers
        if total_sum % 2 != 0:
            return False
            
        target_sub_sum = total_sum // 2
        # Initialize boolean state tracking map; index 0 is always true
        boolean_state_row = [False] * (target_sub_sum + 1)
        boolean_state_row[0] = True
        
        for num in value_pool:
            # Step backward through the row to safely update combinations without using fresh values twice
            for sum_checkpoint in range(target_sub_sum, num - 1, -1):
                if boolean_state_row[sum_checkpoint - num]:
                    boolean_state_row[sum_checkpoint] = True
                    
        return boolean_state_row[target_sub_sum]

if __name__ == "__main__":
    sample_pool = [1, 5, 11, 5]
    partition_status = BalancedPartitionValidator.verify_split_feasibility(sample_pool)
    print(f"Balanced Array Split Verification Status Result: {partition_status}")